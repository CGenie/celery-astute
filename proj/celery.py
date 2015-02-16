from __future__ import absolute_import

from celery import Celery

BROKER_URL = 'amqp://guest:guest@localhost:5672//'

app = Celery(broker=BROKER_URL,
             backend=BROKER_URL,
             propagate=True,
             include=['proj.tasks'])


if __name__ == '__main__':
    app.start()
