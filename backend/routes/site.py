'''
Routes relatives aux sites
'''

import geojson

from flask import request
from sqlalchemy.orm.exc import NoResultFound
from shapely.geometry import Point, asShape
from geoalchemy2.shape import to_shape, from_shape

from geonature.utils.env import DB
from geonature.utils.utilssqlalchemy import json_resp, GenericQuery

from geonature.core.gn_permissions import decorators as permissions

from geonature.core.gn_monitoring.models import TBaseSites, corSiteModule
from geonature.core.gn_commons.repositories import (
    TMediumRepository
)

from pypnusershub import routes as fnauth

from ..blueprint import blueprint, ID_MODULE
from ..models.models import (
    InfoSite,
    RelChirositeTNomenclaturesAmenagement,
    RelChirositeTNomenclaturesMenace
)

from ..utils.repos import (
    GNMonitoringSiteRepository,
    InvalidBaseSiteData,
    attach_uuid_to_medium
)  # TODO déplacement repos dans core
from ..utils.relations import get_updated_relations


@blueprint.route('/sites', methods=['GET'])
@permissions.check_cruved_scope("R", False, module_code="SUIVI_CHIRO")
@json_resp
def get_sites_chiro():
    '''
    Retourne la liste des sites chiro
    '''
    limit = int(request.args.get('limit', 1000))
    offset = int(request.args.get('offset', 0))

    data = GenericQuery(
        DB.session, 'v_sites_chiro', 'monitoring_chiro', "geom",
        {}, limit, offset
    ).return_query()

    data["total"] = data["total_filtered"]
    return data



@blueprint.route('/site/<id_site>', methods=['GET'])
@permissions.check_cruved_scope("R", False, module_code="SUIVI_CHIRO")
@json_resp
def get_one_site_chiro(id_site):
    '''
    Retourne le site chiro identifié par `id_site`
    '''
    try:
        result = DB.session.query(InfoSite).filter_by(id_base_site=id_site).one()
        if result:
            return _format_site_data(result)
    except NoResultFound:
        # Si le site n'a toujours pas d'info site associé mais qu'il a un base site
        try:
            basesite = DB.session.query(TBaseSites).filter_by(
                id_base_site=id_site
            ).filter(
                TBaseSites.modules.any(
                    corSiteModule.c.id_module == ID_MODULE
                )
            ).one()
            result = InfoSite()
            result.base_site = basesite
            if result:
                return _format_site_data(result)
        except NoResultFound:
            return {'err': 'site introuvable', 'id_site': id_site}, 404


@blueprint.route('/site', defaults={'id_site': None}, methods=['POST', 'PUT'])
@blueprint.route('/site/<id_site>', methods=['POST', 'PUT'])
@permissions.check_cruved_scope("C", False, module_code="SUIVI_CHIRO")
@json_resp
def create_or_update_site_chiro(id_site=None):
    '''
    Met à jour ou créé un site chiro
     - c-a-d création du base site si besoin
     - création info site

        params :
            id_site : id base site
    '''

    try:
        db_sess = DB.session
        req_data = request.get_json()
        data = _prepare_site_data(req_data, db_sess)
        base_repo = GNMonitoringSiteRepository(db_sess, id_app=ID_MODULE)

        # Création du base site si besoin
        if not id_site:
            id_site = data.get('id_base_site', None)

        base_site = base_repo.handle_write(
            base_site_id=id_site,
            data=data
        )

        # Création de la données infos site propre à chiro
        infos_site = None
        if id_site:
            infos_site = db_sess.query(InfoSite).get(id_site)

        if not infos_site:
            infos_site = InfoSite(base_site=base_site)
            db_sess.add(infos_site)

        for field in data:
            if hasattr(infos_site, field):
                setattr(infos_site, field, data[field])

        db_sess.commit()
        infos_site.base_site = base_site

        # Création des médiasn
        if (data['medium']):
            attach_uuid_to_medium(
                data['medium'],
                base_site.uuid_base_site
            )

        # Si modification sync synthese
        if id_site:
            base_repo.sync_synthese(base_site.uuid_base_site)

        return _format_site_data(infos_site)
    except InvalidBaseSiteData:
        db_sess.rollback()
        return ({
                'data': data,
                'errmsg': 'Données base site invalides'
                }, 400)
    except ValueError:  # TODO vérifier type erreur
        db_sess.rollback()
        return ({
                'data': data,
                'errmsg': 'Données infos site invalides'
                }, 400)


@blueprint.route('/site/<id_site>', methods=['DELETE'])
@permissions.check_cruved_scope("D", False, module_code="SUIVI_CHIRO")
@json_resp
def delete_site_chiro(id_site):
    '''
    supprime un site chiro
    params :
        id_site : identifiant base site
    args :
        cascade : commande la suppression du base site si true
    '''
    cascade = request.args.get('cascade', True)
    try:
        info_site = DB.session.query(InfoSite).filter(
            InfoSite.id_base_site == id_site
        ).one()
    except NoResultFound:
        # Site introuvable
        return {}, 404
    else:
        for amenagement in info_site.amenagements_ids:
            DB.session.delete(amenagement)
        for menace in info_site.menaces_ids:
            DB.session.delete(menace)
        base_site_id = info_site.id_base_site
        DB.session.delete(info_site)
        try:
            base_repo = GNMonitoringSiteRepository(
                DB.session, id_app=ID_MODULE
            )
            base_repo.handle_delete(base_site_id, cascade)
            DB.session.commit()
            return {'data': id_site}
        except InvalidBaseSiteData:
            # Données relatives à base site erronnéee
            # ex : tentative de suppression d'un base site non lié
            # à l'application
            DB.session.rollback()
            return ({
                'data': id_site,
                'errmsg': 'Erreur de suppression'
                }, 400)


def _format_site_data(data):
    '''
        Procédure de sérialisation non récursive des modèles
    '''
    base = data.base_site.as_dict(recursif=False)
    base["id"] = data.base_site.id_base_site
    geometry = geojson.Feature(
        geometry=to_shape(getattr(data.base_site, 'geom'))
    )
    base['geom'] = [geometry['geometry']['coordinates']]
    result = data.as_dict(recursif=False)
    result['menaces_ids'] = [
        menace.id_nomenclature_menaces
        for menace in data.menaces_ids
    ]
    result['amenagements_ids'] = [
        amenagement.id_nomenclature_amenagement
        for amenagement in data.amenagements_ids
    ]
    base.update(result)

    # get medium
    medium = TMediumRepository().get_medium_for_entity(
        entity_uuid=data.base_site.uuid_base_site
    )
    if (medium):
        base['medium'] = [m.as_dict() for m in medium]

    return base



def _prepare_site_data(data, db):
    """
    Prépare les données en vue d'une insertion en base de données
    params :
        data : données à préparer (dict <- request.get_json())
        db : session DB à utiliser pour charger les relations
    """

    data['geom'] = from_shape(Point(*data['geom'][0]), srid=4326)

    data['menaces_ids'] = [rel for rel in get_updated_relations(
        db,
        RelChirositeTNomenclaturesMenace,
        data['menaces_ids'],
        data['id_base_site'],
        'id_base_site',
        'id_nomenclature_menaces'
    )]
    data['amenagements_ids'] = [rel for rel in get_updated_relations(
        db,
        RelChirositeTNomenclaturesAmenagement,
        data['amenagements_ids'],
        data['id_base_site'],
        'id_base_site',
        'id_nomenclature_amenagement'
    )]
    return data
