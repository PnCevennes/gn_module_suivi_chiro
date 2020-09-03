DROP SCHEMA  IF EXISTS monitoring_chiro CASCADE;
CREATE SCHEMA monitoring_chiro;

CREATE TABLE monitoring_chiro.cor_contact_taxons_nomenclature_indices (
    id_contact_taxon integer NOT NULL,
    id_nomenclature_indice integer NOT NULL ,
    uuid_chiro_visite_contact_indices uuid DEFAULT public.uuid_generate_v4()
);


CREATE TABLE monitoring_chiro.cor_counting_contact (
    id_counting_contact integer NOT NULL,
    id_contact_taxon bigint NOT NULL,
    id_nomenclature_life_stage integer NOT NULL,
    id_nomenclature_sex integer NOT NULL,
    id_nomenclature_obj_count integer NOT NULL,
    id_nomenclature_type_count integer,
    count_min integer,
    count_max integer,
    validation_comment text,
    unique_id_sinp uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    CONSTRAINT check_cor_counting_contact_count_max CHECK (((count_max >= count_min) AND (count_max > 0))),
    CONSTRAINT check_cor_counting_contact_count_min CHECK ((count_min > 0))
);

COMMENT ON COLUMN monitoring_chiro.cor_counting_contact.id_nomenclature_life_stage IS 'Correspondance nomenclature INPN = stade_vie (10)';

COMMENT ON COLUMN monitoring_chiro.cor_counting_contact.id_nomenclature_sex IS 'Correspondance nomenclature INPN = sexe (9)';

COMMENT ON COLUMN monitoring_chiro.cor_counting_contact.id_nomenclature_obj_count IS 'Correspondance nomenclature INPN = obj_denbr (6)';

COMMENT ON COLUMN monitoring_chiro.cor_counting_contact.id_nomenclature_type_count IS 'Correspondance nomenclature INPN = typ_denbr (21)';


CREATE SEQUENCE monitoring_chiro.cor_counting_contact_id_counting_contact_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE monitoring_chiro.cor_counting_contact_id_counting_contact_seq OWNED BY monitoring_chiro.cor_counting_contact.id_counting_contact;



CREATE TABLE monitoring_chiro.cor_site_infos_nomenclature_amenagements (
    id_base_site integer NOT NULL,
    id_nomenclature_amenagement integer NOT NULL,
    uuid_chiro_site_amenagements uuid DEFAULT public.uuid_generate_v4()
);

CREATE TABLE monitoring_chiro.cor_site_infos_nomenclature_menaces (
    id_base_site integer NOT NULL,
    id_nomenclature_menaces integer NOT NULL,
    uuid_chiro_site_menaces uuid DEFAULT public.uuid_generate_v4()
);

CREATE TABLE monitoring_chiro.t_contact_taxon_biometries (
    id_biometrie integer NOT NULL,
    id_contact_taxon bigint NOT NULL,
    id_nomenclature_life_stage integer NOT NULL,
    id_nomenclature_sex integer NOT NULL,
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
    id_digitiser integer,
    uuid_chiro_biometrie uuid DEFAULT public.uuid_generate_v4()
);


CREATE SEQUENCE monitoring_chiro.t_contact_taxon_biometries_id_biometrie_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE monitoring_chiro.t_contact_taxon_biometries_id_biometrie_seq OWNED BY monitoring_chiro.t_contact_taxon_biometries.id_biometrie;


CREATE TABLE monitoring_chiro.t_site_infos (
    id_base_site integer NOT NULL,
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
    id_nomenclature_frequentation integer,
    site_actif boolean,
    actions text,
    db_suivi_id integer,
    app character varying,
    uuid_chiro_site_infos uuid DEFAULT public.uuid_generate_v4()
);


CREATE TABLE monitoring_chiro.t_visite_conditions (
    id_base_visit integer NOT NULL,
    geom public.geometry,
    temperature numeric(4,2),
    humidite numeric(4,2),
    id_nomenclature_mod_id integer,
    uuid_chiro_visite_conditions uuid DEFAULT public.uuid_generate_v4(),
    CONSTRAINT enforce_dims_geom CHECK ((public.st_ndims(geom) = 2)),
    CONSTRAINT enforce_srid_geom CHECK ((public.st_srid(geom) = 4326))
);


