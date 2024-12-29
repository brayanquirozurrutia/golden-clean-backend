# Golden Clean Backend

This is the backend for the **Golden Clean** project, developed with Django and Docker.

## Requirements

- Python 3.10+
- Docker and Docker Compose

## Initial Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/brayanquirozurrutia/golden-clean-backend.git
   cd golden-clean-backend
   ```

2. Create the `.env` file based on `sample.env`:
   ```bash
   cp sample_env .env
   ```

   Then edit the `.env` file to configure your values.

3. Generate a new `SECRET_KEY`:
   ```bash
   python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
   ```

   Copy and paste this key into the `SECRET_KEY` field in the `.env` file.

4. Build and start the containers with Docker:
   ```bash
   docker-compose up --build
   ```

5. Apply database migrations:
   ```bash
   docker exec -it golden-clean-backend-web-1 python manage.py migrate
   ```

6. Access the application at [http://localhost:8000](http://localhost:8000).

## Project Structure

- **`sample.env`**: Template for environment variables.
- **`Dockerfile`**: Configuration to build the Docker image.
- **`docker-compose.yml`**: Docker services orchestration.
- **`requirements.txt`**: Project dependencies.

## Author

Developed with ❤️ by [Brayan Nicolas Quiroz Urrutia](https://github.com/brayanquirozurrutia).
