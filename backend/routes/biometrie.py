from flask import request
from ..blueprint import routes


@routes.route('/biometries', methods=['GET'])
def get_biometries_chiro():
    pass


@routes.route('/biometrie/<id_biometrie>', methods=['GET'])
def get_one_biometrie_chiro(id_biometrie):
    pass


@routes.route('/biometrie', methods=['POST', 'PUT'])
def create_biometrie_chiro():
    pass


@routes.route('/biometrie/<id_biometrie>', methods=['POST', 'PUT'])
def update_biometrie_chiro(id_biometrie):
    pass


@routes.route('/biometrie/<id_biometrie>', methods=['DELETE'])
def delete_biometrie_chiro(id_biometrie):
    pass