CREATE TABLE monitoring_chiro.t_visite_contact_taxons (
    id_contact_taxon integer NOT NULL,
    id_base_visit integer NOT NULL,
    tx_presume character varying(250) DEFAULT NULL::character varying,
    cd_nom integer,
    nom_complet character varying(255),
    espece_incertaine boolean DEFAULT false NOT NULL,
    id_nomenclature_preuve_repro integer,
    id_nomenclature_behaviour integer,
    id_nomenclature_bio_condition integer,
    id_nomenclature_observation_status integer,
    indices_cmt character varying(1000),
    commentaire character varying(1000),
    id_digitiser integer,
    uuid_chiro_visite_contact_taxon uuid DEFAULT public.uuid_generate_v4()
);


CREATE TABLE monitoring_chiro.cor_visite_area (
  id_base_visit integer NOT NULL,
  id_area integer NOT NULL
);

CREATE SEQUENCE monitoring_chiro.t_visite_contact_taxons_id_contact_taxon_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER TABLE ONLY monitoring_chiro.cor_counting_contact ALTER COLUMN id_counting_contact SET DEFAULT nextval('monitoring_chiro.cor_counting_contact_id_counting_contact_seq'::regclass);

ALTER TABLE ONLY monitoring_chiro.t_contact_taxon_biometries ALTER COLUMN id_biometrie SET DEFAULT nextval('monitoring_chiro.t_contact_taxon_biometries_id_biometrie_seq'::regclass);

ALTER TABLE ONLY monitoring_chiro.t_visite_contact_taxons ALTER COLUMN id_contact_taxon SET DEFAULT nextval('monitoring_chiro.t_visite_contact_taxons_id_contact_taxon_seq'::regclass);

-- ################### --
-- CONSTRAINTS --
ALTER TABLE monitoring_chiro.cor_counting_contact
    ADD CONSTRAINT check_cor_counting_contact_life_stage CHECK (ref_nomenclatures.check_nomenclature_type_by_mnemonique(id_nomenclature_life_stage, 'STADE_VIE')) NOT VALID;

ALTER TABLE monitoring_chiro.t_contact_taxon_biometries
    ADD CONSTRAINT check_cor_counting_contact_life_stage CHECK (ref_nomenclatures.check_nomenclature_type_by_mnemonique(id_nomenclature_life_stage, 'STADE_VIE')) NOT VALID;

ALTER TABLE monitoring_chiro.t_visite_contact_taxons
    ADD CONSTRAINT check_t_visite_contact_taxons_bio_condition CHECK (ref_nomenclatures.check_nomenclature_type_by_mnemonique(id_nomenclature_bio_condition, 'ETA_BIO')) NOT VALID;

ALTER TABLE monitoring_chiro.t_visite_contact_taxons
    ADD CONSTRAINT check_t_visite_contact_taxons_preuve_repro CHECK (ref_nomenclatures.check_nomenclature_type_by_mnemonique(id_nomenclature_preuve_repro, 'CHI_REPRO')) NOT VALID;

ALTER TABLE monitoring_chiro.t_visite_contact_taxons
    ADD CONSTRAINT check_t_visite_contact_taxons_behaviour CHECK (ref_nomenclatures.check_nomenclature_type_by_mnemonique(id_nomenclature_behaviour, 'CHI_ACTIVITE')) NOT VALID;

ALTER TABLE monitoring_chiro.t_visite_contact_taxons
    ADD CONSTRAINT check_t_visite_contact_taxons_obs_status CHECK (ref_nomenclatures.check_nomenclature_type_by_mnemonique(id_nomenclature_observation_status, 'STATUT_OBS')) NOT VALID;

ALTER TABLE monitoring_chiro.cor_counting_contact
    ADD CONSTRAINT check_cor_counting_contact_obj_count CHECK (ref_nomenclatures.check_nomenclature_type_by_mnemonique(id_nomenclature_obj_count, 'OBJ_DENBR')) NOT VALID;

ALTER TABLE monitoring_chiro.cor_counting_contact
    ADD CONSTRAINT check_cor_counting_contact_sexe CHECK (ref_nomenclatures.check_nomenclature_type_by_mnemonique(id_nomenclature_sex, 'SEXE')) NOT VALID;

