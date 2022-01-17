'''
point d'entrée du module chiro
'''

from sqlalchemy.orm.exc import NoResultFound


from flask import Blueprint, request, current_app, jsonify

from geonature.utils.env import DB
from geonature.utils.utilssqlalchemy import json_resp

from geonature.core.gn_monitoring.models import TBaseVisits
from .models.models import InfoSite, ContactTaxon, Biometrie



import os 
 
from .utils.config_manager import generate_config

from geonature.core.gn_permissions import decorators as permissions
 

blueprint = Blueprint('gn_module_suivi_chiro', __name__)


def base_breadcrumb(type):
    if type == 'site':
       return {'id': None, 'link': '#/suivi_chiro/site', 'label': 'Sites'}
    elif type == 'inventaire':
        return {'id': None, 'link': '#/suivi_chiro/inventaire', 'label': 'Inventaire'}
    else:
        return {}

def load_site(id_site):
    try:
        result = DB.session.query(InfoSite).filter_by(id_base_site=id_site).one()
        return [
            base_breadcrumb('site'),
            {
                'id': id_site,
                'link': '#/suivi_chiro/site/%s' % id_site,
                'label': result.base_site.base_site_name
            }
        ]
    except NoResultFound:
        return [base_breadcrumb('inventaire')]



def load_visite(id_visite):
    result = DB.session.query(
        TBaseVisits
    ).filter_by(id_base_visit=id_visite).one()

    bread = load_site(result.id_base_site)

    if len(bread) == 1:
        link = "inventaire"
    else:
        link = "observation"
    bread.append({
        'id': id_visite,
        'link': '#/suivi_chiro/{}/{}'.format(link, id_visite),
        'label': str(result.visit_date_min)
    })
    return bread


def load_taxon(id_taxon):
    result = DB.session.query(
        ContactTaxon
    ).filter_by(id_contact_taxon=id_taxon).one()

    bread = load_visite(result.id_base_visit)
    bread.append({
        'id': id_taxon,
        'link': '#/suivi_chiro/taxons/%s' % id_taxon,
        'label': str(result.nom_complet)
    })
    return bread


def load_biometrie(id_biometrie):
    result = DB.session.query(
        Biometrie
    ).filter_by(id_biometrie=id_biometrie).one()

    bread = load_taxon(result.id_contact_taxon)
    bread.append({
        'id': id_biometrie,
        'link': '#/suivi_chiro/biometrie/%s' % id_biometrie,
        'label': str(result.id_biometrie)
    })
    return bread


@blueprint.route('/config/breadcrumb')
@json_resp
def breadcrumb():
    view = request.args.get('view')
    id_obj = request.args.get('id', None)

    out = []

    if id_obj:
        if view == 'site':
            out = load_site(id_obj)
        elif view == 'observation' or view == 'inventaire':
            out = load_visite(id_obj)
        elif view == 'taxons':
            out = load_taxon(id_obj)
        elif view == 'biometrie':
            out = load_biometrie(id_obj)
    else:
        out = [base_breadcrumb(view)]
    return out




from .routes import (
    site,
    visite,
    contact_taxon,
    biometrie
)


# PATCH lié à la suppression de la route config du coeur de GeoNature et à son déplacement dans le module chiro
@blueprint.route("/config", methods=["GET"])
@permissions.check_cruved_scope("R", False, module_code="SUIVIS")
def get_config():
    """
        Parse and return configuration files as toml
        
        Définition de routes "génériques"  c-a-d pouvant servir à tous modules
        Initialement situé dans le coeur de GeoNature mais considéré comme trop spécifique
            la route et les méthodes afférentes ont été déplacées dans le module chiro
            qui est le seul à ma connaissance à utiliser ce mécanisme
    """
    app_name = request.args.get("app", "base_app")
    vue_name = request.args.getlist("vue")

    base_path = os.path.abspath(os.path.join(current_app.static_folder, "configs"))
    conf_path = os.path.abspath(
            os.path.join(base_path, app_name, *vue_name)
    )
    # test : file inside config folder
    if not conf_path.startswith(base_path):
        return "Not a valid config path", 404

    if not vue_name:
        vue_name = ["default"]
    filename = "{}.toml".format(
        conf_path
    )
    config_file = generate_config(filename)
    return jsonify(config_file)
