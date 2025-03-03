import requests
import time


BASE_URL = "http://127.0.0.1:8000/api"
USERNAMES = ["testuser1", "testuser2"]
PASSWORDS = ["dupa1234567", "dupa1234567"]


def register_and_get_token(id):
    print("📌 Rejestracja użytkownika...")
    requests.post(f"{BASE_URL}/register/", json={"username": USERNAMES[id], "password": PASSWORDS[id]})

    time.sleep(1)

    print("📌 Pobieranie tokenu...")
    response = requests.post(f"{BASE_URL}/token/", json={"username": USERNAMES[id], "password": PASSWORDS[id]})
    if response.status_code == 200:
        token = response.json().get("token")
        print(f"✅ Token pobrany: {token}")
        return token
    else:
        print("❌ Nie udało się pobrać tokena:", response.json())
        return None


def create_hydroponic_system(token, name, description):
    headers = {"Authorization": f"Token {token}"}
    data = {"name": name, "description": description}
    response = requests.post(f"{BASE_URL}/hydroponic_system/", headers=headers, json=data)

    if response.status_code == 201:
        hydroponic_system_id = response.json()["id"]
        print(f"✅ System '{name}' utworzony (ID: {hydroponic_system_id})")
        return hydroponic_system_id
    else:
        print("❌ Błąd przy tworzeniu systemu:", response.json())
        return None


def get_sensors(token, hydroponic_system_id):
    headers = {"Authorization": f"Token {token}"}
    response = requests.get(f"{BASE_URL}/sensors/", headers=headers)

    if response.status_code == 200:
        sensors = [s for s in response.json() if s["hydroponic_system"] == hydroponic_system_id]
        print(f"✅ Znaleziono {len(sensors)} czujniki dla systemu {hydroponic_system_id}.")
        return sensors
    else:
        print("❌ Błąd przy pobieraniu czujników:", response.json())
        return []


def create_measurement(token, sensor_id, value):
    headers = {"Authorization": f"Token {token}"}
    data = {"sensor": sensor_id, "value": value}
    response = requests.post(f"{BASE_URL}/measurements/", headers=headers, json=data)

    if response.status_code == 201:
        print(f"✅ Dodano pomiar {value} do czujnika {sensor_id}")
    else:
        print("❌ Błąd przy dodawaniu pomiaru:", response.json())


def main():
    token_user_1 = register_and_get_token(0)
    token_user_2 = register_and_get_token(1)

    if not token_user_1:
        return

    hydroponic_system_A_user_1 = create_hydroponic_system(token_user_1, "HydroSystem A", "duuuuupa A")
    hydroponic_system_B_user_1 = create_hydroponic_system(token_user_1, "HydroSystem B", "duuuuupa B")
    hydroponic_system_C_user_1 = create_hydroponic_system(token_user_1, "HydroSystem C", "duuuuupa C")

    if hydroponic_system_A_user_1 and hydroponic_system_B_user_1 and hydroponic_system_C_user_1:
        time.sleep(2)

        sensors1 = get_sensors(token_user_1, hydroponic_system_A_user_1)
        sensors2 = get_sensors(token_user_1, hydroponic_system_B_user_1)
        sensors3 = get_sensors(token_user_1, hydroponic_system_C_user_1)

        for sensor in sensors1 + sensors2 + sensors3:
            create_measurement(token_user_1, sensor["id"], 6.8)
            create_measurement(token_user_1, sensor["id"], 7.1)

    if not token_user_1:
        return

    hydroponic_system_A_user_2 = create_hydroponic_system(token_user_2, "HydroSystem A", "duuuuupa A")
    hydroponic_system_B_user_2 = create_hydroponic_system(token_user_2, "HydroSystem B", "duuuuupa B")
    hydroponic_system_C_user_2 = create_hydroponic_system(token_user_2, "HydroSystem C", "duuuuupa C")

    if hydroponic_system_A_user_2 and hydroponic_system_B_user_2 and hydroponic_system_C_user_2:
        time.sleep(2)

        sensors1 = get_sensors(token_user_2, hydroponic_system_A_user_2)
        sensors2 = get_sensors(token_user_2, hydroponic_system_B_user_2)
        sensors3 = get_sensors(token_user_2, hydroponic_system_C_user_2)

        for sensor in sensors1 + sensors2 + sensors3:
            create_measurement(token_user_2, sensor["id"], 2.5)
            create_measurement(token_user_2, sensor["id"], 0.1)


if __name__ == "__main__":
    main()
