# -*- coding: utf-8 -*-
import requests
import xmlrpclib
import ast
from openerp import fields, models, api


class PABIWebConfigSettings(models.TransientModel):
    _name = 'pabi.web.config.settings'
    _inherit = 'res.config.settings'

    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env.user.company_id,
    )
    # PABIWeb
    pabiweb_active = fields.Boolean(
        string='Open Connection to PABI Web.',
        related='company_id.pabiweb_active',
    )
    pabiweb_hr_url = fields.Char(
        string='PABI Web URL for HR Salary',
        related='company_id.pabiweb_hr_url',
    )
    pabiweb_exp_url = fields.Char(
        string='PABI Web URL for Expense',
        related='company_id.pabiweb_exp_url',
    )
    pabiweb_pcm_url = fields.Char(
        string='PABI Web URL for Procurement',
        related='company_id.pabiweb_pcm_url',
    )
    pabiweb_file_prefix = fields.Char(
        string='PABI Web URL for attachment prefix',
        related='company_id.pabiweb_file_prefix',
    )
    # e-HR
    pabiehr_active = fields.Boolean(
        string='Open Connection to e-HR Webservice',
        related='company_id.pabiehr_active',
    )
    pabiehr_login_url = fields.Char(
        string='e-HR Login URL',
        related='company_id.pabiehr_login_url',
    )
    pabiehr_user = fields.Char(
        string='e-HR Login',
        related='company_id.pabiehr_user',
    )
    pabiehr_password = fields.Char(
        string='e-HR Password',
        related='company_id.pabiehr_password',
    )
    pabiehr_data_url = fields.Char(
        string='e-HR Data Retrival URL',
        related='company_id.pabiehr_data_url',
    )
    pabiehr_data_mapper = fields.Text(
        string='Odoo & e-HR Mapper Dict',
        related='company_id.pabiehr_data_mapper',
    )

    @api.model
    def _get_alfresco_connect(self, type):
        _URL = {'hr': 'pabiweb_hr_url',
                'exp': 'pabiweb_exp_url',
                'pcm': 'pabiweb_pcm_url', }
        ConfParam = self.env['ir.config_parameter']
        pabiweb_active = self.env.user.company_id.pabiweb_active
        if not pabiweb_active:
            return False
        url = self.env.user.company_id[_URL[type]]
        username = self.env.user.login
        password = ConfParam.get_param('pabiweb_password')
        connect_string = url % (username, password)
        alfresco = xmlrpclib.ServerProxy(connect_string)
        return alfresco

    @api.model
    def _get_pabiehr_connect(self):
        if not self.env.user.company_id.pabiehr_active:
            return False
        url = self.env.user.company_id.pabiehr_login_url
        user = self.env.user.company_id.pabiehr_user
        password = self.env.user.company_id.pabiehr_password
        data = {'username': user, 'password': password}
        # Login
        response = requests.post(url, data=data)
        res = ast.literal_eval(response.text)
        token = res.get('Bearer', False)
        return token
