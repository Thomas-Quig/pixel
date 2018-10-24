# Evan Widloski - 2018-10-15
# Skeleton Flask App for Twilight
from flask import Flask, request, make_response
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import logging
import tkinter as tk
import threading
from tkinter import *
master = Tk()

# w = Canvas(master, width=1600, height=900)
# w.create_rectangle(0, 0, 100, 100, fill="blue", outline = 'blue')
# w.create_rectangle(50, 50, 100, 100, fill="red", outline = 'blue')
# w.pack()
# master.mainloop()


class TkApp(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.start()

    def callback(self):
        self.root.quit()

    def run(self):
        self.root = tk.Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.callback)
        self.w = tk.Canvas(self.root, width=1600, height=900)
        # self.w.create_rectangle(0, 0, 100, 100, fill="blue", outline = 'blue')
        # self.w.create_rectangle(50, 50, 100, 100, fill="red", outline = 'blue')
        self.w.pack()

        label = tk.Label(self.root, text="Hello World")
        label.pack()

        self.root.mainloop()

tkapp = TkApp()

logging.basicConfig(level=logging.INFO, format='%(message)s')

app = Flask(__name__)
limiter = Limiter(app, key_func=get_remote_address)

screen_width = 1600
screen_height = 900

display_width = 16
display_height = 16

pixel_width = screen_width / display_width
pixel_height = screen_height / display_height


# @limiter.limit("2/minute")
@app.route('/', methods=['POST'])
def hello():
    """POST endpoint for JSON data"""

    try:
        x = int(request.headers.get('x'))
        y = int(request.headers.get('y'))
        color = request.headers.get('color')

        print(x, y, color)

        tkapp.w.create_rectangle(
            x * pixel_width,
            y * pixel_height,
            x * pixel_width + pixel_width,
            y * pixel_height + pixel_height,
            fill=color,
            width=0
        )
    except Exception:
        return "you suck\n"
    finally:
        return "success\n"


@app.errorhandler(429)
def ratelimit(e):
    """Custom response for rate limit exceeded"""

    return make_response("Rate limit exceeded: {}\n".format(e.description), 429)
