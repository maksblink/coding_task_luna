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


def get_user_id(token):
    headers = {"Authorization": f"Token {token}"}
    response = requests.get(f"{BASE_URL}/me/", headers=headers)
    if response.status_code == 200:
        return response.json().get("id")
    else:
        print("❌ Błąd przy pobieraniu ID użytkownika:", response.json())
        return None



def create_hydroponic_system(token, name, description, user_id):
    headers = {"Authorization": f"Token {token}"}
    data = {"name": name, "description": description, "owner": user_id}
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

    if not token_user_1 or not token_user_2:
        return

    user1_id = get_user_id(token_user_1)
    user2_id = get_user_id(token_user_2)

    hydro1_A = create_hydroponic_system(token_user_1, "HydroSystem A", "duuuuupa A", user1_id)
    hydro1_B = create_hydroponic_system(token_user_1, "HydroSystem B", "duuuuupa B", user1_id)
    hydro1_C = create_hydroponic_system(token_user_1, "HydroSystem C", "duuuuupa C", user1_id)

    hydro2_A = create_hydroponic_system(token_user_2, "HydroSystem A", "duuuuupa A", user2_id)
    hydro2_B = create_hydroponic_system(token_user_2, "HydroSystem B", "duuuuupa B", user2_id)
    hydro2_C = create_hydroponic_system(token_user_2, "HydroSystem C", "duuuuupa C", user2_id)

    if all([hydro1_A, hydro1_B, hydro1_C, hydro2_A, hydro2_B, hydro2_C]):
        time.sleep(2)

        sensors1 = get_sensors(token_user_1, hydro1_A) + get_sensors(token_user_1, hydro1_B) + get_sensors(token_user_1, hydro1_C)
        sensors2 = get_sensors(token_user_2, hydro2_A) + get_sensors(token_user_2, hydro2_B) + get_sensors(token_user_2, hydro2_C)

        for sensor in sensors1:
            create_measurement(token_user_1, sensor["id"], 6.8)
            create_measurement(token_user_1, sensor["id"], 7.1)

        for sensor in sensors2:
            create_measurement(token_user_2, sensor["id"], 2.5)
            create_measurement(token_user_2, sensor["id"], 0.1)


if __name__ == "__main__":
    main()
