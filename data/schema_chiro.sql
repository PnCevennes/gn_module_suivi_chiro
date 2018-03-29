DROP SCHEMA IF EXISTS monitoring_chiro CASCADE;
CREATE SCHEMA monitoring_chiro;

CREATE TABLE monitoring_chiro.t_site_infos
(
  id_site_infos serial PRIMARY KEY,
  id_base_site integer  NOT NULL
      REFERENCES gn_monitoring.t_base_sites (id_base_site) MATCH SIMPLE
      ON UPDATE CASCADE ON DELETE CASCADE
     ,
  description text,
  menace_cmt text,
  contact_nom character varying(25),
  contact_prenom character varying(25),
  contact_adresse character varying(150),
  contact_code_postal character varying(5),
  contact_ville character varying(100),
  contact_telephone character varying(15),
  contact_portable character varying(15),
  contact_commentaire text,
  id_nomenclature_frequentation integer REFERENCES ref_nomenclatures.t_nomenclatures (id_nomenclature) MATCH SIMPLE
      ON UPDATE CASCADE ON DELETE NO ACTION,
  site_actif boolean,
  actions text
);

CREATE UNIQUE INDEX index_t_site_infos_id_base_site
  ON monitoring_chiro.t_site_infos
  USING btree
  (id_base_site);



CREATE TABLE monitoring_chiro.t_visite_conditions
(
  id_visite_cond serial PRIMARY KEY,
  id_base_visit integer NOT NULL
      REFERENCES gn_monitoring.t_base_visits (id_base_visit) MATCH SIMPLE
      ON UPDATE CASCADE ON DELETE CASCADE,
  geom public.geometry,
  temperature numeric(4,2),
  humidite numeric(4,2),
  id_nomenclature_mod_id integer REFERENCES ref_nomenclatures.t_nomenclatures (id_nomenclature) MATCH SIMPLE
      ON UPDATE CASCADE ON DELETE NO ACTION,
  CONSTRAINT enforce_dims_geom CHECK (st_ndims(geom) = 2),
  CONSTRAINT enforce_srid_geom CHECK (st_srid(geom) = 4326)
);


CREATE INDEX index_monitoring_chiro_t_visite_conditions_geom
  ON monitoring_chiro.t_visite_conditions
  USING gist
  (geom);


-- Trigger: trg_add_obs_geom on gn_monitoring.t_base_visits

-- DROP TRIGGER trg_add_obs_geom ON gn_monitoring.t_base_visits;

CREATE OR REPLACE FUNCTION gn_monitoring.fct_trg_add_obs_geom()
  RETURNS trigger AS
$BODY$
BEGIN
	IF (NEW.geom IS NULL) THEN
		NEW.geom = (
			SELECT geom
			FROM gn_monitoring.t_base_sites s
			JOIN gn_monitoring.t_base_visits v ON s.id_base_site = v.id_base_site
			WHERE id_base_visit = NEW.id_base_visit
		);
	END IF;
	return NEW;
END;
$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;


CREATE TRIGGER trg_add_obs_geom
  BEFORE INSERT OR UPDATE
  ON monitoring_chiro.t_visite_conditions
  FOR EACH ROW
  EXECUTE PROCEDURE gn_monitoring.fct_trg_add_obs_geom();


CREATE UNIQUE INDEX index_t_visite_conditions_id_base_visit
  ON monitoring_chiro.t_visite_conditions
  USING btree
  (id_base_visit);



