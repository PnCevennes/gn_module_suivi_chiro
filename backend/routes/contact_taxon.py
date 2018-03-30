from flask import request

from geonature.utils.env import DB
from geonature.utils.utilssqlalchemy import json_resp

from ..blueprint import blueprint
from ..models.contact_taxon import ContactTaxon


@blueprint.route('/contact_taxons/<id_base_visit>', methods=['GET'])
@json_resp
def get_contact_taxons_chiro(id_base_visit):
    '''
    retourne toutes les observations de taxons liées à une visite
    identifiée par `id_base_visit`
    '''
    results = (DB.session.query(ContactTaxon)
            .filter(ContactTaxon.id_base_visit==id_base_visit)
            .all())
    return [otx.as_dict(recursif=False) for otx in results]


@blueprint.route('/contact_taxon/<id_contact_taxon>', methods=['GET'])
@json_resp
def get_one_contact_taxon_chiro(id_contact_taxon):
    result = DB.session.query(ContactTaxon).get(id_contact_taxon)
    return result.as_dict(recursif=True)


@blueprint.route('/contact_taxon', methods=['POST', 'PUT'])
def create_contact_taxon_chiro():
    pass


@blueprint.route('/contact_taxon/<id_contact_taxon>', methods=['POST', 'PUT'])
def update_contact_taxon_chiro(id_contact_taxon):
    pass


@blueprint.route('/contact_taxon/<id_contact_taxon>', methods=['DELETE'])
def delete_contact_taxon_chiro(id_contact_taxon):
    pass

