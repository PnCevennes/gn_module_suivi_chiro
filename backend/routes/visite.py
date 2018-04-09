from flask import request

from geonature.utils.env import DB
from geonature.utils.utilssqlalchemy import json_resp
from geonature.core.gn_monitoring.models import TBaseVisits

from ..blueprint import blueprint
from ..models.visite import ConditionsVisite


def _format_visite_data(data):
    result = data.as_dict()
    result.update(data.base_visit.as_dict(recursif=False))
    result['observers'] = [
        o.id_role for o in data.base_visit.observers
    ]
    return result


@blueprint.route('/visites/<id_base_site>', methods=['GET'])
@json_resp
def get_visites_chiro(id_base_site):
    results = (
        DB.session.query(ConditionsVisite)
        .filter(ConditionsVisite.base_visit.has(
            id_base_site=id_base_site)
        )
        .all()
    )
    return list(map(_format_visite_data, results))


@blueprint.route('/visite/<id_cond_visite>', methods=['GET'])
@json_resp
def get_one_visite_chiro(id_cond_visite):
    result = DB.session.query(ConditionsVisite).get(id_cond_visite)
    return _format_visite_data(result)


@blueprint.route('/visite', methods=['POST', 'PUT'])
def create_visite_chiro():
    pass


@blueprint.route('/visite/<id_visite>', methods=['POST', 'PUT'])
def update_visite_chiro(id_visite):
    pass


@blueprint.route('/visite/<id_visite>', methods=['DELETE'])
def delete_visite_chiro(id_visite):
    pass

