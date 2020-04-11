from PIL import Image
from retry import retry
import pika
import pika.exceptions
import io
import os
import logging

default_image_size = 384, 384


def resize(buffer):
    img = Image.open(buffer)
    print(f"Processing image of size {img.size}")
    out = img.resize(default_image_size)
    buffer = io.BytesIO()
    out.save(buffer, "PNG")
    return buffer


def on_message(channel, method, header, body):
    try:
        buffer = io.BytesIO(body)
        buffer = resize(buffer)
        img_bytes = buffer.getvalue()
        body = img_bytes
    except:
        logging.exception("Error trying to resize image")
        body = []

    channel.basic_publish(exchange='',
                          routing_key=header.reply_to,
                          properties=pika.BasicProperties(correlation_id=header.correlation_id),
                          body=body)
    channel.basic_ack(delivery_tag=method.delivery_tag)


@retry(pika.exceptions.AMQPConnectionError, delay=5, jitter=(1, 3))
def consume():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=os.getenv("RABBITMQ_HOST", "localhost")))

    channel = connection.channel()
    channel.queue_declare(queue='resize_rpc_queue')
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='resize_rpc_queue', on_message_callback=on_message)

    try:
        print("Awaiting RPC requests...")
        channel.start_consuming()
    except KeyboardInterrupt:
        channel.stop_consuming()
        connection.close()
    except pika.exceptions.ConnectionClosedByBroker:
        pass


if __name__ == '__main__':
    logging.basicConfig()
    consume()
