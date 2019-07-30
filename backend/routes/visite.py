from flask import request

from shapely.geometry import Point
from geoalchemy2.shape import to_shape, from_shape

from sqlalchemy.orm.exc import NoResultFound

from geonature.utils.env import DB
from geonature.utils.utilssqlalchemy import json_resp, GenericQuery

from geonature.core.gn_monitoring.models import TBaseVisits

from pypnusershub import routes as fnauth

from ..blueprint import blueprint
from ..models.models import ConditionsVisite
from ..utils.repos import (
    GNMonitoringVisiteRepository,
    GNMonitoringContactTaxon
)  # TODO déplacement repos dans core


def _format_visite_data(data):
    result = data.as_dict()
    result.update(data.base_visit.as_dict(recursif=False))
    result['observers'] = [
        o.id_role for o in data.base_visit.observers
    ]
    result["id"] = data.base_visit.id_base_visit
    return result


@blueprint.route('/visites/<id_base_site>', methods=['GET'])
@fnauth.check_auth(3)
@json_resp
def get_all_visites_chiro(id_base_site):

    limit = int(request.args.get('limit', 1000))
    offset = int(request.args.get('offset', 0))

    data = GenericQuery(
        DB.session, 'v_visites_chiro', 'monitoring_chiro', None,
        {"id_base_site": id_base_site}, limit, offset
    ).return_query()

    data["total"] = data["total_filtered"]
    return data


@blueprint.route('/visite/<id_base_visit>', methods=['GET'])
@fnauth.check_auth(3)
@json_resp
def get_one_visite_chiro(id_base_visit):
    try:
        result = DB.session.query(ConditionsVisite).filter_by(
            id_base_visit=id_base_visit
        ).one()
        return _format_visite_data(result)
    except NoResultFound:
        return (
            {'err': 'visite introuvable', 'id_base_visit': id_base_visit},
            404
        )


@blueprint.route('/visite', defaults={'id_visite': None}, methods=['POST', 'PUT'])
@blueprint.route('/visite/<id_visite>', methods=['POST', 'PUT'])
@fnauth.check_auth(3)
@json_resp
def create_or_update_visite_chiro(id_visite=None):
    db_sess = DB.session
    data = request.get_json()
    print(data)

    # creation de base visite
    if not id_visite:
        id_visite = data.get('id', None)

    base_repo = GNMonitoringVisiteRepository(db_sess)
    base_visit = base_repo.handle_write(
        id_base_visite=id_visite,
        data=data
    )

    # creation condition visite
    visite = None

    if 'geom' in data:
        data['geom'] = from_shape(Point(*data['geom'][0]), srid=4326)

    if id_visite:
        visite = db_sess.query(ConditionsVisite).get(id_visite)
    else:
        visite = ConditionsVisite()

    for field in data:
        if hasattr(ConditionsVisite, field):
            setattr(visite, field, data[field])
    visite.base_visit = base_visit

    db_sess.add(visite)
    try:
        db_sess.commit()
    except Exception as e:
        db_sess.rollback()
        raise(e)

    # creation ajout rapide de taxons
    __taxons__ = data['__taxons__'] if '__taxons__' in data else None
    if __taxons__:
        for contact in __taxons__:
            contact['id_base_visit'] = visite.id_base_visit
            GNMonitoringContactTaxon(db_sess, contact, True).handle_write()

    return _format_visite_data(visite)


@blueprint.route('/visite/<id_visite>', methods=['DELETE'])
@fnauth.check_auth(3)
@json_resp
def delete_visite_chiro(id_visite):
    '''
        Suppression d'un enregistrement visite
    '''
    try:
        visite = DB.session.query(TBaseVisits).filter(
            TBaseVisits.id_base_visit == id_visite
        ).one()
    except NoResultFound:
        return {}, 404

    else:
        try:
            DB.session.delete(visite)
            DB.session.commit()
            return {'data': id_visite}
        except Exception:
            DB.session.rollback()
            return ({
                'data': id_visite,
                'errmsg': 'Erreur de suppression'
                }, 400)


@blueprint.route('/inventaires', methods=['GET'])
@fnauth.check_auth(3)
@json_resp
def get_all_inventaires_chiro():
    data = GenericQuery(
        DB.session, 'v_inventaires_chiro', 'monitoring_chiro', "geom",
        {}, 1000, 0
    ).return_query()

    data["total"] = data["total_filtered"]
    return data
