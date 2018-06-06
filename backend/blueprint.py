'''
point d'entrée du module chiro
'''

from flask import Blueprint, request

from geonature.utils.env import DB
from geonature.utils.utilssqlalchemy import json_resp

from geonature.core.gn_monitoring.models import TBaseVisits
from .models.site import InfoSite
from .models.contact_taxon import ContactTaxon
from .models.biometrie import Biometrie


ID_APP = 101  # TODO récupérer l'identifiant d'application par le front


blueprint = Blueprint('gn_module_suivi_chiro', __name__)


def load_site(id_site):
    result = DB.session.query(InfoSite).filter_by(id_base_site=id_site).one()
    return {
        'id': id_site,
        'link': '#/suivi_chiro/site/%s' % id_site,
        'label': result.base_site.base_site_name
    }


def load_visite(id_visite):
    result = DB.session.query(
        TBaseVisits
    ).filter_by(id_base_visit=id_visite).one()

    bread = [load_site(result.id_base_site)]

    bread.append({
        'id': id_visite,
        'link': '#/suivi_chiro/observation/%s' % id_visite,
        'label': str(result.visit_date)
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

    out = [{'id': None, 'link': '#/suivi_chiro/site', 'label': 'Sites'}]

    if id_obj:
        if view == 'site':
            out.append(load_site(id_obj))
        if view == 'observation':
            breads = load_visite(id_obj)
            for bread in breads:
                out.append(bread)
        if view == 'taxons':
            breads = load_taxon(id_obj)
            for bread in breads:
                out.append(bread)
        if view == 'biometrie':
            breads = load_biometrie(id_obj)
            for bread in breads:
                out.append(bread)

    return out


from .routes import (
    site,
    visite,
    contact_taxon,
    biometrie
)
