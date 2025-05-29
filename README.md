# 🌱 Django CRUD API - Hydroponic System

## 📌 Opis projektu

Ten projekt to aplikacja Django z REST API umożliwiająca zarządzanie systemami hydroponicznymi, czujnikami oraz ich pomiarami. Pozwala użytkownikom na rejestrację, autoryzację oraz operacje CRUD (Create, Read, Update, Delete) na danych.

---

## 🚀 Instalacja

1️⃣ **Klonowanie repozytorium**

```sh
git clone https://github.com/maksblink/coding_task_luna.git
cd django_crud
```

2️⃣ **Utworzenie i aktywacja środowiska wirtualnego**

```sh
python -m venv .venv
source .venv/bin/activate # macOS/Linux
source .venv\Scripts\activate # Windows
```

3️⃣ **Instalacja zależności**

```sh
pip install -r requirements.txt
```

4️⃣ **Migracje bazy danych**

```sh
python manage.py migrate
```

5️⃣ **Tworzenie użytkownika administratora** (opcjonalnie)

```sh
python manage.py createsuperuser
```

---

## 🛠 Uruchamianie aplikacji

```sh
python manage.py runserver
```

Aplikacja będzie dostępna pod adresem: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## 🐟 Populate DB i Random
Aby zasilić bazę danych przykładowymi danymi,

### Można skorzystać z polecenia:

```sh
python populate_db
```

Następnie aby generować losowe dane od czujników, można skorzystać z polecenia:

```sh
python random_generator.py
```

---

## 🌀 Endpoints API

### 🔑 Autoryzacja
| Metoda | Endpoint                     | Opis | Autoryzacja |
|-|-|-|-|
| `POST` | `/api/register/` | Rejestracja użytkownika | Nie wymagana ❌ |
| `POST` | `/api/token/` | Pobranie tokenu autoryzacji | Nie wymagana ❌ |

📝 Rejestracja użytkownika (Metoda `POST`)
-
📩 Body (przykładowe):

```sh
{
    "username": "testuser77",
    "email": "test@example.com",
    "password": "securepassword123"
}
```

🔄 Odpowiedź (przykładowa):

```sh
{
    "token": "3da872696b0c61812328d0602867df7090811b06",
    "message": "Rejestracja zakończona sukcesem"
}
```

📝 Pobieranie tokenu (Metoda `POST`)
-
📩 Body (przykładowe):

```sh
{
    "username": "testuser77",
    "password": "securepassword123"
}
```

🔄 Odpowiedź (przykładowa):

```sh
{
    "token": "3da872696b0c61812328d0602867df7090811b06"
}
```

---

## 🌱 Systemy hydroponiczne
| Metoda | Endpoint                     | Opis | Autoryzacja |
|-|-|-|-|
| `GET` | `/api/hydroponic_system/`    | Pobranie listy systemów hydroponicznych | Wymagana ✅ |
| `POST` | `/api/hydroponic_system/`    | Dodanie nowego systemu hydroponicznego | Wymagana ✅ |
| `PUT` | `/api/hydroponic_system/<int>/` | Edycja systemu hydroponicznego | Wymagana ✅ |
| `PATCH` | `/api/hydroponic_system/<int>/` | Częściowa aktualizacja systemu hydroponicznego | Wymagana ✅ |
| `DELETE` | `/api/hydroponic_system/<int>/` | Usunięcie systemu hydroponicznego | Wymagana ✅ |

📝 Dodanie nowego systemu hydroponicznego (Metoda `POST`)
-
📩 Body (przykładowe):

```sh
{
    "name": "HydroSystem A",
    "description": "Opis A"
}
```
Pamiętaj o autoryzacji (token).

🔄 Odpowiedź (przykładowa):

```sh
{
    "id": 91,
    "name": "HydroSystem A",
    "description": "Opis A",
    "created_at": "2025-03-05T15:17:34.989539Z",
    "updated_at": "2025-03-05T15:17:34.989539Z",
    "sensors": [
        "sensor_type = pH, hydroponic_system = HydroSystem A",
        "sensor_type = temperature, hydroponic_system = HydroSystem A",
        "sensor_type = TDS, hydroponic_system = HydroSystem A"
    ]
}
```

📝 Edycja systemu hydroponicznego (Metoda `PUT`)
-
📩 Body (przykładowe):

```sh
{
    "name": "HydroSystem A",
    "description": "Opis A"
}
```
Pamiętaj o autoryzacji (token).

🔄 Odpowiedź (przykładowa):

```sh
{
    "id": 91,
    "name": "HydroSystem A",
    "description": "Opis A",
    "created_at": "2025-03-05T15:17:34.989539Z",
    "updated_at": "2025-03-05T15:17:34.989539Z",
    "sensors": [
        "sensor_type = pH, hydroponic_system = HydroSystem A",
        "sensor_type = temperature, hydroponic_system = HydroSystem A",
        "sensor_type = TDS, hydroponic_system = HydroSystem A"
    ]
}
```

📝 Częściowa aktualizacja systemu hydroponicznego (Metoda `PATCH`)
-
📩 Body (przykładowe):