ALTER TABLE monitoring_chiro.cor_counting_contact
    ADD CONSTRAINT check_cor_counting_contact_type_count CHECK (ref_nomenclatures.check_nomenclature_type_by_mnemonique(id_nomenclature_type_count, 'TYP_DENBR')) NOT VALID;


ALTER TABLE monitoring_chiro.t_contact_taxon_biometries
    ADD CONSTRAINT check_cor_counting_contact_sexe CHECK (ref_nomenclatures.check_nomenclature_type_by_mnemonique(id_nomenclature_sex, 'SEXE')) NOT VALID;



-- @TODO Finalize check constraints

-- ################### --
--- PRIMARY KEY --
ALTER TABLE ONLY monitoring_chiro.t_visite_conditions
    ADD CONSTRAINT t_visite_conditions_pkey PRIMARY KEY (id_base_visit);


ALTER TABLE ONLY monitoring_chiro.cor_counting_contact
    ADD CONSTRAINT cor_counting_contact_pkey PRIMARY KEY (id_counting_contact);


ALTER TABLE ONLY monitoring_chiro.cor_site_infos_nomenclature_amenagements
    ADD CONSTRAINT pk_amenagement_f PRIMARY KEY (id_base_site, id_nomenclature_amenagement);


ALTER TABLE ONLY monitoring_chiro.cor_contact_taxons_nomenclature_indices
    ADD CONSTRAINT pk_cor_contact_taxons_nomenclature_indices PRIMARY KEY (id_contact_taxon, id_nomenclature_indice);


ALTER TABLE ONLY monitoring_chiro.cor_site_infos_nomenclature_menaces
    ADD CONSTRAINT pk_menaces_f PRIMARY KEY (id_base_site, id_nomenclature_menaces);


ALTER TABLE ONLY monitoring_chiro.t_contact_taxon_biometries
    ADD CONSTRAINT t_contact_taxon_biometries_pkey PRIMARY KEY (id_biometrie);

ALTER TABLE ONLY monitoring_chiro.t_site_infos
    ADD CONSTRAINT t_site_infos_pkey PRIMARY KEY (id_base_site);


ALTER TABLE ONLY monitoring_chiro.t_visite_contact_taxons
    ADD CONSTRAINT t_visite_contact_taxons_pkey PRIMARY KEY (id_contact_taxon);

ALTER TABLE ONLY monitoring_chiro.cor_visite_area
    ADD CONSTRAINT pk_cor_visite_area PRIMARY KEY (id_base_visit, id_area);

ALTER TABLE ONLY monitoring_chiro.cor_visite_area
  ADD CONSTRAINT fk_cor_visite_area_id_base_site FOREIGN KEY (id_base_visit) REFERENCES monitoring_chiro.t_visite_conditions (id_base_visit) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE ONLY monitoring_chiro.cor_visite_area
  ADD CONSTRAINT fk_cor_visite_area_id_area FOREIGN KEY (id_area) REFERENCES ref_geo.l_areas (id_area);


-- ################### --
-- INDEX --

CREATE INDEX index_monitoring_chiro_t_visite_conditions_geom ON monitoring_chiro.t_visite_conditions USING gist (geom);

CREATE INDEX index_t_contact_taxon_biometries_id_contact_taxon ON monitoring_chiro.t_contact_taxon_biometries USING btree (id_contact_taxon);

CREATE UNIQUE INDEX index_t_site_infos_id_base_site ON monitoring_chiro.t_site_infos USING btree (id_base_site);

CREATE UNIQUE INDEX index_t_visite_conditions_id_base_visit ON monitoring_chiro.t_visite_conditions USING btree (id_base_visit);

CREATE INDEX index_t_visite_contact_taxons_id_base_visit ON monitoring_chiro.t_visite_contact_taxons USING btree (id_base_visit);


-- ################### --
-- FOREIGN KEYS --

ALTER TABLE ONLY monitoring_chiro.cor_contact_taxons_nomenclature_indices
    ADD CONSTRAINT cor_contact_taxons_nomenclature_ind_id_nomenclature_indice_fkey FOREIGN KEY (id_nomenclature_indice) REFERENCES ref_nomenclatures.t_nomenclatures(id_nomenclature) ON UPDATE CASCADE;

