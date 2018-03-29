from flask import request
from ..blueprint import routes


@routes.route('/observation_taxons', methods=['GET'])
def get_observation_taxons_chiro():
    pass


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

