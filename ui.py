import constants
import PySimpleGUI as sg
from pathlib import Path
from PIL import Image, ImageTk, UnidentifiedImageError
from webptools import dwebp  # pip install webptools
import io
import os
import datetime
import requests
import shutil
from pprint import pprint
from typing import Union, List


def row(elems: Union[str, list] = '', events=True, size=(12, 1), size2=(50, 1), font=('default', 10, 'normal'),
        text_color='#3e64ff') -> list:
    """
    Returns a pair with a Text element followed by an Inpux element.
    Textbox receives tha key '-tElem-'
    Inputbox receives the key '-iElem-'
    :param elems: list or str label of element and is also used for key
    :param events: bool whether events are enabled (e.g. interactive)
    :param size: size of textbox
    :param size2: size of inputbox
    :param font: ('Font Name', font size, 'font weight') e.g. ('Arial', 10, 'bold')
    :param text_color: str valid color or #hexcolor
    """
    if type(elems) != list:
        elems = [elems]
    elif type(elems) == list:
        pass
    retval = []

    for elem in elems:
        retval.append(sg.T(elem, size=size, key=f'-t{elem}-', font=font, text_color=text_color, enable_events=events))
        retval.append(sg.I(size=size2, key=f'-i{elem}-', enable_events=events))
    return retval


