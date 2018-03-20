'''
Modeles de données propres aux biometries suivi chiro
'''


from sqlalchemy import ForeignKey

from geonature.utils.env import DB
from geonature.utils.utilssqlalchemy import serializable
from geonature.core.gn_medias.models import TMedias


@serializable
class Biometrie(DB.Model):
    '''
    Données de biométrie sur un individu
    '''
    __tablename__ = 't_subpr_observationtaxon_biometrie'
    __table_args__ = {'schema': 'chiro'}
    __mapper_args__ = {'column_prefix': 'cbio_'}
    id = DB.Column('id', DB.Integer, primary_key=True)
    cotx_id = DB.Column('fk_cotx_id', DB.Integer)
    age_id = DB.Column(DB.Integer)
    sexe_id = DB.Column(DB.Integer)
    ab = DB.Column(DB.Float)
    poids = DB.Column(DB.Float)
    d3mf1 = DB.Column(DB.Float) #mesure doigt3 phalange 1
    d3f2f3 = DB.Column(DB.Float) #mesure doigt3 phalanges 2-3
    d3total = DB.Column(DB.Float) #total doigt 3
    d5 = DB.Column(DB.Float) #mesure doigt 5
    cm3sup = DB.Column(DB.Float) #mesure canine - 3e molaire sup
    cm3inf = DB.Column(DB.Float) #mesure canine - 3e molaire inf
    cb = DB.Column(DB.Float) #mesure condylobasale
    lm = DB.Column(DB.Float) #mesure mandibule inf
    oreille = DB.Column(DB.Float)
    commentaire = DB.Column(DB.Unicode(250))
    meta_create_timestamp = DB.Column('meta_create_timestamp', DB.Date)
    meta_update_timestamp = DB.Column('meta_update_timestamp', DB.Date)
    meta_numerisateur_id = DB.Column('meta_numerisateur_id', DB.Integer)
