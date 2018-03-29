from flask import request

from geonature.utils.utilssqlalchemy import json_resp
from pypnnomenclature.models import TNomenclatures
from pypnnomenclature import repository

from ..blueprint import blueprint as routes
from ..models.site import InfoSite

from geonature.utils.env import DB



def _format_site_data(data):
    result = data.as_dict(recursif=False)
    result.update(data.base_site.as_dict())
    result['menaces_ids'] = [
            menace.id_nomenclature_menaces
            for menace in data.menaces_ids]
    result['amenagements_ids'] = [
            amenagement.id_nomenclature_amenagement
            for amenagement in data.amenagements_ids]
    return result


@routes.route('/sites', methods=['GET'])
@json_resp
def get_sites_chiro():
    '''
    Retourne la liste des sites chiro
    '''
    limit = int(request.args.get('limit', 10))
    offset = int(request.args.get('offset', 1))
    results = (DB.session.query(InfoSite)
            .order_by(InfoSite.id_site_infos)
            .limit(limit)
            .offset((offset-1)*limit)
            .all())
    return list(map(_format_site_data, results))


@routes.route('/site/<id_site>', methods=['GET'])
@json_resp
def get_one_site_chiro(id_site):
    '''
    Retourne le site chiro identifié par `id_site`
    '''
    result = DB.session.query(InfoSite).get(id_site)
    if result:
        return _format_site_data(result)
    return {'err': 'site introuvable', 'id_site': id_site}, 404


@routes.route('/site', methods=['POST', 'PUT'])
def create_site_chiro():
    pass


@routes.route('/site/<id_site>', methods=['POST', 'PUT'])
def update_site_chiro(id_site):
    pass


@routes.route('/site/<id_site>', methods=['DELETE'])
def delete_site_chiro(id_site):
    pass
