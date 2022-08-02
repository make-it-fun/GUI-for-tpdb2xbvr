# project dependencies
from stupidserver import StupidServer
import constants
from tpdb2xbvr import get_scene, search, get_xtras, handle_request
from typing import Optional

# external dependencies
import json
import PIL
import pyperclip
import PySimpleGUI as sg
import shutil
from datetime import date
from natsort import natsorted
from pathlib import Path, PurePosixPath
from typing import Optional, Union
from ui import Gui


def calculate_age(born: date, age_date: Optional[date] = None) -> Optional[int]:
    """ accepts a datetime.date and returns age based on current date"""

    if born is None:
        return None

    calc_date = age_date if age_date else date.today()
    return calc_date.year - born.year - ((calc_date.month, calc_date.day) < (born.month, born.day))


def console(text: str, type: str = None) -> None:
    """ Displays a message to the console
        prefix: optional str to insert before message, such as 'warning' or 'error'
    """
    prefix = ''
    if type is not None:
        prefix = f'**** {type.upper()} ****\n'
    gui.window['-CONSOLE-'].update(f'{prefix}{text}')
    gui.window.refresh()


def create_config(file: str, contents=None) -> None:
    """ creates a json config file"""

    if contents == None:
        data = {
            'key': '',
            'ip': 'localhost',
            'port': '6969'
        }

    else:
        data = contents

    # ensure directory exists
    Path(file).parent.mkdir(parents=True, exist_ok=True)

    # write file
    with open(file, 'w') as outfile:
        json.dump(data, outfile)
    global console_text
    if contents == None:
        console_text += f'Created config file {file}.  Now add your API key\n'
    else:
        console_text += f'Created config file {file}.\n'


def fix_search(query, lookup):
    for k, v in lookup.lower():
        if k in query.lower():
            query.replace()


def get_config(file: str, contents: dict = None, create=True) -> dict:
    """ reads a json config file
        if file does not exist, optionally creates it (and any necessary dirs) with 'contents' dict
    """
    if contents == None:
        data = None
    else:
        data = contents
    if not Path(file).exists() and create:
        create_config(file, data)
    try:
        with open(file) as config_file:
            return json.load(config_file)
    except Exception as e:
        print(e)
        return None


def highlight_cast(input: str, text: str) -> None:
    """
    updates the cast text and input fields by highlighting the event
    :param input:
    :param text:
    :return:
    """
    gui.update_elems('icast ', {'background_color': '#5edfff'},
                     exclude=[input])
    gui.update_elem(elem=input, arguments={'background_color': '#ffa0dc'})
    # update clicked input text box pink, make the rest default
    gui.update_elems('tcast ', {'text_color': sg.theme_text_color(), 'font': 'default 10 normal'},
                     exclude=[text])
    gui.update_elem(elem=text, arguments={'text_color': '#ffa0dc', 'font': 'default 10 bold'})


def init_performer(perf):
    """ creates the xtras dict entries for filenames, filepaths, and file_idx
    :param perf: performer name, as included in 'xtras' dict
    :return: None
    """
    if perf:
        filepaths = [f for f in Path(f'img/performers/{perf}/').glob('*') if
                     f.suffix in {'.jpg', '.png', '.jpeg', '.tiff', '.webp', '.gif'}]
        xtras[perf]['filepaths'] = natsorted(filepaths, key=lambda x: x.stem)
        xtras[perf]['filenames'] = [f.name for f in xtras[perf]['filepaths']]
        xtras[perf]['file_idx'] = 0


def process_image(url: str, dest: Union[Path, str], perf: Optional[str] = None, key: Optional[str] = None,
                  size=(250, 250), add_to_xtras=True) -> None:
    """
    downloads an image and adds it to the xtras dict in the 'images' key
    :param url: image url
    :param dest: file destination, can be a string, pathlib Path, or fileobject
    :param perf: str - performer name.  If empty, image will be added to both xtras[performer]['images']
    :param key: key of gui window image object to update, if any
    :param size: image size
    :return: None
    """
    if gui.img_download(url, dest):

        if 'cast' not in scenes:
            perfs = []
        else:
            if perf == None:
                perfs = scenes['cast']
            else:
                perfs = [perf]

        if add_to_xtras:
            for p in perfs:
                xtras[p]['images'][Path(dest).as_posix()] = url

        if key:
            gui.window[key].update(data=gui.img_resize(dest, newsize=size), size=size)

    # if there was no image at this URL, we need to delete an existing file as it's probably left over from another scene
    else:
        cwd = Path.cwd()
        file_to_delete = Path(Path.cwd() / dest)
        if file_to_delete.is_file():
            file_to_delete.unlink()


