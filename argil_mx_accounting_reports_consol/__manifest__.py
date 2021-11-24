# -*- encoding: utf-8 -*-

{
    'name': 'Reportes Contables Mexico',
    'version': '1',
    "author" : "Argil Consulting",
    "category" : "Account",
    'description': """
Reportes Contables comunmente usados en Mexico
==============================================

Este modulo esta enfocado cuando se maneja multicompany y permite consolidar cuentas de las sucursales hacia la empresa central

        Diversos informes segun los requerimientos de Mexico, basados en 13 periodos al año 
        (12 meses naturales y Periodo Inicial), 
        donde el periodo 0 es de apertura/cierre.
        Los informes son:
	   - Balanza Mensual de Comprobacion
	   - Auxiliar de cuentas (desde la Balanza de comprobacion)
	   - Auxiliar de cuentas
	   - Configurador de Reportes Personalizados
	   - Generador de Reportes Personalizados

	NOTAS IMPORTANTES:
	- Estos reportes funcionan tomando en cuenta lo siguiente:
		+ Deben usarse 13 periodos por cada periodo Fiscal.
		+ El nombre de los periodos es importante, de manera que deben tener orden alfabetico, por ejemplo:
		
        * 01/2012
		* 02/2012
		* 03/2012
		* 04/2012
		* 05/2012
		* 06/2012
		* 07/2012
		* 08/2012
		* 09/2012
		* 10/2012
		* 11/2012
		* 12/2012
        * 13/2012	=> Marcado como periodo de cierre
		

    """,
    "website" : "http://www.argil.mx",
    "depends" : ["account",
                 "l10n_mx_account_tree",
                 "account_period_and_fiscalyear"],
    "data" : [
        "security/ir.model.access.csv",
        "views/account_mx_reports_view.xml",
        "views/account_mx_general_ledger_view.xml",        
        "report/report_balanza_mensual.xml",
        "report/report_auxiliar_cuentas.xml",
        "report/report_general_ledger.xml",
             ],
    "installable" : True,

}
