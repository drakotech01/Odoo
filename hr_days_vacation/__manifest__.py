{
    "name": "Days Vacation",
    "version": "1.0",
    "depends": ["hr", "hr_holidays", "mail", "hr_contract"],
    "author": "F Rapido - Desarrollo de Software",
    "category": "Human Resources",
    "summary": "Gestión de vacaciones de empleados",
    "description": "Calcula días de vacaciones basados en la fecha de ingreso del empleado según la Ley Federal del Trabajo en México.",
    "data": [
        "security/models.xml",
        "security/ir.model.access.csv",
        "views/hr_employee_views.xml",
        #"views/hr_vacation_request_views.xml",
        #"data/email_templates.xml",
        #"report/report_vacation_request_pdf.xml",
        #"report/report_vacation_request_pdf_template.xml"
    ],
    "installable": True,
    "application": False,
    "auto_install": False
}