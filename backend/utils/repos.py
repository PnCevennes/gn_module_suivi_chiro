"""
Utilitaires pour simplifier la création ou la mise à jour des données
des entités gn_monitoring

À déplacer à terme dans Geonature/backend/gn_monitoring
"""
from geonature.core.gn_monitoring.models import TBaseSites


class InvalidBaseSiteData(Exception):
    pass


class GNMonitoringSiteRepository:
    """
    Création mise à jour des sites gn_monitoring
    """
    def __init__(self, db_sess):
        """
        params:
            db_sess = session DB initialisée par la vue cliente
        """
        self.session = db_sess

    def handle_write(self, *, data=None, base_site_id=None):
        '''
        Opérations d'écriture sur la donnée
        params:
            data = dictionnaire de données filtrées ou pas
            base_site_id facultatif (création d'une nouvelle geom)
        '''
        if base_site_id is None:
            # nouvelle geom
            model = TBaseSites()
            self.session.add(model)
        else:
            model = self.session.query(TBaseSites).get(base_site_id)
        try:
            for field in data:
                if hasattr(model, field):
                    setattr(model, field, data[field])

            self.session.flush() # génération de l'id de site
            return model
        except ValueError: # vérifier type erreur
            raise InvalidBaseSiteData()

    def handle_delete(self, base_site_id):
        '''
        suppression de la donnée
        (ne devrait être utilisé qu'en cas d'erreur de saisie)
        params:
            base_site_id
        '''
        model = self.session.query(TBaseSites).get(base_site_id)
        self.session.delete(model)

