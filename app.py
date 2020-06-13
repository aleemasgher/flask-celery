from flask import Flask, flash, render_template, request, redirect
from celery import Celery
from flask_mail import Mail, Message

app = Flask(__name__)
app.config.from_object("config")
app.secret_key = app.config['SECRET_KEY']

# configure celery client
client = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
client.conf.update(app.config)

# configure flask mail integration
mail = Mail(app)


@client.task(name='send_mail')
def send_mail(data):
    msg = Message("Notify me!", sender="Notify me <no-reply@notifyme.com>", recipients=[data['email']])
    msg.body = data['message']
    with app.app_context():
        mail.send(msg)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')

    elif request.method == 'POST':
        if request.form['email'] == '' or request.form['first_name'] == '' or request.form['last_name'] == '' \
                or request.form['message'] == '' or request.form['duration'] == '' \
                or request.form['duration_unit'] == '':
            flash(f"Please fill all the required fields")
            return redirect('.')

        data = {'email': request.form['email'], 'first_name': request.form['first_name'],
                'last_name': request.form['last_name'], 'message': request.form['message']}
        duration = int(request.form['duration'])
        duration_unit = request.form['duration_unit']

        # calculate time in seconds
        if duration_unit == 'minutes':
            duration *= 60
        elif duration_unit == 'hours':
            duration *= 3600
        elif duration_unit == 'days':
            duration *= 86400
        elif duration_unit == 'weeks':
            duration *= 604800


        send_mail.apply_async(args=[data], countdown=duration)
        flash(f"Email will be sent to {data['email']} in {request.form['duration']} {duration_unit}")
        
        return redirect('.')


if __name__ == '__main__':
    app.run(debug=True)
