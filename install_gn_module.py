import subprocess
from pathlib import Path

ROOT_DIR = Path(__file__).absolute().parent


def scriptexecution(filename, gn_db):
    with open(filename, 'r') as s:
        sql_script = s.read()
        gn_db.session.execute(sql_script)
    s.closed
    gn_db.session.commit()
 

def gnmodule_install_db(gn_db, gn_app):
    scriptexecution(str(ROOT_DIR / 'data/schema_chiro.sql'), gn_db)
        


def gnmodule_install_app(gn_db, gn_app):
    '''
        Fonction principale permettant de réaliser les opérations d'installation du module : 
            - Base de données
            - Module (pour le moment rien)
    '''
    with gn_app.app_context() :
        gnmodule_install_db(gn_db, gn_app)
