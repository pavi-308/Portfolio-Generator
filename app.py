from flask import Flask, render_template, request, redirect, session, url_for, send_file
import pdfkit
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/')
def home():
    return redirect(url_for('step1'))

@app.route('/step1', methods=['GET', 'POST'])
def step1():
    error = None
    if request.method == 'POST':
        first_name = request.form.get('firstName')
        middle_name = request.form.get('middleName')
        last_name = request.form.get('lastName')
        email = request.form['email']
        mobile = request.form['mobile']

        if len(first_name) < 3 or len(first_name) > 50:
            error = "Name must be between 3 and 50 characters."
        elif len(last_name) < 2 or len(last_name) > 50:
                error = "Name must be between 2 and 50 characters."
        elif not mobile.isdigit() or len(mobile) != 10:
            error = "Mobile number must be exactly 10 digits."
        else:
           session['first_name'] = first_name
           session['middle_name'] = middle_name
           session['last_name'] = last_name
           session['email'] = email
           session['mobile'] = mobile
        return redirect(url_for('step2'))

    return render_template('step1.html')

@app.route('/step2', methods=['GET', 'POST'])
def step2():
    error = None
    if request.method == 'POST':
        address = request.form['address']
        city = request.form['city']
        state = request.form['state']
        country = request.form['country']

        if not address or not city or not state or not country:
            error = "All fields are required."
        else:
            session['address'] = address
            session['city'] = city
            session['state'] = state
            session['country'] = country
            return redirect(url_for('step3'))

    return render_template('step2.html', error=error)

@app.route('/step3', methods=['GET', 'POST'])
def step3():
    error = None
    if request.method == 'POST':
        education = request.form['education']
        if not education:
            error = "Education field is required."
        else:
            session['education'] = education
            return redirect(url_for('step4'))
    return render_template('step3.html', error=error)

@app.route('/step4', methods=['GET', 'POST'])
def step4():
    error = None
    if request.method == 'POST':
        experience = request.form['experience']
        if not experience:
            error = "Experience field is required."
        else:
            session['experience'] = experience
            return redirect(url_for('step5'))
    return render_template('step4.html', error=error)

@app.route('/step5', methods=['GET', 'POST'])
def step5():
    error = None
    if request.method == 'POST':
        certifications = request.form['certifications']
        if not certifications:
            error = "Certifications field is required."
        else:
            session['certifications'] = certifications
            return redirect(url_for('preview'))
    return render_template('step5.html', error=error)

@app.route('/preview')
def preview():
    return render_template('preview.html', data=session)

@app.route('/download')
def download():
    rendered = render_template('resume_pdf.html', data=session)
    pdfkit.from_string(rendered, 'resume.pdf')
    return send_file('resume.pdf', as_attachment=True)
    pdfkit_config = pdfkit.configuration(wkhtmltopdf='/usr/local/bin/wkhtmltopdf')  # update path as needed
    pdfkit.from_string(rendered, 'resume.pdf', configuration=pdfkit_config)


if __name__ == '__main__':
    app.run(debug=True)
