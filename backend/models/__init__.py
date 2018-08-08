from pypnnomenclature.repository import get_nomenclature_id_term

"""
    Récupération des valeurs des indentifiants des nomenclatures
"""
voc_util = {
    "STADE_VIE": {
        "indetermine": "1",
        "adulte": "2",
        "juvenile": "3"
    },
    "SEXE": {
        "indetermine": "1",
        "femelle": "2",
        "male": "3"
    }
}

COR_COUNTING_VALUE={}

for cd_type in voc_util:
    for k, cd_term in voc_util[cd_type].items():
        value = get_nomenclature_id_term(
            cd_type=cd_type, cd_term=cd_term
        )
        if cd_type not in COR_COUNTING_VALUE:
            COR_COUNTING_VALUE[cd_type] = {}

        COR_COUNTING_VALUE[cd_type][k] = value[0]
