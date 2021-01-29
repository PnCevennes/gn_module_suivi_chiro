"""
Utilitaires pour simplifier la création ou la mise à jour des données
des entités gn_monitoring

À déplacer à terme dans Geonature/backend/gn_monitoring
"""

import logging
from flask import current_app
from sqlalchemy import and_

from geonature.core.gn_monitoring.models import (
    TBaseSites, corSiteModule, TBaseVisits
)

from geonature.core.gn_commons.repositories import (
    TMediaRepository
)
from geonature.core.gn_synthese.utils.process import import_from_table
# from geonature.core.users.models import TRoles

from pypnusershub.db.models import User

from ..models.models import (
    CountingContact,
    RelContactTaxonIndices,
    ContactTaxon
)
from ..models import COR_COUNTING_VALUE

from ..utils.relations import get_updated_relations

# get the root logger
log = logging.getLogger()

def process_synthese(schema_name, table_name, field_name, value):

        try:
            import_from_table(
                schema_name,
                table_name,
                field_name,
                value
            )
        except ValueError as e:
            # warning
            log.warning(
                """Error in module monitoring chiro, process_synthese.
                Function import_from_table with parameters({}, {}, {}) raises the following error :
                {}
                """
                .format(
                    table_name,
                    field_name,
                    value,
                    e
                )
            )

        return

class InvalidBaseSiteData(Exception):
    pass


class GNMonitoringVisiteRepository:
    """
    Création mise à jour des visites gn_monitoring
    """
    def __init__(self, db_sess):
        """
        params:
            db_sess = session DB initialisée par la vue cliente
        """
        self.session = db_sess

    def handle_write(self, *, data=None, id_base_visite=None):
        '''
        Opérations d'écriture sur la donnée
        params:
            data = dictionnaire de données filtrées ou pas
            id_base_visite facultatif (création d'une nouvelle visite)
        '''
        try:
            id_dataset_inventaire = current_app.config["SUIVI_CHIRO"]["id_dataset_inventaire"]
            id_dataset_suivi = current_app.config["SUIVI_CHIRO"]["id_dataset_suivi"]
            id_module = current_app.config.get('SUIVI_CHIRO', {}).get('ID_MODULE')
            if "observers" in data:
                observers = self.session.query(User).\
                    filter(User.id_role.in_(data['observers'])).all()

            if observers:
                data['observers'] = observers

            if id_base_visite is None:
                model = TBaseVisits()
                self.session.add(model)
            else:
                model = self.session.query(TBaseVisits).get(id_base_visite)

            for field in data:
                if hasattr(model, field):
                    setattr(model, field, data[field])

            model.visit_date_max = model.visit_date_min

            # Dataset
            # TODO pour le moment en dur dans la configuration
            #   A voir si peut être mis dans les fichiers de configuration
            if model.id_base_site:
                model.id_dataset = id_dataset_suivi
            else:
                model.id_dataset = id_dataset_inventaire
            model.id_module = id_module
            self.session.flush()  # génération de l'id de la visite
            return model
        except Exception as e:  # vérifier type erreur
            self.session.rollback()
            raise e


class GNMonitoringSiteRepository:
    """
    Création mise à jour des sites gn_monitoring
    """
    def __init__(self, db_sess, id_app):
        """
        params:
            db_sess = session DB initialisée par la vue cliente
        """
        self.session = db_sess
        self.id_app = id_app

    def handle_write(self, *, data=None, base_site_id=None):
        '''
        Opérations d'écriture sur la donnée
        params:
            data = dictionnaire de données filtrées ou pas
            base_site_id facultatif (création d'une nouvelle geom)
        '''
        try:
            if base_site_id is None:
                # nouvelle geom
                model = TBaseSites()
                self.session.add(model)
            else:
                data['id_base_site'] = base_site_id
                model = self.session.query(TBaseSites).get(base_site_id)

            # gestion de la géometrie
            for field in data:
                if hasattr(model, field):
                    setattr(model, field, data[field])

            self.session.flush()  # génération de l'id de site

            # insertion id application
            app = self.session.query(corSiteModule).filter(and_(
                corSiteModule.c.id_base_site == model.id_base_site,
                corSiteModule.c.id_module == self.id_app)
            ).all()
            if not len(app):
                stmt = corSiteModule.insert().values(
                    id_base_site=model.id_base_site, id_module=self.id_app
                )
                self.session.execute(stmt)

            return model
        except ValueError:  # vérifier type erreur
            raise InvalidBaseSiteData()

    def handle_delete(self, base_site_id, cascade):
        '''
        suppression de la donnée
        (ne devrait être utilisé qu'en cas d'erreur de saisie)
        params:
            base_site_id
        Supprime la relation du site à l'application en cours
        Supprime totalement le site s'il n'est plus lié à aucune application
        '''

        # 1 vérifier que le site n'existe pas pour plusieurs applications
        apps = self.session.query(corSiteModule).filter(
            corSiteModule.c.id_base_site == base_site_id
        ).all()
        nb_apps = len(apps)
        if nb_apps == 0:
            # site dans aucune application
            raise InvalidBaseSiteData()

        # 2 : rompre le lien site <-> application
        cur_link = list(filter(lambda x: x[1] == self.id_app, apps))
        if not len(cur_link):
            # site non référencé pour l'application
            raise InvalidBaseSiteData()
        stmt = (corSiteModule.delete()
                .where(corSiteModule.c.id_module == self.id_app)
                .where(corSiteModule.c.id_base_site == base_site_id))
        self.session.execute(stmt)

        # si le site n'existe pas pour une autre application :
        #   3 : supprimer le site
        if nb_apps == 1 and cascade is True:
            model = self.session.query(TBaseSites).get(base_site_id)
            self.session.delete(model)
            return True  # vrai en cas de suppression du site

        # faux si le site est juste déréférencé pour l'application
        return False

    def sync_synthese(self, uuid):
        process_synthese(
            'monitoring_chiro',
            'v_chiro_gn_synthese',
            'uuid_base_site',
            uuid
        )