ALTER TABLE ONLY monitoring_chiro.cor_contact_taxons_nomenclature_indices
    ADD CONSTRAINT cor_contact_taxons_nomenclature_indices_id_contact_taxon_fkey FOREIGN KEY (id_contact_taxon) REFERENCES monitoring_chiro.t_visite_contact_taxons(id_contact_taxon) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE ONLY monitoring_chiro.cor_counting_contact
    ADD CONSTRAINT cor_counting_contact_id_contact_taxon_fkey FOREIGN KEY (id_contact_taxon) REFERENCES monitoring_chiro.t_visite_contact_taxons(id_contact_taxon) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE ONLY monitoring_chiro.cor_site_infos_nomenclature_amenagements
    ADD CONSTRAINT cor_site_infos_nomenclature_am_id_nomenclature_amenagement_fkey FOREIGN KEY (id_nomenclature_amenagement) REFERENCES ref_nomenclatures.t_nomenclatures(id_nomenclature) ON UPDATE CASCADE;

ALTER TABLE ONLY monitoring_chiro.cor_site_infos_nomenclature_amenagements
    ADD CONSTRAINT cor_site_infos_nomenclature_amenagements_id_base_site_fkey FOREIGN KEY (id_base_site) REFERENCES monitoring_chiro.t_site_infos(id_base_site) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE ONLY monitoring_chiro.cor_site_infos_nomenclature_menaces
    ADD CONSTRAINT cor_site_infos_nomenclature_menace_id_nomenclature_menaces_fkey FOREIGN KEY (id_nomenclature_menaces) REFERENCES ref_nomenclatures.t_nomenclatures(id_nomenclature) ON UPDATE CASCADE;

ALTER TABLE ONLY monitoring_chiro.cor_site_infos_nomenclature_menaces
    ADD CONSTRAINT cor_site_infos_nomenclature_menaces_id_base_site_fkey FOREIGN KEY (id_base_site) REFERENCES monitoring_chiro.t_site_infos(id_base_site) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE ONLY monitoring_chiro.cor_counting_contact
    ADD CONSTRAINT fk_cor_counting_contact_life_stage FOREIGN KEY (id_nomenclature_life_stage) REFERENCES ref_nomenclatures.t_nomenclatures(id_nomenclature) ON UPDATE CASCADE;

ALTER TABLE ONLY monitoring_chiro.t_contact_taxon_biometries
    ADD CONSTRAINT fk_cor_counting_contact_life_stage FOREIGN KEY (id_nomenclature_life_stage) REFERENCES ref_nomenclatures.t_nomenclatures(id_nomenclature) ON UPDATE CASCADE;

ALTER TABLE ONLY monitoring_chiro.cor_counting_contact
    ADD CONSTRAINT fk_cor_counting_contact_obj_count FOREIGN KEY (id_nomenclature_obj_count) REFERENCES ref_nomenclatures.t_nomenclatures(id_nomenclature) ON UPDATE CASCADE;

ALTER TABLE ONLY monitoring_chiro.cor_counting_contact
    ADD CONSTRAINT fk_cor_counting_contact_sexe FOREIGN KEY (id_nomenclature_sex) REFERENCES ref_nomenclatures.t_nomenclatures(id_nomenclature) ON UPDATE CASCADE;

ALTER TABLE ONLY monitoring_chiro.t_contact_taxon_biometries
    ADD CONSTRAINT fk_cor_counting_contact_sexe FOREIGN KEY (id_nomenclature_sex) REFERENCES ref_nomenclatures.t_nomenclatures(id_nomenclature) ON UPDATE CASCADE;

ALTER TABLE ONLY monitoring_chiro.cor_counting_contact
    ADD CONSTRAINT fk_cor_counting_contact_typ_count FOREIGN KEY (id_nomenclature_type_count) REFERENCES ref_nomenclatures.t_nomenclatures(id_nomenclature) ON UPDATE CASCADE;

