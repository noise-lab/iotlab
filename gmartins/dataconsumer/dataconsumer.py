#!/usr/bin/env python
import os, sys, dotenv
import pika
import ssl
import certifi
import traceback
from os.path import join, dirname
from dotenv import load_dotenv

#based on https://github.com/rabbitmq/rabbitmq-tutorials/blob/master/python/receive.py


class RabbitMQ(object):
   host = None
   port = 0
   user = None
   password = None
   cert = None
   keyf = None
   certpass = None
   topic = None

   def initRabbitMQ(self):
      if os.getenv('RABBITMQ_SSL_USER') is not None:
         self.user = os.getenv('RABBITMQ_SSL_USER')
      else:
         print("ERROR: RABBITMQ_SSL_USER not set, Exiting...")
         sys.exit(1)
      if os.getenv('RABBITMQ_SSL_PASS') is not None:
         self.password = os.getenv('RABBITMQ_SSL_PASS')
      else:
         print("ERROR: RABBITMQ_SSL_PASS not set, Exiting...")
         sys.exit(1)
      if os.getenv('RABBITMQ_SSL_HOST') is not None:
         self.host = os.getenv('RABBITMQ_SSL_HOST')
      else:
         print("ERROR: RABBITMQ_SSL_HOST not set, Exiting...")
         sys.exit(1)
      if os.getenv('RABBITMQ_SSL_PORT') is not None:
         self.port = os.getenv('RABBITMQ_SSL_PORT')
      else:
         print("ERROR: RABBITMQ_SSL_PORT not set, Exiting...")
         sys.exit(1)
      if os.getenv('RABBITMQ_SSL_CERTFILE') is not None:
         self.cert = os.getenv('RABBITMQ_SSL_CERTFILE')
      else:
         print("ERROR: RABBITMQ_SSL_CERTFILE not set, Exiting...")
         sys.exit(1)
      if os.getenv('RABBITMQ_SSL_PKEYFILE') is not None:
         self.keyf = os.getenv('RABBITMQ_SSL_PKEYFILE')
      else:
         print("ERROR: RABBITMQ_SSL_PKEYFILE not set, Exiting...")
         sys.exit(1)
      if os.getenv('RABBITMQ_SSL_CERTPASS') is not None:
         self.certpass = os.getenv('RABBITMQ_SSL_CERTPASS')
      else:
         print("ERROR: RABBITMQ_SSL_CERTPASS not set, Exiting...")
         sys.exit(1)
      if os.getenv('RABBITMQ_SSL_TOPIC') is not None:
         self.topic = os.getenv('RABBITMQ_SSL_TOPIC')
      else:
         print("ERROR: RABBITMQ_SSL_TOPIC not set, Exiting...")
         sys.exit(1)

def main():
  rabbitmq = RabbitMQ()
  rabbitmq.initRabbitMQ()
  connection = None
  credentials = pika.PlainCredentials(rabbitmq.user, rabbitmq.password)

  context = ssl.create_default_context(cafile=certifi.where());
  #basepath = os.path.join(os.path.dirname(__file__), "../")
  basepath = os.path.dirname(__file__)
  certfile = os.path.join(basepath, rabbitmq.cert)
  keyfile = os.path.join(basepath, rabbitmq.keyf)
  print("RabbitMQ SSL using {0} {1} from {2} to {3}:{4}".format(rabbitmq.cert, rabbitmq.keyf,\
    basepath, rabbitmq.host, rabbitmq.port))
  context.load_cert_chain(certfile, keyfile, rabbitmq.certpass)

  ssl_options = pika.SSLOptions(context, rabbitmq.host)
  try:
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq.host,
        port=int(rabbitmq.port),
        ssl_options = ssl_options,
        virtual_host='/',
        credentials=credentials))
  except Exception as e:
    exc_type, _, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    print("rabbitmq error: ({0}) {1} {2} {3}".format(str(e), exc_type, fname, exc_tb.tb_lineno))
    traceback.print_exc()
    sys.exit(1)
  channel = connection.channel()

  channel.queue_declare(queue=rabbitmq.topic)

  def callback(ch, method, properties, body):
      print("Message:\n%r" % body)

  channel.basic_consume(queue=rabbitmq.topic, on_message_callback=callback, auto_ack=True)

  print(' [*] Waiting for messages. To exit press CTRL+C')
  channel.start_consuming()

if __name__ == '__main__':
   load_dotenv(verbose=True)

   try:
        main()
   except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
