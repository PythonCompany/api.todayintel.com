# example_consumer.py
import pika, os, time
url = os.environ.get('CLOUDAMQP_URL', 'amqp://guest:guest@172.16.238.210:5672/my_vhost')
params = pika.URLParameters(url)
connection = pika.BlockingConnection(params)
channel = connection.channel() # start a channel
channel.queue_declare(queue='python') # Declare a queue
#The processors
def pdf_process_function(msg):
    channel = connection.channel()  # start a channel
    channel.queue_declare(queue='hello')  # Declare a queue
    channel.basic_publish(exchange='',
                          routing_key='hello',
                          body='Hello CloudAMQP!')


# create a function which is called on incoming messages
def callback(ch, method, properties, body):
  pdf_process_function(body)

# set up subscription on the queue
channel.basic_consume('python',
  callback,
  auto_ack=True)

# start consuming (blocks)
channel.start_consuming()
connection.close()