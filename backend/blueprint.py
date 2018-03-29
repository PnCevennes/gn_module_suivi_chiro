from flask import Blueprint


blueprint = Blueprint('gn_module_suivi_chiro', __name__)

@blueprint.route('/')
def gn_module_suivi_chiro_index():
    return 'Ca marche yep yep'

from .routes import (
        site,
        visite,
        observation_taxon,
        biometrie
        )
