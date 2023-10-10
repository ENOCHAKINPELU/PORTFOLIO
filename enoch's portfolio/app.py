from flask import Flask, render_template,request, flash, redirect, url_for
from datetime import datetime
import smtplib
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://testimonial_rsvx_user:zzJXfVXyU1zEI4bisjbV3NfpiXDQtTXh@dpg-ckikaii12bvs739lflg0-a.oregon-postgres.render.com/testimonial_rsvx'
app.config['SECRET_KEY']= 'secretkey'


db = SQLAlchemy(app)

class Testimonial(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    message = db.Column(db.Text)
    #img = db.Column(db.BLOB)

@app.route('/', methods=["POST","GET"])
def home():
    testimonials = Testimonial.query.all()
    return render_template("index.html", t=testimonials)

@app.route('/contact', methods=["POST","GET"])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        # Set up the SMTP connection and send the email
        smtp_server = "smtp.gmail.com"
        smtp_port = 587  # Port for sending email (587 for TLS, 465 for SSL)
        smtp_username = "ifeoluwaakinpelu05@gmail.com"
        smtp_password = "kujiuwyrkwksygov"

        subject = request.form['subject']
        body = f"Name: {name}\nEmail: {email}\nMessage: {message}"

        try:
            # Create an SMTP connection
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(smtp_username, smtp_password)

            # Send the email
            server.sendmail(smtp_username, "ifeoluwaakinpelu05@gmail.com", f"Subject: {subject}\n\n{body}")

            # Close the SMTP connection
            server.quit()

            return "Message sent successfully!"
        except Exception as e:
            return str(e)

@app.route('/resume', methods=["POST","GET"])
def resume():
    return render_template('resume.html')

@app.route('/testimonial', methods=["POST","GET"])
def testimonial():
    if request.method == 'POST':
        name_ = request.form['name'].capitalize()
        message_ = request.form['message']
        # image_ = request.files['img']
        # if image_:
        #     image_name = image_.filename
        #     image_data = image_.read()
        testi = Testimonial(name=name_, message=message_)#, img=image_data)
        db.session.add(testi)
        db.session.commit()
        return redirect(url_for('home'))
    else:
        return render_template('testimonial.html')
        
if __name__ == "__main__":
    app.app_context().push()
    db.create_all()
    app.run(debug=(True))