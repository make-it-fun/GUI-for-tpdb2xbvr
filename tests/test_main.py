from ui import Gui
import PySimpleGUI as sg
import unittest


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.gui = Gui()
        self.gui.window['-SCRAPE-'].update('Test Update Elems')
        while True:
            event, values = self.gui.window.read()
            print(event)
            if event == 'Exit' or event == sg.WIN_CLOSED:
                break
            if event == '-SCRAPE-':
                print('clicked -SCRAPE-')
                self.test_update_elems()


    def test_update_elems(self):

        self.gui.update_elems('tcast ', {'text_color' : 'pink', 'font' : 'default 10 normal'}, max=20, exclude=['-tcast 1-'])





if __name__ == '__main__':
    unittest.main()
