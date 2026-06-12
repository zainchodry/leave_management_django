# Student Leave Management (Django)

A lightweight Django application for managing student leave requests, approvals, and attendance integration. This repository contains the Django project scaffold and apps for accounts, attendance, and leave management.

**Quick links**

- **Project entry:** [manage.py](manage.py)
- **Settings:** [core/settings.py](core/settings.py)
- **Apps:** [accounts/](accounts), [attendance/](attendance), [leave_management/](leave_management)

**Features**

- Submit and track leave requests
- Approve/reject requests (admin/staff interface)
- Attendance integration hooks
- User accounts, authentication, and signals

**Tech stack**

- Python 3.10+ (or compatible)
- Django 3.2+/4.x
- SQLite (default for development)

**Requirements**

- Git
- Python 3.10+ installed
- A virtual environment tool (venv, virtualenv, or similar)

**Development setup (local)**

1. Clone the repository

   git clone <repo-url>
   cd student_leave_management_django

2. Create and activate a virtual environment

   python -m venv venv
   source venv/bin/activate

3. Install dependencies
   - If a `requirements.txt` exists:

     pip install -r requirements.txt

   - If not, install Django and common packages:

     pip install django

4. Create local settings and environment variables

- Copy or create a `.env` (or set environment variables) for secrets, e.g., `SECRET_KEY`, `DATABASE_URL` if using non-default DB. The project reads settings from [core/settings.py](core/settings.py).

5. Apply migrations

   python manage.py migrate

6. (Optional) Create a superuser to access the admin

   python manage.py createsuperuser

7. Run the development server

   python manage.py runserver

Open http://127.0.0.1:8000/ in your browser.

**Database & media**

- By default the project uses SQLite (`db.sqlite3`) for development. If you change to Postgres or another DB, update [core/settings.py](core/settings.py) and provide DB credentials via environment variables.
- Uploaded files (media) are typically stored in a `media/` directory; ensure it's writable and added to `.gitignore` (already included).

**Running tests**

    python manage.py test

**Common management commands**

- Run migrations: `python manage.py migrate`
- Create superuser: `python manage.py createsuperuser`
- Collect static files for deployment: `python manage.py collectstatic`
- Run tests: `python manage.py test`

**Static files & collectstatic**

- For production, set `STATIC_ROOT` in [core/settings.py](core/settings.py) and run `collectstatic` before serving static files from a web server or CDN.

**Environment variables**

- Recommended variables: `SECRET_KEY`, `DEBUG` (False in production), `ALLOWED_HOSTS`, and any database credentials. Keep secrets out of the repository.

**Deployment notes**

- Use a production-ready WSGI server (Gunicorn/uvicorn) behind a reverse proxy (Nginx).
- Configure secure settings: disable `DEBUG`, set proper `ALLOWED_HOSTS`, enable HTTPS, and store secrets in environment variables or a secrets manager.
- Use a production database (Postgres recommended) and configure connection pooling.

**Contributing**

- Fork the repo, create a feature branch, add tests, and open a pull request. Keep changes focused and include migration files when DB models change.

**License**

- Add your preferred license (e.g., MIT) to the repository root as `LICENSE`.

**Contact / Maintainers**

- Provide a contact email or GitHub handle here if you'd like contributors to reach out.
