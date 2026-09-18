# BSIT Event Organizer System

Django implementation of the BSIT Event Organizer System.

## Features

- Administrator, Event Organizer, and Student roles
- Student accounts and profiles
- Dynamic student QR token that refreshes every 25 seconds with a server-synchronized countdown
- Server-side QR token validation
- Event management
- Event-day IN and OUT QR scanning
- Duplicate IN prevention
- OUT requires a valid IN
- Digital stamp awarded only after IN + OUT
- Student digital event card
- Student participation history
- Organizer attendance list and count
- Django admin interface

## Setup

Python 3.11+ is recommended.

```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open http://127.0.0.1:8000/

## Creating users

The easiest way to create users is Django admin:

1. Open `/admin/`
2. Create a User.
3. Create the corresponding Profile.
4. Set the Profile role to `STUDENT`, `ORGANIZER`, or `ADMIN`.

For a student, fill in Student ID, Program, and Year Level.

## QR scanning

The organizer opens an event and chooses IN or OUT. The scanner uses the browser camera through JavaScript.

Camera access normally requires HTTPS in production. `localhost`/`127.0.0.1` is generally allowed by browsers during local development.

## Dynamic QR

The student QR contains a signed temporary token. The token is valid for 25 seconds and does not directly expose the student ID. The server verifies the signature and expiration before accepting a scan. The student page reads the server-provided expiry timestamp, so the visible countdown and QR refresh stay synchronized even when the page is opened partway through a 25-second window.
