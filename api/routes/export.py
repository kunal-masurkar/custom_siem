from flask import Blueprint, request, jsonify, send_file
import io
from reportlab.pdfgen import canvas

export_bp = Blueprint('export', __name__)

@export_bp.route('/export/pdf', methods=['POST'])
def export_pdf():
    dashboard = request.json.get('dashboard', 'default')
    # Placeholder: generate a simple PDF
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)
    p.drawString(100, 750, f"Dashboard Export: {dashboard}")
    p.showPage()
    p.save()
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name=f'{dashboard}.pdf', mimetype='application/pdf') 