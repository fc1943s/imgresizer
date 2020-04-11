from PIL import Image
import unittest
import requests
import io
import random


class Tests(unittest.TestCase):
    def test_resize(self):
        img = Image.new("RGB", (random.randint(1, 1000), random.randint(1, 1000)), color="red")
        buffer = io.BytesIO()
        img.save(buffer, "JPEG")
        img_data = buffer.getvalue()

        r = requests.post("http://api:5000/resize", files={'img': ('img.jpg', img_data, 'image/jpeg')})

        self.assertEqual(200, r.status_code)

        img = Image.open(io.BytesIO(r.content))

        self.assertEqual((384, 384), img.size)

