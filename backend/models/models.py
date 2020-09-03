'''
Modeles de données propres au suivi chiro
'''


from sqlalchemy import ForeignKey, select, func
from sqlalchemy.dialects.postgresql import UUID

from geoalchemy2 import Geometry

from geonature.utils.env import DB
from geonature.utils.utilssqlalchemy import (
        serializable,
        geoserializable
)
from geonature.core.gn_monitoring.models import TBaseSites, TBaseVisits
from pypnnomenclature.models import TNomenclatures


@serializable
class Biometrie(DB.Model):
    '''
    Données de biométrie sur un individu
    '''
    __tablename__ = 't_contact_taxon_biometries'
    __table_args__ = {'schema': 'monitoring_chiro'}
    id_biometrie = DB.Column(DB.Integer, primary_key=True)
    id_contact_taxon = DB.Column(
        DB.Integer,
        ForeignKey('monitoring_chiro.t_visite_contact_taxons.id_contact_taxon')
    )
    id_nomenclature_life_stage = DB.Column(DB.Integer)
    id_nomenclature_sex = DB.Column(DB.Integer)
    ab = DB.Column(DB.Float)
    poids = DB.Column(DB.Float)
    d3mf1 = DB.Column(DB.Float)  # mesure doigt3 phalange 1
    d3f2f3 = DB.Column(DB.Float)  # mesure doigt3 phalanges 2-3
    d3total = DB.Column(DB.Float)  # total doigt 3
    d5 = DB.Column(DB.Float)  # mesure doigt 5
    cm3sup = DB.Column(DB.Float)  # mesure canine - 3e molaire sup
    cm3inf = DB.Column(DB.Float) #mesure canine - 3e molaire inf
    cb = DB.Column(DB.Float)  # mesure condylobasale
    lm = DB.Column(DB.Float)  # mesure mandibule inf
    oreille = DB.Column(DB.Float)
    commentaire = DB.Column(DB.Unicode(250))
    id_digitiser = DB.Column(DB.Integer)


@serializable
class CountingContact(DB.Model):
    __tablename__ = 'cor_counting_contact'
    __table_args__ = {'schema': 'monitoring_chiro'}
    id_counting_contact = DB.Column(DB.Integer, primary_key=True)
    id_contact_taxon = DB.Column(
        DB.Integer,
        ForeignKey('monitoring_chiro.t_visite_contact_taxons.id_contact_taxon')
    )
    # Correspondance nomenclature INPN = stade_vie (10)
    id_nomenclature_life_stage = DB.Column(DB.Integer)
    # Correspondance nomenclature INPN = sexe (9)
    id_nomenclature_sex = DB.Column(DB.Integer)
    # Correspondance nomenclature INPN = obj_denbr (6)
    id_nomenclature_obj_count = DB.Column(
        DB.Integer,
        default=select([func.ref_nomenclatures.get_id_nomenclature('OBJ_DENBR', 'IND')])
    )
    # Correspondance nomenclature INPN = typ_denbr (21)
    id_nomenclature_type_count = DB.Column(
        DB.Integer,
        default=select([func.ref_nomenclatures.get_id_nomenclature('TYP_DENBR', 'Co')])
    )
    count_min = DB.Column(DB.Integer)
    count_max = DB.Column(DB.Integer)
    unique_id_sinp = DB.Column(
        UUID(as_uuid=True),
        default=select([func.uuid_generate_v4()])
    )


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
    id_nomenclature_behaviour = DB.Column(DB.Integer)
    id_nomenclature_preuve_repro = DB.Column(DB.Integer)
    id_nomenclature_bio_condition = DB.Column(DB.Integer)
    id_nomenclature_observation_status = DB.Column(DB.Integer)
    indices_cmt = DB.Column(DB.Unicode(250))
    commentaire = DB.Column(DB.Unicode(250))
    id_digitiser = DB.Column(DB.Integer)
    uuid_chiro_visite_contact_taxon = DB.Column(
        UUID(as_uuid=True),
        default=select([func.uuid_generate_v4()])
    )

    denombrements = DB.relationship(
        "CountingContact",
        cascade="all, delete-orphan"
    )
    indices = DB.relationship(
        RelContactTaxonIndices,
        lazy='joined',
        cascade="all, delete-orphan"
    )


@serializable
@geoserializable
class ConditionsVisite(DB.Model):
    '''
        Informations relatives aux conditions dans lesquelles s'est déroulée
        une visite ou une observation propres aux problématiques chiro
    '''
    __tablename__ = 't_visite_conditions'
    __table_args__ = {'schema': 'monitoring_chiro'}

    id_base_visit = DB.Column(
        DB.Integer,
        ForeignKey(TBaseVisits.id_base_visit),
        primary_key=True
    )
    base_visit = DB.relationship(TBaseVisits)
    geom = DB.Column(Geometry('GEOMETRY', 4326))
    temperature = DB.Column(DB.Float)
    humidite = DB.Column(DB.Float)
    id_nomenclature_mod_id = DB.Column(
        DB.Integer,
        ForeignKey(TNomenclatures.id_nomenclature)
    )


@serializable
class RelChirositeTNomenclaturesMenace(DB.Model):
    '''
    Correspondances entre id nomenclatures des menaces et sites
    '''
    __tablename__ = 'cor_site_infos_nomenclature_menaces'
    __table_args__ = {'schema': 'monitoring_chiro'}
    id_base_site = DB.Column(
        DB.Integer,
        ForeignKey('monitoring_chiro.t_site_infos.id_base_site'),
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
    __table_args__ = {'schema': 'monitoring_chiro'}
    id_base_site = DB.Column(
        DB.Integer,
        ForeignKey('monitoring_chiro.t_site_infos.id_base_site'),
        primary_key=True
    )
    id_nomenclature_amenagement = DB.Column(
        DB.Integer,
        # ForeignKey('ref_nomenclatures.t_nomenclatures.id_nomenclature'),
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

    id_base_site = DB.Column(
        DB.Integer,
        ForeignKey(TBaseSites.id_base_site),
        primary_key=True
    )
    base_site = DB.relationship(TBaseSites)
    description = DB.Column(DB.UnicodeText)
    # rel nomenclature
    id_nomenclature_frequentation = DB.Column(DB.Integer)
    menace_cmt = DB.Column(DB.Unicode(250))
    actions = DB.Column(DB.Unicode(250))
    menaces_ids = DB.relationship(
        RelChirositeTNomenclaturesMenace,
        lazy='joined',
        passive_updates=False
    )
    amenagements_ids = DB.relationship(
        RelChirositeTNomenclaturesAmenagement,
        lazy='joined',
        passive_updates=False
    )
    site_actif = DB.Column(DB.Boolean, default=False)
    contact_nom = DB.Column(DB.Unicode(25))
    contact_prenom = DB.Column(DB.Unicode(25))
    contact_adresse = DB.Column(DB.Unicode(150))
    contact_code_postal = DB.Column(DB.Unicode(5))
    contact_ville = DB.Column(DB.Unicode(100))
    contact_telephone = DB.Column(DB.Unicode(15))
    contact_portable = DB.Column(DB.Unicode(15))
    contact_commentaire = DB.Column(DB.Unicode(250))
