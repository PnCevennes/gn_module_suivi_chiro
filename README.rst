
Module `GeoNature <https://github.com/PnX-SI/GeoNature>`_ permettant de gérer les spécificités du backend du protocole Suivi des chiroptères. Il s'agit d'une API de gestion des données de suivi de "gites" pour les chiroptères.

Ce module est intégré à l'environnement à GeoNature mais dispose de son propre frontend autonome : https://github.com/PnCevennes/projet_suivis_frontend

Installation
============

Prerequis
---------

* Avoir GeoNature installé et fonctionnel
* Avoir installé l'application cliente (si besoin) : https://github.com/PnCevennes/projet_suivis_frontend/

Installation
------------

!! Adapter les chemins si besoin

::

   cd ~/Geonature
   source backend/venv/bin/activate
   geonature install_gn_module ~/gn_modules/gn_module_suivi_chiro/ suivi_chiro
   

Post installation
-----------------

Sur la base de données, lancer la commande suivante :

::
   

   UPDATE utilisateurs.t_applications a SET id_parent = p.id_application
   FROM  utilisateurs.t_applications p
   WHERE p.code_application='SUIVIS' AND a.code_application='SUIVI_CHIRO'


Ajouter ce module comme une application dans le fichier de configuration du frontend.


Trucs en "dur" dans les fichiers de configuration
-------------------------------------------------

* Id menu observateur = 10
* Id liste taxhub des chiroptères = 1000001

Au choix, il faut modifier les fichiers de configuration (.toml) ou adapter les données dans la base

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
