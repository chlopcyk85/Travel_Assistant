import requests
from datetime import datetime
from translate import Translator
from keys import Keys
from scrap import Petrol


class TravelAssistant:
    def __init__(self):
        self.api_openai = Keys.api_openai
        self.api_key = Keys.api_key
        self.api_weather = Keys.api_weather
        self.petrol_data = Petrol()
        self.cena_95 = self.petrol_data.cena_95
        self.cena_98 = self.petrol_data.cena_98
        self.cena_ON = self.petrol_data.cena_ON
        self.cena_LPG = self.petrol_data.cena_LPG
        self.data = None

    def translate(self, text, lang="pl"):
        translator = Translator(to_lang=lang)
        translated_text = translator.translate(text)
        return translated_text

    def get_current_weather(self, city):
        base_url = "http://api.openweathermap.org/data/2.5/weather"
        params = {"q": city, "appid": self.api_weather, "units": "metric"}

        response = requests.get(base_url, params=params)
        data = response.json()

        if response.status_code == 200:
            temperature = data.get("main", {}).get("temp", "")
            description = data.get("weather", [])[0].get("description", "")
            translated_description = self.translate(description)

            return f"Temperatura w {city.capitalize()}: {temperature}°C, \nwarunki pogodowe to: {translated_description.capitalize()}"
        else:
            return "Błąd pobierania danych z aplikacji pogodowej"

    def get_travel_data(self, origin, destination):
        url_google = "https://maps.googleapis.com/maps/api/distancematrix/json?"

        if origin is not None:
            r_maps = requests.get(url_google + 'origins=' + origin +
                                  '&destinations=' + destination +
                                  '&key=' + self.api_key)

            if r_maps.status_code == 200:
                self.data = r_maps.json()
                return self.data
            else:
                return "Błąd pobierania danych z Google Maps"
        else:
            return "Podaj poprawny adres początkowy"

    def usage_petrol(self):
        while True:
            spalanie = input("Podaj ile spala Twój samochód na 100 km?: ")
            spalanie = spalanie.replace(",", ".")
            if spalanie.replace(".", "", 1).isdigit():
                return float(spalanie)
            else:
                print("Podaj poprawną wartość")

    def petrol(self, fuel_type):
        if fuel_type == "1":
            return float(self.cena_95)
        elif fuel_type == "2":
            return float(self.cena_98)
        elif fuel_type == "3":
            return float(self.cena_ON)
        elif fuel_type == "4":
            return float(self.cena_LPG)
        else:
            print("\nNieprawidłowy wybór paliwa, spróbuj ponownie\n")
            return 0.0

    def get_engine_type(self, fuel_type):
        if fuel_type == "1":
            return "silnikiem benzynowym"
        elif fuel_type == "2":
            return "silnikiem benzynowym"
        elif fuel_type == "3":
            return "silnikiem diesel"
        elif fuel_type == "4":
            return "silnikiem zasilanym LPG"
        else:
            print("\nNieprawidłowy wybór paliwa, spróbuj ponownie\n")
            return ""

    def get_city_info(self, destination):
        url = "https://api.openai.com/v1/chat/completions"

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_openai}"
        }
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"Opowiedz mi w paru zdaniach, krótko o miejscu podróży {destination}."},
            ]
        }
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            response_json = response.json()
            destination_description = response_json['choices'][0]['message']['content']
            return destination_description
        else:
            return " # Błąd pobrania informacji o miejscu docelowym, sprawdź połączenie z internetem lub klucze API #"


    def travel_data(self):
        try:
            travel = self.data["rows"][0]["elements"][0]["distance"]["value"]
        except KeyError:
            return "\n # Błędne adresy. Sprawdź poprawność adresów i spróbuj ponownie. #"
            exit()
        travel = travel / 1000
        return travel

    def cost(self, travel, spalanie, cena):
        travel_cost = ((float(travel) / 100) * float(spalanie)) * float(cena)
        return travel_cost

    def run(self):
        origin = input("Skąd rozpoczynasz swoją podróż?: ")
        destination = input("Podaj cel swojej podróży: ")

        fuel_type = input(
            """Jakiego paliwa używasz?
        1) Benzyna e95
        2) Benzyna e98
        3) Ropa ON
        4) LPG
        Wybór (1-4): """
        )
        fuel_price = self.petrol(fuel_type)
        rodzaj_silnika = self.get_engine_type(fuel_type)
        self.get_travel_data(origin, destination)
        weather_info = self.get_current_weather(destination)
        dzisiejsza_data = datetime.now().date()
        spalanie = self.usage_petrol()
        travel = self.travel_data()
        travel_cost = self.cost(travel, spalanie, fuel_price)
        destination_description = self.get_city_info(destination)

        print(f"\n # Odległość z {origin.capitalize()} do {destination.capitalize()} wynosi - {round(travel, 2)} km # ")
        print(f"\nNa dzień {dzisiejsza_data} średnie aktualne ceny paliw w Polsce wynoszą: ")
        print(f"* Cena benzyna E95 wynosi {self.cena_95} zł/l.")
        print(f"* Cena benzyna E98 wynosi {self.cena_98} zł/l.")
        print(f"* Cena paliwa ON wynosi {self.cena_ON} zł/l.")
        print(f"* Cena paliwa LPG wynosi {self.cena_LPG} zł/l.\n")
        print(f"Koszt podróży samochodem {rodzaj_silnika} wynosi {round(travel_cost, 2)} zł")
        print(weather_info)
        print(destination_description)


if __name__ == "__main__":
    assistant = TravelAssistant()
    assistant.run()
