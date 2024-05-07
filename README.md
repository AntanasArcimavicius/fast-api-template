# FastAPI + PostgreSQL + Celery + RabbitMQ (Dockerized)

## This repository provides a minimalistic example of a FastAPI application with:

    PostgreSQL Database: For data persistence.
    Celery + RabbitMQ: For asynchronous task queues.
    Simple Authentication: A dummy user for demonstration (username: johndoe, password: password1234).
    Docker Compose: For easy setup and running of all services.

## Getting Started

Clone the repository:

    git clone https://github.com/AntanasArcimavicius/fast-api-template

Run Docker Compose:

    cd fast-api-template
    docker-compose up -d

The application will be available at http://localhost:8000/.  
Rabbit UI will be available at http://localhost:15672/ with guest user

### Important Notes

Authentication is basic for demonstration purposes only. Implement robust authentication in production.
Explore the code to understand the integration of the technologies.
