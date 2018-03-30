from flask import request

from geonature.utils.env import DB
from geonature.utils.utilssqlalchemy import json_resp

from ..blueprint import blueprint
from ..models.biometrie import Biometrie


@blueprint.route('/biometries/<id_contact_taxon>', methods=['GET'])
@json_resp
def get_biometries_chiro(id_contact_taxon):
    bioms = (DB.session.query(Biometrie)
            .filter(Biometrie.id_contact_taxon==id_contact_taxon)
            .all())
    return [biom.as_dict() for biom in bioms]


@blueprint.route('/biometrie/<id_biometrie>', methods=['GET'])
@json_resp
def get_one_biometrie_chiro(id_biometrie):
    biom = DB.session.query(Biometrie).get(id_biometrie)
    return biom.as_dict()


@blueprint.route('/biometrie', methods=['POST', 'PUT'])
def create_biometrie_chiro():
    pass


@blueprint.route('/biometrie/<id_biometrie>', methods=['POST', 'PUT'])
def update_biometrie_chiro(id_biometrie):
    pass


@blueprint.route('/biometrie/<id_biometrie>', methods=['DELETE'])
def delete_biometrie_chiro(id_biometrie):
    pass

