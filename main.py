import tkinter
import random
import pandas
from tkinter import messagebox

# [--------- app config ---------]
# constants
BACKGROUND_COLOR = "#B1DDC6"


# variables
timer_show_translation = None
timer_show_random_french_word = None
current_word = None


# window setup
window = tkinter.Tk()
window.title("Flashy (language words)")
window.config(padx=80, pady=50, bg=BACKGROUND_COLOR)

# CSV data
try:
    data = pandas.read_csv("./data/words_to_learn.csv")
except FileNotFoundError:
    data = pandas.read_csv("./data/french_words.csv")
finally:
    data_dictionary = data.to_dict(orient="records")


# [--------- handlers ---------]
def set_starting_conditions():
    global  timer_show_random_french_word, timer_show_translation
    timer_show_random_french_word = window.after(2000, show_random_french_word)
    timer_show_translation = window.after(3000, show_translation)

    show_random_french_word()

def show_random_french_word():
    global timer_show_random_french_word, timer_show_translation
    window.after_cancel(timer_show_random_french_word)
    window.after_cancel(timer_show_translation)

    if len(data_dictionary) <= 0:
        canvas.itemconfig(canvas_title, text="")
        canvas.itemconfig(canvas_word, text="Finish!")
        messagebox.showinfo(title="Congratulations!", message="You have learned every word!")
    else:
        timer_show_translation = window.after(3000, show_translation)

        global current_word
        current_word = random.choice(data_dictionary)
        random_french_word = current_word["French"]
        canvas.itemconfig(canvas_title, text="French")
        canvas.itemconfig(canvas_word, text=random_french_word)
        canvas.itemconfig(canvas_background, image=image_card_front)


def show_translation():
    global timer_show_translation, timer_show_random_french_word
    window.after_cancel(timer_show_translation)

    timer_show_random_french_word = window.after(2000, show_random_french_word)

    english_word = current_word["English"]
    canvas.itemconfig(canvas_title, text="English")
    canvas.itemconfig(canvas_word, text=english_word)
    canvas.itemconfig(canvas_background, image=image_card_back)


def remove_known_word():
    global data_dictionary
    updated_words_to_learn_list = [word_object for word_object in data_dictionary if word_object["French"] != current_word["French"]]

    data_dictionary = updated_words_to_learn_list

    updated_words_to_learn = pandas.DataFrame(updated_words_to_learn_list)
    updated_words_to_learn.to_csv("./data/words_to_learn.csv", index=False)

    show_random_french_word()


# [--------- UI ---------]
# canvas
image_card_front = tkinter.PhotoImage(file="./images/card_front.png")
image_card_back = tkinter.PhotoImage(file="./images/card_back.png")

canvas = tkinter.Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
canvas_background = canvas.create_image(400, 273, image=image_card_front)
canvas.grid(row=0, column=0, columnspan=2)
canvas_title = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"))
canvas_word = canvas.create_text(400, 263, text="", font=("Ariel", 60, "bold"))


# buttons
image_button_x = tkinter.PhotoImage(file="./images/wrong.png")
button_unknown_card = tkinter.Button(image=image_button_x, highlightthickness=0, command=show_random_french_word)
button_unknown_card.grid(row=1, column=0)

iamge_button_y = tkinter.PhotoImage(file="./images/right.png")
button_known_card = tkinter.Button(image=iamge_button_y, highlightthickness=0, command=remove_known_word)
button_known_card.grid(row=1, column=1)


# [--------- start app ---------]
# run start function
set_starting_conditions()


# window mainloop
window.mainloop()

