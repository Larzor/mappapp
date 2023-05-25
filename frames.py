import tkinter as tk
from tkinter import ttk
import customtkinter as ctk



class Scrollable(tk.Frame):
    """
       Make a frame scrollable with scrollbar on the right.
       After adding or removing widgets to the scrollable frame,
       call the update() method to refresh the scrollable area.
    """

    def __init__(self, frame):

        scrollbar = ctk.CTkScrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, expand=1)

        self.canvas = tk.Canvas(frame, yscrollcommand=scrollbar.set)
        self.canvas.pack(side=tk.RIGHT, fill=tk.NONE, expand=1, anchor="ne")

        scrollbar.configure(command=self.canvas.yview)

        # self.canvas.bind('<Configure>', self.__fill_canvas)

        # base class initialization
        tk.Frame.__init__(self, frame)

        # assign this obj (the inner frame) to the windows item of the canvas
        self.windows_item = self.canvas.create_window(0,0, window=self, anchor=tk.NE)


    # def __fill_canvas(self, event):
    #     "Enlarge the windows item to the canvas width"

    #     canvas_width = event.width
    #     self.canvas.itemconfig(self.windows_item, width = canvas_width)

    def update(self):
        "Update the canvas and the scrollregion"

        self.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox(self.windows_item))


class ToggledFrame(ctk.CTkFrame):

    def __init__(self, parent, text="", *args, **options):
        ctk.CTkFrame.__init__(self, parent, *args, **options)
        self.show = tk.IntVar()
        # self.updated = True
        self.show.set(1)
        self.title_frame = ctk.CTkFrame(self)
        self.title_frame.pack(fill="x", expand=1)
        self.parent = parent

        self.label:ctk.CTkLabel = ctk.CTkLabel(self.title_frame, text=text)
        self.label.pack(side="left", fill="x", expand=1)

        self.toggle_button = ctk.CTkButton(self.title_frame,width=2,text="+",command=self.toggle)
        
        self.toggle_button.pack(side="left")

        self.sub_frame = ctk.CTkFrame(self,fg_color="white")

    def toggle(self):
        # self.updated = True
        if bool(self.show.get()):
            self.show.set(0)
            self.sub_frame.pack(fill="x", expand=1)
            self.toggle_button.configure(text='-')
            
        else:
            self.show.set(1)
            self.sub_frame.forget()
            self.toggle_button.configure(text='+')
        self.parent.update()
    
    def set_text(self,new_text:str):
        self.label.configure(text=new_text)