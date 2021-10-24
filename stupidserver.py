from http.server import HTTPServer, SimpleHTTPRequestHandler
import PySimpleGUI as sg
import threading


class StupidServer:
    """
    creates simple HTTPServer in its own thread
    usage: server = StupidServer()
           server.setup(ip='localhost', port=8000)
    """

    def __init__(self):
        self.running = False
        self.first_run = True

    def setup(self, ip='localhost', port=8000):
        self.port = port
        self.ip = ip
        self.http_server = HTTPServer((ip, port), SimpleHTTPRequestHandler)
        self.first_run = False

    def start(self):
        try:
            thread = threading.Thread(target=self.http_server.serve_forever)
            thread.deamon = True
            thread.start()
            self.running = True
            text = f'starting server on port {self.port}'
        except:
            self.running = False
            text = f'unable to start server on port {self.port}'
        return text

    def stop(self):
        try:

            self.running = False
            self.http_server.shutdown()
            text = f'stopped server on port {self.port}'
        except:
            self.running = True
            text = f'unable to shutdown server'
        return text


if __name__ == '__main__':
    # command to find and kill process in windows
    # netstat -ano|findstr 8000 (pick port)
    # tskill #######

    server = StupidServer()
    server.setup(ip='localhost', port=6969)

    window = sg.Window('HTTP Threads Server Test',
                       [[
                           sg.Button('Stop', key='-STOP-', size=(20, 1)),
                           sg.Button('Start', key='-START-', size=(20, 1), enable_events=True)
                       ]], size=(400, 50))

    while True:
        event, values = window.read()

        if event == 'Exit' or event == sg.WIN_CLOSED:
            if server.running:
                server.stop()
            break

        elif event == '-START-':
            if not server.running:
                server.start()
            else:
                print('server is already running')

        elif event == '-STOP-':
            if server.running:
                server.stop()
            else:
                print('server is already stopped')
