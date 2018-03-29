from flask import request

from geonature.utils.env import DB
from geonature.utils.utilssqlalchemy import json_resp

from ..blueprint import blueprint as routes
from ..models.observation_taxon import ContactTaxon


@routes.route('/observation_taxons/<id_base_visit>', methods=['GET'])
@json_resp
def get_observation_taxons_chiro(id_base_visit):
    results = (DB.session.query(ContactTaxon)
            .filter(ContactTaxon.id_base_visit==id_base_visit)
            .all())
    return [otx.as_dict(recursif=True) for otx in results]


@routes.route('/observation_taxon/<id_observation_taxon>', methods=['GET'])
def get_one_observation_taxon_chiro(id_observation_taxon):
    pass


@routes.route('/observation_taxon', methods=['POST', 'PUT'])
def create_observation_taxon_chiro():
    pass


@routes.route('/observation_taxon/<id_observation_taxon>', methods=['POST', 'PUT'])
def update_observation_taxon_chiro(id_observation_taxon):
    pass


@routes.route('/observation_taxon/<id_observation_taxon>', methods=['DELETE'])
def delete_observation_taxon_chiro(id_observation_taxon):
    pass

