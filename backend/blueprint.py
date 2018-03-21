from flask import Blueprint


blueprint = Blueprint('gn_module_validation', __name__)

@blueprint.route('/')
def gn_module_validation_test():
    return 'Ca marche yep yep'