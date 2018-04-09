-- AVANT chiro.vue_chiro_site;

--DROP  VIEW monitoring_chiro.v_sites_chiro;
CREATE OR REPLACE VIEW monitoring_chiro.v_sites_chiro AS 
 SELECT s.id_base_site AS id,
    s.id_base_site,
    s.base_site_name,
    s.base_site_code,
    s.first_use_date,
    s.id_inventor,
    (((obr.nom_role::text || ' '::text) || obr.prenom_role::text))::character varying(255) AS nom_observateur,
    s.meta_create_date,
    s.meta_update_date,
    NULL::character varying AS ref_commune,
    s.geom,
    s.id_nomenclature_type_site,
    l.label_default AS type_lieu,
    c.id_nomenclature_frequentation,
    c.menace_cmt,
    c.contact_nom,
    c.contact_prenom,
    c.contact_adresse,
    c.contact_code_postal,
    c.contact_ville,
    c.contact_telephone,
    c.contact_portable,
    c.contact_commentaire,
    c.site_actif,
    c.actions,
    ( SELECT max(v.visit_date) AS max
           FROM gn_monitoring.t_base_visits v
          WHERE v.id_base_site = s.id_base_site) AS dern_obs,
    ( SELECT count(*) AS count
           FROM gn_monitoring.t_base_visits v
          WHERE v.id_base_site = s.id_base_site) AS nb_obs,
    '<h4><a href="#!/suivi_chiro/site/' || s.id_base_site || '">' || s.base_site_name || '</a></h4>'::varchar(500) as geom_popup
   FROM gn_monitoring.t_base_sites s
     JOIN gn_monitoring.cor_site_application csa ON s.id_base_site = csa.id_base_site AND csa.id_application = 101
     LEFT JOIN monitoring_chiro.t_site_infos c ON c.id_base_site = s.id_base_site
     LEFT JOIN utilisateurs.t_roles obr ON obr.id_role = s.id_inventor
     LEFT JOIN ref_nomenclatures.t_nomenclatures l ON l.id_nomenclature = s.id_nomenclature_type_site
  ORDER BY s.id_base_site DESC;


-- AVANT  chiro.vue_chiro_obs_ss_site;
CREATE OR REPLACE VIEW monitoring_chiro.v_inventaires_chiro AS 
SELECT obs.id_base_visit as id,
    obs.id_base_visit,
	cco.geom, 
	obs.visit_date,
	obs.comments,
	obs.meta_create_date,
	obs.meta_update_date,
	NULL::text as ref_commune, --TODO
  (upper(num.nom_role::text) || ' '::text) || num.prenom_role::text AS numerisateur,
	cco.temperature,
	cco.humidite,
	cco.id_nomenclature_mod_id,
	( SELECT count(*) AS count
           FROM monitoring_chiro.t_visite_contact_taxons a
          WHERE a.id_base_visit = obs.id_base_visit) AS nb_taxons,
  ( SELECT sum(c.count_min) AS count
      FROM monitoring_chiro.t_visite_contact_taxons a
      JOIN monitoring_chiro.cor_counting_contact c
      ON a.id_contact_taxon = c.id_contact_taxon
    WHERE a.id_base_visit = obs.id_base_visit
  ) AS abondance
FROM gn_monitoring.t_base_visits obs
JOIN monitoring_chiro.t_visite_conditions cco ON cco.id_base_visit = obs.id_base_visit
LEFT JOIN utilisateurs.t_roles num ON num.id_role = obs.id_digitiser
WHERE obs.id_base_site IS NULL
ORDER BY obs.visit_date DESC;


--- chiro.vue_chiro_obs
CREATE OR REPLACE VIEW monitoring_chiro.v_visites_chiro AS 
 SELECT obs.id_base_visit as id,
    obs.id_base_visit,
	s.base_site_name,
	obs.visit_date,
	obs.comments,
	obs.meta_create_date,
	obs.meta_update_date,
	obs.id_digitiser,
        (upper(num.nom_role::text) || ' '::text) || num.prenom_role::text AS numerisateur,
	NULL::text as ref_commune, --TODO
	cco.temperature,
	cco.humidite,
	cco.id_nomenclature_mod_id,
	( SELECT count(*) AS count
           FROM monitoring_chiro.t_visite_contact_taxons a
          WHERE a.id_base_visit = obs.id_base_visit) AS nb_taxons,
        ( SELECT sum(c.count_min) AS count
           FROM monitoring_chiro.t_visite_contact_taxons a
           JOIN monitoring_chiro.cor_counting_contact c
           ON a.id_contact_taxon = c.id_contact_taxon
          WHERE a.id_base_visit = obs.id_base_visit
        ) AS abondance
FROM gn_monitoring.t_base_visits obs
JOIN monitoring_chiro.t_visite_conditions cco ON cco.id_base_visit = obs.id_base_visit
JOIn gn_monitoring.t_base_sites s ON s.id_base_site = obs.id_base_site
LEFT JOIN utilisateurs.t_roles num ON num.id_role = obs.id_digitiser
ORDER BY obs.visit_date DESC;

