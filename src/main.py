# author: PES2UG23CS368 Nathan Matthew Paul
# author: PES2UG23CS371 Navneet Nayak
# author: I am a loser Nevin Mathew Thomas
# author: PES2UG23CS390 Nilay Srivastava
# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2023

# import stuff
import tkinter as tk

# setup
root = tk.Tk()
root.title('Typing Speed Test')
root.geometry('900x600')

# functions
def sendKeys(event):
    try:
        print(event.char)
    except tk.TclError:
        pass

# paragraph text
para = [
    "Lorem ipsum dolor sit amet, qui minim labore adipisicing minim sint cillum sint consectetur cupidatat."
]

# display the paragraph
text_widget = tk.Text(root, wrap=tk.WORD, height=5, width=40)
text_widget.pack()
text_widget.insert('1.0', para[0])

# Timer
seconds_left=60
def update_timer():
    global seconds_left

    if seconds_left > 0:
        seconds_left -= 1
        timer_label.config(text=f"Time left: {seconds_left} seconds")
        root.after(1000, update_timer)
    else:
        timer_label.config(text="Time's up!")

timer_label = tk.Label(root, text=f"Time left: {seconds_left} seconds",)
timer_label.pack()
def click():
    global seconds_left
    seconds_left = 60
    update_timer()

bt1 = tk.Button(root,text="Start timer", bg='light blue', fg='green',command=click)
bt1.pack()

# capture the keys
root.bind('<KeyPress>', sendKeys)
root.mainloop()