def update_file_idx(idx, increment):
    idx += increment
    if idx == len(xtras[current_performer]['filepaths']):
        idx = 0
    elif idx < 0:
        idx = len(xtras[current_performer]['filepaths']) - 1
    return idx


def update_gui():
    """
    updates most gui elements

    """
    gui.window.finalize()
    if xtras and current_performer in xtras:
        performer = xtras[current_performer]
        age = calculate_age(performer['dob'])
        if age == None:
            age = "N/A"

        file_idx = performer['file_idx']
        filepaths = performer['filepaths']
        filenames = performer['filenames']
        if filepaths:
            try:
                gui.window['-BIGIMAGE-'].update(data=gui.img_resize(filepaths[file_idx], newsize=(400, 400)))
            except PIL.UnidentifiedImageError:
                try:
                    gui.img_convert_webp(input=str(filepaths[file_idx]), output=str(filepaths[file_idx]))
                    gui.window['-BIGIMAGE-'].update(data=gui.img_resize(filepaths[file_idx], newsize=(400, 400)))
                except Exception:
                    print('error, could not convert webp to png file')
            # if filenames:
            gui.window['-FILES-'].update(values=filenames, set_to_index=file_idx)
            gui.window['-FILES-'].update(scroll_to_index=file_idx)
            gui.window['-BIGIMAGE FRAME-'].update(value=filenames[file_idx])
        else:
            gui.window['-FILES-'].update(values=[])

        gui.window['-PERFORMER-'].update(f'{current_performer} (Age: {age})')
        try:
            released_age = calculate_age(performer['dob'], date.fromisoformat(scenes['released']))
            if released_age == None:
                released_age = "of unknown age"

            gui.window['-ARTIST-'].update(f'...was {released_age} in this scene.')
        except Exception as e:
            print(e)
            release_age = 0
            gui.window['-ARTIST-'].update(f'...no scene age data is avaiable')


