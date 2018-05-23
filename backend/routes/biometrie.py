from flask import request

from geonature.utils.env import DB
from geonature.utils.utilssqlalchemy import json_resp

from ..blueprint import blueprint
from ..models.biometrie import Biometrie

def _format_biometrie_data (data):
    biom = data.as_dict()
    biom['id'] = data.id_biometrie
    return biom

@blueprint.route('/biometries/<id_contact_taxon>', methods=['GET'])
@json_resp
def get_biometries_chiro(id_contact_taxon):
    bioms = (
        DB.session.query(Biometrie).filter(
            Biometrie.id_contact_taxon == id_contact_taxon
        ).all()
    )
    return [_format_biometrie_data(biom) for biom in bioms]


@blueprint.route('/biometrie/<id_biometrie>', methods=['GET'])
@json_resp
def get_one_biometrie_chiro(id_biometrie):
    biom = DB.session.query(Biometrie).get(id_biometrie)
    return _format_biometrie_data(biom)


@blueprint.route('/biometrie', methods=['POST', 'PUT'])
@blueprint.route('/biometrie/<id_biometrie>', methods=['POST', 'PUT'])
@json_resp
def create_or_update_biometrie_chiro(id_biometrie=None):
    db_sess = DB.session
    data = request.get_json()

    data_biom = {}
    for field in data:
        if hasattr(Biometrie, field):
            data_biom[field] = data[field]
    biom = Biometrie(**data_biom)

    if id_biometrie:
        db_sess.merge(biom)
    else:
        db_sess.add(biom)

    try:
        db_sess.commit()
    except Exception as e:
        db_sess.rollback()
        raise(e)
        return {e.args}, 500

    return _format_biometrie_data(biom)

@blueprint.route('/biometrie/<id_biometrie>', methods=['DELETE'])
def delete_biometrie_chiro(id_biometrie):
    pass

