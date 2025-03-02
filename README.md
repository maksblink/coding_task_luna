# coding_task_luna


Instalacja i konfiguracja

1. Klonowanie repozytorium

git clone https://github.com/maksblink/coding_task_luna.git

2. Tworzenie i aktywacja wirtualnego środowiska

python -m venv .venv
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate  # Windows

3. Instalacja zależności

pip install -r requirements.txt

4. Konfiguracja bazy danych

python manage.py migrate
python manage.py createsuperuser

5. Uruchomienie serwera

python manage.py runserver

Teraz aplikacja jest dostępna pod http://127.0.0.1:8000/.