ALTER TABLE ONLY monitoring_chiro.cor_counting_contact
    ADD CONSTRAINT fk_cor_stage_number_id_taxon FOREIGN KEY (id_contact_taxon) REFERENCES monitoring_chiro.t_visite_contact_taxons(id_contact_taxon) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE ONLY monitoring_chiro.t_contact_taxon_biometries
    ADD CONSTRAINT t_contact_taxon_biometries_id_contact_taxon_fkey FOREIGN KEY (id_contact_taxon) REFERENCES monitoring_chiro.t_visite_contact_taxons(id_contact_taxon) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE ONLY monitoring_chiro.t_contact_taxon_biometries
    ADD CONSTRAINT t_contact_taxon_biometries_id_digitiser_fkey FOREIGN KEY (id_digitiser) REFERENCES utilisateurs.t_roles(id_role) ON UPDATE CASCADE;

ALTER TABLE ONLY monitoring_chiro.t_site_infos
    ADD CONSTRAINT t_site_infos_id_nomenclature_frequentation_fkey FOREIGN KEY (id_nomenclature_frequentation) REFERENCES ref_nomenclatures.t_nomenclatures(id_nomenclature) ON UPDATE CASCADE;

ALTER TABLE ONLY monitoring_chiro.t_visite_conditions
    ADD CONSTRAINT t_visite_conditions_id_nomenclature_mod_id_fkey FOREIGN KEY (id_nomenclature_mod_id) REFERENCES ref_nomenclatures.t_nomenclatures(id_nomenclature) ON UPDATE CASCADE;

ALTER TABLE ONLY monitoring_chiro.t_visite_contact_taxons
    ADD CONSTRAINT t_visite_contact_taxons_id_digitiser_fkey FOREIGN KEY (id_digitiser) REFERENCES utilisateurs.t_roles(id_role) ON UPDATE CASCADE;

ALTER TABLE ONLY monitoring_chiro.t_visite_contact_taxons
    ADD CONSTRAINT t_visite_contact_taxons_id_nomenclature_behaviour_fkey FOREIGN KEY (id_nomenclature_behaviour) REFERENCES ref_nomenclatures.t_nomenclatures(id_nomenclature) ON UPDATE CASCADE;

ALTER TABLE ONLY monitoring_chiro.t_visite_contact_taxons
    ADD CONSTRAINT t_visite_contact_taxons_id_nomenclature_preuve_repro_fkey FOREIGN KEY (id_nomenclature_preuve_repro) REFERENCES ref_nomenclatures.t_nomenclatures(id_nomenclature) ON UPDATE CASCADE;


ALTER TABLE monitoring_chiro.t_visite_conditions
  ADD CONSTRAINT t_visite_condition_id_base_visit_fkey FOREIGN KEY (id_base_visit) REFERENCES gn_monitoring.t_base_visits (id_base_visit) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE monitoring_chiro.t_visite_contact_taxons
  ADD CONSTRAINT t_visite_contact_taxons_id_base_visit_fkey FOREIGN KEY (id_base_visit) REFERENCES gn_monitoring.t_base_visits (id_base_visit) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE ONLY monitoring_chiro.t_visite_contact_taxons
    ADD CONSTRAINT fk_t_visite_contact_taxons_observation_status FOREIGN KEY (id_nomenclature_observation_status)
      REFERENCES ref_nomenclatures.t_nomenclatures (id_nomenclature) MATCH SIMPLE
      ON UPDATE CASCADE ON DELETE NO ACTION;


-- ################### --
-- TRIGGERS --

CREATE TRIGGER tri_log_changes AFTER INSERT OR DELETE OR UPDATE ON monitoring_chiro.t_visite_contact_taxons FOR EACH ROW EXECUTE PROCEDURE gn_commons.fct_trg_log_changes();

CREATE TRIGGER tri_log_changes AFTER INSERT OR DELETE OR UPDATE ON monitoring_chiro.cor_contact_taxons_nomenclature_indices FOR EACH ROW EXECUTE PROCEDURE gn_commons.fct_trg_log_changes();

CREATE TRIGGER tri_log_changes AFTER INSERT OR DELETE OR UPDATE ON monitoring_chiro.t_visite_conditions FOR EACH ROW EXECUTE PROCEDURE gn_commons.fct_trg_log_changes();