class Gui:

    def __init__(self):

        col1 = [
            [
                sg.Text('Scraper', text_color='#ffa0dc', font=('BRADDON', 20), size=(35, 1),
                        justification='center')
            ],
            [
                sg.Button('Scrape', size=(30, 1), key='-SCRAPE-', button_color=('black', '#ffa0dc'),
                          enable_events=True),
                sg.Button('Start Webserver {BETA}', size=(30, 1), key='-WEBSERVER BUTTON-', enable_events=True)
            ],
            [sg.T('Webserver URL '),
             sg.I(key='-WEBSERVER-', size=(42, 1), background_color='light yellow', enable_events=True),
             sg.T('Port'), sg.I(key='-PORT-', size=(5, 1), background_color='light yellow', enable_events=True)],
            [
                sg.T('ThePornDB Key'),
                sg.I(key='-API KEY-', size=(42, 1), background_color='light yellow', enable_events=True),
                sg.Button('Save Config', size=(8, 1), key='-SAVE CONFIG-', enable_events=True, pad=(7, 0))
            ],
            [sg.HorizontalSeparator()],
            [sg.T('ThePornDB URL', text_color='#000000', key='-tThePornDB URL-'),
             sg.I('', key='-iThePornDB URL-', size=(42, 1), enable_events=True),
             sg.Button('Export', size=(8, 1), key='-EXPORT-', enable_events=True), ],
            [sg.HorizontalSeparator()],
            row('title'),
            row('studio'),
            row('site'),
            row('_id'),
            row('scene_id'),
            row('scene_type'),
            row('synopsis'),
            row('released'),
            row('homepage_url'),
            row('covers'),
            row('gallery'),

            [
                sg.Text('Tags', font=('Default', 12, 'bold'))
            ],
            [
                sg.Input(size=(15, 1), key='-itag1-'), sg.Input(size=(15, 1), key='-itag2-'),
                sg.Input(size=(15, 1), key='-itag3-'), sg.Input(size=(15, 1), key='-itag4-'),

            ],
            [
                sg.Input(size=(15, 1), key='-itag5-'), sg.Input(size=(15, 1), key='-itag6-'),
                sg.Input(size=(15, 1), key='-itag7-'), sg.Input(size=(15, 1), key='-itag8-'),
            ],
            [
                sg.Input(size=(15, 1), key='-itag9-'), sg.Input(size=(15, 1), key='-itag10-'),
                sg.Input(size=(15, 1), key='-itag11-'), sg.Input(size=(15, 1), key='-itag12-'),

            ],
            [
                sg.Input(size=(15, 1), key='-itag13-'), sg.Input(size=(15, 1), key='-itag14-'),
                sg.Input(size=(15, 1), key='-itag15-'), sg.Input(size=(15, 1), key='-itag16-')
            ],
            [
                sg.Input(size=(15, 1), key='-itag17-'), sg.Input(size=(15, 1), key='-itag18-'),
                sg.Input(size=(15, 1), key='-itag19-'), sg.Input(size=(15, 1), key='-itag20-')
            ],
            [
                sg.Input(size=(15, 1), key='-itag21-'), sg.Input(size=(15, 1), key='-itag22-'),
                sg.Input(size=(15, 1), key='-itag23-'), sg.Input(size=(15, 1), key='-itag24-')
            ],
            [
                sg.Input(size=(15, 1), key='-itag25-'), sg.Input(size=(15, 1), key='-itag26-'),
                sg.Input(size=(15, 1), key='-itag27-'), sg.Input(size=(15, 1), key='-itag28-')
            ],
            [
                sg.Input(size=(15, 1), key='-itag29-'), sg.Input(size=(15, 1), key='-itag30-'),
                sg.Input(size=(15, 1), key='-itag31-'), sg.Input(size=(15, 1), key='-itag32-')
            ],
            [
                sg.Input(size=(15, 1), key='-itag33-'), sg.Input(size=(15, 1), key='-itag34-'),
                sg.Input(size=(15, 1), key='-itag35-'), sg.Input(size=(15, 1), key='-itag36-')
            ],
            [
                sg.Input(size=(15, 1), key='-itag37-'), sg.Input(size=(15, 1), key='-itag38-'),
                sg.Input(size=(15, 1), key='-itag39-'), sg.Input(size=(15, 1), key='-itag40-')
            ],
            [
                sg.Input(size=(15, 1), key='-itag41-'), sg.Input(size=(15, 1), key='-itag42-'),
                sg.Input(size=(15, 1), key='-itag43-'), sg.Input(size=(15, 1), key='-itag44-')
            ],
            [
                sg.Input(size=(15, 1), key='-itag45-'), sg.Input(size=(15, 1), key='-itag46-'),
                sg.Input(size=(15, 1), key='-itag47-'), sg.Input(size=(15, 1), key='-itag48-')
            ],
            [
                sg.Input(size=(15, 1), key='-itag49-'), sg.Input(size=(15, 1), key='-itag50-'),
                sg.Input(size=(15, 1), key='-itag51-'), sg.Input(size=(15, 1), key='-itag52-')
            ],

        ]

        studios_unique = sorted(list({x for x in constants.STUDIOS.values() if x != ''}))
        studio_buttons = []
        current_row = []
        studios_len = len(studios_unique)
        for idx, studio in enumerate(studios_unique, start=1):
            current_row.append(sg.Button(studio, key=f'-studio{idx}-', size=(12, 1)))
            if (idx) % 3 == 0 or idx ==studios_len:
                studio_buttons.append(current_row)
                current_row = []


        col2_top = [
            [
                sg.Text('Find a Scene', text_color='#ffa0dc', font=('BRADDON', 20), size=(25, 1),
                        justification='center'),
            ],
            [

            ],
            [

                sg.T('Search'),
                sg.I(key='-iSearch-', size=(31, 1), background_color='light yellow', enable_events=True),
                sg.Button('Submit', size=(7, 1), key='-SUBMIT-', button_color=('black', '#ffa0dc'),
                          enable_events=True, bind_return_key=True),
            ],
            [
                sg.T('Studio'),
                sg.I(key='-iSearch Studio-', size=(13, 0), pad=(9,0), background_color='light yellow', ),
                sg.T('*Optional. Can also click below.'),
            ],
            [
                sg.Listbox(values=[], size=(48, 15), enable_events=True, key='-SCENE RESULTS-')
            ],
            *studio_buttons,  # unpack dynamic list of buttons
        ]

        col2_mid = [
            [
                sg.Frame(
                    title='', key='-SEARCH IMAGE FRAME-', size=(250, 150), pad=(50, 0),
                    layout=[
                        [sg.Image(data=Gui.img_resize('img/placeholders/bigimage-placeholder.png', first=True,
                                                      newsize=(250, 150)),
                                  enable_events=True,
                                  key='-SEARCH IMAGE-',
                                  size=(250, 150))]
                    ]
                ),
            ],
        ]

        col3_top = [
            [
                sg.Text('Performers', text_color='#ffa0dc', font=('BRADDON', 20), size=(35, 1),
                        justification='center')],
            # [
            #     sg.HorizontalSeparator()
            # ],
            row(['cast 1', 'cast 7'], size=(5, 1), size2=(25, 1)),
            row(['cast 2', 'cast 8'], size=(5, 1), size2=(25, 1)),
            row(['cast 3', 'cast 9'], size=(5, 1), size2=(25, 1)),
            row(['cast 4', 'cast 10'], size=(5, 1), size2=(25, 1)),
            row(['cast 5', 'cast 11'], size=(5, 1), size2=(25, 1)),
            row(['cast 6', 'cast 12'], size=(5, 1), size2=(25, 1)),
        ]

        col3_mid = [
            [
                sg.Text('Covers', text_color=('#ffa0dc'), font=('BRADDON', 15), size=(15, 1), justification='center',
                        pad=(20, 0)),
                sg.Text('Gallery', text_color=('#ffa0dc'), font=('BRADDON', 15), size=(15, 1), justification='center',
                        pad=(80, 0))
            ],
        ]

        col3_bot = [
            [
                sg.Frame('Cover', [[sg.Image(
                    data=Gui.img_resize('./img/placeholders/cover-placeholder.jpg', first=True, newsize=(250, 250)),
                    key='-COVER-',
                    size=(250, 250))]]),

                sg.Frame('Gallery', [[sg.Image(
                    data=Gui.img_resize('./img/placeholders/gallery-placeholder.png', first=True, newsize=(250, 250)),
                    key='-GALLERY-',
                    size=(250, 250))]]),

            ]
        ]

        col3_console = [
            [sg.Text('Console')],
            [sg.Multiline(key='-CONSOLE-', size=(75, 16), write_only=True, autoscroll=True)],
        ]

        col4_top = [
            [sg.Text('Performer Info', text_color='#ffa0dc', font=('BRADDON', 20), size=(25, 1), key='-PERFORMER-')],
            [
                sg.Text(f'Artist:', key='-ARTIST-', size=(30, 1)),
                sg.Button(f'Download Art', key='-DOWNLOAD ART-'),
                sg.Button(f'Delete Art', key='-DELETE ART-'),

            ],
            [sg.Listbox(values=[], size=(57, 10), enable_events=True, key='-FILES-')]
        ]

        col4_mid = [
            [
                sg.Frame(
                    title='', key='-BIGIMAGE FRAME-', size=(500, 500), element_justification='c',
                    layout=[
                        [sg.Image(data=Gui.img_resize('./img/placeholders/bigimage-placeholder.png', first=True,
                                                      newsize=(400, 400)),
                                  enable_events=True,
                                  key='-BIGIMAGE-',
                                  size=(400, 400))]
                    ]
                ),
            ],
        ]

        col4_bot = [
            [
                sg.T(''),
                sg.Button("<", size=(10, 1), pad=(1, 1), key='-LEFT-'),
                sg.Button(">", size=(10, 1), key='-RIGHT-'),
                sg.Button("Make Cover", size=(10, 1), key='-MAKE COVER-'),
                sg.Button("Add to Gallery", size=(10, 1), key='-ADD TO GALLERY-'),
                sg.T('')
            ]
        ]

        WIN_HEIGHT = 835

        layout = [
            [
                # left column
                sg.Column(col1, size=(500, WIN_HEIGHT)),
                # sg.Column(col2_top, size=(370, WIN_HEIGHT)),
                sg.VSeperator(),
                sg.Column(
                    layout=[
                        [sg.Column(col2_top, size=(370, 650))],  # middle column top
                        [sg.Column(col2_mid, size=(370, 180), )],  # middle column middle
                    ]
                ),

                sg.VSeperator(),
                sg.Column(
                    layout=[
                        [sg.Column(col3_top, size=(550, 200))],  # middle column top
                        [sg.Column(col3_mid, size=(550, 30))],  # middle column middle
                        [sg.Column(col3_bot, size=(550, 300))],  # middle column bottom
                        [sg.Column(col3_console, size=(550, 300))]
                    ]
                ),
                sg.VSeperator(),
                sg.Column(
                    layout=[
                        [sg.Column(col4_top, size=(550, 250))],
                        [sg.Column(col4_mid, size=(550, 500)), ],
                        [sg.Column(col4_bot)],
                    ], size=(430, 830)
                ),
            ]

        ]

        self.window = sg.Window('tpdb2xvbr GUI Helper', layout, finalize=True)

    def bind_inputs(self, elem: str, tk_event='<Button-1>', event='+CLICK+', exclude=[], start=1, end=100) -> None:
        '''
        binds a range of pysimplegui Input elements in the GUI to an event, suck as a left click
        :param elem: the input element base name.  Should not include "-" or "-i", these will automatically be applied.
                     e.g. elem = 'tag' will create '-itag1-', '-itag2-', etc until no matching element is found
        :param tk_event: see below
        :param event: str that will be appended onto the input, so that elem = 'cast 1', event='+CLICK+' will produce event '-cast 1-+CLICKED+'
        :param exclude: list of element keys to exclude e.g. ['-i cast2-']
        :start int of first input key value
        :end   int of final input key value (pythonic, will not be included)

        a valid tkinter_event_string, such as

                  <Button-1>        Button 1 is the leftmost button, button 2 is the middle button
                  (where available), and button 3 the rightmost button.

                  <Button-1>, <ButtonPress-1>, and <1> are all synonyms.

                  For mouse wheel support under Linux, use Button-4 (scroll
                  up) and Button-5 (scroll down)

                    <B1-Motion>       The mouse is moved, with mouse button 1 being held down (use
                                      B2 for the middle button, B3 for the right button).

                    <ButtonRelease-1> Button 1 was released. This is probably a better choice in
                                      most cases than the Button event, because if the user
                                      accidentally presses the button, they can move the mouse
                                      off the widget to avoid setting off the event.

                    <Double-Button-1> Button 1 was double clicked. You can use Double or Triple as
                                      prefixes.

                    <Enter>           The mouse pointer entered the widget (this event doesn’t mean
                                      that the user pressed the Enter key!).

                    <Leave>           The mouse pointer left the widget.

                    <FocusIn>         Keyboard focus was moved to this widget, or to a child of
                                      this widget.

                    <FocusOut>        Keyboard focus was moved from this widget to another widget.

                    <Return>          The user pressed the Enter key. For an ordinary 102-key
                                      PC-style keyboard, the special keys are Cancel (the Break
                                      key), BackSpace, Tab, Return(the Enter key), Shift_L (any
                                      Shift key), Control_L (any Control key), Alt_L (any Alt key),
                                      Pause, Caps_Lock, Escape, Prior (Page Up), Next (Page Down),
                                      End, Home, Left, Up, Right, Down, Print, Insert, Delete, F1,
                                      F2, F3, F4, F5, F6, F7, F8, F9, F10, F11, F12, Num_Lock, and
                                      Scroll_Lock.

                    <Key>             The user pressed any key. The key is provided in the char
                                      member of the event object passed to the callback (this is an
                                      empty string for special keys).

                    a                 The user typed an “a”. Most printable characters can be used
                                      as is. The exceptions are space (<space>) and less than
                                      (<less>). Note that 1 is a keyboard binding, while <1> is a
                                      button binding.

                    <Shift-Up>        The user pressed the Up arrow, while holding the Shift key
                                      pressed. You can use prefixes like Alt, Shift, and Control.

                    <Configure>       The widget changed size (or location, on some platforms). The
                                      new size is provided in the width and height attributes of
                                      the event object passed to the callback.

                    <Activate>        A widget is changing from being inactive to being active.
                                      This refers to changes in the state option of a widget such
                                      as a button changing from inactive (grayed out) to active.


                    <Deactivate>      A widget is changing from being active to being inactive.
                                      This refers to changes in the state option of a widget such
                                      as a radiobutton changing from active to inactive (grayed out).

                    <Destroy>         A widget is being destroyed.

                    <Expose>          This event occurs whenever at least some part of your
                                      application or widget becomes visible after having been
                                      covered up by another window.

                    <KeyRelease>      The user let up on a key.

                    <Map>             A widget is being mapped, that is, made visible in the
                                      application. This will happen, for example, when you call the
                                      widget's .grid() method.

                    <Motion>          The user moved the mouse pointer entirely within a widget.

                    <MouseWheel>      The user moved the mouse wheel up or down. At present, this
                                      binding works on Windows and MacOS, but not under Linux.

                    <Unmap>           A widget is being unmapped and is no longer visible.

                    <Visibility>      Happens when at least some part of the application window
                                      becomes visible on the screen.
        more keys can be found here: https://stackoverflow.com/questions/32289175/list-of-all-tkinter-events
        '''

        keys = self.window.AllKeysDict
        for i in range(start, end):
            e = f'-{elem}{i}-'
            if e not in exclude and e in keys:
                self.window[e].bind(tk_event, event)

    def save(self, vals):

        scene = {}

        scene['_id'] = vals['-i_id-']
        scene['scene_id'] = vals['-iscene_id-']
        scene['scene_type'] = vals['-iscene_type-']
        scene['title'] = vals['-ititle-']
        scene['studio'] = vals['-istudio-']
        scene['site'] = vals['-isite-']
        scene['covers'] = [vals['-icovers-']]
        scene['gallery'] = [vals['-igallery-']]

        scene['tags'] = []

        for i in range(1, 53):
            try:
                tag = vals[f'-itag{i}-']
                if tag.strip():
                    scene['tags'].append(tag)
            except Exception as e:
                pass

        cast = []
        for i in range(1, 12):
            try:
                cast_value = vals[f'-icast {i}-']
                if cast_value.strip():
                    cast.append(cast_value)
            except Exception as e:
                pass
        scene['cast'] = cast
        scene['filename'] = None
        scene['duration'] = 1
        scene['synopsis'] = vals['-isynopsis-']
        scene['released'] = vals['-ireleased-']
        scene['homepage_url'] = vals['-ihomepage_url-']

        data = {}
        data['timestamp'] = datetime.datetime.now().isoformat() + 'Z'
        data['bundleVersion'] = '1'
        data['scenes'] = [scene]

        return data

    def update_elem(self, elem: str, arguments: dict) -> None:
        '''
        updates a single pysimplegui element in the GUI
        :param elem: the element base name.  Should not include "-"
                     e.g. elem = 'icast 1' will create '-icast 1-'
        :param arguments: dict of key, value pairs to pass to window.update()
                     e.g. { 'font' : 'default 10 regular', 'value' : 'Alexis Texas' }
        '''
        keys = self.window.AllKeysDict

        if elem in keys:
            try:
                self.window[f'{elem}'].update(**arguments)
            except Exception as e:
                print(f'exception with {e}\nelem: {elem} : arguments:{arguments}')

    def update_elems(self, elem: str, arguments: dict, min=1, max=100, exclude: list = []) -> None:
        '''
        updates a range of pysimplegui elements in the GUI
        :param elem: the element key base name.  Should not include "-"
                     e.g. elem = 'itag' will create '-itag1-', '-itag2-', etc until no matching element is found
        :param arguments: dict of key, value pairs to pass to window.update()
                     e.g. { 'font' : 'default 10 regular', 'value' : 'Alexis Texas' }
        :min: int first element to update
        :max: int last element to update
        :exclude: list of element keys to exclude
        '''

        for i in range(min, max):
            e = f'-{elem}{i}-'
            if e not in exclude:
                self.update_elem(e, arguments)

    def update_inputs(self, elem: str, items: list, translate=None) -> None:
        '''
        updates a range of pysimplegui Input elements in the GUI
        :param elem: the input box element base name.  Should not include "-" or "-i", these will automatically be applied.
                     e.g. elem = 'tag' will create '-itag1-', '-itag2-', etc until no matching element is found
        :param items: list of strs to populate Input elements
        '''

        i = 1
        for item in items:
            if translate:
                item = Gui.translate_str(item, translate=translate)
            e = f'-i{elem}{i}-'
            self.update_elem(e, arguments={'value': item})
            i += 1

    @staticmethod
    def translate_str(my_str, translate):
        for key, val in translate.items():
            for v in val:
                v = v.lower()
                my_str = my_str.lower()
                my_str = my_str.replace(v, key)
        return my_str

    @staticmethod
    def img_convert_webp(input, output) -> None:
        '''
        converts a webp file to a png
        :param input: file, str or Path
        :param output: file, str or Path
        '''

        curdir = Path.cwd()
        # dwebp does not like it when we are not in the target directory
        tempdir = Path(input).parent

        os.chdir(tempdir)  # temporarily change to the target directory
        dwebp(input_image=Path(input).name, output_image=Path(output).name, option="-o", logging="-v")  # convert
        os.chdir(curdir)  # change back to original directory

    @staticmethod
    def img_resize(f: Union[Path, str], newsize=(200, 200), first=False) -> ImageTk.PhotoImage:
        '''Resize image data using PIL and return in Tk-Friendly format'''

        try:
            img = Image.open(f)
        except UnidentifiedImageError as e:
            print(e)
            return None

        width, height = img.size

        if width > height:
            new_width = newsize[0]
            new_height = height / width * newsize[0]
        elif width < height:
            new_height = newsize[1]
            new_width = width / height * newsize[1]
        else:  # width == height:
            new_width, new_height = newsize[0], newsize[1]

        img = img.resize((int(new_width), int(new_height)), resample=Image.BICUBIC)

        if first:
            return Gui.img_tk_first(img)
        else:
            return ImageTk.PhotoImage(img)

    @staticmethod
    def img_tk_first(img):
        '''Return a byte-like object the first time an image is displayed to avoid Tk Error'''
        bio = io.BytesIO()
        img.save(bio, format='PNG')
        del img
        return bio.getvalue()

    @staticmethod
    def img_thumb(f, maxsize=(200, 200), first=False):
        '''Return a thumbnail that is always smaller than the original object' in Tk-friendly format'''

        img = Image.open(f)
        img.thumbnail(maxsize)  # thumnail() mutates img in place
        if first:
            return Gui.img_tk_first(img)
        else:
            return ImageTk.PhotoImage(img)

    @staticmethod
    def img_download(url, fname):
        ''' downloads an image from a url
            url: str - valid URL
            fname: str or Path filename
        '''
        try:
            r = requests.get(url, stream=True)
            if r.status_code == 200:
                r.raw.decode_content = True

                with open(fname, 'wb') as f:
                    shutil.copyfileobj(r.raw, f)
                return True
            else:
                return False
        except Exception as e:
            print(e)
            return False


if __name__ == '__main__':

    sg.theme('Light Blue5')
    gui = Gui()

    timeout = 0

    # MAIN EVENT LOOP
    while True:
        event, values = gui.window.read(timeout=timeout)
        if event == 'Exit' or event == sg.WIN_CLOSED:
            break

    pass  # used to set debugging breakpoint
