
DROP VIEW IF EXISTS monitoring_chiro.v_chiro_gn_synthese ;
CREATE OR REPLACE VIEW monitoring_chiro.v_chiro_gn_synthese AS
WITH  source AS (
  SELECT id_source FROM gn_synthese.t_sources WHERE name_source = 'SUIVI_CHIRO'
), cor_nom_act_comp AS (
    SELECT ca.id_nomenclature as id_nomenclature_act, co.id_nomenclature as id_nomenclature_comp
    FROM ref_nomenclatures.t_nomenclatures ca
    JOIN  ref_nomenclatures.t_nomenclatures co
    ON  ca.id_type = ref_nomenclatures.get_id_nomenclature_type('CHI_ACTIVITE')
        AND
        co.id_type = ref_nomenclatures.get_id_nomenclature_type('OCC_COMPORTEMENT')
        AND ca.cd_nomenclature = co.cd_nomenclature
)
SELECT
  ccc.unique_id_sinp as unique_id_sinp,
  v.uuid_base_visit as unique_id_sinp_grp,
  (SELECT id_source FROM source) as id_source,
  ccc.id_counting_contact as entity_source_pk_value,
  s.uuid_base_site,
  v.id_dataset as id_dataset,
 v.id_module as id_module,
-- MISSING FIELD id_nomenclature_geo_object_nature,
v.id_nomenclature_grp_typ as id_nomenclature_grp_typ,
-- MISSING FIELD  id_nomenclature_obs_meth,
-- NOT IN SYNTHESE v.id_nomenclature_tech_collect_campanule as id_nomenclature_tech_collect_campanule,
vct.id_nomenclature_bio_condition as id_nomenclature_bio_condition,
-- MISSING FIELD id_nomenclature_bio_status,
-- MISSING FIELD id_nomenclature_naturalness,
-- MISSING FIELD id_nomenclature_exist_proof,
-- MISSING FIELD id_nomenclature_diffusion_level,
CASE
  WHEN NOT s.uuid_base_site IS NULL THEN sr.id_nomenclature_sensitivity
  ELSE NULL
END as id_nomenclature_sensitivity, -- cas des sites => données sensibiles quelque soit le critère
ccc.id_nomenclature_life_stage,
ccc.id_nomenclature_sex,
ccc.id_nomenclature_obj_count,
ccc.id_nomenclature_type_count,
vct.id_nomenclature_observation_status,
-- MISSING FIELD id_nomenclature_blurring,
-- MISSING FIELD id_nomenclature_source_status,
-- MISSING FIELD id_nomenclature_info_geo_type,
cnac.id_nomenclature_comp as id_nomenclature_behaviour,
ccc.count_min,
ccc.count_max,
vct.cd_nom as cd_nom,
COALESCE(tx_presume, vct.nom_complet, t.nom_complet) as nom_cite,
s.altitude_min,
s.altitude_max,
-- CAS particulier des inventaires
COALESCE(s.geom,vc.geom)  as the_geom_4326,
st_centroid(COALESCE(s.geom,vc.geom)) as the_geom_point,
st_transform(COALESCE(geom_local,vc.geom), 2154) as the_geom_local,
visit_date_min as date_min,
visit_date_max as date_max,
obs.observers as observers,
obs.ids_observers as ids_observers,
-- MISSING FIELD determiner,
vct.id_digitiser as id_digitiser,
-- MISSING FIELD id_nomenclature_determination_method,
v.comments as comment_context,
vct.commentaire as comment_description
FROM monitoring_chiro.cor_counting_contact ccc
JOIN monitoring_chiro.t_visite_contact_taxons vct
ON ccc.id_contact_taxon = vct.id_contact_taxon
JOIN taxonomie.taxref t
ON t.cd_nom = vct.cd_nom
JOIN gn_monitoring.t_base_visits v
ON vct.id_base_visit = v.id_base_visit
LEFT OUTER JOIN monitoring_chiro.t_visite_conditions vc
ON vc.id_base_visit = v.id_base_visit
LEFT OUTER JOIN gn_monitoring.t_base_sites s
ON s.id_base_site = v.id_base_site
LEFT OUTER  JOIN (
    SELECT id_base_visit,  array_agg(r.id_role) as ids_observers, string_agg(CONCAT(r.nom_role, ' ', r.prenom_role), ', ') as observers
    FROM gn_monitoring.cor_visit_observer vr
    JOIN utilisateurs.t_roles r
    ON vr.id_role = r.id_role
    GROUP BY id_base_visit
) obs
ON obs.id_base_visit = v.id_base_visit
LEFT OUTER JOIN cor_nom_act_comp cnac
ON cnac.id_nomenclature_act = vct.id_nomenclature_behaviour
LEFT OUTER JOIN gn_sensitivity.t_sensitivity_rules_cd_ref sr
ON sr.cd_ref = t.cd_ref;