CREATE TABLE monitoring_chiro.t_visite_contact_taxons
(
  id_contact_taxon serial PRIMARY KEY,
  id_base_visit integer NOT NULL 
      REFERENCES gn_monitoring.t_base_visits (id_base_visit) MATCH SIMPLE
      ON UPDATE CASCADE ON DELETE CASCADE,
      
  tx_presume character varying(250) DEFAULT NULL::character varying,
  cd_nom integer,
  nom_complet character varying(255),
  espece_incertaine boolean NOT NULL DEFAULT false,
  
  id_nomenclature_preuve_repro integer REFERENCES ref_nomenclatures.t_nomenclatures (id_nomenclature) MATCH SIMPLE
      ON UPDATE CASCADE ON DELETE NO ACTION,  -- prv_id
  id_nomenclature_activite integer REFERENCES ref_nomenclatures.t_nomenclatures (id_nomenclature) MATCH SIMPLE
      ON UPDATE CASCADE ON DELETE NO ACTION,   --  act_id
  indices_cmt character varying(1000), --description des indices
  
  commentaire character varying(1000),
  
  meta_create_date timestamp without time zone DEFAULT now(),
  meta_update_date timestamp without time zone,
  id_digitiser integer
      REFERENCES utilisateurs.t_roles (id_role) MATCH SIMPLE
      ON UPDATE CASCADE ON DELETE NO ACTION
);


CREATE INDEX index_t_visite_contact_taxons_id_base_visit
  ON monitoring_chiro.t_visite_contact_taxons
  USING btree
  (id_base_visit);


-- Trigger: trg_date_changes on monitoring_chiro.pr_visite_observationtaxon

-- DROP TRIGGER trg_date_changes ON monitoring_chiro.pr_visite_observationtaxon;

CREATE TRIGGER trg_date_changes
  BEFORE INSERT OR UPDATE
  ON monitoring_chiro.t_visite_contact_taxons
  FOR EACH ROW
  EXECUTE PROCEDURE public.fct_trg_meta_dates_change();


CREATE TABLE monitoring_chiro.cor_counting_contact
(
  id_counting_contact serial PRIMARY KEY,
  id_contact_taxon bigint NOT NULL
      REFERENCES monitoring_chiro.t_visite_contact_taxons (id_contact_taxon) MATCH SIMPLE
      ON UPDATE CASCADE ON DELETE CASCADE,
  
  id_nomenclature_life_stage integer NOT NULL, -- Correspondance nomenclature INPN = stade_vie (10)
  id_nomenclature_sex integer NOT NULL, -- Correspondance nomenclature INPN = sexe (9)
  id_nomenclature_obj_count integer NOT NULL, -- Correspondance nomenclature INPN = obj_denbr (6)
  id_nomenclature_type_count integer, -- Correspondance nomenclature INPN = typ_denbr (21)
  
  count_min integer,
  count_max integer,
  
  id_nomenclature_valid_status integer, -- Correspondance nomenclature INPN = statut_valid (101)
  id_validator integer,
  validation_comment text,
  meta_validation_date timestamp without time zone,
  
  meta_create_date timestamp without time zone,
  meta_update_date timestamp without time zone,
  
  unique_id_sinp uuid NOT NULL DEFAULT public.uuid_generate_v4(),
  
  CONSTRAINT fk_cor_counting_contact_life_stage FOREIGN KEY (id_nomenclature_life_stage)
      REFERENCES ref_nomenclatures.t_nomenclatures (id_nomenclature) MATCH SIMPLE
      ON UPDATE CASCADE ON DELETE NO ACTION,
  CONSTRAINT fk_cor_counting_contact_obj_count FOREIGN KEY (id_nomenclature_obj_count)
      REFERENCES ref_nomenclatures.t_nomenclatures (id_nomenclature) MATCH SIMPLE
      ON UPDATE CASCADE ON DELETE NO ACTION,
  CONSTRAINT fk_cor_counting_contact_sexe FOREIGN KEY (id_nomenclature_sex)
      REFERENCES ref_nomenclatures.t_nomenclatures (id_nomenclature) MATCH SIMPLE
      ON UPDATE CASCADE ON DELETE NO ACTION,
  CONSTRAINT fk_cor_counting_contact_t_roles FOREIGN KEY (id_validator)
      REFERENCES utilisateurs.t_roles (id_role) MATCH SIMPLE
      ON UPDATE CASCADE ON DELETE NO ACTION,
  CONSTRAINT fk_cor_counting_contact_typ_count FOREIGN KEY (id_nomenclature_type_count)
      REFERENCES ref_nomenclatures.t_nomenclatures (id_nomenclature) MATCH SIMPLE
      ON UPDATE CASCADE ON DELETE NO ACTION,
  CONSTRAINT fk_cor_counting_contact_valid_status FOREIGN KEY (id_nomenclature_valid_status)
      REFERENCES ref_nomenclatures.t_nomenclatures (id_nomenclature) MATCH SIMPLE
      ON UPDATE CASCADE ON DELETE NO ACTION,
  CONSTRAINT fk_cor_stage_number_id_taxon FOREIGN KEY (id_contact_taxon)
      REFERENCES monitoring_chiro.t_visite_contact_taxons (id_contact_taxon) MATCH SIMPLE
      ON UPDATE CASCADE ON DELETE CASCADE,
  CONSTRAINT check_cor_counting_contact_count_max CHECK (count_max >= count_min AND count_max > 0),
  CONSTRAINT check_cor_counting_contact_count_min CHECK (count_min > 0),
  CONSTRAINT check_cor_counting_contact_life_stage CHECK (ref_nomenclatures.check_nomenclature_type(id_nomenclature_life_stage, 10)),
  CONSTRAINT check_cor_counting_contact_obj_count CHECK (ref_nomenclatures.check_nomenclature_type(id_nomenclature_obj_count, 6)),
  CONSTRAINT check_cor_counting_contact_sexe CHECK (ref_nomenclatures.check_nomenclature_type(id_nomenclature_sex, 9)),
  CONSTRAINT check_cor_counting_contact_type_count CHECK (ref_nomenclatures.check_nomenclature_type(id_nomenclature_type_count, 21)),
  CONSTRAINT check_cor_counting_contact_valid_status CHECK (ref_nomenclatures.check_nomenclature_type(id_nomenclature_valid_status, 101))
);

