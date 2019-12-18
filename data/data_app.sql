
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


INSERT INTO gn_synthese.t_sources(name_source, desc_source, entity_source_pk_field)
VALUES ('SUIVI_CHIRO', 'Données issues du module de suivis des chiroptères', 'monitoring_chiro.cor_counting_contact.id_counting_contact');