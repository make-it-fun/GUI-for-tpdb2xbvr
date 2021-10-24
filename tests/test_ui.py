from ui import Gui
from pathlib import Path
from PIL import Image, ImageTk
import os


import unittest


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        # gui has paths relative to the root folder
        os.chdir('..')
        self.gui = Gui()

    # converts a '.webp' file to a '.png', then opens it
    def test_img_convert_webp(self):
        source = 'tests/data/test.webp'
        dest = 'tests/data/test.png'
        Path(dest).unlink(missing_ok=True)  # remove dest file if it exists
        self.gui.img_convert_webp(source, dest)
        img = Image.open(dest)
        img.show()


if __name__ == '__main__':
    unittest.main()
