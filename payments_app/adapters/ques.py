from celery import Celery

app = Celery("tasks", broker="amqp://guest:guest@rabbitmq:5672//")
