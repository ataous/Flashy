from random import choice
from tkinter import *

import pandas as pd

BACKGROUND_COLOR = "#B1DDC6"
SRC_DATA_FILE = "data/french_words.csv"
DATA_FILE = "data/word_to_learn.csv"
FLIP_DELAY = 3000

try:
    data = pd.read_csv(DATA_FILE)
except FileNotFoundError:
    data = pd.read_csv(SRC_DATA_FILE)

to_learn = data.to_dict(orient="records")
card = {}


# -------------------------- Func -------------------------- #
def flip_card():
    global back_card_img
    canvas.itemconfig(canvas_img, image=back_card_img)
    canvas.itemconfig(title, text="English", fill="white")
    canvas.itemconfig(word, text=card["English"], fill="white")


def next_card():
    global front_card_img
    canvas.itemconfig(canvas_img, image=front_card_img)

    global card, flip_timer
    root.after_cancel(flip_timer)
    try:
        card = choice(to_learn)
    except IndexError:
        canvas.itemconfig(title, text="", fill="black")
        canvas.itemconfig(word, text="You're Done.", fill="black")
    else:
        canvas.itemconfig(title, text="French", fill="black")
        canvas.itemconfig(word, text=card["French"], fill="black")
        flip_timer = root.after(FLIP_DELAY, flip_card)


def is_known():
    global card
    try:
        to_learn.remove(card)
    except ValueError:
        pass
    else:
        new_data = pd.DataFrame(to_learn)
        new_data.to_csv(DATA_FILE, index=False)
        next_card()


# -------------------------- GUI -------------------------- #
root = Tk()
root.title("Flashy")
root.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = root.after(FLIP_DELAY, func=flip_card)

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
front_card_img = PhotoImage(file="images/card_front.png")
back_card_img = PhotoImage(file="images/card_back.png")
canvas_img = canvas.create_image(400, 263, image=front_card_img)
title = canvas.create_text(400, 150, text="", font=("Arial", 24, "italic"))
word = canvas.create_text(400, 263, text="", font=("Arial", 45, "bold"))
canvas.grid(row=0, column=0, columnspan=2)

btn_wrong_img = PhotoImage(file="images/wrong.png")
btn_wrong_answer = Button(image=btn_wrong_img, relief=FLAT, bg=BACKGROUND_COLOR, command=next_card)
btn_wrong_answer.grid(row=1, column=0)

btn_right_img = PhotoImage(file="images/right.png")
btn_right_answer = Button(image=btn_right_img, relief=FLAT, bg=BACKGROUND_COLOR, command=is_known)
btn_right_answer.grid(row=1, column=1)

next_card()
root.mainloop()
