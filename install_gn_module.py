import shutil
import os
# import subprocess
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
    scriptexecution(str(ROOT_DIR / 'data/data_chiro.sql'), gn_db)
    scriptexecution(str(ROOT_DIR / 'data/views.sql'), gn_db)


def gnmodule_install_app(gn_db, gn_app):
    '''
        Fonction principale permettant de réaliser les opérations
        d'installation du module :
            - Base de données
            - Module (pour le moment rien)
    '''
    with gn_app.app_context():
        # Création des liens symboliques pour la configuration
        try :
            config_path = Path(gn_app.config['BASE_DIR']) / 'static/configs'
            try:
                shutil.copytree(
                    str(ROOT_DIR / 'configs.sample'),
                    str(ROOT_DIR / 'configs')
                )
            except OSError as e:
                print(e)
            if config_path.is_dir():
                os.symlink(
                    str(ROOT_DIR / 'configs'),
                    str(config_path / 'suivi_chiro')
                )
            else:
                raise Exception('''
                    unable to create config file symlink : config_path doesn't exists
                ''')
        except Exception as e:
            print(e)
        # Installation du module de la base
        gnmodule_install_db(gn_db, gn_app)
