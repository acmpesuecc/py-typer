# Creating a typing test tool that measures users typing speed and accuracy, providing an entertaining way to improve keyboard skills.
# author: PES2UG23CS368 Nathan Matthew Paul
# author: PES2UG23CS371 Navneet Nayak
# author: PES2UG23CS381 Nevin Mathew Thomas
# author: PES2UG23CS390 Nilay Srivastava
# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2023

import time
import threading
import text_module
from tkinter import *
from tkinter import ttk
from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg) 
from pygame import mixer
import os

sounds = [os.path.abspath("sounds\keyboardclick1") + ".mp3", os.path.abspath("sounds\keyboardclick2") + ".wav", os.path.abspath("sounds\keyboardclick3") + ".wav"]

should_play = True
soundID = 0

mixer.init()
mixer.music.load(sounds[soundID])

class Window:
    def td(self, s):
        self.clear()
        self.time_difficulty = s
        self.restart()

    def choose_td(self):
        self.clear()
        Button(self.window, text="30s", font=("roboto", 30), highlightbackground="gray25", fg="#ebc934", background="gray25", command=lambda: self.td(30)).place(rely=0.5, relx=0.2, anchor=CENTER)
        Button(self.window, text="60s", font=("roboto", 30), highlightbackground="gray25", fg="#ebc934", background="gray25", command=lambda: self.td(60)).place(rely=0.5, relx=0.5, anchor=CENTER)
        Button(self.window, text="120s", font=("roboto", 30), highlightbackground="gray25", fg="#ebc934", background="gray25", command=lambda: self.td(120)).place(rely=0.5, relx=0.8, anchor=CENTER)

    def wd(self, m):
        self.clear()
        self.stop_threads = True
        self.word_difficulty = m
        self.restart()

    def choose_wd(self):
        self.clear()
        Button(self.window, text="easy", font=("roboto", 30), highlightbackground="gray25", fg="#ebc934", background="gray25", command=lambda: self.wd(1)).place(rely=0.4, relx=0.2, anchor=CENTER)
        Button(self.window, text="medium", font=("roboto", 30), highlightbackground="gray25", fg="#ebc934", background="gray25", command=lambda: self.wd(2)).place(rely=0.4, relx=0.5, anchor=CENTER)
        Button(self.window, text="hard", font=("roboto", 30), highlightbackground="gray25", fg="#ebc934", background="gray25", command=lambda: self.wd(3)).place(rely=0.4, relx=0.8, anchor=CENTER)
        Button(self.window, text="freestyle", font=("roboto", 30), highlightbackground="gray25", fg="#ebc934", background="gray25", command=lambda: self.wd(0)).place(rely=0.6, relx=0.5, anchor=CENTER)

    def __init__(self):
        self.stop_threads = False

        self.soundID = soundID

        self.window = Tk()
        self.window.title('py-typer')
        self.window.configure(background="gray25")
        self.window.geometry("900x500")
        self.window.resizable(False, False)
        self.frame = ttk.Frame(self.window, padding=10).grid()

        self.restarted = False

        self.window.grid_columnconfigure((0, 1), weight=1)
        self.window.grid_rowconfigure((0, 1, 2, 3, 4, 5), weight=1)

        self.graph = True
        self.time_difficulty = 30 # 30s for now to easily debug WPM and accuracy
        self.word_difficulty = 1  # 1: means easy, 2: means hard, 3: means difficult, 0: means freestyle mode

        self.setup()

    def clear(self):       
        for widget in self.window.winfo_children():
            widget.destroy()
        
    def setup(self):
        self.mixer_init()

        self.x=[]
        self.y=[]

        self.misspelled = 0
        self.spelled = 1
        self.total_time = self.time_difficulty + 1
        self.accuracy = 0
        self.wpm = 0
        self.write_able = True
        self.cursor_blink = True

        self.type_time = self.total_time - 1

        if self.word_difficulty == 1: text=text_module.easy
        elif self.word_difficulty == 2: text=text_module.medium
        elif self.word_difficulty == 3: text=text_module.hard
        else: text=text_module.freestyle

        self.title_label = Label(self.window, text="py-typer", font=("roboto condensed", 66), fg="#ebc934", background="gray25")
        self.title_label.place(rely=0.05, relx=0.01, anchor=W)

        self.untyped_text = Label(self.window, text=text, font=("roboto condensed", 61), background="gray25", fg="gray60")
        self.untyped_text.place(relx=0.5, rely=0.5, anchor=W)

        self.typed_text = Label(self.window, text="", font=("roboto condensed", 61), fg="#ebc934", background="gray25")
        self.typed_text.place(relx=0.5, rely=0.5, anchor=E)

        self.time_label = Label(self.window, text=self.type_time, font=("roboto condensed", 30), fg="#ebc934", background="gray25")
        self.time_label.grid(row=1, column=2, sticky=S)

        self.accuracy_label = Label(self.window, text=self.accuracy, font=("roboto condensed", 30), fg="#ebc934", background="gray25")
        self.accuracy_label.grid(row=1, column=3, sticky=S)

        self.wpm_label = Label(self.window, text=self.wpm, font=("roboto condensed", 30), fg="#ebc934", background="gray25")
        self.wpm_label.grid(row=1, column=4, sticky=S)

        self.cursor_label = Label(self.window, text="||", background="gray25", fg="gray60", font=("roboto", 20), wraplength=1)
        self.cursor_label.place(relx=0.499, rely=0.51, anchor=CENTER)

        self.calculate_accuracy()
        self.calculate_wpm()
        self.cursor_blinking()

        self.window.bind('<KeyPress>', self.key_press)

    def restart(self):
        self.restarted = True
        self.stop_threads = False
        self.clear()
        self.setup()
        self.mixer_init()

    def plot_graph(self):
        self.mixer_uninit()
        
        self.fig = Figure(figsize = (3, 2), dpi = 100) 
        self.fig.clf()
        plot1 = self.fig.add_subplot() 
        plot1.plot(self.x, self.y, color="#ebc934")
        plot1.set_facecolor("#404040")
        plot1.tick_params(axis='x', colors="grey")
        plot1.tick_params(axis='y', colors="grey")
        plot1.spines['left'].set_color('#404040')        # setting up Y-axis tick color to red
        plot1.spines['top'].set_color('#404040')
        plot1.spines['right'].set_color('#404040')        # setting up Y-axis tick color to red
        plot1.spines['bottom'].set_color('#404040')
        self.fig.patch.set_facecolor("#404040")
        canvas = FigureCanvasTkAgg(self.fig, master = self.window)   
        canvas.draw()
        canvas.get_tk_widget().grid(row=1, column=2)

    def main_menu(self):
        self.clear()
        self.mixer_uninit()

        results_label = Label(self.window, text=self.wpm + "  " + self.accuracy, font=("roboto", 50, "bold"), background="gray25", fg="#ebc934")
        results_label.grid(row=1, column=0)

        restart_button = Button(self.window, text="Restart", font=("roboto", 30), background="gray25", command=self.restart, highlightbackground="gray25", fg="#ebc934")
        restart_button.grid(row=2, column=0)
   
        change_sound_button = Button(self.window, text="Sound", font=("roboto", 30), background="gray25", command=self.change_sound, highlightbackground="gray25", fg="#ebc934")
        change_sound_button.grid(row=2, column=1)
        
        mode_button = Button(self.window, text="Mode", font=("roboto", 30), highlightbackground="gray25", fg="#ebc934", background="gray25", bg="gray25", command=self.modes)
        mode_button.grid(row=2, column=2)

        self.plot_graph()

    def key_press(self, event):
        self.play_sound()
        
        if not self.write_able:
            return None
        if event.keysym == "Shift_L" or event.keysym == "Shift_R":
            return None
        if self.spelled == 1:
            self.start_timer()
        try:
            if event.char == self.untyped_text.cget('text')[:1]:
                self.typed_text.configure(text=self.typed_text.cget('text') + event.char)
                self.untyped_text.configure(text=self.untyped_text.cget('text')[1:])
                self.spelled += 1
                if len(self.untyped_text.cget('text')) < 1:
                    self.clear()
                    self.stop_threads = True
                    self.main_menu()
            else:
                self.misspelled += 1
            self.calculate_accuracy()
        except TclError: pass


    def mixer_uninit(self):
        mixer.quit()
        should_play = False

    def mixer_init(self):
        mixer.init()
        mixer.music.load(sounds[self.soundID])
        should_play = True
        
    def change_sound(self):
        if(self.soundID == len(sounds) - 1):
            self.soundID = 0
        else:
            self.soundID += 1
        
        print(self.soundID)
        
        mixer.init()
        mixer.music.load(sounds[self.soundID])

        self.play_sound()
        
        
    def play_sound(self):
        if(should_play):
            mixer.music.play()

    def start_timer(self):
        self.timer_thread = threading.Thread(target=self.countdown_thread)
        self.timer_thread.daemon = True
        self.timer_thread.start()

    def countdown_thread(self):
        while self.type_time > 0 and self.write_able:
            if self.stop_threads:
                break
            time.sleep(1)
            self.type_time -= 1
            try:
                self.time_label.configure(text=self.type_time)
            except TclError:
                pass

        if self.write_able:
            self.write_able = False
            self.stop_threads = True
            self.main_menu()

    def calculate_accuracy(self):
        self.accuracy = str(int((self.spelled / (self.spelled + self.misspelled)) * 100)) + "%"
        try:
            self.accuracy_label.configure(text=self.accuracy)
        except TclError:
            pass

    def calculate_wpm(self):
        try:
            words_typed = len(self.typed_text.cget('text').split())
            elapsed_time = self.total_time - self.type_time
            self.wpm = int((words_typed / elapsed_time) * 60) 
            self.y.append(self.wpm)
            self.wpm = str(self.wpm) + " WPM"
            self.wpm_label.configure(text=self.wpm)
            self.x.append(elapsed_time)
        except TclError:
            pass
        self.window.after(1000, self.calculate_wpm)
 
    def modes(self):
        self.clear()
        Button(self.window, text="Time Difficulty", font=("roboto", 30), highlightbackground="gray25", fg="#ebc934", background="gray25", command=self.choose_td).place(rely=0.4, relx=0.5, anchor=CENTER)
        Button(self.window, text="Word Difficulty", font=("roboto", 30), highlightbackground="gray25", fg="#ebc934", background="gray25", command=self.choose_wd).place(rely=0.6, relx=0.5, anchor=CENTER)

    def cursor_blinking(self):
        if self.cursor_blink:
            try:
                self.cursor_label.configure(text="")
            except TclError:
                pass
            self.cursor_blink = False
        else:
            try:
                self.cursor_label.configure(text="||")
            except TclError:
                pass
            self.cursor_blink = True
        self.window.after(500, self.cursor_blinking)

window = Window()
window.window.mainloop()