class GNMonitoringContactTaxon():
    """
    Création mise à jour des sites gn_monitoring
    """
    # tableau de correspondance dans le cadre de la saisie rapide
    # @TODO mettre en parametre de configuration
    cor_counting_life_stage = COR_COUNTING_VALUE["STADE_VIE"]
    cor_counting_sex = COR_COUNTING_VALUE["SEXE"]

    def __init__(self, db_sess, data, saisie_rapide=False):
        """
        params:
            db_sess : session DB initialisée par la vue cliente
            data : Données relative au contact taxons
            saisie_rapide : Indique s'il y a eu une saisie rapide des taxons
                implique un traitement particulier
        """
        self.session = db_sess
        self.data = data
        self.saisie_rapide = saisie_rapide

        self.id_contact_taxon = (
            data['id_contact_taxon'] if 'id_contact_taxon' in data else None
        )

        if saisie_rapide:
            self.denombrements = self.prepare_data_sasie_rapide()
        else:
            if 'denombrements' in data:
                self.denombrements = self.data['denombrements']
        self.data.pop('denombrements', None)

    def prepare_data_sasie_rapide(self):
        denombrements = []
        for key in self.data:
            if key.startswith('denombrement.') and self.data[key]:
                (sex, live_stage) = key[13:].split('_')
                denombrement = {
                    'id_nomenclature_life_stage': self.cor_counting_life_stage[live_stage],
                    'id_nomenclature_sex': self.cor_counting_sex[sex],
                    'count_min': self.data[key],
                    'count_max': self.data[key],
                    'id_nomenclature_obj_count': COR_COUNTING_VALUE["OBJ_DENBR"]["individu"],
                    'id_nomenclature_type_count': COR_COUNTING_VALUE["TYP_DENBR"]["Compté"]
                }
                denombrements.append(denombrement)

        return denombrements

    def handle_write(self):

        # creation contact taxon
        data_occ = {}

        for field in self.data:
            if hasattr(ContactTaxon, field):
                data_occ[field] = self.data[field]

        if 'indices' in data_occ:
            data_occ.pop('indices')
        contact_taxon = ContactTaxon(**data_occ)

        if 'indices' in self.data:
            indices = [rel for rel in get_updated_relations(
                self.session,
                RelContactTaxonIndices,
                self.data['indices'],
                self.id_contact_taxon,
                'id_contact_taxon',
                'id_nomenclature_indice'
            )]
            contact_taxon.indices = indices

        # creation dénombrement
        self.data['denombrements'] = []
        for d in self.denombrements:
            attliste = [k for k in d]
            for att in attliste:
                if not getattr(CountingContact, att, False):
                    d.pop(att)
            counting = CountingContact(**d)
            contact_taxon.denombrements.append(counting)

        if self.id_contact_taxon:
            self.session.merge(contact_taxon)
        else:
            self.session.add(contact_taxon)
        try:
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise(e)

        # Création des média
        if 'medium' in self.data:
            attach_uuid_to_medium(
                self.data['medium'],
                contact_taxon.uuid_chiro_visite_contact_taxon
            )
        for ctd in contact_taxon.denombrements:
            self.sync_synthese(ctd.unique_id_sinp)

        return contact_taxon

    def sync_synthese(self, uuid):
        process_synthese(
            'monitoring_chiro',
            'v_chiro_gn_synthese',
            'unique_id_sinp',
            uuid
        )

def attach_uuid_to_medium(medium, uuid_attached_row):
    '''
        Fonction permettant de ratacher à posteriori
        une liste de media à une entité
    '''
    # Si liste vide aucun traitement
    if not medium:
        return

    for m in medium:
        m['uuid_attached_row'] = uuid_attached_row
        mr = TMediaRepository(data=m, id_media=m['id_media'])
        mr.media.uuid_attached_row = uuid_attached_row
        mr._persist_media_db()


