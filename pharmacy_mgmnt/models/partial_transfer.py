from openerp import models, fields, api


class PartialTransfer1(models.TransientModel):
    _name = 'partial.transf'

    full_trans = fields.Boolean()
    racks_id_1 = fields.Many2one('product.medicine.types', string='From')
    racks_id_2 = fields.Many2one('product.medicine.types', string='To')
    stock_part_id = fields.One2many(
        comodel_name='partial.transfernew1',
        inverse_name='full_id1',
        string=' ',
        store=True,
    )

    @api.multi
    def load_lines(self):
        self.stock_part_id = False
        # self.write({'stock_part_id':False})
        # stock_obj = self.env['entry.stock'].search([])
        stock_obj = self.env['entry.stock'].search([('rack', '=', self.racks_id_1.id),('qty', '!=', 0)])
        if stock_obj:
            new_lines = []
            for rec in stock_obj:
                new_lines.append((0, 0, {
                    'qty': round(rec.qty, 0),
                    'name': rec.medicine_1.name,
                    'medicine_1': rec.medicine_1.id,
                    'potency': rec.potency.id,
                    'medicine_name_packing': rec.medicine_name_packing.id,
                    'company': rec.company.id,
                    'batch_2': rec.batch_2.id,
                    'entry_stock_id': rec.id,
                }))
            self.write({'stock_part_id': new_lines})
        else:
            self.stock_part_id = [(5, 0, 0)]
            print("no stock")
        return {
            'context': self.env.context,
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'partial.transf',
            'res_id': self.id,
            'view_id': False,
            'type': 'ir.actions.act_window',
            'target': 'new',
        }

    @api.onchange('racks_id_1')
    def onchange_load_lines(self):
        # self.stock_part_id = False
        stock_obj = self.env['entry.stock'].search([('rack', '=', self.racks_id_1.id),('qty', '!=', 0)])
        if stock_obj:
            new_lines = []
            for rec in stock_obj:
                print("rec.id",rec.id)
                new_lines.append((0, 0, {
                    'qty': round(rec.qty, 0),
                    'name': rec.medicine_1.name,
                    'medicine_1': rec.medicine_1.id,
                    'potency': rec.potency.id,
                    'medicine_name_packing': rec.medicine_name_packing.id,
                    'company': rec.company.id,
                    'batch_2': rec.batch_2.id,
                    'entry_stock_id': rec.id,
                }))
            self.stock_part_id = new_lines
            self.write({'stock_part_id': new_lines})
        else:
            self.stock_part_id = [(5, 0, 0)]
            print("no stock")
        return {
            'context': self.env.context,
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'partial.transf',
            'res_id': self.id,
            'view_id': False,
            'type': 'ir.actions.act_window',
            'target': 'new',
        }
    @api.multi
    def part_transfer(self):
        # stock_obj = self.env['entry.stock'].search([('rack', '=', self.racks_id_1.id)])
        # if stock_obj:
        if self.stock_part_id:
            for item in self.stock_part_id:
                print("item.entry_stock_id", item.entry_stock_id)
                if item.qty_transfer != 0:
                    if item.qty == float(item.qty_transfer):
                        item.entry_stock_id.rack = self.racks_id_2.id
                    else:
                        balance_qty = item.qty - float(item.qty_transfer)
                        item.entry_stock_id.write({'qty': balance_qty})
                        vals={
                            'qty': item.qty_transfer,
                            'name': item.medicine_1.name,
                            'medicine_1': item.medicine_1.id,
                            'potency': item.potency.id,
                            'medicine_name_packing': item.medicine_name_packing.id,
                            'company': item.company.id,
                            'batch_2': item.batch_2.id,
                            'entry_stock_id': item.id,
                            'medicine_grp1':item.entry_stock_id.medicine_grp1.id,
                            'mrp':item.entry_stock_id.mrp,
                            'manf_date':item.entry_stock_id.manf_date,
                            'expiry_date':item.entry_stock_id.expiry_date,
                            'invoice_line_tax_id4':item.entry_stock_id.invoice_line_tax_id4,
                            'rack':self.racks_id_2.id,
                            'hsn_code':item.entry_stock_id.hsn_code

                        }
                        self.env['entry.stock'].create(vals)
            for rec in self:
                rec.write({'stock_part_id': [(5, 0, 0)]})

        return {
            'context': self.env.context,
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'partial.transf',
            'res_id': self.id,
            'view_id': False,
            'type': 'ir.actions.act_window',
            'target': 'new',
        }


    @api.multi
    def full_transfer(self):
        stock_obj = self.env['entry.stock'].search([('rack', '=', self.racks_id_1.id)])
        if stock_obj:
            for rec in stock_obj:
                rec.write({'rack': self.racks_id_2.id})
            for rec in self:
                rec.write({'stock_part_id': [(5, 0, 0)]})

        return {
            'context': self.env.context,
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'partial.transf',
            'res_id': self.id,
            'view_id': False,
            'type': 'ir.actions.act_window',
            'target': 'new',
        }


class PartTranserNew1(models.TransientModel):
    _name = 'partial.transfernew1'
#
    expiry_date = fields.Date(string='Expiry Date')
    manf_date = fields.Date(string='Manufacturing Date')
    potency = fields.Many2one('product.medicine.subcat', 'Potency', )
    batch_2 = fields.Many2one('med.batch', "Batch")
    rack = fields.Many2one('product.medicine.types', 'Rack')
    qty = fields.Float('Stock')
    company = fields.Many2one('product.medicine.responsible', 'Company')
    medicine_name_packing = fields.Many2one('product.medicine.packing', 'Packing', )
    medicine_1 = fields.Many2one('product.product', string="Medicine")
    qty_received = fields.Float('Qty Transfer')
    full_id1 = fields.Many2one('partial.transf', string='Stock')
    qty_transfer = fields.Char('Transfer_Qty')
    entry_stock_id = fields.Many2one('entry.stock')
