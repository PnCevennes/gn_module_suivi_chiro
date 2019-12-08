
-- ###########################
-- Insertion des applications
-- ###########################

INSERT INTO utilisateurs.t_applications(nom_application, desc_application, code_application)
SELECT 'suivi', 'Méta application concernant les protocoles de suivis', 'SUIVIS'
WHERE
    NOT EXISTS (
        SELECT id_application FROM utilisateurs.t_applications WHERE code_application = 'SUIVIS'
    );

INSERT INTO utilisateurs.t_applications(nom_application, desc_application, code_application, id_parent)
SELECT 'suivi_chiro', 'Application de suivis des chiroptères', 'SUIVI_CHIRO',
	(SELECT id_application FROM utilisateurs.t_applications WHERE code_application = 'SUIVIS')
WHERE
    NOT EXISTS (
        SELECT id_application FROM utilisateurs.t_applications WHERE code_application = 'SUIVI_CHIRO'
    );

