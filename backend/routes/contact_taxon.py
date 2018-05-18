from flask import request

from geonature.utils.env import DB
from geonature.utils.utilssqlalchemy import json_resp
from geonature.core.gn_commons.repositories import TMediumRepository

from pypnnomenclature.models import TNomenclatures


from ..blueprint import blueprint
from ..models.contact_taxon import ContactTaxon, RelContactTaxonIndices
from ..models.counting_contact import CountingContact

from ..utils.relations import get_updated_relations

from ..utils.repos import (
    attach_uuid_to_medium
 ) # TODO déplacement repos dans core

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
    result = DB.session.query(ContactTaxon).get(id_contact_taxon)
    return _format_occtax_data(result)


@blueprint.route('/contact_taxon', methods=['POST', 'PUT'])
@json_resp
def create_contact_taxon_chiro():
    db_sess = DB.session
    data = request.get_json()

    data['indices'] = [rel for rel in get_updated_relations(
        db_sess,
        RelContactTaxonIndices,
        data['indices'],
        None,
        'id_contact_taxon',
        'id_nomenclature_indice'
    )]

    # creation dénombrement
    denombrements = []
    if 'denombrements' in data:
        for d in data['denombrements']:
            counting = CountingContact()
            if d:
                for field in d:
                    if hasattr(counting, field):
                        setattr(counting, field, d[field])
                denombrements.append(counting)
        data["denombrements"] = denombrements

    # creation contact taxon
    contact_taxon = ContactTaxon()
    for field in data:
        if hasattr(contact_taxon, field):
            setattr(contact_taxon, field, data[field])

    db_sess.add(contact_taxon)
    db_sess.commit()

    # Création des média
    if (data['medium']):
        attach_uuid_to_medium(
            data['medium'],
            contact_taxon.uuid_chiro_visite_contact_taxon
        )

    return _format_occtax_data(contact_taxon)

@blueprint.route('/contact_taxon/<id_contact_taxon>', methods=['POST', 'PUT'])
def update_contact_taxon_chiro(id_contact_taxon):
    pass


@blueprint.route('/contact_taxon/<id_contact_taxon>', methods=['DELETE'])
def delete_contact_taxon_chiro(id_contact_taxon):
    pass

