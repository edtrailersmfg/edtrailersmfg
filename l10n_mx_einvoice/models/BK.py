    def get_account_tax_amounts_detail_from_invoice(self):

        taxes_amounts_by_invoice_traslados = {}
        taxes_amounts_by_invoice_retenciones = {}

        taxes_amounts_traslados_totales = []
        taxes_amounts_retenciones_totales = []

        taxes_amounts_traslados_totales_dict = {}
        taxes_amounts_retenciones_totales_dict = {}

        TotalTrasladosBaseIVA16 = False
        TotalTrasladosImpuestoIVA16 = False
        TotalTrasladosBaseIVA8 = False
        TotalTrasladosImpuestoIVA8 = False
        TotalTrasladosBaseIVA0 = False
        TotalTrasladosImpuestoIVA0 = False
        TotalTrasladosBaseIVAExento = False

        TotalRetencionesIVA = False
        TotalRetencionesISR = False
        TotalRetencionesIEPS = False

        MontoTotalPagos = 0.0

        decimal_presicion = 2


        for payment in self:
            # MontoTotalPagos = payment.amount

            _logger.info("\n####### MontoTotalPagos: %s" % MontoTotalPagos)

            _logger.info("\n####### Moneda: %s" % payment.currency_id.name)

            payment_currency_rate = payment.currency_id.with_context({'date': payment.date}).rate
            payment_currency_rate = payment_currency_rate != 0 and 1.0/payment_currency_rate or 0.0
            if payment_currency_rate == 1.0:
                payment_currency_rate = 1
            else:
                payment_currency_rate = float('%.4f' % payment_currency_rate)
            _logger.info("\n####### TC: %s" % payment_currency_rate)

            if payment.payment_invoice_line_ids:
                for pinvoice in payment.payment_invoice_line_ids:
                    monto_pago = pinvoice.monto_pago
                    
                    monto_pago_payment_currency = 0.0
                    invoice_id = pinvoice.invoice_id
                    invoice_amount_total = invoice_id.amount_total
                    invoice_amount_total_payment_currency = 0.0

                    #### Cambios Agosto 2022 ####
                    invoice_currency_name = invoice_id.currency_id.name
                    payment_currency_name = payment.currency_id.name
                    _logger.info("\n########### Moneda de la Factura: %s" % invoice_currency_name)
                    _logger.info("\n########### Moneda del Pago: %s" % payment_currency_name)

                    ##### ### ### ### ### ### ###

                    x_date = fields.Date.context_today(self)
                    if payment.currency_id==payment.company_id.currency_id or payment.currency_id == invoice_id.currency_id:
                        x_date = payment.date
                    elif payment.currency_id != invoice_id.currency_id:
                        x_date = invoice_id.invoice_date

                    if MontoTotalPagos <= 0.0:
                        if payment.currency_id == payment.company_id.currency_id:
                            MontoTotalPagos = payment.amount
                        else:
                            # monto_total_pago_mxn = round(payment.currency_id._convert(round(float("%.2f" % payment.amount), 2), payment.company_id.currency_id, payment.company_id, x_date), 2)
                            monto_total_pago_mxn = payment.amount * payment_currency_rate
                            MontoTotalPagos = monto_total_pago_mxn

                    #revisa la cantidad que se va a pagar en el docuemnto
                    equivalencia_dr  = round(pinvoice.invoice_currency_rate,6)
                    if invoice_id.currency_id == invoice_id.company_id.currency_id:
                        if  payment.currency_id != payment.company_id.currency_id:
                            ############# Factura en Pesos Pago en Moneda Extranjera")
                            equivalencia_dr = payment.currency_id._convert(1, payment.company_id.currency_id, payment.company_id, x_date)
                            invoice_currency_name = invoice_id.currency_id.name
                            payment_currency_name = payment.currency_id.name
                            ######## equivalencia_dr 02: ", equivalencia_dr)
                            pinvoice.equivalencia_dr = equivalencia_dr

                    if payment.currency_id.id != invoice_id.currency_id.id:
                        if payment.currency_id.name == 'MXN':
                            _logger.info("\n########## Factura Moneda E. Pago en Pesos >>>> ")
                            invoice_amount_total_payment_currency = invoice_id.amount_total / equivalencia_dr
                            monto_pago_payment_currency = monto_pago / equivalencia_dr
                        else:
                            _logger.info("\n########## Factura Moneda E. Pago en Moneda E. >>>> ")
                            invoice_amount_total_payment_currency = invoice_id.amount_total / equivalencia_dr
                            monto_pago_payment_currency = monto_pago / equivalencia_dr
                    else:
                        equivalencia_dr = 1
                        invoice_amount_total_payment_currency = invoice_id.amount_total
                        monto_pago_payment_currency = monto_pago

                    if equivalencia_dr == 1:
                       decimal_presicion = 2
                    else:
                        if invoice_currency_name == 'MXN' and payment_currency_name == 'USD':
                            decimal_presicion = 2
                        else:
                            decimal_presicion = 6

                    paid_percentage = monto_pago_payment_currency / invoice_amount_total_payment_currency

                    _logger.info("\n######## decimal_presicion : %s " % decimal_presicion)
                    _logger.info("\n######## monto_pago : %s " % monto_pago)
                    _logger.info("\n######## invoice_id : %s " % invoice_id)
                    _logger.info("\n######## invoice_amount_total : %s " % invoice_amount_total)
                    _logger.info("\n######## invoice_amount_total_payment_currency : %s " % invoice_amount_total_payment_currency)
                    _logger.info("\n######## paid_percentage : %s " % paid_percentage)
                    _logger.info("\n######## monto_pago_payment_currency : %s " % monto_pago_payment_currency)

                    taxes, iva_exento = invoice_id._get_global_taxes(decimal_presicion)
                    total_impuestos = taxes.get('total_impuestos', 0.0)
                    total_retenciones = taxes.get('total_retenciones', 0.0)
                    _logger.info("\n##### total_impuestos: %s " % total_impuestos)
                    _logger.info("\n##### total_retenciones: %s " % total_retenciones)
                    _logger.info("\n##### iva_exento: %s " % iva_exento)

                    sat_code_tax = 'IVA'

                    ######## Traslados ########
                    list_taxes_invoice_details_traslados = []

                    ######## Retenciones ########
                    list_taxes_invoice_details_retenciones = []


                    ################### BORARRRRRRRRR ####################################
                    # print("####### TC -- invoice_currency_rate: %s" % pinvoice.invoice_currency_rate)
                    # print("####### TC -- payment_currency_rate: %s" % payment_currency_rate)
                    # print("######## decimal_presicion : %s " % decimal_presicion)
                    # print("######## monto_pago : %s " % monto_pago)
                    # print("######## invoice_id : %s " % invoice_id)
                    # print("######## invoice_amount_total : %s " % invoice_amount_total)
                    # print("######## invoice_amount_total_payment_currency : %s " % invoice_amount_total_payment_currency)
                    # print("######## paid_percentage : %s " % paid_percentage)
                    # print("######## monto_pago_payment_currency : %s " % monto_pago_payment_currency)
                    # print("##### total_impuestos: %s " % total_impuestos)
                    # print("##### total_retenciones: %s " % total_retenciones)
                    # print("##### iva_exento: %s " % iva_exento)

                    # print("##### taxes: %s " % taxes)
                    # print("############################ ============================== ############################" )
                    ################### FIN BORARRRRRRRRR ####################################

                    # _logger.info("\n##### Impuestos Agrupados para la Facturación: %s " % taxes)
                    if total_impuestos or total_retenciones:                    
                        if 'total_impuestos' in taxes:
                            TotalImpuestosTrasladados = taxes['total_impuestos']

                            for tax_line in taxes['impuestos']:
                                BaseDR=abs(float(tax_line['amount_base']))
                                ImpuestoDR=tax_line['sat_code_tax'] 
                                TipoFactorDR=tax_line['type']
                                TasaOCuotaDR=abs(tax_line['rate'])
                                ImporteDR=abs(float(tax_line['tax_amount']))

                                ############ Factura en USD Dolares
                                #----------- Pago en MXN ( BIEN )
                                #----------- Pago en USD ( BIEN )
                                ############ Factura en MXN Pesos
                                #----------- Pago en MXN ( BIEN )

                                ##### Factura en USD y Pago en USD y MXN #####
                                if invoice_currency_name == 'USD':
                                    _logger.info("\n########### Factura en USD >>>> ")
                                    if payment_currency_name == 'MXN':
                                        _logger.info("\n########### Pago en MXN >>>> ")
                                    elif payment_currency_name == 'USD':
                                        _logger.info("\n########### Pago en USD >>>> ")
                                    else:
                                        _logger.info("\n########### Pago en Moneda no contemplada >>>> ")
                                elif invoice_currency_name == 'MXN':
                                    _logger.info("\n########### Factura en MXN >>>> ")
                                    if payment_currency_name == 'MXN':
                                        _logger.info("\n########### Pago en MXN >>>> ")
                                    elif payment_currency_name == 'USD':
                                        _logger.info("\n########### Pago en USD >>>> ")
                                    else:
                                        _logger.info("\n########### Pago en Moneda no contemplada >>>> ")
                                #### Truncamos #####                              

                                ############## BASE DR ################
                                #######################################

                                BaseDRT = float(self.truncate(BaseDR, decimal_presicion))
                                BaseDRAmount = BaseDRT * paid_percentage
                                BaseDRAmountT = float(self.truncate(BaseDRAmount, decimal_presicion))
                                if invoice_currency_name == 'USD' and payment_currency_name == 'MXN':
                                    ### FACTURA USD y PAGO en MXN >>>>>>>>>>>
                                    base_dr = BaseDRAmountT / equivalencia_dr
                                else:
                                    if invoice_currency_name == 'MXN' and payment_currency_name == 'USD':
                                        ### FACTURA MXN y PAGO en USD >>>>>>>>>>>
                                        base_dr = BaseDRAmountT / equivalencia_dr
                                    else:
                                        base_dr = invoice_id.currency_id._convert(BaseDRAmountT, payment.currency_id, payment.company_id, x_date)
                                # Truncamos
                                base_dr = float(self.truncate(base_dr, decimal_presicion))

                                base_dr_mxn = 0.0
                                if payment.currency_id == payment.company_id.currency_id:
                                    base_dr_mxn = base_dr
                                else:
                                    if invoice_currency_name == 'MXN' and payment_currency_name == 'USD':
                                        base_dr_mxn = base_dr
                                    else:
                                        base_dr_mxn = base_dr * payment_currency_rate

                                base_dr_mxn = float(self.truncate(base_dr_mxn, decimal_presicion))

                                sat_code_tax = tax_line['sat_code_tax']

                                ############## IMPORTE DR ################
                                ##########################################

                                # Eliminamos el Redondeo ##
                                ### Convertimos el Monto Pago a Monto Factura
                                ImporteDRT = float(self.truncate(ImporteDR, decimal_presicion))
                                ImporteDRAmount = ImporteDRT * paid_percentage
                                ImporteDRAmountT = float(self.truncate(ImporteDRAmount, decimal_presicion))
                                importe_dr = invoice_id.currency_id._convert(ImporteDRAmountT, payment.currency_id, payment.company_id, x_date)
                                # Truncamos
                                importe_dr = float(self.truncate(importe_dr, decimal_presicion))

                                ImporteDRManualCompute = BaseDRAmountT * float(TasaOCuotaDR)
                                ImporteDRManualCompute = float(self.truncate(ImporteDRManualCompute, decimal_presicion))

                                importe_dr_mxn = 0.0

                                
                                if payment.currency_id == payment.company_id.currency_id:
                                    if invoice_currency_name == 'USD' and payment_currency_name == 'MXN':
                                        ### FACTURA USD y PAGO en MXN >>>>>>>>>>>
                                        importe_dr_mxn = ImporteDRManualCompute / equivalencia_dr
                                    else:
                                        importe_dr_mxn = invoice_id.currency_id._convert(ImporteDRManualCompute, payment.currency_id, payment.company_id, x_date)
                                else:
                                    if invoice_currency_name == 'MXN' and payment_currency_name == 'USD':
                                        importe_dr_mxn = ImporteDRManualCompute / equivalencia_dr
                                    else:
                                        importe_dr_mxn = ImporteDRManualCompute * payment_currency_rate

                                    

                                importe_dr_mxn = float(self.truncate(importe_dr_mxn, decimal_presicion))

                                base_dr_to_sum = base_dr_mxn
                                importe_dr_to_sum = importe_dr_mxn
                                if payment.currency_id != payment.company_id.currency_id:
                                    if invoice_id.currency_id != payment.currency_id:
                                        base_dr_to_sum = BaseDRAmountT
                                        importe_dr_to_sum = ImporteDRManualCompute

                                if TipoFactorDR == 'Exento':
                                    TotalTrasladosBaseIVAExento = TotalTrasladosBaseIVAExento + base_dr_to_sum
                                else:
                                    if invoice_currency_name == 'MXN' and payment_currency_name == 'USD':
                                        if '%0.*f' % (2, TasaOCuotaDR) == '0.16':
                                            # IVA 16
                                            TotalTrasladosBaseIVA16 = TotalTrasladosBaseIVA16 + (base_dr_mxn * equivalencia_dr)
                                            TotalTrasladosImpuestoIVA16 = TotalTrasladosImpuestoIVA16 + (importe_dr_mxn * equivalencia_dr)
                                        elif '%0.*f' % (2, TasaOCuotaDR) == '0.08':
                                            # IVA 8
                                            TotalTrasladosBaseIVA8 = TotalTrasladosBaseIVA8 + (base_dr_mxn * equivalencia_dr)
                                            TotalTrasladosImpuestoIVA8 = TotalTrasladosImpuestoIVA8 + (importe_dr_mxn * equivalencia_dr)
                                        elif '%0.*f' % (2, TasaOCuotaDR) == '0.00':
                                            # IVA 0
                                            TotalTrasladosBaseIVA0 = TotalTrasladosBaseIVA0 + (base_dr_mxn * equivalencia_dr)
                                            TotalTrasladosImpuestoIVA0 = TotalTrasladosImpuestoIVA0 + (importe_dr_mxn * equivalencia_dr)

                                    else:
                                        if '%0.*f' % (2, TasaOCuotaDR) == '0.16':
                                            # IVA 16
                                            TotalTrasladosBaseIVA16 = TotalTrasladosBaseIVA16 + base_dr_to_sum
                                            TotalTrasladosImpuestoIVA16 = TotalTrasladosImpuestoIVA16 + importe_dr_to_sum
                                        elif '%0.*f' % (2, TasaOCuotaDR) == '0.08':
                                            # IVA 8
                                            TotalTrasladosBaseIVA8 = TotalTrasladosBaseIVA8 + base_dr_to_sum
                                            TotalTrasladosImpuestoIVA8 = TotalTrasladosImpuestoIVA8 + importe_dr_to_sum
                                        elif '%0.*f' % (2, TasaOCuotaDR) == '0.00':
                                            # IVA 0
                                            TotalTrasladosBaseIVA0 = TotalTrasladosBaseIVA0 + base_dr_to_sum
                                            TotalTrasladosImpuestoIVA0 = TotalTrasladosImpuestoIVA0 + importe_dr_to_sum

                                if invoice_currency_name == 'MXN' and payment_currency_name == 'USD':
                                    BaseDRAmountT =  base_dr_mxn * equivalencia_dr
                                    BaseDRAmountT = float(self.truncate(BaseDRAmountT, decimal_presicion))

                                    ImporteDRManualCompute = importe_dr_mxn * equivalencia_dr
                                    ImporteDRManualCompute = float(self.truncate(ImporteDRManualCompute, decimal_presicion))

                                    tax_invoice_vals_traslados = {
                                                                    'BaseDR': BaseDRAmountT,
                                                                    'ImpuestoDR': ImpuestoDR,
                                                                    'TipoFactorDR': TipoFactorDR,
                                                                    'TasaOcuotaDR': '%0.*f' % (6, TasaOCuotaDR),
                                                                    'ImporteDR': ImporteDRManualCompute,
                                                                 }
                                else:
                                    tax_invoice_vals_traslados = {
                                                                    'BaseDR': '%0.*f' % (decimal_presicion, BaseDRAmountT),
                                                                    'ImpuestoDR': ImpuestoDR,
                                                                    'TipoFactorDR': TipoFactorDR,
                                                                    'TasaOcuotaDR': '%0.*f' % (6, TasaOCuotaDR),
                                                                    'ImporteDR': ImporteDRManualCompute,
                                                                 }

                                tax_invoice_vals_traslados_totals = tax_invoice_vals_traslados.copy()

                                if invoice_id.currency_id == payment.currency_id:
                                    tax_invoice_vals_traslados_totals.update({
                                                                                    'BaseDR': float('%0.*f' % (decimal_presicion, BaseDRAmountT)),
                                                                                    'ImporteDR': ImporteDRManualCompute,
                                                                                })
                                else:
                                    if invoice_currency_name == 'MXN' and payment_currency_name == 'USD':
                                        # base_dr_mxn = base_dr_mxn / equivalencia_dr
                                        # base_dr_mxn = float(self.truncate(base_dr_mxn, decimal_presicion))

                                        # importe_dr_mxn = importe_dr_mxn / equivalencia_dr
                                        # importe_dr_mxn = float(self.truncate(importe_dr_mxn, decimal_presicion))

                                        tax_invoice_vals_traslados_totals.update({
                                                                                        'BaseDR': base_dr_mxn,
                                                                                        'ImporteDR': importe_dr_mxn,
                                                                                    })
                                    else:
                                        tax_invoice_vals_traslados_totals.update({
                                                                                        'BaseDR': base_dr_mxn,
                                                                                        'ImporteDR': importe_dr_mxn,
                                                                                    })

                                list_taxes_invoice_details_traslados.append(tax_invoice_vals_traslados)
                                taxes_amounts_by_invoice_traslados.update({
                                                                invoice_id: list_taxes_invoice_details_traslados,
                                                            })


                                total_imp_trasl_name = ImpuestoDR + '-' + TipoFactorDR + '-' + '%0.*f' % (2, TasaOCuotaDR)
                                if total_imp_trasl_name in taxes_amounts_traslados_totales_dict:
                                    BaseDR_prev = taxes_amounts_traslados_totales_dict[total_imp_trasl_name]['BaseDR']
                                    ImporteDR_prev = taxes_amounts_traslados_totales_dict[total_imp_trasl_name]['ImporteDR']

                                    BaseDR_new = float(BaseDR_prev) + base_dr
                                    ImporteDR_new = float(ImporteDR_prev) + importe_dr
                                    taxes_amounts_traslados_totales_dict[total_imp_trasl_name]['BaseDR'] = '%0.*f' % (2, BaseDR_new)
                                    taxes_amounts_traslados_totales_dict[total_imp_trasl_name]['ImporteDR'] = '%0.*f' % (decimal_presicion, ImporteDR_new)
                                else:
                                    taxes_amounts_traslados_totales_dict.update({
                                                                                   total_imp_trasl_name : tax_invoice_vals_traslados_totals,
                                                                                })

                            # raise UserError("AQUI")
                        if 'total_retenciones' in taxes:
                            if 'total_retenciones' in taxes and taxes['total_retenciones'] > 0.0:

                                TotalImpuestosRetenidos = taxes['total_retenciones']
                                for tax_line in taxes['retenciones']:
                                    BaseDR=abs(float(tax_line['amount_base']))
                                    ImpuestoDR=tax_line['sat_code_tax'] 
                                    TipoFactorDR=tax_line['type']
                                    TasaOCuotaDR=abs(tax_line['rate'])
                                    ImporteDR=abs(float(tax_line['tax_amount']))

                                    ############ Factura en USD Dolares
                                    #----------- Pago en MXN ( BIEN )
                                    #----------- Pago en USD ( BIEN )
                                    ############ Factura en MXN Pesos
                                    #----------- Pago en MXN ( BIEN )

                                    ##### Factura en USD y Pago en USD y MXN #####
                                    if invoice_currency_name == 'USD':
                                        _logger.info("\n########### Factura en USD >>>> ")
                                        if payment_currency_name == 'MXN':
                                            _logger.info("\n########### Pago en MXN >>>> ")
                                        elif payment_currency_name == 'USD':
                                            _logger.info("\n########### Pago en USD >>>> ")
                                        else:
                                            _logger.info("\n########### Pago en Moneda no contemplada >>>> ")
                                    elif invoice_currency_name == 'MXN':
                                        _logger.info("\n########### Factura en MXN >>>> ")
                                        if payment_currency_name == 'MXN':
                                            _logger.info("\n########### Pago en MXN >>>> ")
                                        elif payment_currency_name == 'USD':
                                            _logger.info("\n########### Pago en USD >>>> ")
                                        else:
                                            _logger.info("\n########### Pago en Moneda no contemplada >>>> ")
                                    #### Truncamos #####                              

                                    ############## BASE DR ################
                                    #######################################

                                    BaseDRT = float(self.truncate(BaseDR, decimal_presicion))
                                    BaseDRAmount = BaseDRT * paid_percentage
                                    BaseDRAmountT = float(self.truncate(BaseDRAmount, decimal_presicion))
                                    if invoice_currency_name == 'USD' and payment_currency_name == 'MXN':
                                        ### FACTURA USD y PAGO en MXN >>>>>>>>>>>
                                        base_dr = BaseDRAmountT / equivalencia_dr
                                    else:
                                        if invoice_currency_name == 'MXN' and payment_currency_name == 'USD':
                                            ### FACTURA MXN y PAGO en USD >>>>>>>>>>>
                                            base_dr = BaseDRAmountT / equivalencia_dr
                                        else:
                                            base_dr = invoice_id.currency_id._convert(BaseDRAmountT, payment.currency_id, payment.company_id, x_date)
                                    # Truncamos
                                    base_dr = float(self.truncate(base_dr, decimal_presicion))

                                    base_dr_mxn = 0.0
                                    if payment.currency_id == payment.company_id.currency_id:
                                        base_dr_mxn = base_dr
                                    else:
                                        if invoice_currency_name == 'MXN' and payment_currency_name == 'USD':
                                            base_dr_mxn = base_dr
                                        else:
                                            base_dr_mxn = base_dr * payment_currency_rate

                                    base_dr_mxn = float(self.truncate(base_dr_mxn, decimal_presicion))

                                    sat_code_tax = tax_line['sat_code_tax']

                                    ############## IMPORTE DR ################
                                    ##########################################

                                    # Eliminamos el Redondeo ##
                                    ### Convertimos el Monto Pago a Monto Factura
                                    ImporteDRT = float(self.truncate(ImporteDR, decimal_presicion))
                                    ImporteDRAmount = ImporteDRT * paid_percentage
                                    ImporteDRAmountT = float(self.truncate(ImporteDRAmount, decimal_presicion))
                                    importe_dr = invoice_id.currency_id._convert(ImporteDRAmountT, payment.currency_id, payment.company_id, x_date)
                                    # Truncamos
                                    importe_dr = float(self.truncate(importe_dr, decimal_presicion))

                                    ImporteDRManualCompute = BaseDRAmountT * float(TasaOCuotaDR)
                                    ImporteDRManualCompute = float(self.truncate(ImporteDRManualCompute, decimal_presicion))

                                    importe_dr_mxn = 0.0

                                    
                                    if payment.currency_id == payment.company_id.currency_id:
                                        if invoice_currency_name == 'USD' and payment_currency_name == 'MXN':
                                            ### FACTURA USD y PAGO en MXN >>>>>>>>>>>
                                            importe_dr_mxn = ImporteDRManualCompute / equivalencia_dr
                                        else:
                                            importe_dr_mxn = invoice_id.currency_id._convert(ImporteDRManualCompute, payment.currency_id, payment.company_id, x_date)
                                    else:
                                        if invoice_currency_name == 'MXN' and payment_currency_name == 'USD':
                                            importe_dr_mxn = ImporteDRManualCompute / equivalencia_dr
                                        else:
                                            importe_dr_mxn = ImporteDRManualCompute * payment_currency_rate

                                        

                                    importe_dr_mxn = float(self.truncate(importe_dr_mxn, decimal_presicion))

                                    base_dr_to_sum = base_dr_mxn
                                    importe_dr_to_sum = importe_dr_mxn
                                    if payment.currency_id != payment.company_id.currency_id:
                                        if invoice_id.currency_id != payment.currency_id:
                                            base_dr_to_sum = BaseDRAmountT
                                            importe_dr_to_sum = ImporteDRManualCompute

                                    sat_code_tax = tax_line['sat_code_tax']

                                    if invoice_currency_name == 'MXN' and payment_currency_name == 'USD':
                                        if sat_code_tax == 'IVA' or sat_code_tax == '002':
                                            # IVA 16
                                            TotalRetencionesIVA = TotalRetencionesIVA + (importe_dr_mxn * equivalencia_dr)
                                        elif sat_code_tax == 'ISR' or sat_code_tax == '001':
                                            # IVA 8
                                            TotalRetencionesISR = TotalRetencionesISR + (importe_dr_mxn * equivalencia_dr)
                                        elif sat_code_tax == 'IEPS' or sat_code_tax == '003':
                                            # IVA 0
                                            TotalRetencionesIEPS = TotalRetencionesIEPS + (importe_dr_mxn * equivalencia_dr)
                                    else:
                                        if sat_code_tax == 'IVA' or sat_code_tax == '002':
                                            # IVA 16
                                            TotalRetencionesIVA = TotalRetencionesIVA + importe_dr_to_sum
                                        elif sat_code_tax == 'ISR' or sat_code_tax == '001':
                                            # IVA 8
                                            TotalRetencionesISR = TotalRetencionesISR + importe_dr_to_sum
                                        elif sat_code_tax == 'IEPS' or sat_code_tax == '003':
                                            # IVA 0
                                            TotalRetencionesIEPS = TotalRetencionesIEPS + importe_dr_to_sum

                                    if invoice_currency_name == 'MXN' and payment_currency_name == 'USD':
                                        BaseDRAmountT =  base_dr_mxn * equivalencia_dr
                                        BaseDRAmountT = float(self.truncate(BaseDRAmountT, decimal_presicion))

                                        ImporteDRManualCompute = importe_dr_mxn * equivalencia_dr
                                        ImporteDRManualCompute = float(self.truncate(ImporteDRManualCompute, decimal_presicion))

                                        tax_invoice_vals_retenciones = {
                                                                        'BaseDR': BaseDRAmountT,
                                                                        'ImpuestoDR': ImpuestoDR,
                                                                        'TipoFactorDR': TipoFactorDR,
                                                                        'TasaOcuotaDR': '%0.*f' % (6, TasaOCuotaDR),
                                                                        'ImporteDR': ImporteDRManualCompute,
                                                                     }
                                    else:
                                        tax_invoice_vals_retenciones = {
                                                                        'BaseDR': '%0.*f' % (decimal_presicion, BaseDRAmountT),
                                                                        'ImpuestoDR': ImpuestoDR,
                                                                        'TipoFactorDR': TipoFactorDR,
                                                                        'TasaOcuotaDR': '%0.*f' % (6, TasaOCuotaDR),
                                                                        'ImporteDR': ImporteDRManualCompute,
                                                                     }

                                    tax_invoice_vals_retenciones_totals = tax_invoice_vals_retenciones.copy()

                                    if invoice_id.currency_id == payment.currency_id:
                                        tax_invoice_vals_retenciones_totals.update({
                                                                                        'BaseDR': float('%0.*f' % (decimal_presicion, BaseDRAmountT)),
                                                                                        'ImporteDR': ImporteDRManualCompute,
                                                                                    })
                                    else:
                                        if invoice_currency_name == 'MXN' and payment_currency_name == 'USD':
                                            # base_dr_mxn = base_dr_mxn / equivalencia_dr
                                            # base_dr_mxn = float(self.truncate(base_dr_mxn, decimal_presicion))

                                            # importe_dr_mxn = importe_dr_mxn / equivalencia_dr
                                            # importe_dr_mxn = float(self.truncate(importe_dr_mxn, decimal_presicion))

                                            tax_invoice_vals_retenciones_totals.update({
                                                                                            'BaseDR': base_dr_mxn,
                                                                                            'ImporteDR': importe_dr_mxn,
                                                                                        })
                                        else:
                                            tax_invoice_vals_retenciones_totals.update({
                                                                                            'BaseDR': base_dr_mxn,
                                                                                            'ImporteDR': importe_dr_mxn,
                                                                                        })

                                    list_taxes_invoice_details_retenciones.append(tax_invoice_vals_retenciones)
                                    taxes_amounts_by_invoice_retenciones.update({
                                                                    invoice_id: list_taxes_invoice_details_retenciones,
                                                                })

                                    total_imp_ret_name = ImpuestoDR + '-' + TipoFactorDR + '-' + '%0.*f' % (2, TasaOCuotaDR)
                                    if total_imp_ret_name in taxes_amounts_retenciones_totales_dict:
                                        BaseDR_prev = taxes_amounts_retenciones_totales_dict[total_imp_ret_name]['BaseDR']
                                        ImporteDR_prev = taxes_amounts_retenciones_totales_dict[total_imp_ret_name]['ImporteDR']

                                        BaseDR_new = float(BaseDR_prev) + base_dr
                                        ImporteDR_new = float(ImporteDR_prev) + importe_dr
                                        taxes_amounts_retenciones_totales_dict[total_imp_ret_name]['BaseDR'] = '%0.*f' % (2, BaseDR_new)
                                        taxes_amounts_retenciones_totales_dict[total_imp_ret_name]['ImporteDR'] = '%0.*f' % (decimal_presicion, ImporteDR_new)
                                    else:
                                        taxes_amounts_retenciones_totales_dict.update({
                                                                                       total_imp_ret_name : tax_invoice_vals_retenciones_totals,
                                                                                    })

                    #### IVA EXENTO ####
                    else:
                        if iva_exento:
                            if 'total_impuestos' in taxes:
                                TotalImpuestosTrasladados = taxes['total_impuestos']
                                
                                for tax_line in taxes['impuestos']:
                                    BaseDR=abs(float(tax_line['amount_base']))
                                    ImpuestoDR=tax_line['sat_code_tax'] 
                                    TipoFactorDR=tax_line['type']
                                    TasaOCuotaDR=abs(tax_line['rate'])
                                    ImporteDR=abs(float(tax_line['tax_amount']))

                                    ############ Factura en USD Dolares
                                    #----------- Pago en MXN ( BIEN )
                                    #----------- Pago en USD ( BIEN )
                                    ############ Factura en MXN Pesos
                                    #----------- Pago en MXN ( BIEN )

                                    ##### Factura en USD y Pago en USD y MXN #####
                                    if invoice_currency_name == 'USD':
                                        _logger.info("\n########### Factura en USD >>>> ")
                                        if payment_currency_name == 'MXN':
                                            _logger.info("\n########### Pago en MXN >>>> ")
                                        elif payment_currency_name == 'USD':
                                            _logger.info("\n########### Pago en USD >>>> ")
                                        else:
                                            _logger.info("\n########### Pago en Moneda no contemplada >>>> ")
                                    elif invoice_currency_name == 'MXN':
                                        _logger.info("\n########### Factura en MXN >>>> ")
                                        if payment_currency_name == 'MXN':
                                            _logger.info("\n########### Pago en MXN >>>> ")
                                        elif payment_currency_name == 'USD':
                                            _logger.info("\n########### Pago en USD >>>> ")
                                        else:
                                            _logger.info("\n########### Pago en Moneda no contemplada >>>> ")
                                    #### Truncamos #####                              

                                    ############## BASE DR ################
                                    #######################################

                                    BaseDRT = float(self.truncate(BaseDR, decimal_presicion))
                                    BaseDRAmount = BaseDRT * paid_percentage
                                    BaseDRAmountT = float(self.truncate(BaseDRAmount, decimal_presicion))
                                    if invoice_currency_name == 'USD' and payment_currency_name == 'MXN':
                                        ### FACTURA USD y PAGO en MXN >>>>>>>>>>>
                                        base_dr = BaseDRAmountT / equivalencia_dr
                                    else:
                                        if invoice_currency_name == 'MXN' and payment_currency_name == 'USD':
                                            ### FACTURA MXN y PAGO en USD >>>>>>>>>>>
                                            base_dr = BaseDRAmountT / equivalencia_dr
                                        else:
                                            base_dr = invoice_id.currency_id._convert(BaseDRAmountT, payment.currency_id, payment.company_id, x_date)
                                    # Truncamos
                                    base_dr = float(self.truncate(base_dr, decimal_presicion))

                                    base_dr_mxn = 0.0
                                    if payment.currency_id == payment.company_id.currency_id:
                                        base_dr_mxn = base_dr
                                    else:
                                        if invoice_currency_name == 'MXN' and payment_currency_name == 'USD':
                                            base_dr_mxn = base_dr
                                        else:
                                            base_dr_mxn = base_dr * payment_currency_rate

                                    base_dr_mxn = float(self.truncate(base_dr_mxn, decimal_presicion))

                                    sat_code_tax = tax_line['sat_code_tax']

                                    ############## IMPORTE DR ################
                                    ##########################################

                                    # Eliminamos el Redondeo ##
                                    ### Convertimos el Monto Pago a Monto Factura
                                    ImporteDRT = float(self.truncate(ImporteDR, decimal_presicion))
                                    ImporteDRAmount = ImporteDRT * paid_percentage
                                    ImporteDRAmountT = float(self.truncate(ImporteDRAmount, decimal_presicion))
                                    importe_dr = invoice_id.currency_id._convert(ImporteDRAmountT, payment.currency_id, payment.company_id, x_date)
                                    # Truncamos
                                    importe_dr = float(self.truncate(importe_dr, decimal_presicion))

                                    ImporteDRManualCompute = BaseDRAmountT * float(TasaOCuotaDR)
                                    ImporteDRManualCompute = float(self.truncate(ImporteDRManualCompute, decimal_presicion))

                                    importe_dr_mxn = 0.0

                                    if payment.currency_id == payment.company_id.currency_id:
                                        if invoice_currency_name == 'USD' and payment_currency_name == 'MXN':
                                            ### FACTURA USD y PAGO en MXN >>>>>>>>>>>
                                            importe_dr_mxn = ImporteDRManualCompute / equivalencia_dr
                                        else:
                                            importe_dr_mxn = invoice_id.currency_id._convert(ImporteDRManualCompute, payment.currency_id, payment.company_id, x_date)
                                    else:
                                        if invoice_currency_name == 'MXN' and payment_currency_name == 'USD':
                                            importe_dr_mxn = ImporteDRManualCompute / equivalencia_dr
                                        else:
                                            importe_dr_mxn = ImporteDRManualCompute * payment_currency_rate

                                        

                                    importe_dr_mxn = float(self.truncate(importe_dr_mxn, decimal_presicion))

                                    base_dr_to_sum = base_dr_mxn
                                    importe_dr_to_sum = importe_dr_mxn
                                    if payment.currency_id != payment.company_id.currency_id:
                                        if invoice_id.currency_id != payment.currency_id:
                                            base_dr_to_sum = BaseDRAmountT
                                            importe_dr_to_sum = ImporteDRManualCompute

                                    if TipoFactorDR == 'Exento':
                                        TotalTrasladosBaseIVAExento = TotalTrasladosBaseIVAExento + base_dr_to_sum
                                    else:
                                        if invoice_currency_name == 'MXN' and payment_currency_name == 'USD':
                                            if TipoFactorDR == 'Exento':
                                                TotalTrasladosBaseIVAExento = TotalTrasladosBaseIVAExento + (base_dr_mxn * equivalencia_dr)
                                            else:
                                                if '%0.*f' % (2, TasaOCuotaDR) == '0.16':
                                                    # IVA 16
                                                    TotalTrasladosBaseIVA16 = TotalTrasladosBaseIVA16 + (base_dr_mxn * equivalencia_dr)
                                                    TotalTrasladosImpuestoIVA16 = TotalTrasladosImpuestoIVA16 + (importe_dr_mxn * equivalencia_dr)
                                                elif '%0.*f' % (2, TasaOCuotaDR) == '0.08':
                                                    # IVA 8
                                                    TotalTrasladosBaseIVA8 = TotalTrasladosBaseIVA8 + (base_dr_mxn * equivalencia_dr)
                                                    TotalTrasladosImpuestoIVA8 = TotalTrasladosImpuestoIVA8 + (importe_dr_mxn * equivalencia_dr)
                                                elif '%0.*f' % (2, TasaOCuotaDR) == '0.00':
                                                    # IVA 0
                                                    TotalTrasladosBaseIVA0 = TotalTrasladosBaseIVA0 + (base_dr_mxn * equivalencia_dr)
                                                    TotalTrasladosImpuestoIVA0 = TotalTrasladosImpuestoIVA0 + (importe_dr_mxn * equivalencia_dr)
                                        else:
                                            if TipoFactorDR == 'Exento':
                                                TotalTrasladosBaseIVAExento = TotalTrasladosBaseIVAExento + (base_dr_mxn * equivalencia_dr)
                                            else:
                                                if '%0.*f' % (2, TasaOCuotaDR) == '0.16':
                                                    # IVA 16
                                                    TotalTrasladosBaseIVA16 = TotalTrasladosBaseIVA16 + base_dr_to_sum
                                                    TotalTrasladosImpuestoIVA16 = TotalTrasladosImpuestoIVA16 + importe_dr_to_sum
                                                elif '%0.*f' % (2, TasaOCuotaDR) == '0.08':
                                                    # IVA 8
                                                    TotalTrasladosBaseIVA8 = TotalTrasladosBaseIVA8 + base_dr_to_sum
                                                    TotalTrasladosImpuestoIVA8 = TotalTrasladosImpuestoIVA8 + importe_dr_to_sum
                                                elif '%0.*f' % (2, TasaOCuotaDR) == '0.00':
                                                    # IVA 0
                                                    TotalTrasladosBaseIVA0 = TotalTrasladosBaseIVA0 + base_dr_to_sum
                                                    TotalTrasladosImpuestoIVA0 = TotalTrasladosImpuestoIVA0 + importe_dr_to_sum

                                    if invoice_currency_name == 'MXN' and payment_currency_name == 'USD':
                                        BaseDRAmountT =  base_dr_mxn * equivalencia_dr
                                        BaseDRAmountT = float(self.truncate(BaseDRAmountT, decimal_presicion))

                                        ImporteDRManualCompute = importe_dr_mxn * equivalencia_dr
                                        ImporteDRManualCompute = float(self.truncate(ImporteDRManualCompute, decimal_presicion))

                                        tax_invoice_vals_traslados = {
                                                                        'BaseDR': BaseDRAmountT,
                                                                        'ImpuestoDR': ImpuestoDR,
                                                                        'TipoFactorDR': TipoFactorDR,
                                                                        'TasaOcuotaDR': '%0.*f' % (6, TasaOCuotaDR),
                                                                        'ImporteDR': ImporteDRManualCompute,
                                                                     }
                                    else:
                                        tax_invoice_vals_traslados = {
                                                                        'BaseDR': '%0.*f' % (decimal_presicion, BaseDRAmountT),
                                                                        'ImpuestoDR': ImpuestoDR,
                                                                        'TipoFactorDR': TipoFactorDR,
                                                                        'TasaOcuotaDR': '%0.*f' % (6, TasaOCuotaDR),
                                                                        'ImporteDR': ImporteDRManualCompute,
                                                                     }

                                    tax_invoice_vals_traslados_totals = tax_invoice_vals_traslados.copy()

                                    if invoice_id.currency_id == payment.currency_id:
                                        tax_invoice_vals_traslados_totals.update({
                                                                                        'BaseDR': float('%0.*f' % (decimal_presicion, BaseDRAmountT)),
                                                                                        'ImporteDR': ImporteDRManualCompute,
                                                                                    })
                                    else:
                                        if invoice_currency_name == 'MXN' and payment_currency_name == 'USD':
                                            # base_dr_mxn = base_dr_mxn / equivalencia_dr
                                            # base_dr_mxn = float(self.truncate(base_dr_mxn, decimal_presicion))

                                            # importe_dr_mxn = importe_dr_mxn / equivalencia_dr
                                            # importe_dr_mxn = float(self.truncate(importe_dr_mxn, decimal_presicion))

                                            tax_invoice_vals_traslados_totals.update({
                                                                                            'BaseDR': base_dr_mxn,
                                                                                            'ImporteDR': importe_dr_mxn,
                                                                                        })
                                        else:
                                            tax_invoice_vals_traslados_totals.update({
                                                                                            'BaseDR': base_dr_mxn,
                                                                                            'ImporteDR': importe_dr_mxn,
                                                                                        })

                                    list_taxes_invoice_details_traslados.append(tax_invoice_vals_traslados)
                                    taxes_amounts_by_invoice_traslados.update({
                                                                    invoice_id: list_taxes_invoice_details_traslados,
                                                                })

                                    total_imp_trasl_name = ImpuestoDR + '-' + TipoFactorDR + '-' + '%0.*f' % (2, TasaOCuotaDR)
                                    if total_imp_trasl_name in taxes_amounts_traslados_totales_dict:
                                        BaseDR_prev = taxes_amounts_traslados_totales_dict[total_imp_trasl_name]['BaseDR']
                                        ImporteDR_prev = taxes_amounts_traslados_totales_dict[total_imp_trasl_name]['ImporteDR']

                                        BaseDR_new = float(BaseDR_prev) + base_dr
                                        ImporteDR_new = float(ImporteDR_prev) + importe_dr
                                        taxes_amounts_traslados_totales_dict[total_imp_trasl_name]['BaseDR'] = '%0.*f' % (2, BaseDR_new)
                                        taxes_amounts_traslados_totales_dict[total_imp_trasl_name]['ImporteDR'] = '%0.*f' % (decimal_presicion, ImporteDR_new)
                                    else:
                                        taxes_amounts_traslados_totales_dict.update({
                                                                                       total_imp_trasl_name : tax_invoice_vals_traslados_totals,
                                                                                    })


        if taxes_amounts_traslados_totales_dict:
            for taxt in taxes_amounts_traslados_totales_dict.keys():
                taxvals = taxes_amounts_traslados_totales_dict[taxt]
                taxes_amounts_traslados_totales.append(taxvals)
        if taxes_amounts_retenciones_totales_dict:
            for taxr in taxes_amounts_retenciones_totales_dict.keys():
                taxvals = taxes_amounts_retenciones_totales_dict[taxr]
                taxes_amounts_retenciones_totales.append(taxvals)

        ###### Los totales los convertimos a moneda nacional ######## 

        #### Cambios Agosto 2022 ####
        if self.currency_id.name == 'MXN':
            decimal_presicion = 2
        ##### ### ### ### ### ### ###
        _logger.info("\n############# decimal_presicion: %s " % decimal_presicion)
        tax_amounts_dr = {
                                    'TotalRetencionesIVA' : '%0.*f' % (decimal_presicion, TotalRetencionesIVA) if TotalRetencionesIVA else False,
                                    'TotalRetencionesISR' : '%0.*f' % (decimal_presicion, TotalRetencionesISR) if TotalRetencionesISR else False,
                                    'TotalRetencionesIEPS' : '%0.*f' % (decimal_presicion, TotalRetencionesIEPS) if TotalRetencionesIEPS else False,
                                    'TotalTrasladosBaseIVA16' : '%0.*f' % (decimal_presicion, TotalTrasladosBaseIVA16) if TotalTrasladosBaseIVA16 else False,
                                    'TotalTrasladosImpuestoIVA16' : '%0.*f' % (decimal_presicion, TotalTrasladosImpuestoIVA16) if TotalTrasladosImpuestoIVA16 else False,
                                    'TotalTrasladosBaseIVA8' : '%0.*f' % (decimal_presicion, TotalTrasladosBaseIVA8) if TotalTrasladosBaseIVA8 else False,
                                    'TotalTrasladosImpuestoIVA8' : '%0.*f' % (decimal_presicion, TotalTrasladosImpuestoIVA8) if TotalTrasladosImpuestoIVA8 else False,
                                    'TotalTrasladosBaseIVA0' : '%0.*f' % (decimal_presicion, TotalTrasladosBaseIVA0) if TotalTrasladosBaseIVA0 else False,
                                    'TotalTrasladosImpuestoIVA0' : '%0.*f' % (decimal_presicion, TotalTrasladosImpuestoIVA0) if TotalTrasladosImpuestoIVA0 else False,
                                    'TotalTrasladosBaseIVAExento' : '%0.*f' % (decimal_presicion, TotalTrasladosBaseIVAExento) if TotalTrasladosBaseIVAExento else False,
                                    'TrasladosDR': taxes_amounts_by_invoice_traslados,
                                    'RetencionesDR': taxes_amounts_by_invoice_retenciones,
                                    'TrasladosDRTotales': taxes_amounts_traslados_totales,
                                    'RetencionesDRTotales': taxes_amounts_retenciones_totales,
                                    'MontoTotalPagos': '%0.*f' % (decimal_presicion, MontoTotalPagos),
                              }

        # raise UserError("DEBUG >>>>>")

        return tax_amounts_dr