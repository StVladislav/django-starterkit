# django-starterkit — Ready-to-Use Django Project Boilerplate

A ready-to-use Django project template for the rapid development and deployment of modern web applications.

---

## Features

- **Custom user model** with email authentication (easily extendable for any needs)
- **Djoser** and **DRF** for fast REST API development
- **PostgreSQL** with full-text search support (trigram, GinIndex)
- **Redis** and **Celery** (worker + beat) for background tasks
- **Flower** for Celery task monitoring
- **Docker Compose** for development and testing (everything starts with a single command)
- **Pre-configured systemd unit files** for server deployment (gunicorn, celery, celery-beat, and flower)
- **Celery task and schedule examples** (task launch, status check, and periodic tasks)
- **Full-text search examples** based on a ready-made model
- **WEBP image support** via ResizedImageField
- **Separated dev/prod environments** (different docker-compose and .env files)
- **Comprehensive Django boilerplate examples** — from models, serializers, and URL routing to endpoint tests, providing a solid foundation and reference for rapid development
- **Email sending with HTML templates** using Celery for asynchronous delivery, including a ready-to-use modern email template (`templates/emails/notification.html`)
- **Simple permission** use custom permision (`utils/permissions/IsAdminOrReadOnly`) as an example.

---

## Project Structure

- `config/` — Django settings
- `utils/` — helper utilities
- `src._test/` — API, Celery, full-text search, serializers and etc. examples
- `src.authentication/` — everything related to authentication and the User model
- `deploy/docker-compose.dev.yml` — launches all services for development
- `deploy/docker-prod/` — production files (docker-compose, Dockerfile, .env)
- `deploy/systemd/` — ready-to-use systemd unit files for server deployment
- `templates/emails/notification.html` — html example for email notification message

---

## Quick Start

1. **Clone the repository:**

```
git clone https://github.com/your-username/django-starterkit.git
cd django-starterkit/deploy
```

2. **Set up superuser, database and SMTP (email) credentials for develpment:**

```
Open .env in the deploy/.env and change default velues for superuser and database if you need.
```

**Note:** You can use default `.env` values at the first time. And don't forget to change them for `deploy/systemd/.env` or `deploy/docker-prod/.env` before production.

3. **Start development services:**

```
From /path/to/django-starterkit/deploy

docker compose -f docker-compose.dev.yml build
docker compose -f docker-compose.dev.yml up
```

After this, the following will be available:

- Django: http://localhost:8000/admin
- Flower: http://localhost:5555

**P.S. use *admin@datalizecrm.com* as the login and _123_ as the password for sign in to admin. You can change it into .env file**

3. **That's it!**  
   You can start developing right away without spending time on environment setup.

---

## Celery API Usage Examples

### 1. Launch a test Celery task (`src._test.views.run_celery_task`)

```
curl -X GET http://localhost:8000/api/test/run_celery_task/
```

**Response:**

```
JSON
{
    "status": "Task started successfully",
    "task_id": "f2c6c8c3-7b5e-4f8e-8c3e-..."
}
```

### 2. Check task status by ID (`src._test.views.check_celery_task`)

```
curl -X GET http://localhost:8000/api/test/check_celery_task/<task_id>/
```

Replace `<task_id>` with the value from the previous response.

**Example:**

```
curl -X GET http://localhost:8000/api/test/check_celery_task/f2c6c8c3-7b5e-4f8e-8c3e-...
```

**Possible responses:**

- If the task is still running:

```
JSON
{
    "status": "pending",
    "result": null
}
```

- If the task is finished:

```
JSON
{
    "status": "completed",
    "details": "Task finished successfully",
    "result": "your result"
}
```

---

## Product Search API Example (Full-text search, `src._test.views.search_product`)

For demonstration, the abstract product model `src._test.models.Product` is used, with the appropriate index defined.

```
curl -X GET "http://localhost:8000/api/test/product_search/?q=name"
```

---

## Key Features

### 1. Custom User Model — `src.authentication.models.User`

- Email authentication
- Easily extendable with new fields
- Hassle-free migration and future support

### 2. Celery & Flower Integration

- Fast launch and monitoring of background tasks
- API examples for task launching and status checking (`src._test.tasks` and `src._test.views`)
- Ready-to-use systemd units for production (`./deploy/systemd`)

### 3. PostgreSQL + Trigram Search

- Model example with GinIndex and trigram for fast search (`src._test.models`)
- API example for searching by name (`src._test.views`)

### 4. Image Processing