CREATE TRIGGER tri_log_changes AFTER INSERT OR DELETE OR UPDATE ON monitoring_chiro.t_site_infos FOR EACH ROW EXECUTE PROCEDURE gn_commons.fct_trg_log_changes();

CREATE TRIGGER tri_log_changes AFTER INSERT OR DELETE OR UPDATE ON monitoring_chiro.cor_site_infos_nomenclature_menaces FOR EACH ROW EXECUTE PROCEDURE gn_commons.fct_trg_log_changes();

CREATE TRIGGER tri_log_changes AFTER INSERT OR DELETE OR UPDATE ON monitoring_chiro.cor_site_infos_nomenclature_amenagements FOR EACH ROW EXECUTE PROCEDURE gn_commons.fct_trg_log_changes();

CREATE TRIGGER tri_log_changes AFTER INSERT OR DELETE OR UPDATE ON monitoring_chiro.t_contact_taxon_biometries FOR EACH ROW EXECUTE PROCEDURE gn_commons.fct_trg_log_changes();

CREATE TRIGGER tri_log_changes AFTER INSERT OR DELETE OR UPDATE ON monitoring_chiro.cor_counting_contact FOR EACH ROW EXECUTE PROCEDURE gn_commons.fct_trg_log_changes();

CREATE OR REPLACE FUNCTION monitoring_chiro.fct_trg_delete_synthese_cor_counting_contact()
  RETURNS trigger AS
$BODY$
BEGIN
    --Suppression des données dans la synthèse
    DELETE FROM gn_synthese.synthese WHERE unique_id_sinp = OLD.unique_id_sinp;
    RETURN OLD;
END;
$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;

CREATE TRIGGER tri_delete_synthese_cor_counting_contact AFTER DELETE ON monitoring_chiro.cor_counting_contact FOR EACH ROW EXECUTE PROCEDURE monitoring_chiro.fct_trg_delete_synthese_cor_counting_contact();

CREATE OR REPLACE FUNCTION monitoring_chiro.fct_trg_get_nom_complet()
  RETURNS trigger AS
$BODY$
DECLARE
BEGIN
  NEW.nom_complet = (SELECT nom_complet FROM taxonomie.taxref WHERE cd_nom = NEW.cd_nom);
  RETURN NEW;
END;
$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;



CREATE TRIGGER trg_get_nom_complet
  BEFORE INSERT OR UPDATE
  ON  monitoring_chiro.t_visite_contact_taxons
  FOR EACH ROW
  EXECUTE PROCEDURE monitoring_chiro.fct_trg_get_nom_complet();

CREATE FUNCTION monitoring_chiro.fct_trg_duplicate_site_geom()
  RETURNS trigger AS
$BODY$
BEGIN

	UPDATE  monitoring_chiro.t_visite_conditions vc SET geom = NEW.geom
	FROM gn_monitoring.t_base_visits v
	WHERE vc.id_base_visit = v.id_base_visit AND v.id_base_site = NEW.id_base_site;
  RETURN NEW;
END;
$BODY$
LANGUAGE plpgsql;


CREATE TRIGGER trg_chiro_duplicate_site_geom
  AFTER INSERT OR UPDATE OF geom ON gn_monitoring.t_base_sites
  FOR EACH ROW
  EXECUTE PROCEDURE  monitoring_chiro.fct_trg_duplicate_site_geom();

CREATE FUNCTION monitoring_chiro.fct_trg_cor_visite_condition_area()
  RETURNS trigger AS
$BODY$
BEGIN

	DELETE FROM monitoring_chiro.cor_visite_area WHERE id_base_visit = NEW.id_base_visit;
	INSERT INTO monitoring_chiro.cor_visite_area
	SELECT NEW.id_base_visit, (ref_geo.fct_get_area_intersection(NEW.geom)).id_area;

  RETURN NEW;
END;
$BODY$
LANGUAGE plpgsql;


CREATE TRIGGER trg_cor_visite_area
  AFTER INSERT OR UPDATE OF geom ON monitoring_chiro.t_visite_conditions
  FOR EACH ROW
  EXECUTE PROCEDURE monitoring_chiro.fct_trg_cor_visite_condition_area();
