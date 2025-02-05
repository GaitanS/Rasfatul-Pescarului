# Răsfățul Pescarului

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/downloads/release/python-3120/)
[![Django](https://img.shields.io/badge/Django-5.1.5-green.svg)](https://www.djangoproject.com/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple.svg)](https://getbootstrap.com/)

Un magazin online pentru pescari, cu locații de pescuit și tutoriale video. Proiectul este dezvoltat folosind Django și oferă o experiență completă de cumpărături online, cu sistem de autentificare securizat, procesare plăți și gestionare comenzi.

## Funcționalități

### Magazin
- Listare produse cu filtrare pe categorii
- Detalii produs
- Coș de cumpărături
- Checkout cu plată prin card sau transfer bancar
- Sistem de comenzi și facturare

### Autentificare
- Înregistrare cu verificare email
- Autentificare cu protecție împotriva atacurilor brute force
- Resetare parolă
- Profil utilizator
- Istoric comenzi

### Locații de pescuit
- Hartă interactivă
- Filtrare pe județe
- Detalii locație (facilități, reguli, prețuri)

### Tutoriale
- Galerie video
- Categorii tutoriale
- Player video încorporat

## Tehnologii

- Python 3.12
- Django 5.1.5
- Bootstrap 5.3
- SQLite
- Stripe pentru plăți
- Google reCAPTCHA
- Google Maps API

## Instalare

1. Clonați repository-ul:
```bash
git clone https://github.com/GaitanS/Rasfatul-Pescarului.git
cd RasfatulPescarului
```

2. Creați și activați un mediu virtual:
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows
```

3. Instalați dependențele:
```bash
pip install -r requirements.txt
```

4. Creați fișierul .env și configurați variabilele de mediu:
```env
# Django settings
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Email settings
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=your-name <your-email@gmail.com>

# Email verification
EMAIL_VERIFICATION_TIMEOUT_DAYS=1
EMAIL_VERIFICATION_URL=http://localhost:8000/verify-email/

# reCAPTCHA settings
RECAPTCHA_PUBLIC_KEY=your-recaptcha-public-key
RECAPTCHA_PRIVATE_KEY=your-recaptcha-private-key
RECAPTCHA_REQUIRED_SCORE=0.85

# Stripe settings
STRIPE_PUBLIC_KEY=your-stripe-public-key
STRIPE_SECRET_KEY=your-stripe-secret-key
STRIPE_WEBHOOK_SECRET=your-stripe-webhook-secret
```

Pentru a obține cheile necesare:
- [Creați un cont Gmail și generați o parolă pentru aplicație](https://support.google.com/accounts/answer/185833?hl=ro)
- [Obțineți chei reCAPTCHA](https://www.google.com/recaptcha/admin)
- [Creați un cont Stripe și obțineți cheile API](https://stripe.com/docs/keys)

5. Aplicați migrările:
```bash
python manage.py migrate
```

6. Creați un superuser:
```bash
python manage.py createsuperuser
```

7. Populați baza de date cu date inițiale:
```bash
python manage.py populate_db
```

8. Rulați serverul de dezvoltare:
```bash
python manage.py runserver
```

## Structura proiectului

```
RasfatulPescarului/
├── main/                   # Aplicația principală
│   ├── management/        # Comenzi personalizate
│   ├── migrations/        # Migrări bază de date
│   ├── templatetags/      # Tag-uri template personalizate
│   ├── utils/            # Utilități (email, plăți, etc.)
│   ├── models.py         # Modele bază de date
│   ├── views.py          # View-uri
│   └── urls.py           # URL-uri
├── static/                # Fișiere statice
│   ├── css/
│   ├── js/
│   └── images/
├── templates/             # Template-uri
│   ├── account/          # Template-uri cont utilizator
│   ├── emails/           # Template-uri email
│   ├── locations/        # Template-uri locații
│   ├── shop/            # Template-uri magazin
│   └── tutorials/        # Template-uri tutoriale
├── media/                # Fișiere încărcate
├── requirements.txt      # Dependențe Python
└── manage.py            # Script management Django
```

## Securitate

- Protecție CSRF
- Rate limiting pentru autentificare
- Validare parolă complexă
- Verificare email
- Sesiuni securizate
- Sanitizare input
- XSS protection

## Contribuție

1. Fork repository-ul
2. Creați un branch nou (`git checkout -b feature/AmazingFeature`)
3. Faceți modificările dorite
4. Rulați testele și asigurați-vă că totul funcționează
5. Commit modificările (`git commit -m 'Add some AmazingFeature'`)
6. Push la branch (`git push origin feature/AmazingFeature`)
7. Deschideți un Pull Request

### Ghid de contribuție

1. Asigurați-vă că codul respectă standardele PEP 8
2. Adăugați comentarii și docstrings pentru cod nou
3. Actualizați documentația dacă este necesar
4. Adăugați teste pentru funcționalități noi
5. Verificați că toate testele existente trec

## Securitate

Dacă descoperiți o vulnerabilitate de securitate, vă rugăm să trimiteți un email la security@rasfatulpescarului.ro în loc să deschideți un issue public.

## Licență

Distribuit sub licența MIT. Vezi `LICENSE` pentru mai multe informații.
