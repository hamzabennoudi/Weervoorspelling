from flask import Flask, render_template, request
import requests
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/forecast.html', methods=['POST'])
def forecast():
    country = request.form.get('country')
    city = request.form.get('city')

    api_key = '424be75514604fddbbb143238241703'  # Vervang dit met je eigen WeatherAPI-sleutel

    url = f'http://api.weatherapi.com/v1/forecast.json?key={api_key}&q={city},{country}&days=3'
    print(f"{url}")
    response = requests.get(url)
    data = response.json()

    forecast_days = data['forecast']['forecastday']


    def get_dag_van_de_week(date_string):
        dagen_van_de_week = ['Maandag', 'Dinsdag', 'Woensdag', 'Donderdag', 'Vrijdag', 'Zaterdag', 'Zondag']
        datum = datetime.strptime(date_string, '%Y-%m-%d')
        dag_index = datum.weekday()
        return dagen_van_de_week[dag_index]

    for day in forecast_days:
        day['dag_van_de_week'] = get_dag_van_de_week(day['date'])


    return render_template('forecast.html', country=country, city=city, forecast_days=forecast_days)

if __name__ == '__main__':
    app.run(debug=True)