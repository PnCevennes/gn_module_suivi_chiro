'''
Fonctions facilitant la manipulation des relations lors des update
'''

def get_updated_relations(db, cls, data, reference, left, right):
    '''
    Charge les relations conservées
    Crée les nouvelles relations
    Supprime les relations non conservées
    params :
        db : session db
        cls : class Relation
        data : liste des ids droits
        reference : id gauche
        left : nom du champ gauche
        right : nom du champ droit
    '''
    objs = db.query(cls).filter(getattr(cls, left)==reference).all()
    for obj in objs:
        id_rel = getattr(obj, right)
        if id_rel in data:
            data.remove(id_rel)
            yield obj
        else:
            db.delete(obj)
    for id_rel in data:
        yield cls(**{right: id_rel})

