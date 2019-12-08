'''
    Routes permettant de manipuler les objets biometrie
'''
from flask import request

from sqlalchemy.orm.exc import NoResultFound

from geonature.utils.env import DB
from geonature.utils.utilssqlalchemy import json_resp, GenericQuery
from geonature.core.gn_permissions import decorators as permissions

from ..blueprint import blueprint
from ..models.models import Biometrie


def _format_biometrie_data(data):
    biom = data.as_dict()
    biom['id'] = data.id_biometrie
    return biom


@blueprint.route('/biometries/<id_contact_taxon>', methods=['GET'])
@permissions.check_cruved_scope("R", False, module_code="SUIVI_CHIRO")
@json_resp
def get_biometries_chiro(id_contact_taxon):
    '''
        Récupération de l'ensemble des biométries
        associé à un contact taxon
    '''

    limit = int(request.args.get('limit', 1000))
    offset = int(request.args.get('offset', 0))
    data = GenericQuery(
        DB.session, 'v_biometrie', 'monitoring_chiro', None,
        {"id_contact_taxon": id_contact_taxon}, limit, offset
    ).return_query()

    data["total"] = data["total_filtered"]
    return data


@blueprint.route('/biometrie/<id_biometrie>', methods=['GET'])
@permissions.check_cruved_scope("R", False, module_code="SUIVI_CHIRO")
@json_resp
def get_one_biometrie_chiro(id_biometrie):
    '''
        Récupération du détail d'une biométrie
    '''
    biom = DB.session.query(Biometrie).get(id_biometrie)
    return _format_biometrie_data(biom)


@blueprint.route('/biometrie', methods=['POST', 'PUT'])
@blueprint.route('/biometrie/<id_biometrie>', methods=['POST', 'PUT'])
@permissions.check_cruved_scope("C", False, module_code="SUIVI_CHIRO")
@json_resp
def create_or_update_biometrie_chiro(id_biometrie=None):
    '''
        Création ou mise à jour d'une biométrie
    '''
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
        return {e.args}, 500

    return _format_biometrie_data(biom)


@blueprint.route('/biometrie/<id_biometrie>', methods=['DELETE'])
@permissions.check_cruved_scope("D", False, module_code="SUIVI_CHIRO")
@json_resp
def delete_biometrie_chiro(id_biometrie):
    '''
        Suppression d'une biométrie
    '''
    try:
        visite = DB.session.query(Biometrie).filter(
            Biometrie.id_biometrie == id_biometrie
        ).one()
    except NoResultFound:
        return {}, 404

    else:
        try:
            DB.session.delete(visite)
            DB.session.commit()
            return {'data': id_biometrie}
        except Exception:
            DB.session.rollback()
            return (
                {
                    'data': id_biometrie,
                    'errmsg': 'Erreur de suppression'
                },
                400
            )
