from flask import request
from sqlalchemy.orm.exc import NoResultFound

from geonature.utils.env import DB
from geonature.utils.utilssqlalchemy import json_resp
from pypnnomenclature.models import TNomenclatures

from ..blueprint import blueprint
from ..models.site import InfoSite, RelChirositeTNomenclaturesAmenagement, RelChirositeTNomenclaturesMenace

import geojson
from geoalchemy2.shape import to_shape

ID_APP = 101 # TODO récupérer l'identifiant d'application par le front


def _format_site_data(data):
    '''
    Procédure de sérialisation non récursive des modèles
    '''
    base = data.base_site.as_dict(recursif=False)
    geometry = geojson.Feature(geometry=to_shape(getattr(data.base_site, 'geom')))
    base['geom'] = [geometry['geometry']['coordinates']]
    result = data.as_dict(recursif=False)
    result['menaces_ids'] = [
            menace.id_nomenclature_menaces
            for menace in data.menaces_ids]
    result['amenagements_ids'] = [
            amenagement.id_nomenclature_amenagement
            for amenagement in data.amenagements_ids]
    base.update(result)
    return base


@blueprint.route('/sites', methods=['GET'])
@json_resp
def get_sites_chiro():
    '''
    Retourne la liste des sites chiro
    '''
    limit = int(request.args.get('limit', 10))
    offset = int(request.args.get('offset', 1))
    results = (
        DB.session.query(InfoSite)
        .order_by(InfoSite.id_site_infos)
        .limit(limit)
        .offset((offset-1)*limit)
        .all()
    )
    return list(map(_format_site_data, results))


@blueprint.route('/site/<id_site>', methods=['GET'])
@json_resp
def get_one_site_chiro(id_site):
    '''
    Retourne le site chiro identifié par `id_site`
    '''
    result = DB.session.query(InfoSite).filter_by(id_base_site=id_site).one()
    if result:
        return _format_site_data(result)
    return {'err': 'site introuvable', 'id_site': id_site}, 404




import pprint # TODO remove
from ..utils.repos import GNMonitoringSiteRepository, InvalidBaseSiteData
from shapely.geometry import Point
from geoalchemy2.shape import from_shape


def _prepare_site_data(data, db):
    """
    Prépare les données en vue d'une insertion en base de données
    params :
        data : données à préparer (dict <- request.get_json())
        db : session DB à utiliser pour charger les relations
    """

    data['geom'] = from_shape(Point(*data['geom'][0]), srid=4326)

    menaces = []
    for menace_id in data['menaces_ids']:
        menaces.append(RelChirositeTNomenclaturesMenace(id_nomenclature_menaces=menace_id))
    data['menaces_ids'] = menaces

    amenagements = []
    for amenagement_id in data['amenagements_ids']:
        amenagements.append(RelChirositeTNomenclaturesAmenagement(id_nomenclature_amenagement=amenagement_id))

    data['amenagements_ids'] = amenagements
    return data


@blueprint.route('/site', methods=['POST', 'PUT'])
@json_resp
def create_site_chiro():
    '''
    Crée un nouveau site chiro
    suggestion process :
        data = request.get_json()
        base_site = geonature.core.gn_monitoring.handle_base_site(data)
        info_site = InfoSite(data)
        info_site.base_site = base_site
        ...
    '''
    try:
        db_sess = DB.session
        req_data = request.get_json()
        data = _prepare_site_data(req_data, db_sess)
        base_repo = GNMonitoringSiteRepository(db_sess, id_app=ID_APP)
        # creation site de base
        base_site = base_repo.handle_write(data=data, base_site_id=data.get('id_base_site', None))

        # creation infos_site
        infos_site = InfoSite(base_site=base_site)
        for field in data:
            if hasattr(infos_site, field):
                setattr(infos_site, field, data[field])

        db_sess.add(infos_site)
        db_sess.commit()
        return infos_site.as_dict()
    except InvalidBaseSiteData:
        db.sess.rollback()
        return ({
                'data': data,
                'errmsg': 'Données base site invalides'
                }, 400)
    except ValueError: #TODO vérifier type erreur
        db_sess.rollback()
        return ({
                'data': data,
                'errmsg': 'Données infos site invalides'
                }, 400)


@blueprint.route('/site/<id_site>', methods=['POST', 'PUT'])
@json_resp
def update_site_chiro(id_site):
    '''
    Met à jour un site chiro
    suggestion process :
        data = request.get_json()
        base_site = geonature.core.gn_monitoring.handle_base_site(data)
        info_site = DB.session.query(InfoSite).get(id_site)
        ...
    '''

    try:
        db_sess = DB.session
        data = _prepare_site_data(request.get_json(), db_sess)
        base_repo = GNMonitoringSiteRepository(db_sess, id_app=ID_APP)
        base_site = base_repo.handle_write(
                base_site_id=id_site,
                data=data)
        infos_site = db_sess.query(InfoSite).get(data['id_site_infos'])

        for menace in infos_site.menaces_ids:
            db_sess.delete(menace)
        for amenagement in infos_site.amenagements_ids:
            db_sess.delete(amenagement)

        for field in data:
            if hasattr(infos_site, field):
                setattr(infos_site, field, data[field])
        db_sess.commit()
        return infos_site.as_dict()
    except InvalidBaseSiteData:
        db.sess.rollback()
        return ({
                'data': data,
                'errmsg': 'Données base site invalides'
                }, 400)
    except ValueError: #TODO vérifier type erreur
        db_sess.rollback()
        return ({
                'data': data,
                'errmsg': 'Données infos site invalides'
                }, 400)



@blueprint.route('/site/<id_site>', methods=['DELETE'])
@json_resp
def delete_site_chiro(id_site):
    '''
    supprime un site chiro
    suggestion process :
        info_site = DB.session.query(InfoSite).get(id_site)
        ...
    '''
    try:
        info_site = DB.session.query(InfoSite).filter(InfoSite.id_base_site==id_site).one()
        for amenagement in info_site.amenagements_ids:
            DB.session.delete(amenagement)
        for menace in info_site.menaces_ids:
            DB.session.delete(menace)
        base_site_id = info_site.id_base_site
        DB.session.delete(info_site)
        base_repo = GNMonitoringSiteRepository(DB.session, id_app=ID_APP)
        base_repo.handle_delete(base_site_id)
        DB.session.commit()
        return {'data': id_site}
    except InvalidBaseSiteData:
        DB.session.rollback()
        return ({
            'data': id_site,
            'errmsg': 'Erreur de suppression'
            }, 400)
    except NoResultFound:
        DB.session.rollback()
        return {}, 404


