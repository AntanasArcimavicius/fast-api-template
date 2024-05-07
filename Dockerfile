# https://fastapi.tiangolo.com/deployment/docker/
FROM python:3.10-slim as requirements-stage

WORKDIR /tmp

RUN pip install poetry

COPY ./pyproject.toml ./poetry.lock* /tmp/
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

FROM python:3.10-slim

WORKDIR /code

COPY --from=requirements-stage /tmp/requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./payments_app /code/payments_app

CMD ["uvicorn", "payments_app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]