- Custom ResizedImageField with webp support (`utils.fields.ResizedImageField`)
- Example of automatic file cleanup on object deletion (`src._test.receivers`)

### 5. Environment Separation

- Local development (`docker-compose.dev.yml`)
- Production (`docker-prod/` and `systemd/`)

**P.S. systemd is preferred for production deployments**

---

## Testing & Examples

This section demonstrates how to use tests in django-starterkit with real-world examples.

---

### Note on Environment Setup and Running Dev Environment

- Environment variables required for email and other services are defined in the `.env` file located in the `deploy/` directory.
- For easiest setup and testing, navigate to the `deploy/` folder and run the development environment using Docker Compose:

  ```
  cd deploy/
  docker compose -f docker-compose.dev.yml build
  docker compose -f docker-compose.dev.yml up
  ```

- This will start all necessary services including Django, Celery, Redis, and others with the correct environment variables loaded.
- After the services are up, you can open the Django shell (`python manage.py shell`) inside the running container or your local environment to trigger email tasks.
- This approach ensures your development environment closely mirrors production settings while allowing quick iteration and testing.

---

### Email Notifications

- **Fully configured email sending** via Django with support for HTML templates.
- Uses **Celery** for asynchronous email delivery, ensuring non-blocking app performance.
- Includes a modern, responsive HTML email template located at:  
  `templates/emails/notification.html`
- The template supports dynamic content via context variables for easy customization.
- SMTP settings (e.g., Gmail) are configurable in `settings.py` and can be managed securely through environment variables.
- Provides a Celery task example that sends emails with both HTML and plain-text versions for maximum compatibility across email clients.
- Recommended for user notifications, registration confirmations, password resets, and other important messaging.

### Usage Example

To test email sending via Celery from the Django shell:

1.  Open the Django shell:
    ```
    python manage.py shell
    ```
2.  Import the task and trigger an email:

    ```
    from src._test.tasks import send_email_notification
    from datetime import datetime

    send_email_notification.delay(
        subject="Hello from django-starterkit",
        to_email="test@example.com",  # Replace with your email
        context={
            "subject": "Hello from django-starterkit",
            "message": "This is a test email sent from your Django application using Celery!",
            "action_url": "http://localhost:8000/",  # Optional: a link for the button
            "year": datetime.now().year,
        }
    )
    ```

    _(Note: Ensure your Celery worker is running for the email to be processed and sent.)_

---

### Authentication API Tests

- Uses Djoser and Django REST Framework.
- Shows how to customize Djoser serializers (e.g., password confirmation, additional user fields).
- Demonstrates proper configuration of authentication endpoints.
- Provides the examples of clean and maintainable API tests using `rest_framework.test.APITestCase`.
- Manages token authentication flows within tests.

All tests are located in the `src.authentication.tests` module.

To run the tests:

```
python manage.py test authentication
```

_Note for Windows users:_ set the environment variable before running:

```
$env:PYTHONPATH="src"
```

---

### Tests for the `_test` Demo App

- The example of a test for the product search endpoint.
- Illustrates how to write tests for business logic and API.

Tests are located in `src._test.tests`.

To run the tests:

```
python manage.py test _test
```

_Note for Windows users:_ set the environment variable before running:

```
$env:PYTHONPATH="src"
```

---

### Why This Matters

- Covers real-world scenarios: registration, login, password confirmation.
- Demonstrates best practices for integrating Djoser with a custom user model.
- Speeds up development with ready-to-use tests.
- Easy to extend test coverage (e.g., password reset, profile updates).

---

These tests serve as a valuable example for developers building on top of this starter kit or implementing similar authentication workflows.

## Deployment on Server

1. Install PostgreSQL server
2. Create database and install pg_trgm extension
3. Install Redis
4. Copy files from `deploy/systemd/` to your server's `/etc/systemd/system/`
5. Set up your environment variables (`/path/to/.env`)
6. Start services via systemd:

```
sudo systemctl daemon-reload

sudo systemctl start gunicorn
sudo systemctl start celery
sudo systemctl start celery-beat
sudo systemctl start flower
```

---

## Why is this useful?

- **Saves time:** No need to set up boilerplate every time
- **Production-ready:** Most best practices already implemented
- **Easy start:** One command to launch all services
- **Flexible:** Structure can be easily adapted for any project

---

## Contact & Support

If you have questions or suggestions, please open an issue or contact me at [sv6382@gmail.com](mailto:sv6382@gmail.com).

---

## License

MIT License

---

**Stars ⭐ and pull requests are welcome!**
