from flask import request

from geonature.utils.env import DB
from geonature.utils.utilssqlalchemy import json_resp

from ..blueprint import blueprint
from ..models.site import InfoSite

import geojson
from geoalchemy2.shape import to_shape


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


@blueprint.route('/site', methods=['POST', 'PUT'])
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
    #TODO
    pass


@blueprint.route('/site/<id_site>', methods=['POST', 'PUT'])
def update_site_chiro(id_site):
    '''
    Met à jour un site chiro
    suggestion process :
        data = request.get_json()
        base_site = geonature.core.gn_monitoring.handle_base_site(data)
        info_site = DB.session.query(InfoSite).get(id_site)
        ...
    '''
    #TODO
    pass


@blueprint.route('/site/<id_site>', methods=['DELETE'])
def delete_site_chiro(id_site):
    '''
    Met à jour un site chiro
    suggestion process :
        info_site = DB.session.query(InfoSite).get(id_site)
        ...
    '''
    #TODO
    pass
