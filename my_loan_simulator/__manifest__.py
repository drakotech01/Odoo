# -*- coding: utf-8 -*-
{
    "name": "Simulador de Crédito",
    "summary": """
        Módulo para simular planes de pagos de crédito.
    """,
    "description": """
        Este módulo permite a los usuarios simular planes de pagos con cuotas fijas.
        - Calcula la cuota semanal fija.
        - Genera un plan de pagos detallado.
        - Muestra la amortización del capital.
        - Incluye seguimiento de cambios (chatter).
        - Permite generar reportes en PDF.
    """,
    "author": "Tu Nombre",
    "website": "http://www.tu-sitio-web.com",
    "category": "Finance",
    "version": "1.0",
    "depends": ["base", "mail"],
    "data": [
        "security/ir.model.access.csv",
        "views/clientes_credito.xml",
        "views/loan_simulator_views.xml",
        "views/menu.xml",
        # "views/res_partner_views.xml",
        # "Mueveelreportealprincipioparaasegurarquesecargueprimeroreport/loan_simulator_template.xml",
        #"report/loan_simulator_report.xml",
    ],
    "installable": True,
    "application": True,
    "license": "AGPL-3",
}
