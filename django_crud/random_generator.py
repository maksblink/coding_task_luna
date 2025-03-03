import requests
import time
import random

BASE_URL = "http://127.0.0.1:8000/api"
USERNAME = "testuser1"
PASSWORD = "dupa1234567"


def get_token(username, password):
    response = requests.post(f"{BASE_URL}/token/", json={"username": username, "password": password})
    if response.status_code == 200:
        return response.json().get("token")
    else:
        print("❌ Błąd logowania:", response.json())
        return None


def get_user_id(token):
    headers = {"Authorization": f"Token {token}"}
    response = requests.get(f"{BASE_URL}/me/", headers=headers)
    if response.status_code == 200:
        return response.json().get("id")
    else:
        print("❌ Błąd pobierania ID użytkownika:", response.json())
        return None


def get_hydroponic_systems(token):
    headers = {"Authorization": f"Token {token}"}
    response = requests.get(f"{BASE_URL}/hydroponic_system/", headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print("❌ Błąd pobierania systemów:", response.json())
        return []


def get_sensors(token, hydroponic_system_id):
    headers = {"Authorization": f"Token {token}"}
    response = requests.get(f"{BASE_URL}/sensors/?hydroponic_system={hydroponic_system_id}", headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"❌ Błąd pobierania czujników dla systemu {hydroponic_system_id}:", response.json())
        return []


def create_measurement(token, sensor_id, value):
    headers = {"Authorization": f"Token {token}"}
    data = {"sensor": sensor_id, "value": value}
    response = requests.post(f"{BASE_URL}/measurements/", headers=headers, json=data)

    if response.status_code == 201:
        print(f"✅ Pomiar {value} wysłany dla czujnika {sensor_id}")
    else:
        print(f"❌ Błąd przy wysyłaniu pomiaru {value}:", response.json())


def main():
    token = get_token(USERNAME, PASSWORD)
    if not token:
        return

    user_id = get_user_id(token)
    if not user_id:
        return

    print("📌 Pobieranie systemów hydroponicznych...")
    hydroponic_systems = get_hydroponic_systems(token)

    if not hydroponic_systems:
        print("⚠️ Brak systemów hydroponicznych, skrypt kończy działanie.")
        return

    print(f"✅ Znaleziono {len(hydroponic_systems)} systemów.")

    sensors = []
    for system in hydroponic_systems:
        system_id = system["id"]
        system_sensors = get_sensors(token, system_id)
        sensors.extend(system_sensors)

    if not sensors:
        print("⚠️ Brak czujników, skrypt kończy działanie.")
        return

    print(f"✅ Znaleziono {len(sensors)} czujników.")

    while True:
        print("⏳ Generowanie nowych pomiarów...")
        for sensor in sensors:
            random_value = round(random.uniform(0.0, 14.0), 2)  # pH w zakresie 0-14
            create_measurement(token, sensor["id"], random_value)

        print("⏳ Czekam 60 sekund na kolejne pomiary...")
        time.sleep(10)  # Czekaj 60 sekund


if __name__ == "__main__":
    main()
