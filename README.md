# Răsfățul Pescarului

Un magazin online pentru pescari, cu locații de pescuit și tutoriale video.

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
git clone [repository-url]
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
```
SECRET_KEY=your-secret-key
DEBUG=True
SITE_URL=http://localhost:8000

# Email
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Stripe
STRIPE_PUBLIC_KEY=your-stripe-public-key
STRIPE_SECRET_KEY=your-stripe-secret-key
STRIPE_WEBHOOK_SECRET=your-stripe-webhook-secret

# reCAPTCHA
RECAPTCHA_PUBLIC_KEY=your-recaptcha-public-key
RECAPTCHA_PRIVATE_KEY=your-recaptcha-private-key
```

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

1. Fork repository
2. Creați un branch nou (`git checkout -b feature/AmazingFeature`)
3. Commit modificările (`git commit -m 'Add some AmazingFeature'`)
4. Push la branch (`git push origin feature/AmazingFeature`)
5. Deschideți un Pull Request

## Licență

Distribuit sub licența MIT. Vezi `LICENSE` pentru mai multe informații.
