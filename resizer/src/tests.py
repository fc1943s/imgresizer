import unittest
from PIL import Image
from . import app
import io
import random


class ResizeTests(unittest.TestCase):
    def test_resize(self):
        im = Image.new("RGB", (random.randint(1, 1000), random.randint(1, 1000)), color="red")
        buffer = io.BytesIO()
        im.save(buffer, "JPEG")

        buffer = app.resize(buffer)

        im = Image.open(buffer)
        self.assertEqual(app.default_image_size, im.size)


if __name__ == '__main__':
    unittest.main()

