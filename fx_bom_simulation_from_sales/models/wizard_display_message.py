# -*- coding:utf-8 -*-
from odoo import fields, models, api


class WizardDisplayMessage(models.TransientModel):
    _name = 'wizard.display.message'

    message = fields.Char('Msg', readonly=True)

    @api.model
    def get_message_act(self, msg, tittle='Información'):
        new_id = self.create({'message' : msg})
        return {
            'type' : 'ir.actions.act_window',
            'name' : tittle,
            'res_model' : self._name,
            'view_mode' : 'form',
            'target' : 'new',
            'res_id' : new_id.id
        }

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        res = super(WizardDisplayMessage, self).fields_view_get(view_id, view_type, toolbar, submenu)
        res['arch'] = """
            <form string="Información" edit="0">
                <sheet>
                    <h3>
                        <field name="message" readonly="1"/>
                    </h3>
                </sheet>
                <footer>
                    <button special="cancel" string="Aceptar" class="oe_highlight"/>
                </footer>
            </form>
        """
        return res