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
    ( SELECT max(v.visit_date_min) AS max
           FROM gn_monitoring.t_base_visits v
          WHERE v.id_base_site = s.id_base_site) AS dern_obs,
    ( SELECT count(*) AS count
           FROM gn_monitoring.t_base_visits v
          WHERE v.id_base_site = s.id_base_site) AS nb_obs,
    ((('<h4><a href="#/suivi_chiro/site/'::text || s.id_base_site) || '">'::text) || s.base_site_name::text) || '</a></h4>'::character varying(500)::text AS geom_popup
   FROM gn_monitoring.t_base_sites s
     JOIN gn_monitoring.cor_site_module csa ON s.id_base_site = csa.id_base_site AND csa.id_module = (( SELECT m.id_module
           FROM gn_commons.t_modules m
          WHERE m.module_code = 'SUIVI_CHIRO'::text))
     LEFT JOIN monitoring_chiro.t_site_infos c ON c.id_base_site = s.id_base_site
     LEFT JOIN utilisateurs.t_roles obr ON obr.id_role = s.id_inventor
     LEFT JOIN ref_nomenclatures.t_nomenclatures l ON l.id_nomenclature = s.id_nomenclature_type_site
  ORDER BY s.id_base_site DESC;


CREATE OR REPLACE VIEW monitoring_chiro.v_inventaires_chiro AS
 SELECT obs.id_base_visit AS id,
    obs.id_base_visit,
    cco.geom,
    obs.visit_date_min,
    obs.comments,
    obs.meta_create_date,
    obs.meta_update_date,
    NULL::text AS ref_commune, --TODO
    (upper(num.nom_role::text) || ' '::text) || num.prenom_role::text AS numerisateur,
    cco.temperature,
    cco.humidite,
    cco.id_nomenclature_mod_id,
    obr.observers,
    ( SELECT count(*) AS count
           FROM monitoring_chiro.t_visite_contact_taxons a
          WHERE a.id_base_visit = obs.id_base_visit) AS nb_taxons,
    ( SELECT sum(c.count_min) AS count
           FROM monitoring_chiro.t_visite_contact_taxons a
             JOIN monitoring_chiro.cor_counting_contact c ON a.id_contact_taxon = c.id_contact_taxon
          WHERE a.id_base_visit = obs.id_base_visit) AS abondance,
   '<h4><a href="#/suivi_chiro/inventaire/' || obs.id_base_visit || '">' || obs.visit_date_min::text ||  '</a></h4>'  AS geom_popup
   FROM gn_monitoring.t_base_visits obs
     JOIN monitoring_chiro.t_visite_conditions cco ON cco.id_base_visit = obs.id_base_visit
     LEFT JOIN utilisateurs.t_roles num ON num.id_role = obs.id_digitiser
     LEFT JOIN LATERAL (
        SELECT array_agg(CONCAT(nom_role, ' ', prenom_role)) as observers
        FROM  gn_monitoring.cor_visit_observer crole
        JOIN utilisateurs.t_roles r ON crole.id_role = r.id_role
        WHERE crole.id_base_visit = obs.id_base_visit
     ) obr ON true
  WHERE obs.id_base_site IS NULL
  ORDER BY obs.visit_date_min DESC;


--- chiro.vue_chiro_obs
CREATE OR REPLACE VIEW monitoring_chiro.v_visites_chiro AS
 SELECT obs.id_base_visit AS id,
    obs.id_base_visit,
    s.id_base_site,
    s.base_site_name,
    s.geom,
    obs.visit_date_min,
    obs.comments,
    NULL as meta_create_date,
    NULL as meta_update_date,
    obs.id_digitiser,
    (upper(num.nom_role::text) || ' '::text) || num.prenom_role::text AS numerisateur,
    NULL::text AS ref_commune,
    cco.temperature,
    cco.humidite,
    cco.id_nomenclature_mod_id,
    observers,
    ( SELECT count(*) AS count
           FROM monitoring_chiro.t_visite_contact_taxons a
          WHERE a.id_base_visit = obs.id_base_visit) AS nb_taxons,
    ( SELECT sum(c.count_min) AS count
           FROM monitoring_chiro.t_visite_contact_taxons a
             JOIN monitoring_chiro.cor_counting_contact c ON a.id_contact_taxon = c.id_contact_taxon
          WHERE a.id_base_visit = obs.id_base_visit) AS abondance
   FROM gn_monitoring.t_base_visits obs
     JOIN monitoring_chiro.t_visite_conditions cco ON cco.id_base_visit = obs.id_base_visit
     JOIN gn_monitoring.t_base_sites s ON s.id_base_site = obs.id_base_site
     LEFT JOIN utilisateurs.t_roles num ON num.id_role = obs.id_digitiser
     LEFT JOIN LATERAL (
        SELECT array_agg(CONCAT(nom_role, ' ', prenom_role)) as observers
        FROM  gn_monitoring.cor_visit_observer crole
        JOIN utilisateurs.t_roles r ON crole.id_role = r.id_role
        WHERE crole.id_base_visit = obs.id_base_visit
     ) obr ON true
  ORDER BY obs.visit_date_min DESC;

CREATE OR REPLACE VIEW monitoring_chiro.v_obs_taxons AS
SELECT
ct.id_contact_taxon as id,
ct.id_contact_taxon,
ct.id_base_visit,
ct.tx_presume,
ct.cd_nom,
ct.nom_complet,
ccc.nb_total_min,
ccc.nb_total_max
       /*espece_incertaine, id_nomenclature_preuve_repro, id_nomenclature_activite,
       indices_cmt, commentaire, meta_create_date, meta_update_date,
       id_digitiser, db_suivi_id, app*/
FROM monitoring_chiro.t_visite_contact_taxons ct
left outer JOIN (SELECT id_contact_taxon, sum(count_min)  as nb_total_min, sum(count_max) as nb_total_max FROM monitoring_chiro.cor_counting_contact group by id_contact_taxon) ccc
ON ct.id_contact_taxon = ccc.id_contact_taxon;


CREATE OR REPLACE VIEW monitoring_chiro.v_biometrie AS
SELECT id_biometrie as id, id_biometrie, id_contact_taxon, id_nomenclature_life_stage, id_nomenclature_sex,
       ab, poids, d3mf1, d3f2f3, d3total, d5, cm3sup, cm3inf, cb, lm,
       oreille, commentaire, id_digitiser, uuid_chiro_biometrie
  FROM monitoring_chiro.t_contact_taxon_biometries;
