'''
point d'entrée du module chiro
'''

from flask import Blueprint, request

from geonature.utils.env import DB
from geonature.utils.utilssqlalchemy import json_resp

from .models.site import InfoSite

ID_APP = 101 # TODO récupérer l'identifiant d'application par le front


blueprint = Blueprint('gn_module_suivi_chiro', __name__)


def load_site(id_site):
    result = DB.session.query(InfoSite).filter_by(id_base_site=id_site).one()
    return {
            'id': id_site,
            'link': '#/suivi_chiro/site/%s' % id_site,
            'label': result.base_site.base_site_name
            }


@blueprint.route('/')
def gn_module_suivi_chiro_index():
    return 'Ca marche yep yep'


@blueprint.route('/config/breadcrumb')
@json_resp
def breadcrumb():
    view = request.args.get('view')
    id_obj = request.args.get('id', None)

    out = [{'id': None, 'link': '#/suivi_chiro/site', 'label': 'Sites'}]

    if view == 'site':
        if id_obj:
            out.append(load_site(id_obj))

    return out


from .routes import (
        site,
        visite,
        contact_taxon,
        biometrie
        )