def update_headers(value):
    return {
        "Authorization": f"Bearer {value}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }


def write_config(file: str) -> None:
    """
    saves the current GUI config info to a json config file
    :param file: file to be saved (e.g. 'config.json')
    """
    contents = {
        'key': values['-API KEY-'],
        'ip': values['-WEBSERVER-'],
        'port': values['-PORT-']
    }
    print(contents)
    with open(file, 'w') as outfile:
        json.dump(contents, outfile)


def write_json(file: str, data_to_write) -> None:
    """
    saves the current GUI config info to a json config file
    :param file: file to be saved (e.g. 'config.json')
    """
    print(data_to_write)
    with open(file, 'w') as outfile:
        json.dump(data_to_write, outfile, ensure_ascii=True, indent=2)


if __name__ == '__main__':

    # Variables Setup
    THUMBSIZE = (250, 250)
    BIGSIZE = (400, 400)
    xtras = {}
    scenes = {}
    console_text = ''
    current_performer = ''

    config = get_config('data/config.json')
    last_scraped = get_config('data/last_scraped.json', {'-iThePornDB URL-': ''})
    headers = update_headers(config['key'])

    # Directory Setup

    # GUI Setup
    sg.theme('Light Blue5')
    gui = Gui()
    gui.window.refresh()

    # trap for left-click events on input elements
    gui.bind_inputs('icast ', tk_event='<Button-1>', event='+CLICK+', start=1, end=12)

    # populate the url input either with the last scraped url or the url for "Paddy's Pub"
    if not last_scraped['-iThePornDB URL-']:
        url = 'https://api.metadataapi.net/scenes/wankz-vr-paddys-pub'
    else:
        url = last_scraped['-iThePornDB URL-']

    gui.window['-iThePornDB URL-'].update(url)
    gui.window['-PORT-'].update(config['port'])
    gui.window['-WEBSERVER-'].update(config['ip'])
    if config['key']:
        gui.window['-API KEY-'].update(config['key'])
    else:
        gui.window['-SAVE CONFIG-'].update(button_color=('black', '#ffa0dc'))

    timeout = None  # may be modified when threads are added

    # Webserver Setup
    server = StupidServer()
    console_text += 'Webserver is buggy.  If GUI freezes, open webserver in browser and refresh it.\n'
    console(console_text, 'Warning')

    # MAIN EVENT LOOP
    while True:
        event, values = gui.window.read(timeout=timeout)

        # Exit
        if event in (sg.WIN_CLOSED, 'Exit'):
            if server.running:
                server.stop()
            break

        if event == '-API KEY-':
            if values['-API KEY-'].strip():
                gui.window.finalize()
                headers = update_headers(config['key'])



        # cast text or input element clicked
        elif 'cast' in event and '+' not in event:
            # if it's a text element, we're still going to change the input element
            if event[:2] == '-t':
                cast_elem = event.replace('-t', '-i', 1)  # change target to input element

            else:
                cast_elem = event  # target already is input element

            # the following makes the input of the clicked element pink and the rest regular
            highlight_cast(cast_elem, event)

            # change the current performer to the clicked cast
            if values[cast_elem].strip():
                current_performer = values[cast_elem]
            update_gui()

        # cast input element clicked.  event will be f'+-icast {#}-+BUTTON+', note the space between 'icast' and '#'
        elif 'icast' in event and '+' in event:
            cast_elem = event.split('+')[0]  # remove '+BUTTON'+ from event
            text_elem = '-t' + cast_elem[2:]  # get the text element as well
            # update clicked input background pink, make the rest default
            highlight_cast(cast_elem, text_elem)

            if values[cast_elem].strip():
                current_performer = values[cast_elem]
            update_gui()

        elif event == '-icovers-':
            gui.window.finalize()
            if values['-icovers-'].strip():
                cover_image = values['-icovers-'].strip()
                if cover_image:
                    process_image(url=cover_image, dest=Path(Path.cwd() / 'img/temp/cover.png'), key='-COVER-',
                                  size=THUMBSIZE)

        elif event == '-igallery-':
            gui.window.finalize()
            if values['-igallery-'].strip():
                gallery_image = values['-igallery-'].strip()
                if gallery_image:
                    process_image(url=gallery_image, dest='img/temp/gallery.png', key='-GALLERY-', size=THUMBSIZE)

        # Scrape
        elif event == '-SCRAPE-':
            # nuke cast inputs
            for i in range(1, 12):
                gui.window[f'-icast {i}-'].update('')

            # nuke tag inputs
            for i in range(1, 53):
                gui.window[f'-itag{i}-'].update('')

            gui.window.finalize()  # finalize gui so we can read value['-API KEY-']

            if not config['key']:
                headers = update_headers(values['-API KEY-'])

            if not values['-API KEY-']:
                sg.popup_ok('Need to enter API Key into "ThePornDB Key" field', title="You Probably Fucked Up")

            # SCRAPE SCENE
            else:
                # ensure img/temp folder exists
                Path(Path.cwd() / 'img/temp').mkdir(parents=True, exist_ok=True)

                console_text += 'Starting Scrape of Scene\n'
                console(console_text)

                url = values['-iThePornDB URL-']
                req = handle_request(url, headers)
                result = get_scene(req, headers=headers)
                xtras = get_xtras(req, headers=headers)

                write_json('data/request.json', data_to_write=req)

                if result is not None:
                    # populate gui fields
                    scenes = result['scenes'][0]
                    gui.window['-ititle-'].update(scenes['title'])
                    gui.window['-istudio-'].update(gui.translate_str(scenes['studio'], translate=constants.DB_STUDIOS))
                    gui.window['-isite-'].update(gui.translate_str(scenes['site'], translate=constants.DB_STUDIOS))
                    gui.window['-i_id-'].update(scenes['_id'])
                    gui.window['-iscene_id-'].update(scenes['scene_id'])
                    gui.window['-isynopsis-'].update(scenes['synopsis'])
                    gui.window['-ireleased-'].update(scenes['released'])
                    gui.window['-ihomepage_url-'].update(scenes['homepage_url'])
                    gui.update_inputs('tag', scenes['tags'], translate=constants.TAGS)
                    gui.update_inputs('cast ', scenes['cast'])

                    cover_image = scenes['covers'][0]
                    gui.window['-icovers-'].update(cover_image)

                    gallery_image = scenes['gallery'][0]
                    gui.window['-igallery-'].update(gallery_image)

                    console_text += 'Downloading Scene Images\n'
                    console(console_text)

                    # delete existing temp images
                    img_dir = Path(Path.cwd() / 'img/temp')
                    files = [f for f in img_dir.glob('*') if f.is_file()]
                    for f in files:
                        Path(f).unlink()

                    # populate image elements
                    process_image(cover_image, 'img/temp/cover.png', key='-COVER-', size=THUMBSIZE, add_to_xtras=True)
                    process_image(gallery_image, 'img/temp/gallery.png', key='-GALLERY-', size=THUMBSIZE)

                    # get scene poster
                    process_image(scenes['posters'][0], f'img/temp/poster0.png')

                    # get scene background 0
                    process_image(scenes['background'][0], f'img/temp/background0.png')

                    # get scene media
                    process_image(scenes['media'], f'img/temp/media.png')

                    # copy URL to clipboard
                    pyperclip.copy(url)
                    console_text += 'Copied Scene TPDB URL to Clipboard\n'
                    console(console_text)


                    if xtras:
                        for performer in xtras:
                            # ensure performer directory exists
                            xtras_dir = Path(Path.cwd() / f'img/performers/{performer}')
                            xtras_dir.mkdir(exist_ok=True, parents=True)

                            # copy media already in '/img/temp' to '/img/performers/{performer}'
                            img_dir = Path(Path.cwd() / 'img/temp')
                            files = [f for f in img_dir.glob('*') if f.is_file()]
                            for file in files:
                                # strip digits from filenames (e.g. background1.png becomes background.png)
                                removed_digits = ''.join(
                                    [c for c in file.stem if
                                     not c.isdigit()])
                                # if the filename is a match for the following...
                                if any(x in removed_digits for x in
                                       ['background', 'media', 'posters', 'gallery', 'cover'] if
                                       'placeholder' not in removed_digits):
                                    # copy the appropriate images to the img/performers/{performer} dir
                                    shutil.copy(file, xtras_dir / file.name)

                                    # if artwork has already been downloaded, load the performer artwork
                            temp = (Path.cwd() / f'img/performers/{performer}/xtra0.png')
                            if Path(Path.cwd() / f'img/performers/{performer}/xtra0.png').is_file():
                                init_performer(performer)
                            else:
                                # download the first image for each performer
                                try:
                                    performer_image_url = xtras[performer]['artist_posters'][0]
                                    imagepath = Path(f'img/performers/{performer}')
                                    gui.img_download(performer_image_url, Path(imagepath / 'xtra0.png'))
                                except IndexError as e:
                                    print(e)
                                    performer_image_url = []

                                # make filepaths, which is currently just a list of a single poster path
                                filepaths = [f for f in Path(f'img/performers/{performer}/').glob('*')
                                             if
                                             f.suffix in {'.jpg', '.png', '.jpeg', '.tiff', '.webp',
                                                          '.gif'}]
                                xtras[performer]['filepaths'] = filepaths

                                # make filenames from filepaths
                                xtras[performer]['filenames'] = [f.name for f in filepaths]

                            # set file_idx to newly downloaded xtra file xtra0.png
                            try:
                                xtras[performer]['file_idx'] = xtras[performer]['filenames'].index('xtra0.png')
                            except ValueError as e:
                                print(e)
                                xtras[performer]['file_idx'] = 0

                    try:
                        current_performer = list(xtras)[0]  # assign the first performer as the current performer
                    except IndexError as e:
                        print(e)
                        current_performer = None

                    highlight_cast('-icast 1-', '-tcast 1-')

                    update_gui()  # will update the BIGIMAGE and ARTIST fields based on current_performer

                    last_scraped = 'data/last_scraped.json'
                    write_json(last_scraped, {'-iThePornDB URL-': values['-iThePornDB URL-']})

                    write_json('data/result.json', data_to_write=result)


                else:  # if result is None
                    sg.popup_error(
                        'Problem scraping!\nThere was a problem scraping the scene.\nIs your API key correct?\nIs your scene URL correct?')


        elif event == '-DOWNLOAD ART-':

            if xtras:
                for performer in xtras:
                    # create folders
                    Path(Path.cwd() / f'img/performers/{performer}').mkdir(parents=True, exist_ok=True)

                    # alert user
                    console_text += f'Downloading additional art for {performer}\n'
                    console(console_text)

                    # download all images
                    if not xtras[performer]['artist_posters']:
                        console_text += f'No additional artwork available for {performer}.\n'
                        console(console_text)
                    else:
                        img_cache = {}
                        for idx, poster_url in enumerate(xtras[performer]['artist_posters']):
                            # skip the first image as we already have it downloaded
                            if idx == 0:
                                continue
                            xtra_img = Path(f'img/performers/{performer}/xtra{idx}.png')
                            process_image(url=poster_url, dest=xtra_img,
                                          perf=performer)

                            # add the image location as a key to and the url so we can access later for gallery and covers
                            img_cache[xtra_img.name] = poster_url
                            console_text += f'Downloaded {xtra_img.name}\n'
                            console(console_text)

                        # write the dict to "img_cache.json" file so that we can access the URLs later without re-scraping
                        if img_cache:
                            write_json(f'img/performers/{performer}/img_cache.json', img_cache)

                    # load performer filepaths, filenames, create file_idx, etc
                    init_performer(performer)
                    try:  # set to new xtra art download xtra1.png. We've already downlaoded xtra0.png previously
                        file_idx = xtras[performer]['filenames'].index('xtra1.png')
                        xtras[performer]['file_idx'] = file_idx
                    except Exception as e:
                        print(f'Exception: {e}')
                update_gui()

        # delete artist folder and all images
        elif event == '-DELETE ART-':
            if xtras:
                print('deleting art')

                for performer in xtras:
                    pth = Path(Path.cwd() / f'img/performers/{performer}')
                    if pth.is_dir():
                        for item in pth.glob('*'):
                            if item.is_file():
                                item.unlink()
                        pth.rmdir()  # remove dir
                        # reset paths, names, idx
                        xtras[performer]['filepaths'] = []
                        xtras[performer]['filenames'] = []
                        xtras[performer]['file_idx'] = 0

                # remove the files and replace images with
                update_gui()
                gui.window['-FILES-'].update([])
                gui.window['-BIGIMAGE-'].update(
                    data=gui.img_resize('img/placeholders/bigimage-placeholder.png', newsize=BIGSIZE),
                    size=BIGSIZE)


        # replace cover or gallery
        elif event in ['-ADD TO GALLERY-', '-MAKE COVER-']:
            if event == '-ADD TO GALLERY-':
                gui_elem = '-GALLERY-'
                url_elem = '-igallery-'
            else:
                gui_elem = '-COVER-'
                url_elem = '-icovers-'

            # update GUI gallery image
            try:
                selected = values['-FILES-'][0]
                filepaths = xtras[current_performer]['filepaths']
                file_idx = xtras[current_performer]['file_idx']
                selected_path = filepaths[file_idx]
                gui.window[gui_elem].update(data=gui.img_resize(selected_path, newsize=THUMBSIZE))

            except IndexError as e:
                selected_path = None
                print(e)

            if selected_path:
                # update '-igallery-' URL
                try:
                    new_url = None
                    # if selected image is from the current scene (and not artist xtra images)
                    if xtras[current_performer]['images']:

                        selected_key = selected_path.name  # poster0.png, etc
                        for key, val in xtras[current_performer]['images'].items():
                            if Path(key).name == selected_key:
                                new_url = xtras[current_performer]['images'][f'img/temp/{selected_key}']

                    # if selected image is not from the current scene, check if it's an xtra image
                    if not new_url:
                        xtra_key = selected_path.name
                        art = get_config(f'img/performers/{current_performer}/img_cache.json')
                        if art and xtra_key in art:
                            new_url = art[xtra_key]
                    if new_url:
                        gui.window[url_elem].update(new_url)

                except Exception as e:
                    print(e)



        # Webserver
        elif event == '-WEBSERVER BUTTON-':
            if not server.running:
                server.setup(ip=values['-WEBSERVER-'], port=int(values['-PORT-']))
                server.start()
                console_text += '*** Started Webserver ***\n'
                gui.window['-WEBSERVER BUTTON-'].update('Stop Webserver {see console}')
            else:
                console_text += f'Attempting to stop server.  May need to click\n "refresh" in your browser to complete shutdown.\n'
                console(console_text)
                gui.window['-WEBSERVER BUTTON-'].update('Start Webserver {BETA}')
                server.stop()
                console_text += '*** Stopped Webserver ***\n'
            console(console_text)

        # Save config.json file in /data
        elif event == '-SAVE CONFIG-':
            if values['-API KEY-']:
                write_config('data/config.json')
                gui.window['-SAVE CONFIG-'].update(button_color=sg.theme_button_color())
            else:
                sg.popup_ok('There was a problem', 'You need to enter an API key before you save your config file.')

        elif event in ['-LEFT-', '-RIGHT-']:
            if xtras and current_performer in xtras:
                if xtras[current_performer]['filepaths']:
                    increment = -1 if event == '-LEFT-' else 1

                    xtras[current_performer]['file_idx'] = update_file_idx(xtras[current_performer]['file_idx'],
                                                                           increment)
                    update_gui()

        # file listbox element was clicked
        elif event in ['-FILES-']:
            try:
                val = values['-FILES-'][0]
            except IndexError as e:
                val = []
            if xtras and current_performer in xtras and val:
                try:
                    xtras[current_performer]['file_idx'] = xtras[current_performer]['filenames'].index(val)
                # if files were deleted, reset index to 0 for current performer
                except ValueError as e:
                    xtras[current_performer]['file_idx'] = 0
            update_gui()

        # save scene data to JSON file for import
        elif event == '-EXPORT-':
            if values['-ititle-'].strip():
                data = gui.save(values)
                file = 'data/scene.json'
                write_json(file, data)
                webserver = values['-WEBSERVER-']
                port = values['-PORT-']

                # copy webserver:port/file to clipboard
                clip_path = f'http://{webserver}:{port}/{file}'
                pyperclip.copy(clip_path)
                console_text += f'Saved JSON file to clipboard as: {clip_path}\n'

                # show popup that scene was imported but webserver not running
                if 'Start' in gui.window['-WEBSERVER BUTTON-'].get_text():
                    sg.popup(
                        'Scene Imported\n\nFIle location has been copied to the clipboard.\nYou may want to start the webserver.')
                    console_text += 'Maybe you should start the webserver?'
                else:
                    sg.popup_quick(
                        'Scene Imported\n\nFile location has been copied to the clipboard so that you can paste into XBVR. ',
                        auto_close_duration=2)
            else:
                sg.popup_ok('You need to scrape a scene first')
            console(console_text)

        elif event == '-SUBMIT-':
            if not config['key']:
                headers = update_headers(values['-API KEY-'])

            if not values['-API KEY-']:
                sg.popup_ok('Need to enter API Key into "ThePornDB Key" field', title="You Probably Fucked Up")
            else:
                search_val = f"{values['-iSearch Studio-']} {values['-iSearch-']}"
                if search_val:
                    gui.window.finalize()
                    console_text += f'Searching for: {search_val}\n'
                    console(console_text)
                    search_result = search(query=search_val, headers=headers)
                    if search_result['data']:
                        console_text += f'Search returned {len(search_result["data"])} results.\n'
                        console(console_text)
                        search_scenes = []
                        for s in search_result['data']:
                            search_scenes.append(s['slug'])
                        search_scenes = natsorted(search_scenes, key=lambda x: x)
                        gui.window['-SCENE RESULTS-'].update(search_scenes)

                    else:
                        scene_result = []
                        search_scenes = []
                        console_text += f'Search did not find any matches.\n'
                        console(console_text)
                        gui.window['-SCENE RESULTS-'].update(search_scenes)
                        gui.window.finalize()

        elif event == '-SCENE RESULTS-':
            # make search dir if it doesn't exist
            Path(Path.cwd() / 'img/temp/search').mkdir(parents=True, exist_ok=True)

            gui.window.finalize()
            if values['-SCENE RESULTS-']:
                selected_scene = values['-SCENE RESULTS-'][0]
                gui.window['-iThePornDB URL-'].update(f'https://api.metadataapi.net/scenes/{selected_scene}')
                if search_result and search_scenes:
                    # search_idx = search_scenes.index(selected_scene)
                    search_idx = 0
                    for idx, result in enumerate(search_result['data']):
                        if result['slug'] == selected_scene:
                            search_idx = idx
                    # search_idx = search_result.index(selected_scene)
                    if 'image' in search_result['data'][search_idx]:
                        scene_result_thumb = search_result['data'][search_idx]['image']
                        process_image(scene_result_thumb, dest='img/temp/search/cover.png', size=(250, 150),
                                      key='-SEARCH IMAGE-')
                else:
                    gui.window['-SEARCH IMAGE-'].update(
                        data=Gui.img_resize('img/placeholders/bigimage-placeholder.png', first=False,
                                            newsize=(250, 150)))



        # if studio button was clicked, populate the studio search input
        elif '-studio' in event:
            gui.window.finalize()
            studio_selected = True
            gui.window['-iSearch Studio-'].update(gui.window[f'{event}'].get_text(), visible=True)
    gui.window.close()
