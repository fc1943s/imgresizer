from flask import Flask, request, send_file
import uuid
import pika
import io
import os


class Client:
    def __init__(self):
        self.response = None
        self.corr_id = None

    def publish(self, img_bytes):
        self.response = None
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=os.getenv("RABBITMQ_HOST", "localhost")))

        channel = connection.channel()
        callback_queue = channel.queue_declare(queue='', exclusive=True).method.queue
        channel.basic_consume(
            queue=callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True)

        self.corr_id = str(uuid.uuid4())
        channel.basic_publish(
            exchange='',
            routing_key='resize_rpc_queue',
            properties=pika.BasicProperties(
                reply_to=callback_queue,
                correlation_id=self.corr_id,
            ),
            body=img_bytes)
        while self.response is None:
            connection.process_data_events()

    def on_response(self, _ch, _method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, img_bytes):
        try:
            self.publish(img_bytes)
        except Exception as e:
            return None, f"Error trying to process image: {e}"

        if not self.response:
            return None, f"Unknown error while processing image."

        return self.response, None


client = Client()

app = Flask(__name__)


@app.route('/resize', methods=["POST"])
def resize():
    img_name = "img"
    if img_name not in request.files:
        return f"Image not uploaded (name={img_name})", 400

    file = request.files[img_name]

    if not file.mimetype.startswith("image/"):
        return "Invalid image", 400

    img_bytes = file.stream.read()

    print(f"Received image with {len(img_bytes)} bytes. Dispatching...")

    img_bytes, error = client.call(img_bytes)

    if img_bytes is None:
        return error, 400

    buffer = io.BytesIO(img_bytes)

    return send_file(buffer, mimetype="image/png")


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
