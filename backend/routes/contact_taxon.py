'''
    Routes permettant de manipuler et récupérer les
    données relatives au contact taxon
'''

from flask import request
from sqlalchemy.orm.exc import NoResultFound

from geonature.utils.env import DB
from geonature.utils.utilssqlalchemy import json_resp
from geonature.core.gn_commons.repositories import TMediumRepository


from ..blueprint import blueprint
from ..models.contact_taxon import ContactTaxon, RelContactTaxonIndices
from ..models.counting_contact import CountingContact

from ..utils.relations import get_updated_relations

from ..utils.repos import (
    GNMonitoringContactTaxon
)  # TODO déplacement repos dans core


def _format_occtax_data(data):
    '''
        Procédure de sérialisation non récursive des modèles
    '''
    result = data.as_dict(recursif=False)
    result['id'] = data.id_contact_taxon
    result['indices'] = [
        indice.id_nomenclature_indice
        for indice in data.indices
    ]
    result['denombrements'] = [
        d.as_dict()
        for d in data.denombrements
    ]
    # get medium
    medium = TMediumRepository.get_medium_for_entity(
        data.uuid_chiro_visite_contact_taxon
    )
    if (medium):
        result['medium'] = [m.as_dict() for m in medium]

    return result


@blueprint.route('/contact_taxons/<id_base_visit>', methods=['GET'])
@json_resp
def get_contact_taxons_chiro(id_base_visit):
    '''
        retourne toutes les observations de taxons liées à une visite
        identifiée par `id_base_visit`
    '''
    results = (
        DB.session.query(ContactTaxon)
        .filter(ContactTaxon.id_base_visit == id_base_visit)
        .all()
    )
    return [otx.as_dict(recursif=False) for otx in results]


@blueprint.route('/contact_taxon/<id_contact_taxon>', methods=['GET'])
@json_resp
def get_one_contact_taxon_chiro(id_contact_taxon):
    '''
        Retourne le détail d'un contact taxon
    '''
    result = DB.session.query(ContactTaxon).get(id_contact_taxon)
    if result:
        return _format_occtax_data(result)
    else:
        return {"data": "{} not found".format(id_contact_taxon)}, 404


@blueprint.route('/contact_taxon', methods=['POST', 'PUT'])
@blueprint.route('/contact_taxon/<id_contact_taxon>', methods=['POST', 'PUT'])
@json_resp
def create_or_update_contact_taxon_chiro(id_contact_taxon=None):
    '''
        Création ou mise à jour d'un contact taxon
    '''
    db_sess = DB.session
    data = request.get_json()

    if id_contact_taxon:
        data['id_contact_taxon'] = id_contact_taxon

    contact_taxon = GNMonitoringContactTaxon(
        db_sess, data, saisie_rapide=False
    ).handle_write()

    return _format_occtax_data(contact_taxon)


@blueprint.route('/obs_taxon/many', methods=['POST', 'PUT'])
@json_resp
def create_many_contact_taxon_chiro():
    '''
        Création d'enregistrements
        de contact taxon en mode saisie rapide
    '''
    db_sess = DB.session
    data = request.get_json()

    id_base_visit = data.get('refId', None)
    ids = []
    __taxons__ = data['__items__'] if '__items__' in data else None
    if __taxons__:
        for contact in __taxons__:
            contact['id_base_visit'] = id_base_visit
            data = GNMonitoringContactTaxon(db_sess, contact, True).handle_write()
            ids.append(data.id_contact_taxon)
    return {"ids": ids}



@blueprint.route('/contact_taxon/<id_contact_taxon>', methods=['DELETE'])
@json_resp
def delete_contact_taxon_chiro(id_contact_taxon):
    '''
        Suppression d'un enregistrement de contact taxon
    '''
    try:
        contact = DB.session.query(ContactTaxon).filter(
            ContactTaxon.id_contact_taxon == id_contact_taxon
        ).one()
    except NoResultFound:
        return {}, 404

    else:
        try:
            DB.session.delete(contact)
            DB.session.commit()
            return {'data': id_contact_taxon}
        except Exception:
            DB.session.rollback()
            return ({
                'data': id_contact_taxon,
                'errmsg': 'Erreur de suppression'
                }, 400)


