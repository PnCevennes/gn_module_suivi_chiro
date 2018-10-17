import shutil
import os
import subprocess

from pathlib import Path

ROOT_DIR = Path(__file__).absolute().parent


def gnmodule_install_app(gn_db, gn_app):
    '''
        Fonction principale permettant de réaliser les opérations
        d'installation du module :
            - Base de données
            - Module (pour le moment rien)
    '''
    with gn_app.app_context():

        subprocess.call(
            [
                ROOT_DIR / 'install_db.sh', 
                str(Path(gn_app.config['BASE_DIR']).parent)
            ], 
            cwd=gn_app.config['BASE_DIR']
        )

        # Création des liens symboliques pour la configuration
        try :
            config_path = Path(gn_app.config['BASE_DIR']) / 'static/configs'
            try:
                shutil.copytree(
                    str(ROOT_DIR / 'configs.sample'),
                    str(ROOT_DIR / 'configs')
                )
            except OSError as e:
                print('Erreur de copie')
                print(e)
                pass
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

        
        # Ajout de l'application en tant que module du frontend
        suivi_app_file_dir = Path(
            gn_app.config.get('BASE_DIR') + gn_app.static_url_path, 
            'configs/suivis', 
            'apps.toml'
        )

        with open(str(ROOT_DIR / 'configs/apps.toml')) as config_chiro:
            with open(suivi_app_file_dir, "a") as suivi_app_file:
                suivi_app_file.write("\n\n")
                suivi_app_file.writelines(config_chiro)
            suivi_app_file.close()
        config_chiro.close()
