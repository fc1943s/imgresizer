import unittest
from PIL import Image
from . import app
import io
import random


class ResizeTests(unittest.TestCase):
    def test_resize(self):
        img = Image.new("RGB", (random.randint(1, 1000), random.randint(1, 1000)), color="red")
        buffer = io.BytesIO()
        img.save(buffer, "JPEG")

        buffer = app.resize(buffer)

        img = Image.open(buffer)
        self.assertEqual(app.default_image_size, img.size)


if __name__ == '__main__':
    unittest.main()

