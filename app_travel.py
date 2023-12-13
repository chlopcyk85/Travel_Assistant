from flask import Flask, render_template, request
from datetime import datetime
from travel_assist import TravelAssistant
import requests
from datetime import datetime
from translate import Translator
from keys import Keys
from scrap import Petrol


app_travel = Flask(__name__)
assistant = TravelAssistant()


@app_travel.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        origin = request.form['startLocation']
        destination = request.form['DestLocation']
        try:
            consumption = float(request.form['petrol'].replace(",", "."))
        except ValueError:
            return "Nieprawidłowa wartość spalania. Wprowadź poprawną liczbę."
        fuel_type = request.form['paliwo']

        try:
            assistant.get_travel_data(origin, destination)
        except ValueError:
            return "Wprowadzono błędne adresy. Sprawdź poprawność adresów i spróbuj ponownie"
        weather_info = assistant.get_current_weather(destination)
        today_date = datetime.now().date()
        fuel_price = assistant.petrol(fuel_type)
        travel_distance = assistant.travel_data()

        try:
            travel_cost = assistant.cost(travel_distance, float(consumption), float(fuel_price))
        except ValueError:
            return " Wprowadzono błędne adresy. Sprawdź poprawność adresów i spróbuj ponownie "

        destination_description = assistant.get_city_info(destination)

        return render_template(
            'results.html',
            origin=origin,
            destination=destination,
            travel_distance=round(travel_distance, 2),
            today_date=today_date,
            fuel_95=assistant.cena_95,
            fuel_98=assistant.cena_98,
            fuel_on=assistant.cena_ON,
            fuel_lpg=assistant.cena_LPG,
            consumption=float(consumption),
            fuel_price=float(fuel_price),
            travel_cost=round(travel_cost, 2),
            weather_info=weather_info,
            destination_description=destination_description
        )

    return render_template('index.html')


@app_travel.route('/summary', methods=['POST'])
def summary():
    if request.method == 'POST':
        origin = request.form.get('startLocation')
        destination = request.form.get('DestLocation')
        try:
            consumption = float(request.form['petrol'].replace(",", "."))
        except ValueError:
            return "Nieprawidłowa wartość spalania. Wprowadź poprawną liczbę."
        fuel_type = request.form.get('paliwo')

        try:
            assistant.get_travel_data(origin, destination)
        except ValueError:
            return "Wprowadzono błędne adresy. Sprawdź poprawność adresów i spróbuj ponownie"

        weather_info = assistant.get_current_weather(destination)
        today_date = datetime.now().date()
        fuel_price = assistant.petrol(fuel_type)
        travel_distance = assistant.travel_data()
        try:
            travel_cost = assistant.cost(travel_distance, float(consumption), float(fuel_price))
        except ValueError:
            return "Wprowadzono błędne adresy. Sprawdź poprawność adresów i spróbuj ponownie"
        destination_description = assistant.get_city_info(destination)

        return render_template(
            'summary.html',
            travel_distance=round(travel_distance, 2),
            today_date=today_date,
            fuel_95=assistant.cena_95,
            fuel_98=assistant.cena_98,
            fuel_on=assistant.cena_ON,
            fuel_lpg=assistant.cena_LPG,
            consumption=float(consumption),
            fuel_price=float(fuel_price),
            travel_cost=round(travel_cost, 2),
            weather_info=weather_info,
            destination_description=destination_description,
            destination=destination,
            origin=origin
        )


if __name__ == "__main__":
    app_travel.run(debug=True)