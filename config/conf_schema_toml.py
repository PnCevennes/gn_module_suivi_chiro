'''
   Spécification du schéma toml des paramètres de configurations
   Fichier spécifiant les types des paramètres et leurs valeurs par défaut
   Fichier à ne pas modifier. Paramètres surcouchables dans config/config_gn_module.tml
'''

from marshmallow import Schema, fields


class GnModuleSchemaConf(Schema):
   id_dataset_suivis = fields.Integer()
   id_dataset_inventaires = fields.Integer()

