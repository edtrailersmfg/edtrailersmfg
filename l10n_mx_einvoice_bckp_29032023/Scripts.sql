/* Eliminar los Regimen Fiscales */

--create table partner_regimen_rel  (
--    partner_id integer,
--    regimen_fiscal text,
--    );

--insert into partner_regimen_rel (partner_id, regimen_fiscal)
--select res_partner.id, regimen_fiscal.name from res_partner join regimen_fiscal on regimen_fiscal.id = res_partner.regimen_fiscal_id
--;

update res_partner set regimen_fiscal_id=null;

/* IMPUESTOS */

update account_tax set sat_code_tax = '001' where UPPER(name) like '%ISR%';
update account_tax set sat_code_tax = '002' where UPPER(name) like '%IVA%';
update account_tax set sat_code_tax = '002' where UPPER(name) like '%IEPS%';

update account_tax set sat_tasa_cuota = 'Tasa' where amount_type in ('percent','division');
update account_tax set sat_tasa_cuota = 'Cuota' where amount_type='fixed';
update account_tax set sat_tasa_cuota = 'Excento' where amount=0.0;

/* ACTUALIZAR LAS FACTURAS VIEJAS */

update account_invoice set metodo_pago_id = 1, uso_cfdi_id = 1 where metodo_pago_id is null;

/* ACTUALIZAR LOS CODIGOS POSTALES PARA DIRECCIONES DE CLIENTES */

update res_partner set zip_sat_id=res_country_zip_sat_code.id 
                                    from res_country_zip_sat_code 
                                    where res_country_zip_sat_code.code = res_partner.zip
                                    and res_partner.zip_sat_id is null;
