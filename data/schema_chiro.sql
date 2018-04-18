DROP SCHEMA IF EXISTS monitoring_chiro CASCADE;
CREATE SCHEMA monitoring_chiro;

CREATE TABLE monitoring_chiro.cor_contact_taxons_nomenclature_indices (
    id_contact_taxon integer NOT NULL,
    id_nomenclature_indice integer NOT NULL,
    uuid_chiro_visite_contact_indices uuid DEFAULT public.uuid_generate_v4()
);



--
-- TOC entry 341 (class 1259 OID 1066380)
-- Name: cor_counting_contact; Type: TABLE; Schema: monitoring_chiro;
--

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
    db_suivi_id integer,
    app character varying,
    CONSTRAINT check_cor_counting_contact_count_max CHECK (((count_max >= count_min) AND (count_max > 0))),
    CONSTRAINT check_cor_counting_contact_count_min CHECK ((count_min > 0))
);


--
-- TOC entry 4277 (class 0 OID 0)
-- Dependencies: 341
-- Name: COLUMN cor_counting_contact.id_nomenclature_life_stage; Type: COMMENT; Schema: monitoring_chiro;
--

COMMENT ON COLUMN monitoring_chiro.cor_counting_contact.id_nomenclature_life_stage IS 'Correspondance nomenclature INPN = stade_vie (10)';


--
-- TOC entry 4278 (class 0 OID 0)
-- Dependencies: 341
-- Name: COLUMN cor_counting_contact.id_nomenclature_sex; Type: COMMENT; Schema: monitoring_chiro;
--

COMMENT ON COLUMN monitoring_chiro.cor_counting_contact.id_nomenclature_sex IS 'Correspondance nomenclature INPN = sexe (9)';


--
-- TOC entry 4279 (class 0 OID 0)
-- Dependencies: 341
-- Name: COLUMN cor_counting_contact.id_nomenclature_obj_count; Type: COMMENT; Schema: monitoring_chiro;
--

COMMENT ON COLUMN monitoring_chiro.cor_counting_contact.id_nomenclature_obj_count IS 'Correspondance nomenclature INPN = obj_denbr (6)';


--
-- TOC entry 4280 (class 0 OID 0)
-- Dependencies: 341
-- Name: COLUMN cor_counting_contact.id_nomenclature_type_count; Type: COMMENT; Schema: monitoring_chiro;
--

COMMENT ON COLUMN monitoring_chiro.cor_counting_contact.id_nomenclature_type_count IS 'Correspondance nomenclature INPN = typ_denbr (21)';


--
-- TOC entry 340 (class 1259 OID 1066378)
-- Name: cor_counting_contact_id_counting_contact_seq; Type: SEQUENCE; Schema: monitoring_chiro;
--

CREATE SEQUENCE monitoring_chiro.cor_counting_contact_id_counting_contact_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

--
-- TOC entry 4281 (class 0 OID 0)
-- Dependencies: 340
-- Name: cor_counting_contact_id_counting_contact_seq; Type: SEQUENCE OWNED BY; Schema: monitoring_chiro;
--

ALTER SEQUENCE monitoring_chiro.cor_counting_contact_id_counting_contact_seq OWNED BY monitoring_chiro.cor_counting_contact.id_counting_contact;


--
-- TOC entry 342 (class 1259 OID 1066438)
-- Name: cor_site_infos_nomenclature_amenagements; Type: TABLE; Schema: monitoring_chiro;
--

CREATE TABLE monitoring_chiro.cor_site_infos_nomenclature_amenagements (
    id_site_infos integer NOT NULL,
    id_nomenclature_amenagement integer NOT NULL,
    uuid_chiro_site_amenagements uuid DEFAULT public.uuid_generate_v4()
);



--
-- TOC entry 343 (class 1259 OID 1066453)
-- Name: cor_site_infos_nomenclature_menaces; Type: TABLE; Schema: monitoring_chiro;
--

CREATE TABLE monitoring_chiro.cor_site_infos_nomenclature_menaces (
    id_site_infos integer NOT NULL,
    id_nomenclature_menaces integer NOT NULL,
    uuid_chiro_site_menaces uuid DEFAULT public.uuid_generate_v4()
);