COMMENT ON COLUMN monitoring_chiro.cor_counting_contact.id_nomenclature_life_stage IS 'Correspondance nomenclature INPN = stade_vie (10)';
COMMENT ON COLUMN monitoring_chiro.cor_counting_contact.id_nomenclature_sex IS 'Correspondance nomenclature INPN = sexe (9)';
COMMENT ON COLUMN monitoring_chiro.cor_counting_contact.id_nomenclature_obj_count IS 'Correspondance nomenclature INPN = obj_denbr (6)';
COMMENT ON COLUMN monitoring_chiro.cor_counting_contact.id_nomenclature_type_count IS 'Correspondance nomenclature INPN = typ_denbr (21)';
COMMENT ON COLUMN monitoring_chiro.cor_counting_contact.id_nomenclature_valid_status IS 'Correspondance nomenclature INPN = statut_valid (101)';


CREATE TRIGGER tri_meta_dates_change_cor_counting_contact
  BEFORE INSERT OR UPDATE
  ON monitoring_chiro.cor_counting_contact
  FOR EACH ROW
  EXECUTE PROCEDURE public.fct_trg_meta_dates_change();




CREATE TABLE monitoring_chiro.cor_site_infos_nomenclature_amenagements
(
  id_site_infos integer NOT NULL REFERENCES monitoring_chiro.t_site_infos (id_site_infos) MATCH SIMPLE
      ON UPDATE CASCADE ON DELETE CASCADE,
  id_nomenclature_amenagement integer NOT NULL REFERENCES ref_nomenclatures.t_nomenclatures (id_nomenclature) MATCH SIMPLE
      ON UPDATE CASCADE ON DELETE NO ACTION,
  CONSTRAINT pk_amenagement_f PRIMARY KEY (id_site_infos, id_nomenclature_amenagement)
);



CREATE TABLE monitoring_chiro.cor_site_infos_nomenclature_menaces
(
  id_site_infos integer NOT NULL  REFERENCES monitoring_chiro.t_site_infos (id_site_infos) MATCH SIMPLE
      ON UPDATE CASCADE ON DELETE CASCADE,
  id_nomenclature_menaces integer NOT NULL REFERENCES ref_nomenclatures.t_nomenclatures (id_nomenclature) MATCH SIMPLE
      ON UPDATE CASCADE ON DELETE NO ACTION,
  CONSTRAINT pk_menaces_f PRIMARY KEY (id_site_infos, id_nomenclature_menaces)
);




