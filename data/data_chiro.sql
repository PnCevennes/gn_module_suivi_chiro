
INSERT INTO gn_commons.bib_tables_location(table_desc, schema_name, table_name, pk_field, uuid_field_name)
VALUES
('Liste des taxons observés durant une visite chiroptère', 'monitoring_chiro', 't_visite_contact_taxons', 'id_contact_taxon', 'uuid_chiro_visite_contact_taxon'),
('Liste des indices ayant conduit à l''identification d''un taxon lors d''une visite', 'monitoring_chiro', 'cor_contact_taxons_nomenclature_indices',
'uuid_chiro_visite_contact_indices', 'uuid_chiro_visite_contact_indices'
),
('Conditions de la visite d''un gite de chiroptère', 'monitoring_chiro', 't_visite_conditions', 'id_visite_cond', 'uuid_chiro_visite_conditions'),
('Information complémentaire de description des sites à chiroptère', 'monitoring_chiro', 't_site_infos', 'id_site_infos', 'uuid_chiro_site_infos'),
('Menaces relevés sur un site à chiroptère', 'monitoring_chiro', 'cor_site_infos_nomenclature_menaces', 'uuid_chiro_site_menaces', 'uuid_chiro_site_menaces'),
('Aménagements relevés sur un site à chiroptère', 'monitoring_chiro', 'cor_site_infos_nomenclature_amenagements', 'uuid_chiro_site_amenagements', 'uuid_chiro_site_amenagements'),
('Données de biométrie des chiroptères mesurés lors d''une capture', 'monitoring_chiro', 't_contact_taxon_biometries', 'id_biometrie', 'uuid_chiro_biometrie'),
('Données dénombrement des taxons observés durant une visite chiroptère', 'monitoring_chiro', 'cor_counting_contact', 'id_counting_contact', 'unique_id_sinp') ;

