Sous module de Geonature2 correspondant à une API de gestion des données de suivis de "gites" pourles chiroptères


Installation
============

Prerequis
---------

* avoir Geonature installé et fonctionnel
* avoir installé l'application cliente (si besoin) : https://github.com/PnCevennes/projet_suivis_frontend/

Installation
------------

!! adapter les chemins si besoins

::

   cd ~/Geonature
   source backend/venv/bin/activate
   geonature install_gn_module ~/gn_modules/gn_module_suivi_chiro/ suivi_chiro
   

Post installation
-----------------
Sur la base de données lancer la commande suivante

::
   
   UPDATE utilisateurs.t_applications a SET id_parent = p.id_application
   FROM  utilisateurs.t_applications p
   WHERE p.nom_application='suivi' AND a.nom_application='suivi_chiro'



Ajouter ce module comme une application dans le fichier de configuration du frontend


