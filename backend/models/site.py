'''
Modeles de données propres aux sites suivi chiro
'''


from sqlalchemy import ForeignKey

from geonature.utils.env import DB
from geonature.utils.utilssqlalchemy import (
        serializable,
        geoserializable)
from geonature.core.gn_monitoring.models import TBaseSites
from geonature.core.gn_medias.models import TMedias
from pypnnomenclature.models import TNomenclatures


@serializable
class RelChirositeTNomenclaturesMenace(DB.Model):
    '''
    Correspondances entre id nomenclatures des menaces et sites
    '''
    __tablename__ = 'cor_site_infos_nomenclature_menaces'
    __table_args__ = {'schema': 'monitoring_chiro'}
    id_site_infos = DB.Column(
        DB.Integer,
        ForeignKey('monitoring_chiro.t_site_infos.id_site_infos'),
        primary_key=True
    )
    id_nomenclature_menaces = DB.Column(
        DB.Integer,
        #ForeignKey('ref_nomenclatures.t_nomenclatures.id_nomenclature'),
        ForeignKey(TNomenclatures.id_nomenclature),
        primary_key=True
    )


@serializable
class RelChirositeTNomenclaturesAmenagement(DB.Model):
    '''
    Correspondances entre id nomenclatures des amenagements et sites
    '''
    __tablename__ = 'cor_site_infos_nomenclature_amenagements'
    __table_args__ = {'schema':'monitoring_chiro'}
    id_site_infos = DB.Column(
        DB.Integer,
        ForeignKey('monitoring_chiro.t_site_infos.id_site_infos'),
        primary_key=True
    )
    id_nomenclature_amenagement = DB.Column(
        DB.Integer,
        #ForeignKey('ref_nomenclatures.t_nomenclatures.id_nomenclature'),
        ForeignKey(TNomenclatures.id_nomenclature),
        primary_key=True
    )


@serializable
@geoserializable
class InfoSite(DB.Model):
    '''
    Informations propres aux problématiques chiro pour un site donné
    '''
    __tablename__ = 't_site_infos'
    __table_args__ = {'schema': 'monitoring_chiro'}

    id_site_infos = DB.Column(DB.Integer, primary_key=True)
    id_base_site = DB.Column(
            DB.Integer,
            ForeignKey(TBaseSites.id_base_site)
            ) #fk gn_monitoring.base_site
    base_site = DB.relationship(TBaseSites)
    description = DB.Column(DB.UnicodeText)
    id_nomenclature_frequentation = DB.Column(DB.Integer) #rel nomenclature
    menace_cmt = DB.Column(DB.Unicode(250))
    actions = DB.Column(DB.Unicode(250))
    menaces_ids = DB.relationship(
            RelChirositeTNomenclaturesMenace,
            lazy='joined')
    amenagements_ids = DB.relationship(
            RelChirositeTNomenclaturesAmenagement,
            lazy='joined')
    site_actif = DB.Column(DB.Boolean, default=False)
    contact_nom = DB.Column(DB.Unicode(25))
    contact_prenom = DB.Column(DB.Unicode(25))
    contact_adresse = DB.Column(DB.Unicode(150))
    contact_code_postal = DB.Column(DB.Unicode(5))
    contact_ville = DB.Column(DB.Unicode(100))
    contact_telephone = DB.Column(DB.Unicode(15))
    contact_portable = DB.Column(DB.Unicode(15))
    contact_commentaire = DB.Column(DB.Unicode(250))