CREATE TABLE monitoring_chiro.cor_contact_taxons_nomenclature_indices
(
  id_contact_taxon integer NOT NULL REFERENCES monitoring_chiro.t_visite_contact_taxons (id_contact_taxon) MATCH SIMPLE
      ON UPDATE CASCADE ON DELETE CASCADE,
  id_nomenclature_indice integer NOT NULL REFERENCES ref_nomenclatures.t_nomenclatures (id_nomenclature) MATCH SIMPLE
      ON UPDATE CASCADE ON DELETE NO ACTION,
  CONSTRAINT pk_cor_contact_taxons_nomenclature_indices PRIMARY KEY (id_site_infos, id_nomenclature_indice)
);



-- DROP TABLE monitoring_chiro.subpr_observationtaxon_biometrie;

CREATE TABLE monitoring_chiro.t_contact_taxon_biometries
(
  id_biometrie serial PRIMARY KEY,
  id_contact_taxon bigint NOT NULL
      REFERENCES monitoring_chiro.t_visite_contact_taxons (id_contact_taxon) MATCH SIMPLE
      ON UPDATE CASCADE ON DELETE CASCADE,
  
  id_nomenclature_life_stage integer NOT NULL, -- Correspondance nomenclature INPN = stade_vie (10)
  id_nomenclature_sex integer NOT NULL, -- Correspondance nomenclature INPN = sexe (9)
  
  ab double precision,
  poids double precision,
  d3mf1 double precision,
  d3f2f3 double precision,
  d3total double precision,
  d5 double precision,
  cm3sup double precision,
  cm3inf double precision,
  cb double precision,
  lm double precision,
  oreille double precision,
  commentaire character varying(1000),
  
  
  meta_create_date timestamp without time zone DEFAULT now(),
  meta_update_date timestamp without time zone,
  id_digitiser integer
      REFERENCES utilisateurs.t_roles (id_role) MATCH SIMPLE
      ON UPDATE CASCADE ON DELETE NO ACTION,
      
  CONSTRAINT fk_cor_counting_contact_sexe FOREIGN KEY (id_nomenclature_sex)
      REFERENCES ref_nomenclatures.t_nomenclatures (id_nomenclature) MATCH SIMPLE
      ON UPDATE CASCADE ON DELETE NO ACTION,
  CONSTRAINT fk_cor_counting_contact_life_stage FOREIGN KEY (id_nomenclature_life_stage)
      REFERENCES ref_nomenclatures.t_nomenclatures (id_nomenclature) MATCH SIMPLE
      ON UPDATE CASCADE ON DELETE NO ACTION,
  CONSTRAINT check_cor_counting_contact_life_stage CHECK (ref_nomenclatures.check_nomenclature_type(id_nomenclature_life_stage, 10)),
  CONSTRAINT check_cor_counting_contact_sexe CHECK (ref_nomenclatures.check_nomenclature_type(id_nomenclature_sex, 9))
);

-- Index: monitoring_chiro.idx_291ed261ec9c5fd7

-- DROP INDEX monitoring_chiro.idx_291ed261ec9c5fd7;

CREATE INDEX index_t_contact_taxon_biometries_id_contact_taxon
  ON monitoring_chiro.t_contact_taxon_biometries
  USING btree
  (id_contact_taxon);


-- Trigger: trg_date_changes on monitoring_chiro.subpr_observationtaxon_biometrie

-- DROP TRIGGER trg_date_changes ON monitoring_chiro.subpr_observationtaxon_biometrie;

CREATE TRIGGER trg_date_changes
  BEFORE INSERT OR UPDATE
  ON monitoring_chiro.t_contact_taxon_biometries
  FOR EACH ROW
  EXECUTE PROCEDURE public.fct_trg_meta_dates_change();

