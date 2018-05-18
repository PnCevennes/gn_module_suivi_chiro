from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from geonature.utils.env import DB
from geonature.utils.utilssqlalchemy import serializable
from pypnnomenclature.models import TNomenclatures


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
    id_nomenclature_life_stage = DB.Column(
        DB.Integer
    )
     # Correspondance nomenclature INPN = sexe (9)
    id_nomenclature_sex = DB.Column(DB.Integer)
    # Correspondance nomenclature INPN = obj_denbr (6)
    id_nomenclature_obj_count = DB.Column(DB.Integer)
    # Correspondance nomenclature INPN = typ_denbr (21)
    id_nomenclature_type_count = DB.Column(DB.Integer)
    count_min = DB.Column(DB.Integer)
    count_max = DB.Column(DB.Integer)
    unique_id_sinp = DB.Column(UUID(as_uuid=True))
