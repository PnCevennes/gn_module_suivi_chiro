'''
point d'entrée du module chiro
'''

from flask import Blueprint


blueprint = Blueprint('gn_module_suivi_chiro', __name__)


@blueprint.route('/')
def gn_module_suivi_chiro_index():
    return 'Ca marche yep yep'


ID_APP = 101 # TODO récupérer l'identifiant d'application par le front


from .routes import (
        site,
        visite,
        contact_taxon,
        biometrie
        )
