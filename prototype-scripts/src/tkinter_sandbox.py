"""
Dieses Script wird benutzt um schnell einen UI Prototyp mit Tkinter zu erstellen.
"""

import time
import tkinter

import cv2 as cv
from tkinter import *
from tkinter.ttk import *
import PIL.Image
import PIL.ImageTk

PADDING = 12
BORDER = 2

# Window created with tkinter
window = Tk()
window.attributes("-fullscreen", True)
window.update()
window_width = window.winfo_width()

Style().configure("TFrame", background="white")
Style().configure("CustomPanel.TLabel", borderwidth=BORDER, relief="flat", background="black")
Style().configure("CustomLabel.TLabel", background="white", font="jetbrainsmono 34")


def key_up(e):
    if e.keysym == 'Escape':
        sys.exit(0)


print(window_width)
image_size = window_width // 2 - PADDING * 2 - BORDER * 2

panel_frame = Frame(window)

# setup images
cv_img = cv.cvtColor(cv.imread("rock.png"), cv.COLOR_BGR2RGB)
cv_img = cv.resize(cv_img, (image_size, image_size))
photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(cv_img))
panel = Label(panel_frame, image=photo, style="CustomPanel.TLabel")
panel.pack(side="left", fill="x", expand=False, padx=(PADDING, PADDING), pady=(PADDING, PADDING))

cam_photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(cv_img * 2))
panel_cam = Label(panel_frame, image=cam_photo, style="CustomPanel.TLabel")
panel_cam.pack(side="right", fill="x", expand=False, padx=(PADDING, PADDING), pady=(PADDING, PADDING))
panel_frame.pack(side="top")
panel_frame.update()
window.update()

cv_img = cv.cvtColor(cv.imread("rock.png"), cv.COLOR_BGR2RGB)
cv_img = cv.resize(cv_img, (image_size, image_size))
photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(cv_img))
panel.configure(image=photo)

cam_photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(cv_img * 2))
panel_cam.configure(image=cam_photo)

label_frame = Frame(window)
label = Label(label_frame, text="let var: i64 = 88 * 33;", style="CustomLabel.TLabel")
label.pack(side="bottom", fill="y", anchor="n", expand=TRUE)
label_frame.pack(side="bottom", fill="both", anchor="center", expand=True)
label_frame.update()

window.bind('<KeyRelease>', key_up)
window.update()
window.mainloop()
