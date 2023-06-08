# -*- coding: utf-8 -*-

from odoo import models, fields, api,_
from odoo.exceptions import ValidationError

class Production_Data(models.Model):
    _name = 'control.production_data'
    _description = "Datos levantados de Producción"

    serie = fields.Many2one('stock.production.lot', string="Serie")
    producto = fields.Many2one(related='serie.product_id', string="Producto")
    centro_trabajo = fields.Selection([
                ('No Iniciado','No Iniciado'),
                ('Producción','Producción'),
                ('Pintura','Pintura'),
                ('Ensamble','Ensamble'),
                ('Terminado','Terminado'),
                ('Hold','Hold'),
            ], string='Centro de Trabajo', 
               default='No Iniciado'
        )
    terminado = fields.Boolean(string='Terminado')
    hold = fields.Boolean(string='Hold')
    semana_laboral = fields.Selection([
            ('1','1'),('2','2'),('3','3'),('4','4'),('5','5'),('6','6'),('7','7'),('8','8'),('9','9'),('10','10'),
            ('11','11'),('12','12'),('13','13'),('14','14'),('15','15'),('16','16'),('17','17'),('18','18'),('19','19'),('20','20'),
            ('21','21'),('22','22'),('23','23'),('24','24'),('25','25'),('26','26'),('27','27'),('28','28'),('29','29'),('30','30'),
            ('31','31'),('32','32'),('33','33'),('34','34'),('35','35'),('36','36'),('37','37'),('38','38'),('39','39'),('40','40'),
            ('41','41'),('42','42'),('43','43'),('44','44'),('45','45'),('46','46'),('47','47'),('48','48'),('49','49'),('50','50'),
            ('51','51'),('52','52')], string="Semana Laboral"
        )

    @api.onchange('centro_trabajo')
    def on_change_centro_trabajo(self):
        for record in self:
            if record.centro_trabajo == 'Terminado':
                record.terminado = True
                record.hold = False
            elif record.centro_trabajo == 'Hold':
                record.terminado = False
                record.hold = True
            else:
                record.terminado = False
                record.hold = False


