from flask import request
from ..blueprint import routes


@routes.route('/visites', methods=['GET'])
def get_visites_chiro():
    pass


@routes.route('/visite/<id_visite>', methods=['GET'])
def get_one_visite_chiro(id_visite):
    pass


@routes.route('/visite', methods=['POST', 'PUT'])
def create_visite_chiro():
    pass


@routes.route('/visite/<id_visite>', methods=['POST', 'PUT'])
def update_visite_chiro(id_visite):
    pass


@routes.route('/visite/<id_visite>', methods=['DELETE'])
def delete_visite_chiro(id_visite):
    pass

