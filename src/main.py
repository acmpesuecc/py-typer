# author: PES2UG23CS368 Nathan Matthew Paul
# author: PES2UG23CS3XX Navneet Nayak
# author: PES2UG23CS3XX Nevin Mathew Thomas
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

# capture the keys
root.bind('<KeyPress>', sendKeys)
root.mainloop()

