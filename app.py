import requests
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/weather.db'

db = SQLAlchemy(app)
db.init_app(app)


class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)


with app.app_context():
    db.create_all()


@app.route('/', methods=['GET', 'POST'])
def index():  # put application's code here
    if request.method == 'POST':
        new_city = request.form.get('city')
        if new_city:
            new_city_obj = City(name=new_city)

            db.session.add(new_city_obj)
            db.session.commit()

    cities = City.query.all()

    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=91e0f56bd42ef4e0c1c3c36ddc79be5e'

    weather_data = []

    for city in cities:
        r = requests.get(url.format(city.name)).json()

        weather = {
            "city": city.name,
            "temperature": r['main']['temp'],
            "description": r['weather'][0]['description'],
            "icon": r['weather'][0]['icon'],
        }

        weather_data.append(weather)

    return render_template("weather.html", weather_data=weather_data)


if __name__ == '__main__':
    app.run()