```sh
{
    "description": "Nowy opis"
}
```

🔄 Odpowiedź (przykładowa):

```sh
{
    "id": 96,
    "name": "HydrsadasdasoSystem A",
    "description": "Nowy safdasfasfopis",
    "created_at": "2025-05-18T19:23:46.340176Z",
    "updated_at": "2025-05-18T19:27:41.859787Z",
    "sensors": [
        "sensor_type = pH, hydroponic_system = HydrsadasdasoSystem A",
        "sensor_type = temperature, hydroponic_system = HydrsadasdasoSystem A",
        "sensor_type = TDS, hydroponic_system = HydrsadasdasoSystem A"
    ]
}

```

---

## 💽 Czujniki
| Metoda | Endpoint              | Opis | Autoryzacja |
|-|-----------------------|-|-|
| `GET` | `/api/sensors/`       | Pobranie listy czujników       | Wymagana ✅ |
| `POST` | `/api/sensors/`       | Dodanie nowego czujnika        | Wymagana ✅ |
| `PUT` | `/api/sensors/<int>/` | Edycja czujnika                | Wymagana ✅ |
| `PATCH` | `/api/sensors/<int>/` | Częściowa aktualizacja czujnika | Wymagana ✅ |
| `DELETE` | `/api/sensors/<int>/` | Usunięcie czujnika             | Wymagana ✅ |

📝 Dodanie nowego czujnika (Metoda `POST`)
-
📩 Body (przykładowe):

```sh
{
    "sensor_type": "temperature",
    "hydroponic_system": 91
}
```
Pamiętaj o autoryzacji (token).

🔄 Odpowiedź (przykładowa):

```sh
{
    "id": 240,
    "hydroponic_system": 91,
    "sensor_type": "temperature",
    "measurements": []
}
```

📝 Edycja czujnika (Metoda `PUT`)
-
📩 Body (przykładowe):

```sh
{
    "sensor_type": "pH",
    "hydroponic_system": 86
}
```
Pamiętaj o autoryzacji (token).

🔄 Odpowiedź (przykładowa):

```sh
{
    "id": 259,
    "hydroponic_system": 86,
    "sensor_type": "pH",
    "measurements": []
}
```

📝 Częściowa aktualizacja czujnika (Metoda `PATCH`)
-
📩 Body (przykładowe):
```sh
{
    "sensor_type": "TDS"
}
```
Pamiętaj o autoryzacji (token).

🔄 Odpowiedź (przykładowa):

```sh
{
    "id": 259,
    "hydroponic_system": 86,
    "sensor_type": "TDS",
    "measurements": []
}
```

---

## 📊 Pomiary
| Metoda   | Endpoint                   | Opis | Autoryzacja |
|----------|----------------------------|-|------------|
| `GET`    | `/api/measurements/`       | Pobranie listy pomiarów | Wymagana ✅ |
| `POST`   | `/api/measurements/`       | Dodanie nowego pomiaru | Wymagana ✅ |
| `PUT`    | `/api/measurements/<int>/` | Edycja czujnika | Wymagana ✅ |
| `PATCH`  | `/api/measurements/<int>/` | Częściowa aktualizacja pomiaru | Wymagana ✅ |
| `DELETE` | `/api/measurements/<int>/` | 	Usunięcie pomiaru | Wymagana ✅ |

📝 Dodanie  nowego pomiaru (Metoda `POST`)
-
📩 Body (przykładowe):
```sh
{
    "sensor": 221,
    "value": 22.5,
    "timestamp": "2024-03-05T12:00:00Z"
}
```
Pamiętaj o autoryzacji (token).

🔄 Odpowiedź (przykładowa):

```sh
{
    "id": 15622,
    "sensor": 221,
    "value": 22.5,
    "timestamp": "2025-05-18T19:55:54.550437Z"
}
```

📝 Edycja pomiaru (Metoda `PUT`)
-
📩 Body (przykładowe):

```sh
{
    "id": 15622,
    "sensor": 221,
    "value": 34.7,
    "timestamp": "2025-05-18T19:55:54.550437Z"
}
```
Pamiętaj o autoryzacji (token).

🔄 Odpowiedź (przykładowa):

```sh
{
    "id": 15622,
    "sensor": 221,
    "value": 34.7,
    "timestamp": "2025-05-18T19:55:54.550437Z"
}
```

📝 Częściowa aktualizacja pomiaru (Metoda `PATCH`)
-
📩 Body (przykładowe):
```sh
{
    "value": 5.0
}
```

🔄 Odpowiedź (przykładowa):

```sh
{
    "id": 15622,
    "sensor": 221,
    "value": 5.0,
    "timestamp": "2025-05-18T19:55:54.550437Z"
}
```

---

## 🛠 Technologie
✅ **Python 3.12**  
✅ **Django REST Framework**  
✅ **PostgreSQL**  

---

## 👨‍💻 Autorzy
👤 **Maksymilian Moskwytyn**

📧 **Email: moskwytyn.maksymilian@gmail.com**

🔗 **GitHub: https://github.com/maksblink/**

---

## 📚 Licencja
Projekt udostępniany na licencji MIT.
