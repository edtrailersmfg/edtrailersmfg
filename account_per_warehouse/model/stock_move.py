# -*- coding: utf-8 -*-
###########################################################################

from odoo import models, fields, api, _, release
from odoo.exceptions import UserError
from odoo.tools import float_compare, float_round, float_is_zero
import logging
_logger = logging.getLogger(__name__)

class StockMove(models.Model):
    _inherit = "stock.move"

    
    @api.model
    def _get_valued_types(self):
        res = super(StockMove, self)._get_valued_types()
        res.append('internal_transit')
        res.append('supplier_inventory_production')
        return res
    
    
    
    def _get_internal_transit_move_lines(self):
        res = self.env['stock.move.line']
        for move_line in self.move_line_ids:
            if move_line.owner_id and move_line.owner_id != move_line.company_id.partner_id:
                continue
            if move_line.location_id.usage in ('internal','transit') and move_line.location_dest_id.usage in ('internal','transit'):
                res |= move_line
        return res

    def _is_internal_transit(self):
        self.ensure_one()
        if self._get_internal_transit_move_lines():
            return True
        return False
    
    
    def _create_internal_transit_svl(self, forced_quantity=None):
        svl_vals_list = []
        for move in self:
            # move = move.with_context(force_company=move.company_id.id)
            valued_move_lines = move._get_internal_transit_move_lines()
            valued_quantity = 0
            for valued_move_line in valued_move_lines:
                valued_quantity += valued_move_line.product_uom_id._compute_quantity(valued_move_line.qty_done, move.product_id.uom_id)
            if float_is_zero(forced_quantity or valued_quantity, precision_rounding=move.product_id.uom_id.rounding):
                continue
            svl_vals = move.product_id._prepare_internal_transit_svl_vals(forced_quantity or valued_quantity, move.company_id)
            svl_vals.update(move._prepare_common_svl_vals())
            if forced_quantity:
                svl_vals['description'] = 'Correction of %s (modification of past move)' % move.picking_id.name or move.name
            svl_vals_list.append(svl_vals)
        return self.env['stock.valuation.layer'].sudo().create(svl_vals_list)
    
    
    def _get_supplier_inventory_production_move_lines(self):
        res = self.env['stock.move.line']
        for move_line in self.move_line_ids:
            if move_line.owner_id and move_line.owner_id != move_line.company_id.partner_id:
                continue
            if (move_line.location_id.usage == 'supplier' and move_line.location_dest_id.usage in ('inventory','production')) or \
               (move_line.location_id.usage in ('inventory','production') and move_line.location_dest_id.usage == 'supplier'):
                res |= move_line
        return res

    def _is_supplier_inventory_production(self):
        self.ensure_one()
        if self._get_supplier_inventory_production_move_lines():
            return True
        return False
    
    
    def _create_supplier_inventory_production_svl(self, forced_quantity=None):
        svl_vals_list = []
        for move in self:
            # move = move.with_context(force_company=move.company_id.id)
            valued_move_lines = move._get_supplier_inventory_production_move_lines()
            valued_quantity = 0
            for valued_move_line in valued_move_lines:
                valued_quantity += valued_move_line.product_uom_id._compute_quantity(valued_move_line.qty_done, move.product_id.uom_id)
            if float_is_zero(forced_quantity or valued_quantity, precision_rounding=move.product_id.uom_id.rounding):
                continue
            svl_vals = move.product_id._prepare_supplier_inventory_production_svl_vals(forced_quantity or valued_quantity, move.company_id)
            svl_vals.update(move._prepare_common_svl_vals())
            if forced_quantity:
                svl_vals['description'] = 'Correction of %s (modification of past move)' % move.picking_id.name or move.name
            svl_vals_list.append(svl_vals)
        return self.env['stock.valuation.layer'].sudo().create(svl_vals_list)
    

    
    ########
    def _account_entry_move(self, qty, description, svl_id, cost):
        """ Accounting Valuation Entries """
        self.ensure_one()
        if self.product_id.type != 'product':
            _logger.info("No se genera poliza...")
            # no stock valuation for consumable products
            return False
        if self.restrict_partner_id:
            _logger.info("Pertenece a tercero...")
            # if the move isn't owned by the company, we don't make any valuation
            return False

        location_from = self.location_id
        location_to = self.location_dest_id
        company_from = self._is_out() and self.mapped('move_line_ids.location_id.company_id') or False
        company_to = self._is_in() and self.mapped('move_line_ids.location_dest_id.company_id') or False

        _logger.info("self._is_in(): %s" % self._is_in())
        _logger.info("self._is_out(): %s" % self._is_out())
        _logger.info("self._is_internal_transit(): %s" % self._is_internal_transit())
        # Create Journal Entry for products arriving in the company; in case of routes making the link between several
        # warehouse of the same company, the transit location belongs to this company, so we don't need to create accounting entries
        if self._is_in():
            _logger.info("AAA AAA AAA AAA")
            journal_id, acc_src, acc_dest, acc_valuation = self._get_accounting_data_for_valuation()
            if location_from and location_from.usage == 'customer':  # goods returned from customer
                # self.with_context(force_company=company_to.id)._create_account_move_line(acc_dest, acc_valuation, journal_id, qty, description, svl_id, cost)
                self._create_account_move_line(acc_dest, acc_valuation, journal_id, qty, description, svl_id, cost)
            else:
                # self.with_context(force_company=company_to.id)._create_account_move_line(acc_src, acc_valuation, journal_id, qty, description, svl_id, cost)
                self._create_account_move_line(acc_src, acc_valuation, journal_id, qty, description, svl_id, cost)

        # Create Journal Entry for products leaving the company
        if self._is_out():
            _logger.info("BBB BBB BBB BBB")
            cost = -1 * cost
            journal_id, acc_src, acc_dest, acc_valuation = self._get_accounting_data_for_valuation()
            if location_to and location_to.usage == 'supplier':  # goods returned to supplier
                # self.with_context(force_company=company_from.id)._create_account_move_line(acc_valuation, acc_src, journal_id, qty, description, svl_id, cost)
                self._create_account_move_line(acc_valuation, acc_src, journal_id, qty, description, svl_id, cost)
            else:
                # self.with_context(force_company=company_from.id)._create_account_move_line(acc_valuation, acc_dest, journal_id, qty, description, svl_id, cost)
                self._create_account_move_line(acc_valuation, acc_dest, journal_id, qty, description, svl_id, cost)

        if self.company_id.anglo_saxon_accounting:
            _logger.info("CCC CCC CCC CCC")
            # Creates an account entry from stock_input to stock_output on a dropship move. https://github.com/odoo/odoo/issues/12687
            journal_id, acc_src, acc_dest, acc_valuation = self._get_accounting_data_for_valuation()
            if self._is_dropshipped():
                if cost > 0:
                    # self.with_context(force_company=self.company_id.id)._create_account_move_line(acc_src, acc_valuation, journal_id, qty, description, svl_id, cost)
                    self._create_account_move_line(acc_src, acc_valuation, journal_id, qty, description, svl_id, cost)
                else:
                    cost = -1 * cost
                    # self.with_context(force_company=self.company_id.id)._create_account_move_line(acc_valuation, acc_dest, journal_id, qty, description, svl_id, cost)
                    self._create_account_move_line(acc_valuation, acc_dest, journal_id, qty, description, svl_id, cost)
            elif self._is_dropshipped_returned():
                if cost > 0:
                    # self.with_context(force_company=self.company_id.id)._create_account_move_line(acc_valuation, acc_src, journal_id, qty, description, svl_id, cost)
                    self._create_account_move_line(acc_valuation, acc_src, journal_id, qty, description, svl_id, cost)
                else:
                    cost = -1 * cost
                    # self.with_context(force_company=self.company_id.id)._create_account_move_line(acc_dest, acc_valuation, journal_id, qty, description, svl_id, cost)
                    self._create_account_move_line(acc_dest, acc_valuation, journal_id, qty, description, svl_id, cost)

        if self.company_id.anglo_saxon_accounting:
            _logger.info("DDD DDD DDD DDD")
            #eventually reconcile together the invoice and valuation accounting entries on the stock interim accounts
            self._get_related_invoices()._stock_account_anglo_saxon_reconcile_valuation(product=self.product_id)
            

        ###############################################
        ##### ARGIL - Inicio
        ###############################################
        # Por si usa el módulo de stock_repair_spare_parts que agrega el check repair_location en la ubicación
        # Origen: Inventory => Destino: Internal
        if 'repair_location' in location_from._fields and \
            (location_from.repair_location and location_from.usage == 'inventory' and \
            location_to.repair_location and location_to.usage == 'internal'):
            return False

        # Origen Interno/Transito => Destino Interno/Transito 
        # Esto es util para Transferencias entre Almacenes propios,
        # pero usando la ubicacion de Transito para usar Rutas avanzadas.        
        if self._is_internal_transit(): #location_from.usage in ('internal','transit') and location_to.usage in ('internal','transit'):
            _logger.info("EEE EEE EEE EEE")
            journal_id, acc_src, acc_dest, acc_valuation = self._get_accounting_data_for_valuation()
            company_from = company_from or self.env.user.company_id
            # self.with_context(force_company=company_from.id)._create_account_move_line(acc_dest, acc_src, journal_id, qty, description, svl_id, cost)
            self._create_account_move_line(acc_dest, acc_src, journal_id, qty, description, svl_id, cost)
            #OK
            return
        # Origen: Proveedores => Destino Inventario (perdidas) / Produccion
        # Esto aplica para Recepcion de Refacciones de Taller Externo - PENDIENTE DE REVISAR HASTA QUE SE MIGRE FLEET_MRO
        elif self._is_supplier_inventory_production(): 
            _logger.info("FFF FFF FFF FFF")
            if location_from.usage in ('supplier') and location_to.usage in ('inventory','production'):
                journal_id, acc_src, acc_dest, acc_valuation = self._get_accounting_data_for_valuation()
                company_from = company_from or self.env.user.company_id
                # self.with_context(force_company=company_from.id)._create_account_move_line(acc_dest, acc_src, journal_id, qty, description, svl_id, cost)
                self._create_account_move_line(acc_dest, acc_src, journal_id, qty, description, svl_id, cost)
                return
        
            # Origen: Inventario (perdidas) / Produccion => Destino: Proveedores
            # Esto aplica para Devolucion de Refacciones de Taller Externo - PENDIENTE DE REVISAR HASTA QUE SE MIGRE FLEET_MRO
            elif location_from.usage in ('inventory','production') and location_to.usage in ('supplier'):
                journal_id, acc_src, acc_dest, acc_valuation = self._get_accounting_data_for_valuation()
                company_from = company_from or self.env.user.company_id
                # self.with_context(force_company=company_from.id)._create_account_move_line(acc_src, acc_dest, journal_id)
                self._create_account_move_line(acc_src, acc_dest, journal_id)
                return
        
        ###############################################
        ##### ARGIL - Final
        ###############################################
        
    
    def _get_accounting_data_for_valuation(self):
        """ Return the accounts and journal to use to post Journal Entries for
        the real-time valuation of the quant. """
        self.ensure_one()
        accounts_data = self.product_id.product_tmpl_id.get_product_accounts()
        _logger.info("accounts_data: %s" % accounts_data)
        for key in accounts_data.keys():
            _logger.info("%s: %s-%s" % (key, accounts_data[key].code, accounts_data[key].name))        
        _logger.info("000000000000000")
        #########################################
        ## ARGIL - Inicio
        #########################################
        journal_id = accounts_data['stock_journal'].id
        acc_src, acc_dest, acc_valuation = False, False, False
        # Transferencias entre ubicaciones de empresas 'supplier','customer'
        if self.location_id.usage in ('supplier','customer') and self.location_dest_id.usage in ('supplier','customer'):
            _logger.info("111111111111111")
            acc_src = (self.location_id.usage == 'supplier' and self.location_dest_id.usage == 'customer' and \
                            accounts_data['stock_input'].id) or \
                      (self.location_id.usage == 'customer' and self.location_dest_id.usage == 'supplier' and \
                            accounts_data['stock_output'].id)
            acc_dest = (self.location_id.usage == 'supplier' and self.location_dest_id.usage == 'customer' and \
                            accounts_data['stock_output'].id) or \
                       (self.location_id.usage == 'customer' and self.location_dest_id.usage == 'supplier' and \
                            accounts_data['stock_input'].id)
            acc_valuation = False
            _logger.info("journal_id: %s - acc_src: %s - acc_dest: %s - acc_valuation: %s" % (journal_id, acc_src, acc_dest, acc_valuation))
            return journal_id, acc_src, acc_dest, acc_valuation

        # Transferencias entre ubicaciones 'internal','transit','inventory','production'
        if self.location_id.usage in ('internal','transit','inventory','production') and \
           self.location_dest_id.usage in ('internal','transit','inventory','production'):
            _logger.info("222222222222222")
            acc_src = self.location_id.valuation_out_account_id and self.location_id.valuation_out_account_id.id \
                        or accounts_data.get('stock_valuation', False).id
            acc_dest = self.location_dest_id.valuation_in_account_id and self.location_dest_id.valuation_in_account_id.id \
                        or accounts_data.get('stock_valuation', False).id
            if self.location_id.usage == 'internal':
                acc_valuation = acc_src
            else:
                acc_valuation = acc_dest
            _logger.info("journal_id: %s - acc_src: %s - acc_dest: %s - acc_valuation: %s" % (journal_id, acc_src, acc_dest, acc_valuation))
            return journal_id, acc_src, acc_dest, acc_valuation


        
        # Transferencia de Entrada por Compra y/o Devolucion de Venta
        if self.location_id.usage in ('customer','supplier') and self.location_dest_id.usage in ('internal'):
            _logger.info("3333333333333333333333")
            acc_src = self.location_id.usage in ('supplier') and accounts_data['stock_input'].id or False
            acc_dest = self.location_id.usage in ('customer') and accounts_data['stock_output'].id or False
            acc_valuation = self.location_dest_id.valuation_in_account_id and self.location_dest_id.valuation_in_account_id.id \
                        or accounts_data.get('stock_valuation', False).id
            #acc_dest = acc_valuation
            _logger.info("journal_id: %s - acc_src: %s - acc_dest: %s - acc_valuation: %s" % (journal_id, acc_src, acc_dest, acc_valuation))
            return journal_id, acc_src, acc_dest, acc_valuation            


        # Transferencia de Salida Venta y/o Devolucion de Compra
        if self.location_dest_id.usage in ('customer','supplier') and self.location_id.usage in ('internal'):
            _logger.info("44444444444444444444444")
            acc_src = self.location_dest_id.usage in ('supplier') and accounts_data['stock_input'].id or False
            acc_dest = self.location_dest_id.usage in ('customer') and accounts_data['stock_output'].id or False
            acc_valuation = self.location_id.valuation_in_account_id and self.location_id.valuation_in_account_id.id \
                        or accounts_data.get('stock_valuation', False).id
            #acc_dest = acc_valuation
            _logger.info("journal_id: %s - acc_src: %s - acc_dest: %s - acc_valuation: %s" % (journal_id, acc_src, acc_dest, acc_valuation))
            return journal_id, acc_src, acc_dest, acc_valuation
        
        #########################################
        ## ARGIL - Final
        #########################################            

        if self.location_id.valuation_out_account_id:
            acc_src = self.location_id.valuation_out_account_id.id
        else:
            acc_src = accounts_data['stock_input'].id

        if self.location_dest_id.valuation_in_account_id:
            acc_dest = self.location_dest_id.valuation_in_account_id.id
        else:
            acc_dest = accounts_data['stock_output'].id

        acc_valuation = accounts_data.get('stock_valuation', False)
        if acc_valuation:
            acc_valuation = acc_valuation.id
        if not accounts_data.get('stock_journal', False):
            raise UserError(_('You don\'t have any stock journal defined on your product category, check if you have installed a chart of accounts.'))
        if not acc_src:
            raise UserError(_('Cannot find a stock input account for the product %s. You must define one on the product category, or on the location, before processing this operation.') % (self.product_id.display_name))
        if not acc_dest:
            raise UserError(_('Cannot find a stock output account for the product %s. You must define one on the product category, or on the location, before processing this operation.') % (self.product_id.display_name))
        if not acc_valuation:
            raise UserError(_('You don\'t have any stock valuation account defined on your product category. You must define one before processing this operation.'))
        journal_id = accounts_data['stock_journal'].id
        _logger.info("journal_id: %s - acc_src: %s - acc_dest: %s - acc_valuation: %s" % (journal_id, acc_src, acc_dest, acc_valuation))
        _logger.info("55555555555555555555")
        return journal_id, acc_src, acc_dest, acc_valuation



