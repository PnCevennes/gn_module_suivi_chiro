'''
Modeles de données propres aux observations suivi chiro
'''


from sqlalchemy import ForeignKey
from geoalchemy2 import Geometry

from geonature.utils.env import DB
from geonature.utils.utilssqlalchemy import serializable, geoserializable
from geonature.core.gn_monitoring.models import TBaseVisits
from pypnnomenclature.models import TNomenclatures

from .counting_contact import CountingContact

@serializable
@geoserializable
class ConditionsVisite(DB.Model):
    '''
        Informations relatives aux conditions dans lesquelles s'est déroulée
        une visite ou une observation propres aux problématiques chiro
    '''
    __tablename__ = 't_visite_conditions'
    __table_args__ = {'schema': 'monitoring_chiro'}

    id_visite_cond = DB.Column(DB.Integer, primary_key=True)
    # fk gn_monitoring.base_visite
    id_base_visit = DB.Column(
        DB.Integer,
        ForeignKey(TBaseVisits.id_base_visit)
    )
    base_visit = DB.relationship(TBaseVisits)
    geom = DB.Column(Geometry('GEOMETRY', 4326))
    temperature = DB.Column(DB.Float)
    humidite = DB.Column(DB.Float)
    id_nomenclature_mod_id = DB.Column(
        DB.Integer,
        ForeignKey(TNomenclatures.id_nomenclature)
    )
