'''
Modeles de données propres aux observations de taxons suivi chiro
'''


from sqlalchemy import ForeignKey

from geonature.utils.env import DB
from geonature.utils.utilssqlalchemy import serializable

from geonature.core.gn_monitoring.models import TBaseVisits
from pypnnomenclature.models import TNomenclatures

from .counting_contact import CountingContact


@serializable
class RelContactTaxonIndices(DB.Model):
    '''
    Relation entre informations de contact taxon et indices de présence
    '''
    __tablename__ = 'cor_contact_taxons_nomenclature_indices'
    __table_args__ = {'schema': 'monitoring_chiro'}
    id_contact_taxon = DB.Column(
        DB.Integer,
        ForeignKey('monitoring_chiro.t_visite_contact_taxons.id_contact_taxon'),
        primary_key=True
    )
    id_nomenclature_indice = DB.Column(
        DB.Integer,
        ForeignKey(TNomenclatures.id_nomenclature),
        primary_key=True
    )


@serializable
class ContactTaxon(DB.Model):
    '''
    Informations recueillies sur un taxon donné lors d'une visite
    '''
    __tablename__ = 't_visite_contact_taxons'
    __table_args__ = {'schema': 'monitoring_chiro'}
    id_contact_taxon = DB.Column(DB.Integer, primary_key=True)
    id_base_visit = DB.Column(
        DB.Integer,
        ForeignKey(TBaseVisits.id_base_visit)
    )
    tx_presume = DB.Column(DB.Unicode(250))
    cd_nom = DB.Column(DB.Integer)
    nom_complet = DB.Column(DB.Unicode(250))
    espece_incertaine = DB.Column(DB.Boolean, default=False)
    id_nomenclature_activite = DB.Column(DB.Integer)
    id_nomenclature_preuve_repro = DB.Column(DB.Integer)
    indices_cmt = DB.Column(DB.Unicode(250))
    commentaire = DB.Column(DB.Unicode(250))
    id_digitiser = DB.Column(DB.Integer)

    denombrements = DB.relationship("CountingContact")
    indices = DB.relationship(
            RelContactTaxonIndices,
            lazy='joined')

