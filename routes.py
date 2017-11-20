from flask import request, render_template, make_response

from flask_pdf import app

from utils import generate_pdf_weasyprint, generate_simple_pdf


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('hello.html')
    # report = generate_pdf_weasyprint()
    report = generate_simple_pdf()
    response = make_response(report)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=%s.pdf' % 'pdf_report'
    return response


