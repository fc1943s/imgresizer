from PIL import Image
import pika
import io
import os


default_image_size = 384, 384


def resize(buffer):
    im = Image.open(buffer)
    print(f"Processing image of size {im.size}")
    out = im.resize(default_image_size)
    buffer = io.BytesIO()
    out.save(buffer, "PNG")
    return buffer


class Server:
    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=os.getenv("RABBITMQ_HOST", "localhost")))

        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='rpc_queue')

        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(queue='rpc_queue', on_message_callback=self.on_request)

    @staticmethod
    def on_request(ch, method, props, body):
        try:
            try:
                buffer = io.BytesIO(body)
                buffer = resize(buffer)
                img_bytes = buffer.getvalue()
                body = img_bytes
            except Exception as e:
                print(f"Error trying to resize image: {e}")
                body = []

            ch.basic_publish(exchange='',
                             routing_key=props.reply_to,
                             properties=pika.BasicProperties(correlation_id=props.correlation_id),
                             body=body)
            ch.basic_ack(delivery_tag=method.delivery_tag)
        except Exception as e:
            print(f"Error processing request: {e}")

    def listen(self):
        print("Awaiting RPC requests...")
        self.channel.start_consuming()


if __name__ == '__main__':
    Server().listen()

