'''
Modeles de données propres aux sites suivi chiro
'''


from sqlalchemy import ForeignKey

from geonature.utils.env import DB
from geonature.utils.utilssqlalchemy import serializable
from geonature.core.gn_monitoring.models import TBaseSites
from geonature.core.gn_medias.models import TMedias


@serializable
class InfoSite(TBaseSites):
    '''
    Informations propres aux problématiques chiro pour un site donné
    '''
    __tablename__ = 't_pr_site_infos'
    __table_args__ = {'schema': 'chiro'}
    __mapper_args__ = {
            'column_prefix': 'cis_',
            'polymorphic_identity': 'chiro_info_site',
            'polymorphic_on': 'protocol_complements'
            }
    bs_id = DB.Column('fk_bs_id', DB.Integer) #fk gn_monitoring.base_site
    id = DB.Column(DB.Integer, primary_key=True)
    frequentation = DB.Column(DB.Integer) #rel thesaurus
    menaces = DB.relationship(
           Thesaurus,
           secondary='rel_chirosite_thesaurus_menace',
           lazy='joined'
            )
    menace_cmt = DB.Column(DB.Unicode(250))
    actions = DB.Column(DB.Unicode(250))
    amenagements = DB.relationship(
            Thesaurus,
            secondary='rel_chirosite_thesaurus_amenagement',
            lazy='joined'
            )
    fichiers = DB.relationship(
            TMedias,
            secondary='rel_chirosite_fichiers',
            lazy='joined'
            )
    site_actif = DB.Column(DB.Boolean, default=False)
    contact_nom = DB.Column(DB.Unicode(25))
    contact_prenom = DB.Column(DB.Unicode(25))
    contact_adresse = DB.Column(DB.Unicode(150))
    contact_codepostal = DB.Column(DB.Unicode(5))
    contact_ville = DB.Column(DB.Unicode(100))
    contact_telephone = DB.Column(DB.Unicode(15))
    contact_portable = DB.Column(DB.Unicode(15))
    contact_commentaire = DB.Column(DB.Unicode(250))


class RelChirositeThesaurusMenace(DB.Model):
    '''
    Relations entre les sites chiro et les définitions de la nomenclature relatives aux menaces
    '''
    __tablename__ = 'rel_chirosite_thesaurus_menace'
    __table_args__ = {'schema': 'chiro'}
    id_cis = DB.Column(
            DB.Integer,
            DB.ForeignKey(InfoSite.cis_id),
            primary_key=True)
    id_menace = DB.Column(
            DB.Integer,
            DB.ForeignKey('nomenclatures.t_nomenclatures.id_nomenclature'),
            primary_key=True)


class RelChirositeThesaurusAmenagement(DB.Model):
    '''
    Relations entre les sites chiro et les définitions de la nomenclature relatives aux aménagements
    '''
    __tablename__ = 'rel_chirosite_thesaurus_amenagement'
    __table_args__ = {'schema': 'chiro'}
    id_cis = DB.Column(
            DB.Integer,
            DB.ForeignKey(InfoSite.id),
            primary_key=True)
    id_menace = DB.Column(
            DB.Integer,
            DB.ForeignKey('nomenclatures.t_nomenclatures.id_nomenclature'),
            primary_key=True)


class RelChirositeMedias(DB.Model):
    '''
    Relations entre les sites chiro et les fichiers liés
    '''
    __tablename__ = 'rel_chirosite_medias'
    __table_args__ = {'schema': 'chiro'}
    id_cis = DB.Column(
            DB.Integer,
            DB.ForeignKey(InfoSite.id),
            primary_key=True)
    id_fichier = DB.Column(
            DB.Integer,
            DB.ForeignKey(TMedias.id_media),
            primary_key=True)


