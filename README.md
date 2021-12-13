# Localización Mexicana Odoo 15 - Comunitaria y Enterprise


Suite de Aplicaciones que permiten adaptar las regulaciones Estatales en ambitos Fiscales para México, dentro de las principales funciones encontraremos:

* [Facturación Electrónica](https://www.sat.gob.mx/personas/factura-electronica) - Mas Información
* [Contabilidad Electrónica](http://omawww.sat.gob.mx/contabilidadelectronica/Paginas/documentos/infografia.pdf) - Mas Información
* [Complemento Pago Electrónico](http://omawww.sat.gob.mx/tramitesyservicios/Paginas/documentos/PregFrec_RP.pdf) - Preguntas y Respuestas

## Getting Started

Las siguientes instrucciones nos permiten el buen funcionamiento de los modulos en la versión 14.0 de Odoo.

### Requisitos

* Se necesita desinstalar el modulo estandar de Facturación Electónica de Odoo, si es que tenemos la versión Enterprise.

```
 * l10n_mx

 * l10n_mx_edi

```

Necesitamos instalar las siguientes librerias:

```
sudo apt-get install python3-pip
sudo pip3 install M2Crypto
sudo pip3 install jinja2
sudo pip3 install pyopenssl
sudo pip3 install  soappy
sudo pip3 install pycrypto
sudo pip3 install frozendict
sudo pip3 install qrcode
sudo pip3 install qrtools
sudo pip3 install python-dateutil 

sudo apt-get install xsltproc openssl libxml2-utils -y

```

En caso de que ocurra algún error optamos por intalarlas con el gestor del SO, el siguiente ejemplo es con SO derivamos de Debian:

```
sudo apt-get install python3-pyopenssl
sudo apt-get install python3-jinja2

```

## Deployment

Add additional notes about how to deploy this on a live system


### Notas

* Si se tiene una instalación previa de los ultimos ajustes de Ener 2021, es necesario ejecutar los siguientes querys:

```
 * delete from sat_uso_cfdi;

 * ALTER SEQUENCE sat_uso_cfdi_id_seq RESTART WITH 1;

 * delete from sat_tipo_relacion_cfdi;

 * ALTER SEQUENCE sat_tipo_relacion_cfdi_id_seq RESTART WITH 1;
 
 * delete from res_country_state_sat_code;

 * ALTER SEQUENCE res_country_state_sat_code_id_seq RESTART WITH 1;

 * delete from res_country_sat_code;

 * ALTER SEQUENCE res_country_sat_code_id_seq RESTART WITH 1;

 * delete from ir_model where model='overall.config.wizard.sat.models.cfdi';

 * delete from ir_ui_view where model='overall.config.wizard.sat.models.cfdi';

 * delete from ir_model where model = 'res.country.sat.code';

 * delete from ir_ui_view where model='res.country.sat.code';
```

## Authors

* **Israel Cruz Argil** - *Initial work* - [CEO - Argil Consulting](https://www.linkedin.com/in/israel-ca-a431a624/)
* **German Ponce Dominguez** - *Contributor* - [Python Developer Master](https://www.linkedin.com/in/german-ponce-dominguez-07a02b61/)
* **Aldo Luna Guzman** - *Contributor* - [Python Developer Master](https://www.argil.mx)


See also the list of [contributors](https://bitbucket.org/argilconsulting/odoo-mexico-localization) who participated in this project.

## License

Protedigo contra Pirateria bajo la Ley de Protección de Derechos de Autor de México  [Mas información](https://mexico.justia.com/federales/leyes/ley-federal-del-derecho-de-autor/titulo-ii/capitulo-i/) para mas detalles.

## Release NOTES:

* **Versión Beta - 26/09/2021** - *Commit 66032cab0e52bc1b766f4725c1b9a6b5b91ca18b* - [Versión Desarrollada Odoo 14.0](https://bitbucket.org/argilconsulting/odoo-mexico-localization/src/15.0/)
