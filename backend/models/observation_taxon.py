'''
Modeles de données propres aux observations de taxons suivi chiro
'''


from sqlalchemy import ForeignKey

from geonature.utils.env import DB
from geonature.utils.utilssqlalchemy import serializable
from geonature.core.gn_medias.models import TMedias


@serializable
class ObservationTaxon(DB.Model):
    '''
    Informations recueillies sur un taxon donné lors d'une visite
    '''
    __tablename__ = 't_pr_visite_observationtaxon'
    __table_args__ = {'schema': 'chiro'}
    __mapper_args__ = {'column_prefix': 'cotx_'}
    id = DB.Column(DB.Integer, primary_key=True)
    bv_id = DB.Column('fk_bv_id', DB.Integer)
    tx_presume = DB.Column(DB.Unicode(250))
    espece_incertaine = DB.Column(DB.Boolean, default=False)
    effectif_abs = DB.Column(DB.Integer)
    nb_males_adulte = DB.Column(DB.Integer)
    nb_femelles_adulte = DB.Column(DB.Integer)
    nb_males_juvenile = DB.Column(DB.Integer)
    nb_femelles_juvenile = DB.Column(DB.Integer)
    nb_males_indetermine = DB.Column(DB.Integer)
    nb_femelles_indetermine = DB.Column(DB.Integer)
    nb_indetermine_adulte = DB.Column(DB.Integer)
    nb_indetermine_juvenile = DB.Column(DB.Integer)
    nb_indetermine_indetermine = DB.Column(DB.Integer)
    status_validation = DB.Column(DB.Integer)
    commentaires = DB.Column(DB.Unicode(250))
    indices_cmt = DB.Column(DB.Unicode(250))
    cd_nom = DB.Column(DB.Integer)
    nom_complet = DB.Column(DB.Unicode(250))
    validateur = DB.Column(DB.Integer)
    act_id = DB.Column(DB.Integer)
    eff_id = DB.Column(DB.Integer)
    prv_id = DB.Column(DB.Integer)
    num_id = DB.Column(DB.Integer)
    date_validation = DB.Column(DB.Date)
    meta_create_timestamp = DB.Column('meta_create_timestamp', DB.Date)
    meta_update_timestamp = DB.Column('meta_update_timestamp', DB.Date)
    meta_numerisateur_id = DB.Column('meta_numerisateur_id', DB.Integer)


class RelObservationTaxonFichiers(DB.Model):
    '''
    Relation fichiers joints
    '''
    __tablename__ = 'rel_observationtaxon_fichiers'
    __table_args__ = {'schema': 'chiro'}
    cotx_id = DB.Column(
            DB.Integer,
            DB.ForeignKey(ObservationTaxon.id),
            primary_key=True)
    id_fichier = DB.Column(
            DB.Integer,
            DB.ForeignKey(TMedias.id_media),
            primary_key=True)
