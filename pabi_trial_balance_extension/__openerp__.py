# -*- coding: utf-8 -*-
{
    "name": "NSTDA :: PABI2 - Traial Balance Extension for GFMIS",
    "summary": "",
    "version": "1.0",
    "category": "Human Resources",
    "description": """
Add ability to export Trial Balance with mapped account for GFMIS as xlsx
    """,
    "website": "https://ecosoft.co.th/",
    "author": "Kitti U.",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "account_trial_balance_report",
        "pabi_utils",
    ],
    "data": [
        "xlsx_template/xlsx_template_wizard.xml",
        "xlsx_template/templates.xml",
    ],
}
