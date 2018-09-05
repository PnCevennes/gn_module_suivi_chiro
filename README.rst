Présentation
============

Module `GeoNature <https://github.com/PnX-SI/GeoNature>`_ permettant de gérer les spécificités du backend du protocole Suivi des chiroptères. 

Ce module est intégré à l'environnement à GeoNature mais dispose de son propre frontend autonome : https://github.com/PnCevennes/projet_suivis_frontend

Fichiers relatifs à l'installation
==================================

* ``manifest.tml`` (obligatoire) : Fichier contenant la description du module (nom, version de GN supportée, ...)
* ``install_env.sh`` : Installation des paquets Debian
* ``install_gn_module.py`` : Installation du module :

  * commandes SQL
  * extra commandes python
  * ce fichier doit contenir la méthode suivante : ``gnmodule_install_app(gn_db, gn_app)``
* ``requirements.txt`` : Liste des paquets Python
* ``conf_schema_toml.py`` : Schéma Marshmallow de spécification des paramètres du module
* ``conf_gn_module.toml.sample`` : Fichier de configuration du module


Fichiers relatifs au bon fonctionnement du module
=================================================

Backend
-------
Si votre module comporte des routes il doit comporter le fichier suivant : ``backend/blueprint.py``
avec une variable blueprint qui contient toutes les routes.

::

    blueprint = Blueprint('gn_module_validation', __name__)


Frontend
--------

Le dossier ``frontend`` comprend les élements suivant:

* Le dossier ``app`` : comprend le code typescript du module

    Il doit inclure le "module Angular racine", celui-ci doit impérativement s'appeler ``gnModule.module.ts`` 
* Le dossier ``assets`` avec l'ensemble des médias (images, son).
* Un fichier ``package.json`` qui décrit l'ensemble des librairies JS nécessaires au module.

Auteurs
-------

Parc national des Cévennes

* Frédéric FIDON
* Amandine SAHL


Licence
-------

* OpenSource - GPL V3
* Copyleft 2018 - Parc national des Cévennes

.. image:: http://geonature.fr/img/logo-pnc.jpg
    :target: http://www.cevennes-parcnational.fr

