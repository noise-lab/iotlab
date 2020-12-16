## RabbitMQ NetMicroscope Data Consumer for the IoT Lab.

#### Install intructions:

1. unzip env_and_cert.zip
2. python -m venv venv; source venv/bin/activate; python -m pip install -r requirements.txt
3. source .env; python dataconsumer.py

#### Consuming different types of data:

RABBITMQ_SSL_TOPIC=<data topic>; python dataconsumer.py
