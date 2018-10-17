'''
point d'entrée du module chiro
'''

from sqlalchemy.orm.exc import NoResultFound


from flask import Blueprint, request, current_app

from geonature.utils.env import DB, get_module_id
from geonature.utils.utilssqlalchemy import json_resp

from geonature.core.gn_monitoring.models import TBaseVisits
from .models.models import InfoSite, ContactTaxon, Biometrie

try:
    ID_MODULE = get_module_id('suivi_chiro')
except Exception as e:
    # @TODO gérer erreur lors de l'installation
    ID_MODULE = -1


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