--
-- TOC entry 345 (class 1259 OID 1066485)
-- Name: t_contact_taxon_biometries; Type: TABLE; Schema: monitoring_chiro;
--

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
    db_suivi_id integer,
    app character varying,
    uuid_chiro_biometrie uuid DEFAULT public.uuid_generate_v4()
);


--
-- TOC entry 344 (class 1259 OID 1066483)
-- Name: t_contact_taxon_biometries_id_biometrie_seq; Type: SEQUENCE; Schema: monitoring_chiro;
--

CREATE SEQUENCE monitoring_chiro.t_contact_taxon_biometries_id_biometrie_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

--
-- TOC entry 4282 (class 0 OID 0)
-- Dependencies: 344
-- Name: t_contact_taxon_biometries_id_biometrie_seq; Type: SEQUENCE OWNED BY; Schema: monitoring_chiro;
--

ALTER SEQUENCE monitoring_chiro.t_contact_taxon_biometries_id_biometrie_seq OWNED BY monitoring_chiro.t_contact_taxon_biometries.id_biometrie;


--
-- TOC entry 335 (class 1259 OID 1066296)
-- Name: t_site_infos; Type: TABLE; Schema: monitoring_chiro;
--

CREATE TABLE monitoring_chiro.t_site_infos (
    id_site_infos integer NOT NULL,
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


--
-- TOC entry 334 (class 1259 OID 1066294)
-- Name: t_site_infos_id_site_infos_seq; Type: SEQUENCE; Schema: monitoring_chiro;
--

CREATE SEQUENCE monitoring_chiro.t_site_infos_id_site_infos_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 4283 (class 0 OID 0)
-- Dependencies: 334
-- Name: t_site_infos_id_site_infos_seq; Type: SEQUENCE OWNED BY; Schema: monitoring_chiro;
--

ALTER SEQUENCE monitoring_chiro.t_site_infos_id_site_infos_seq OWNED BY monitoring_chiro.t_site_infos.id_site_infos;


--
-- TOC entry 337 (class 1259 OID 1066318)
-- Name: t_visite_conditions; Type: TABLE; Schema: monitoring_chiro;
--

CREATE TABLE monitoring_chiro.t_visite_conditions (
    id_visite_cond integer NOT NULL,
    id_base_visit integer NOT NULL,
    geom public.geometry,
    temperature numeric(4,2),
    humidite numeric(4,2),
    id_nomenclature_mod_id integer,
    db_suivi_id integer,
    app character varying,
    uuid_chiro_visite_conditions uuid DEFAULT public.uuid_generate_v4(),
    CONSTRAINT enforce_dims_geom CHECK ((public.st_ndims(geom) = 2)),
    CONSTRAINT enforce_srid_geom CHECK ((public.st_srid(geom) = 4326))
);

--
-- TOC entry 336 (class 1259 OID 1066316)
-- Name: t_visite_conditions_id_visite_cond_seq; Type: SEQUENCE; Schema: monitoring_chiro;
--

CREATE SEQUENCE monitoring_chiro.t_visite_conditions_id_visite_cond_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

--
-- TOC entry 4284 (class 0 OID 0)
-- Dependencies: 336
-- Name: t_visite_conditions_id_visite_cond_seq; Type: SEQUENCE OWNED BY; Schema: monitoring_chiro;
--

ALTER SEQUENCE monitoring_chiro.t_visite_conditions_id_visite_cond_seq OWNED BY monitoring_chiro.t_visite_conditions.id_visite_cond;


--
-- TOC entry 339 (class 1259 OID 1066344)
-- Name: t_visite_contact_taxons; Type: TABLE; Schema: monitoring_chiro;
--

CREATE TABLE monitoring_chiro.t_visite_contact_taxons (
    id_contact_taxon integer NOT NULL,
    id_base_visit integer NOT NULL,
    tx_presume character varying(250) DEFAULT NULL::character varying,
    cd_nom integer,
    nom_complet character varying(255),
    espece_incertaine boolean DEFAULT false NOT NULL,
    id_nomenclature_preuve_repro integer,
    id_nomenclature_activite integer,
    indices_cmt character varying(1000),
    commentaire character varying(1000),
    id_digitiser integer,
    db_suivi_id integer,
    app character varying,
    uuid_chiro_visite_contact_taxon uuid DEFAULT public.uuid_generate_v4()
);


--
-- TOC entry 338 (class 1259 OID 1066342)
-- Name: t_visite_contact_taxons_id_contact_taxon_seq; Type: SEQUENCE; Schema: monitoring_chiro;
--

CREATE SEQUENCE monitoring_chiro.t_visite_contact_taxons_id_contact_taxon_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;



--
-- TOC entry 4028 (class 2604 OID 1066383)
-- Name: id_counting_contact; Type: DEFAULT; Schema: monitoring_chiro;
--

ALTER TABLE ONLY monitoring_chiro.cor_counting_contact ALTER COLUMN id_counting_contact SET DEFAULT nextval('monitoring_chiro.cor_counting_contact_id_counting_contact_seq'::regclass);


--
-- TOC entry 4038 (class 2604 OID 1066488)
-- Name: id_biometrie; Type: DEFAULT; Schema: monitoring_chiro;
--

ALTER TABLE ONLY monitoring_chiro.t_contact_taxon_biometries ALTER COLUMN id_biometrie SET DEFAULT nextval('monitoring_chiro.t_contact_taxon_biometries_id_biometrie_seq'::regclass);


--
-- TOC entry 4018 (class 2604 OID 1066299)
-- Name: id_site_infos; Type: DEFAULT; Schema: monitoring_chiro;
--

ALTER TABLE ONLY monitoring_chiro.t_site_infos ALTER COLUMN id_site_infos SET DEFAULT nextval('monitoring_chiro.t_site_infos_id_site_infos_seq'::regclass);


--
-- TOC entry 4020 (class 2604 OID 1066321)
-- Name: id_visite_cond; Type: DEFAULT; Schema: monitoring_chiro;
--

ALTER TABLE ONLY monitoring_chiro.t_visite_conditions ALTER COLUMN id_visite_cond SET DEFAULT nextval('monitoring_chiro.t_visite_conditions_id_visite_cond_seq'::regclass);


--
-- TOC entry 4024 (class 2604 OID 1066347)
-- Name: id_contact_taxon; Type: DEFAULT; Schema: monitoring_chiro;
--

ALTER TABLE ONLY monitoring_chiro.t_visite_contact_taxons ALTER COLUMN id_contact_taxon SET DEFAULT nextval('monitoring_chiro.t_visite_contact_taxons_id_contact_taxon_seq'::regclass);


--
-- TOC entry 4032 (class 2606 OID 1110961)
-- Name: check_cor_counting_contact_life_stage; Type: CHECK CONSTRAINT; Schema: monitoring_chiro;
--

ALTER TABLE monitoring_chiro.cor_counting_contact
    ADD CONSTRAINT check_cor_counting_contact_life_stage CHECK (ref_nomenclatures.check_nomenclature_type(id_nomenclature_life_stage, 10)) NOT VALID;


--
-- TOC entry 4040 (class 2606 OID 1110966)
-- Name: check_cor_counting_contact_life_stage; Type: CHECK CONSTRAINT; Schema: monitoring_chiro;
--

ALTER TABLE monitoring_chiro.t_contact_taxon_biometries
    ADD CONSTRAINT check_cor_counting_contact_life_stage CHECK (ref_nomenclatures.check_nomenclature_type(id_nomenclature_life_stage, 10)) NOT VALID;


--
-- TOC entry 4033 (class 2606 OID 1110962)
-- Name: check_cor_counting_contact_obj_count; Type: CHECK CONSTRAINT; Schema: monitoring_chiro;
--

ALTER TABLE monitoring_chiro.cor_counting_contact
    ADD CONSTRAINT check_cor_counting_contact_obj_count CHECK (ref_nomenclatures.check_nomenclature_type(id_nomenclature_obj_count, 6)) NOT VALID;


--
-- TOC entry 4034 (class 2606 OID 1110963)
-- Name: check_cor_counting_contact_sexe; Type: CHECK CONSTRAINT; Schema: monitoring_chiro;
--

ALTER TABLE monitoring_chiro.cor_counting_contact
    ADD CONSTRAINT check_cor_counting_contact_sexe CHECK (ref_nomenclatures.check_nomenclature_type(id_nomenclature_sex, 9)) NOT VALID;


--
-- TOC entry 4041 (class 2606 OID 1110967)
-- Name: check_cor_counting_contact_sexe; Type: CHECK CONSTRAINT; Schema: monitoring_chiro;
--

ALTER TABLE monitoring_chiro.t_contact_taxon_biometries
    ADD CONSTRAINT check_cor_counting_contact_sexe CHECK (ref_nomenclatures.check_nomenclature_type(id_nomenclature_sex, 9)) NOT VALID;


--
-- TOC entry 4035 (class 2606 OID 1110964)
-- Name: check_cor_counting_contact_type_count; Type: CHECK CONSTRAINT; Schema: monitoring_chiro;
--

ALTER TABLE monitoring_chiro.cor_counting_contact
    ADD CONSTRAINT check_cor_counting_contact_type_count CHECK (ref_nomenclatures.check_nomenclature_type(id_nomenclature_type_count, 21)) NOT VALID;


--
-- TOC entry 4054 (class 2606 OID 1066396)
-- Name: cor_counting_contact_pkey; Type: CONSTRAINT; Schema: monitoring_chiro;
--

ALTER TABLE ONLY monitoring_chiro.cor_counting_contact
    ADD CONSTRAINT cor_counting_contact_pkey PRIMARY KEY (id_counting_contact);


--
-- TOC entry 4056 (class 2606 OID 1066442)
-- Name: pk_amenagement_f; Type: CONSTRAINT; Schema: monitoring_chiro;
--

ALTER TABLE ONLY monitoring_chiro.cor_site_infos_nomenclature_amenagements
    ADD CONSTRAINT pk_amenagement_f PRIMARY KEY (id_site_infos, id_nomenclature_amenagement);


--
-- TOC entry 4063 (class 2606 OID 1066835)
-- Name: pk_cor_contact_taxons_nomenclature_indices; Type: CONSTRAINT; Schema: monitoring_chiro;
--

ALTER TABLE ONLY monitoring_chiro.cor_contact_taxons_nomenclature_indices
    ADD CONSTRAINT pk_cor_contact_taxons_nomenclature_indices PRIMARY KEY (id_contact_taxon, id_nomenclature_indice);


--
-- TOC entry 4058 (class 2606 OID 1066457)
-- Name: pk_menaces_f; Type: CONSTRAINT; Schema: monitoring_chiro;
--

ALTER TABLE ONLY monitoring_chiro.cor_site_infos_nomenclature_menaces
    ADD CONSTRAINT pk_menaces_f PRIMARY KEY (id_site_infos, id_nomenclature_menaces);


--
-- TOC entry 4061 (class 2606 OID 1066496)
-- Name: t_contact_taxon_biometries_pkey; Type: CONSTRAINT; Schema: monitoring_chiro;
--

ALTER TABLE ONLY monitoring_chiro.t_contact_taxon_biometries
    ADD CONSTRAINT t_contact_taxon_biometries_pkey PRIMARY KEY (id_biometrie);


--
-- TOC entry 4045 (class 2606 OID 1066304)
-- Name: t_site_infos_pkey; Type: CONSTRAINT; Schema: monitoring_chiro;
--

ALTER TABLE ONLY monitoring_chiro.t_site_infos
    ADD CONSTRAINT t_site_infos_pkey PRIMARY KEY (id_site_infos);


--
-- TOC entry 4049 (class 2606 OID 1066328)
-- Name: t_visite_conditions_pkey; Type: CONSTRAINT; Schema: monitoring_chiro;
--

ALTER TABLE ONLY monitoring_chiro.t_visite_conditions
    ADD CONSTRAINT t_visite_conditions_pkey PRIMARY KEY (id_visite_cond);


--
-- TOC entry 4052 (class 2606 OID 1066355)
-- Name: t_visite_contact_taxons_pkey; Type: CONSTRAINT; Schema: monitoring_chiro;
--

ALTER TABLE ONLY monitoring_chiro.t_visite_contact_taxons
    ADD CONSTRAINT t_visite_contact_taxons_pkey PRIMARY KEY (id_contact_taxon);


--
-- TOC entry 4046 (class 1259 OID 1066339)
-- Name: index_monitoring_chiro_t_visite_conditions_geom; Type: INDEX; Schema: monitoring_chiro;
--

CREATE INDEX index_monitoring_chiro_t_visite_conditions_geom ON monitoring_chiro.t_visite_conditions USING gist (geom);


--
-- TOC entry 4059 (class 1259 OID 1066517)
-- Name: index_t_contact_taxon_biometries_id_contact_taxon; Type: INDEX; Schema: monitoring_chiro;
--

CREATE INDEX index_t_contact_taxon_biometries_id_contact_taxon ON monitoring_chiro.t_contact_taxon_biometries USING btree (id_contact_taxon);


--
-- TOC entry 4043 (class 1259 OID 1066315)
-- Name: index_t_site_infos_id_base_site; Type: INDEX; Schema: monitoring_chiro;
--

CREATE UNIQUE INDEX index_t_site_infos_id_base_site ON monitoring_chiro.t_site_infos USING btree (id_base_site);


--
-- TOC entry 4047 (class 1259 OID 1066341)
-- Name: index_t_visite_conditions_id_base_visit; Type: INDEX; Schema: monitoring_chiro;
--

CREATE UNIQUE INDEX index_t_visite_conditions_id_base_visit ON monitoring_chiro.t_visite_conditions USING btree (id_base_visit);


--
-- TOC entry 4050 (class 1259 OID 1066846)
-- Name: index_t_visite_contact_taxons_id_base_visit; Type: INDEX; Schema: monitoring_chiro;
--

CREATE INDEX index_t_visite_contact_taxons_id_base_visit ON monitoring_chiro.t_visite_contact_taxons USING btree (id_base_visit);


--
-- TOC entry 4087 (class 2620 OID 1118748)
-- Name: tri_log_changes; Type: TRIGGER; Schema: monitoring_chiro;
--

CREATE TRIGGER tri_log_changes AFTER INSERT OR DELETE OR UPDATE ON monitoring_chiro.t_visite_contact_taxons FOR EACH ROW EXECUTE PROCEDURE gn_commons.fct_trg_log_changes();


--
-- TOC entry 4092 (class 2620 OID 1118749)
-- Name: tri_log_changes; Type: TRIGGER; Schema: monitoring_chiro;
--

CREATE TRIGGER tri_log_changes AFTER INSERT OR DELETE OR UPDATE ON monitoring_chiro.cor_contact_taxons_nomenclature_indices FOR EACH ROW EXECUTE PROCEDURE gn_commons.fct_trg_log_changes();


--
-- TOC entry 4086 (class 2620 OID 1118750)
-- Name: tri_log_changes; Type: TRIGGER; Schema: monitoring_chiro;
--

CREATE TRIGGER tri_log_changes AFTER INSERT OR DELETE OR UPDATE ON monitoring_chiro.t_visite_conditions FOR EACH ROW EXECUTE PROCEDURE gn_commons.fct_trg_log_changes();


--
-- TOC entry 4085 (class 2620 OID 1118751)
-- Name: tri_log_changes; Type: TRIGGER; Schema: monitoring_chiro;
--

CREATE TRIGGER tri_log_changes AFTER INSERT OR DELETE OR UPDATE ON monitoring_chiro.t_site_infos FOR EACH ROW EXECUTE PROCEDURE gn_commons.fct_trg_log_changes();


--
-- TOC entry 4090 (class 2620 OID 1118752)
-- Name: tri_log_changes; Type: TRIGGER; Schema: monitoring_chiro;
--

CREATE TRIGGER tri_log_changes AFTER INSERT OR DELETE OR UPDATE ON monitoring_chiro.cor_site_infos_nomenclature_menaces FOR EACH ROW EXECUTE PROCEDURE gn_commons.fct_trg_log_changes();


--
-- TOC entry 4089 (class 2620 OID 1118753)
-- Name: tri_log_changes; Type: TRIGGER; Schema: monitoring_chiro;
--

CREATE TRIGGER tri_log_changes AFTER INSERT OR DELETE OR UPDATE ON monitoring_chiro.cor_site_infos_nomenclature_amenagements FOR EACH ROW EXECUTE PROCEDURE gn_commons.fct_trg_log_changes();


--
-- TOC entry 4091 (class 2620 OID 1118754)
-- Name: tri_log_changes; Type: TRIGGER; Schema: monitoring_chiro;
--

CREATE TRIGGER tri_log_changes AFTER INSERT OR DELETE OR UPDATE ON monitoring_chiro.t_contact_taxon_biometries FOR EACH ROW EXECUTE PROCEDURE gn_commons.fct_trg_log_changes();


--
-- TOC entry 4088 (class 2620 OID 1118755)
-- Name: tri_log_changes; Type: TRIGGER; Schema: monitoring_chiro;
--

CREATE TRIGGER tri_log_changes AFTER INSERT OR DELETE OR UPDATE ON monitoring_chiro.cor_counting_contact FOR EACH ROW EXECUTE PROCEDURE gn_commons.fct_trg_log_changes();


--
-- TOC entry 4083 (class 2606 OID 1066841)
-- Name: cor_contact_taxons_nomenclature_ind_id_nomenclature_indice_fkey; Type: FK CONSTRAINT; Schema: monitoring_chiro;
--

ALTER TABLE ONLY monitoring_chiro.cor_contact_taxons_nomenclature_indices
    ADD CONSTRAINT cor_contact_taxons_nomenclature_ind_id_nomenclature_indice_fkey FOREIGN KEY (id_nomenclature_indice) REFERENCES ref_nomenclatures.t_nomenclatures(id_nomenclature) ON UPDATE CASCADE;


--
-- TOC entry 4084 (class 2606 OID 1066836)
-- Name: cor_contact_taxons_nomenclature_indices_id_contact_taxon_fkey; Type: FK CONSTRAINT; Schema: monitoring_chiro;
--

ALTER TABLE ONLY monitoring_chiro.cor_contact_taxons_nomenclature_indices
    ADD CONSTRAINT cor_contact_taxons_nomenclature_indices_id_contact_taxon_fkey FOREIGN KEY (id_contact_taxon) REFERENCES monitoring_chiro.t_visite_contact_taxons(id_contact_taxon) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 4074 (class 2606 OID 1066397)
-- Name: cor_counting_contact_id_contact_taxon_fkey; Type: FK CONSTRAINT; Schema: monitoring_chiro;
--

ALTER TABLE ONLY monitoring_chiro.cor_counting_contact
    ADD CONSTRAINT cor_counting_contact_id_contact_taxon_fkey FOREIGN KEY (id_contact_taxon) REFERENCES monitoring_chiro.t_visite_contact_taxons(id_contact_taxon) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 4075 (class 2606 OID 1066448)
-- Name: cor_site_infos_nomenclature_am_id_nomenclature_amenagement_fkey; Type: FK CONSTRAINT; Schema: monitoring_chiro;
--

ALTER TABLE ONLY monitoring_chiro.cor_site_infos_nomenclature_amenagements
    ADD CONSTRAINT cor_site_infos_nomenclature_am_id_nomenclature_amenagement_fkey FOREIGN KEY (id_nomenclature_amenagement) REFERENCES ref_nomenclatures.t_nomenclatures(id_nomenclature) ON UPDATE CASCADE;


--
-- TOC entry 4076 (class 2606 OID 1066443)
-- Name: cor_site_infos_nomenclature_amenagements_id_site_infos_fkey; Type: FK CONSTRAINT; Schema: monitoring_chiro;
--

ALTER TABLE ONLY monitoring_chiro.cor_site_infos_nomenclature_amenagements
    ADD CONSTRAINT cor_site_infos_nomenclature_amenagements_id_site_infos_fkey FOREIGN KEY (id_site_infos) REFERENCES monitoring_chiro.t_site_infos(id_site_infos) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 4077 (class 2606 OID 1066463)
-- Name: cor_site_infos_nomenclature_menace_id_nomenclature_menaces_fkey; Type: FK CONSTRAINT; Schema: monitoring_chiro;
--

ALTER TABLE ONLY monitoring_chiro.cor_site_infos_nomenclature_menaces
    ADD CONSTRAINT cor_site_infos_nomenclature_menace_id_nomenclature_menaces_fkey FOREIGN KEY (id_nomenclature_menaces) REFERENCES ref_nomenclatures.t_nomenclatures(id_nomenclature) ON UPDATE CASCADE;


--
-- TOC entry 4078 (class 2606 OID 1066458)
-- Name: cor_site_infos_nomenclature_menaces_id_site_infos_fkey; Type: FK CONSTRAINT; Schema: monitoring_chiro;
--

ALTER TABLE ONLY monitoring_chiro.cor_site_infos_nomenclature_menaces
    ADD CONSTRAINT cor_site_infos_nomenclature_menaces_id_site_infos_fkey FOREIGN KEY (id_site_infos) REFERENCES monitoring_chiro.t_site_infos(id_site_infos) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 4073 (class 2606 OID 1066402)
-- Name: fk_cor_counting_contact_life_stage; Type: FK CONSTRAINT; Schema: monitoring_chiro;
--

ALTER TABLE ONLY monitoring_chiro.cor_counting_contact
    ADD CONSTRAINT fk_cor_counting_contact_life_stage FOREIGN KEY (id_nomenclature_life_stage) REFERENCES ref_nomenclatures.t_nomenclatures(id_nomenclature) ON UPDATE CASCADE;


--
-- TOC entry 4079 (class 2606 OID 1066512)
-- Name: fk_cor_counting_contact_life_stage; Type: FK CONSTRAINT; Schema: monitoring_chiro;
--

ALTER TABLE ONLY monitoring_chiro.t_contact_taxon_biometries
    ADD CONSTRAINT fk_cor_counting_contact_life_stage FOREIGN KEY (id_nomenclature_life_stage) REFERENCES ref_nomenclatures.t_nomenclatures(id_nomenclature) ON UPDATE CASCADE;


--
-- TOC entry 4072 (class 2606 OID 1066407)
-- Name: fk_cor_counting_contact_obj_count; Type: FK CONSTRAINT; Schema: monitoring_chiro;
--

ALTER TABLE ONLY monitoring_chiro.cor_counting_contact
    ADD CONSTRAINT fk_cor_counting_contact_obj_count FOREIGN KEY (id_nomenclature_obj_count) REFERENCES ref_nomenclatures.t_nomenclatures(id_nomenclature) ON UPDATE CASCADE;


--
-- TOC entry 4071 (class 2606 OID 1066412)
-- Name: fk_cor_counting_contact_sexe; Type: FK CONSTRAINT; Schema: monitoring_chiro;
--

ALTER TABLE ONLY monitoring_chiro.cor_counting_contact
    ADD CONSTRAINT fk_cor_counting_contact_sexe FOREIGN KEY (id_nomenclature_sex) REFERENCES ref_nomenclatures.t_nomenclatures(id_nomenclature) ON UPDATE CASCADE;


--
-- TOC entry 4080 (class 2606 OID 1066507)
-- Name: fk_cor_counting_contact_sexe; Type: FK CONSTRAINT; Schema: monitoring_chiro;
--

ALTER TABLE ONLY monitoring_chiro.t_contact_taxon_biometries
    ADD CONSTRAINT fk_cor_counting_contact_sexe FOREIGN KEY (id_nomenclature_sex) REFERENCES ref_nomenclatures.t_nomenclatures(id_nomenclature) ON UPDATE CASCADE;


--
-- TOC entry 4070 (class 2606 OID 1066422)
-- Name: fk_cor_counting_contact_typ_count; Type: FK CONSTRAINT; Schema: monitoring_chiro;
--

ALTER TABLE ONLY monitoring_chiro.cor_counting_contact
    ADD CONSTRAINT fk_cor_counting_contact_typ_count FOREIGN KEY (id_nomenclature_type_count) REFERENCES ref_nomenclatures.t_nomenclatures(id_nomenclature) ON UPDATE CASCADE;


--
-- TOC entry 4069 (class 2606 OID 1066432)
-- Name: fk_cor_stage_number_id_taxon; Type: FK CONSTRAINT; Schema: monitoring_chiro;
--

ALTER TABLE ONLY monitoring_chiro.cor_counting_contact
    ADD CONSTRAINT fk_cor_stage_number_id_taxon FOREIGN KEY (id_contact_taxon) REFERENCES monitoring_chiro.t_visite_contact_taxons(id_contact_taxon) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 4082 (class 2606 OID 1066497)
-- Name: t_contact_taxon_biometries_id_contact_taxon_fkey; Type: FK CONSTRAINT; Schema: monitoring_chiro;
--

ALTER TABLE ONLY monitoring_chiro.t_contact_taxon_biometries
    ADD CONSTRAINT t_contact_taxon_biometries_id_contact_taxon_fkey FOREIGN KEY (id_contact_taxon) REFERENCES monitoring_chiro.t_visite_contact_taxons(id_contact_taxon) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 4081 (class 2606 OID 1066502)
-- Name: t_contact_taxon_biometries_id_digitiser_fkey; Type: FK CONSTRAINT; Schema: monitoring_chiro;
--

ALTER TABLE ONLY monitoring_chiro.t_contact_taxon_biometries
    ADD CONSTRAINT t_contact_taxon_biometries_id_digitiser_fkey FOREIGN KEY (id_digitiser) REFERENCES utilisateurs.t_roles(id_role) ON UPDATE CASCADE;


--
-- TOC entry 4064 (class 2606 OID 1066310)
-- Name: t_site_infos_id_nomenclature_frequentation_fkey; Type: FK CONSTRAINT; Schema: monitoring_chiro;
--

ALTER TABLE ONLY monitoring_chiro.t_site_infos
    ADD CONSTRAINT t_site_infos_id_nomenclature_frequentation_fkey FOREIGN KEY (id_nomenclature_frequentation) REFERENCES ref_nomenclatures.t_nomenclatures(id_nomenclature) ON UPDATE CASCADE;


--
-- TOC entry 4065 (class 2606 OID 1066334)
-- Name: t_visite_conditions_id_nomenclature_mod_id_fkey; Type: FK CONSTRAINT; Schema: monitoring_chiro;
--

ALTER TABLE ONLY monitoring_chiro.t_visite_conditions
    ADD CONSTRAINT t_visite_conditions_id_nomenclature_mod_id_fkey FOREIGN KEY (id_nomenclature_mod_id) REFERENCES ref_nomenclatures.t_nomenclatures(id_nomenclature) ON UPDATE CASCADE;


--
-- TOC entry 4066 (class 2606 OID 1066371)
-- Name: t_visite_contact_taxons_id_digitiser_fkey; Type: FK CONSTRAINT; Schema: monitoring_chiro;
--

ALTER TABLE ONLY monitoring_chiro.t_visite_contact_taxons
    ADD CONSTRAINT t_visite_contact_taxons_id_digitiser_fkey FOREIGN KEY (id_digitiser) REFERENCES utilisateurs.t_roles(id_role) ON UPDATE CASCADE;


--
-- TOC entry 4067 (class 2606 OID 1066366)
-- Name: t_visite_contact_taxons_id_nomenclature_activite_fkey; Type: FK CONSTRAINT; Schema: monitoring_chiro;
--

ALTER TABLE ONLY monitoring_chiro.t_visite_contact_taxons
    ADD CONSTRAINT t_visite_contact_taxons_id_nomenclature_activite_fkey FOREIGN KEY (id_nomenclature_activite) REFERENCES ref_nomenclatures.t_nomenclatures(id_nomenclature) ON UPDATE CASCADE;


--
-- TOC entry 4068 (class 2606 OID 1066361)
-- Name: t_visite_contact_taxons_id_nomenclature_preuve_repro_fkey; Type: FK CONSTRAINT; Schema: monitoring_chiro;
--

ALTER TABLE ONLY monitoring_chiro.t_visite_contact_taxons
    ADD CONSTRAINT t_visite_contact_taxons_id_nomenclature_preuve_repro_fkey FOREIGN KEY (id_nomenclature_preuve_repro) REFERENCES ref_nomenclatures.t_nomenclatures(id_nomenclature) ON UPDATE CASCADE;


-- Completed on 2018-04-18 10:06:54 CEST

--
-- PostgreSQL database dump complete
--