from odoo import api, fields, models

class WizardAddTags(models.TransientModel):
    _name = 'wizard.add.tags'
    _description = 'Wizard to Add Tags to Contacts'

    partner_ids = fields.Many2many(
        'res.partner', 
        string='Contacts',
        help='Contacts to which we will add tags.'
    )
    category_ids = fields.Many2many(
        'res.partner.category',
        string='Tags to Add',
        help='Tags that will be added to the selected contacts.'
    )

    def action_add_tags(self):
        """Write selected tags to each partner (append, do not overwrite)."""
        for partner in self.partner_ids:
            partner.write({
                'category_id': [(4, cat.id) for cat in self.category_ids]
            })
        # Close the wizard
        return {'type': 'ir.actions.act_window_close'}