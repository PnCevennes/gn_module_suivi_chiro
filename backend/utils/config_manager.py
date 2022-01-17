"""
    Fonctions permettant de lire un fichier yml de configuration
    et de le parser
    Initialement situé dans le coeur de GeoNature mais considéré comme trop spécifique
        la route et les méthodes afférentes ont été déplacées dans le module chiro
        qui est le seul à ma connaissance à utiliser ce mécanisme
"""

from sqlalchemy.orm.exc import NoResultFound

from flask import current_app
from pypnnomenclature.repository import (
    get_nomenclature_list_formated,
    get_nomenclature_id_term,
)

from geonature.utils.env import DB
from geonature.utils.utilstoml import load_toml
from geonature.utils.errors import GeonatureApiError

from geonature.core.gn_commons.repositories import get_table_location_id
from geonature.core.users.models import TApplications


def generate_config(file_path):
    """
        Lecture et modification des fichiers de configuration yml
        Pour l'instant utile pour la compatiblité avec l'application
            projet_suivi
            ou le frontend génère les formulaires à partir de ces données
    """
    # Chargement du fichier de configuration
    config = load_toml(file_path)
    config_data = find_field_config(config)
    return config_data

def find_field_config(config_data):
    """
        Parcours des champs du fichier de config
        de façon à trouver toutes les occurences du champ field
        qui nécessite un traitement particulier
    """
    # Calcul de l'url de base pour la construction des routes de configuration
    # PATCH lié à la suppression de la route config du coeur de GeoNature et à son déplacement dans le module chiro
    if current_app.config["SUIVI_CHIRO"]["MODULE_URL"][0:1] == "/" :
        module_url = current_app.config["SUIVI_CHIRO"]["MODULE_URL"][1:] + "/"
    else :
        module_url = current_app.config["SUIVI_CHIRO"]["MODULE_URL"] + "/"

    if isinstance(config_data, dict):
        for ckey in config_data:
            if ckey in ["subSchemaUrl", "subEditSchemaUrl", "formUrl", "config_url"]:
                # PATCH lié à la suppression de la route config du coeur de GeoNature et à son déplacement dans le module chiro
                config_data[ckey] = module_url + config_data[ckey]

            if ckey == "fields":
                config_data[ckey] = parse_field(config_data[ckey])

            elif ckey == "appId":
                # Cas particulier qui permet de passer
                #       du nom d'une application à son identifiant
                # TODO se baser sur un code_application
                #       qui serait unique et non modifiable
                config_data[ckey] = get_app_id(config_data[ckey])

            elif isinstance(config_data[ckey], list):
                for idx, val in enumerate(config_data[ckey]):
                    config_data[ckey][idx] = find_field_config(val)
    return config_data


def parse_field(fieldlist):
    """
       Traitement particulier pour les champs de type field :
       Chargement des listes de valeurs de nomenclature
    """
    for field in fieldlist:
        if "options" not in field:
            field["options"] = {}
        if "thesaurus_code_type" in field:
            field["options"]["choices"] = format_nomenclature_list(
                {
                    "code_type": field["thesaurus_code_type"],
                    "regne": field.get("regne"),
                    "group2_inpn": field.get("group2_inpn"),
                }
            )
            if "default" in field:
                field["options"]["default"] = get_nomenclature_id_term(
                    str(field["thesaurus_code_type"]), str(field["default"]), False
                )

        if "thesaurusHierarchyID" in field:
            field["options"]["choices"] = format_nomenclature_list(
                {
                    "code_type": field["thesaurus_code_type"],
                    "hierarchy": field["thesaurusHierarchyID"],
                }
            )
        if "attached_table_location" in field["options"]:
            (schema_name, table_name) = field["options"]["attached_table_location"].split(
                "."
            )  # noqa
            field["options"]["id_table_location"] = get_table_location_id(schema_name, table_name)

        if "fields" in field:
            field["fields"] = parse_field(field["fields"])

    return fieldlist


def get_app_id(module_code):
    """
        Retourne l'identifiant d'un module
        à partir de son code
    """
    try:
        mod_id = (
            DB.session.query(TApplications.id_application)
            .filter_by(code_application=str(module_code))
            .one()
        )
        return mod_id

    except NoResultFound:
        raise GeonatureApiError(message="module {} not found".format(module_code))


def format_nomenclature_list(params):
    """
        Mise en forme des listes de valeurs de façon à assurer une
        compatibilité avec l'application de suivis
    """
    mapping = {
        "id": {"object": "nomenclature", "field": "id_nomenclature"},
        "libelle": {"object": "nomenclature", "field": "label_default"},
    }
    nomenclature = get_nomenclature_list_formated(params, mapping)
    return nomenclature
