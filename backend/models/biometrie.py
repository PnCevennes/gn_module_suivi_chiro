'''
Modeles de données propres aux biometries suivi chiro
'''


from sqlalchemy import ForeignKey

from geonature.utils.env import DB
from geonature.utils.utilssqlalchemy import serializable


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
            ForeignKey('monitoring_chiro.t_visite_contact_taxon.id_contact_taxon')
            )
    id_nomenclature_life_stage = DB.Column(DB.Integer)
    id_nomenclature_sex = DB.Column(DB.Integer)
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
    meta_create_date = DB.Column(DB.Date)
    meta_update_date = DB.Column(DB.Date)
    id_digitiser = DB.Column(DB.Integer)
