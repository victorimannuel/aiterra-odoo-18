import logging
from odoo import models, fields, api
from odoo.exceptions import UserError
from odoo.tools.safe_eval import safe_eval
from psycopg2 import OperationalError

class MailingList(models.Model):
    _inherit = 'mailing.list'

    contact_filter_domain = fields.Char(string='Contact Filter', help='Domain filter for contacts')
    auto_sync_contacts = fields.Boolean('Auto Sync with Contacts', default=True)

    @api.model
    def _sync_contacts_to_list(self):
        _logger = logging.getLogger(__name__)
        
        try:
            for mlist in self.search([('auto_sync_contacts', '=', True)]):
                _logger.info(f"Starting sync for mailing list: {mlist.name}")
                try:
                    domain = safe_eval(mlist.contact_filter_domain or '[]')
                    contacts = self.env['res.partner'].with_context(active_test=False).search(domain)
                    _logger.info(f"Found {len(contacts)} contacts matching filter")
                    
                    existing_subs = self.env['mailing.contact'].search([
                        ('list_ids', 'in', [mlist.id])
                    ]).mapped('email')

                    for contact in contacts.filtered(lambda c: c.email and c.email not in existing_subs):
                        try:
                            self.env.cr.execute('SAVEPOINT sync_contact')
                            mailing_contact = self.env['mailing.contact'].create({
                                'name': contact.name,
                                'email': contact.email,
                                'list_ids': [(4, mlist.id)]
                            })
                            self.env.cr.execute('RELEASE SAVEPOINT sync_contact')
                            _logger.info(f"Successfully added contact: {contact.email}")
                        except Exception as e:
                            self.env.cr.execute('ROLLBACK TO SAVEPOINT sync_contact')
                            _logger.error(f"Failed to add contact {contact.email}: {e}")
                            continue
                except Exception as e:
                    _logger.error(f"Error processing list {mlist.name}: {e}")
                    continue
        except Exception as e:
            _logger.error(f"Database connection error: {e}")
            raise UserError("Database connection lost. Please try again.")

    @api.model
    def create(self, vals):
        res = super().create(vals)
        if vals.get('auto_sync_contacts') and vals.get('contact_filter_domain'):
            res._sync_contacts_to_list()
        return res

    def write(self, vals):
        res = super().write(vals)
        if 'contact_filter_domain' in vals or 'auto_sync_contacts' in vals:
            self._sync_contacts_to_list()
        return res
        
    def action_sync_contacts(self):
        self._sync_contacts_to_list()
        return True