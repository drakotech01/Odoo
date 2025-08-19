from odoo import http
from odoo.http import request

class SpreadsheetExport(http.Controller):
    @http.route('/spreadsheet/export/<int:doc_id>', auth='user')
    def export_spreadsheet(self, doc_id, **kwargs):
        doc = request.env['spreadsheet.document'].browse(doc_id)
        content = doc.data_json or '{}'
        return request.make_response(content, [
            ('Content-Type', 'application/json'),
            ('Content-Disposition', f'attachment; filename={doc.name}.json')
        ])