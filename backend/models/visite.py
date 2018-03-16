'''
Modeles de données propres aux observations suivi chiro
'''


from sqlalchemy import ForeignKey

from geonature.utils.env import DB
from geonature.utils.utilssqlalchemy import serializable
from geonature.core.gn_monitoring.models import TBaseVisits

from .gn_models_imports import TMedias


@serializable
class ConditionsVisite(TBaseVisits):
    '''
    Informations relatives aux conditions dans lesquelles s'est déroulée une visite ou une observation propres aux problématiques chiro
    '''
    __tablename__ = 't_pr_visite_conditions'
    __table_args__ = {'schema': 'chiro'}
    __mapper_args__ = {
            'column_prefix': 'cvc_',
            'polymorphic_identity': 'chiro_condition_visite',
            'polymorphic_on': 'protocol_visit'
            }
    bv_id = DB.Column('fk_bv_id', DB.Integer) #fk gn_monitoring.base_visite
    temperature = DB.Column(DB.Float)
    humidite = DB.Column(DB.Float)
    mod_id = DB.Column(DB.Integer)
