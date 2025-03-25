# Health API

This repository contains the Health API—a FastAPI application that manages patient medication requests.

## Getting Started

### Prerequisites

- **Python 3.10+**
- **Poetry** (for dependency management and virtual environment management)
- (Optional) **Docker** (for containerization)

### Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/abrarmudhir/health-api.git
   cd health-api
   ```

2. **Install Dependencies**
   Install the required packages using Poetry:
   ```bash
   poetry install
   ```

3. **Activate the Virtual Environment** (optional)
   To enter the Poetry-managed virtual environment:
   ```bash
   poetry shell
   ```

### Running the Application

A custom Poetry script has been set up to start the FastAPI server. Run the application in development mode with
hot-reloading by executing:

```bash
poetry run start
```

The server will start at [http://127.0.0.1:8000](http://127.0.0.1:8000).

### API Documentation

FastAPI automatically generates interactive API documentation. After starting the server, access:

- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

### Running Tests

Tests are written using Pytest. To run the test suite, execute:

```bash
poetry run pytest
```

### Linting and Static Type Checks

For static type checking with mypy, run:

```bash
poetry run mypy .
```

### Docker (Optional)

If you prefer containerization, build and run the application using Docker:

1. **Build the Docker image:**
   ```bash
   docker build -t health-api .
   ```

2. **Run the Docker container:**
   ```bash
   docker run -p 8000:8000 health-api
   ```

Alternatively, using Docker Compose, execute:

3. **Run the Docker container:**
   ```bash
   docker-compose up --build
   ```

4. **Cleanup**
   ```bash
   docker-compose down -v
   ```

### Configure Alembic

1. **Generate the Initial Migration**
   ```bash
   alembic revision --autogenerate -m "Initial migration"
   ```

2. **Apply the Migration**
   ```bash
   alembic upgrade head
   ```