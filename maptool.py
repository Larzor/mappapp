import tkinter as tk
from tkinter import ttk
import tkintermapview as tmap
import customtkinter as ctk
from scen_objects import Scenario_object, ObjectFrame
from geographiclib.geodesic import Geodesic
import math
import geopy.distance as geodist
from buttons import Elements,Object_list
from frames import ToggledFrame, Scrollable

tkwin = tk.Tk()
tkwin.geometry(f"{1300}x{700}")
tkwin.title("Scenario maker tool")

tkwin.update()

themap = tmap.TkinterMapView(tkwin, width=tkwin.winfo_width(), height=tkwin.winfo_height())
themap.place(relx=0.0,rely=0.0,anchor=tk.NW)
themap.set_position(59.16230881,17.62880853)

object_list:Object_list = Object_list()

buttons = Elements(tkwin,themap,object_list)

button_poi = ctk.CTkButton(tkwin, text="POI",command=buttons.poi_button,width=20)

button_truck = ctk.CTkButton(tkwin, text="Truck",command=buttons.truck_button,width=20)

button_static_obj = ctk.CTkButton(tkwin, text="static object",command=buttons.statobj_button)

button_measure = ctk.CTkButton(tkwin,text="Measure Distance",command=buttons.measure_button)

button_coords = ctk.CTkButton(tkwin,text="coords",command=buttons.coord_button)

button_save = ctk.CTkButton(tkwin,text="save scenario",command=buttons.save_button)

button_read = ctk.CTkButton(tkwin,text="load scenario",command=buttons.read_button)

packgen = [i.pack(side=tk.LEFT,padx=10,pady=20,anchor=tk.SW) for i in [button_poi,button_truck,button_static_obj,button_measure,button_coords]]


# Tkinter is not very good at scrolling

# side_list_canvas=tk.Canvas(tkwin)
# side_list_canvas = tk.Canvas(tkwin)
# side_list_canvas.pack(side="right",fill="none",expand=0,anchor="ne")
side_list=ttk.Frame(tkwin)
side_list.pack(side="right",fill=tk.NONE,expand=1,anchor="ne")
scroll = Scrollable(side_list)

# for i in range(30):
#     ttk.Button(scroll, text="I'm a button in the scrollable frame").grid()
# scroll = ctk.CTkScrollbar(side_list_canvas,command=side_list_canvas.yview,orientation="vertical")
# side_list_canvas.pack(side="right",fill="none",expand=0,anchor="ne")
# side_list_canvas.configure(yscrollcommand=scroll.set)
# scroll.pack(side="right",fill="y",expand=0,anchor="ne")
# side_list_canvas.create_window(0,0,anchor="ne",window=side_list, tags="side_list")

# def update_scroll(event=None):
#     side_list_canvas.configure(scrollregion=side_list_canvas.bbox("all"))

# side_list.bind("<Configure>", update_scroll)



side_list.update_idletasks()

# side_list=tk.Frame(tkwin)
# canvas.create_window(0,0,window=side_list, anchor='ne')

# scroll = tk.Scrollbar(side_list, orient=tk.VERTICAL)
# scroll.pack(side="right",fill="y", expand=1)
# scroll.config(command=side_list.yview)
# side_list.configure(yscrollcommand=scroll.set)

# def update_scroll(event=None):
#     side_list.configure(scrollregion="")
#     scroll.update_idletasks()
#     side_list.update_idletasks()

# side_list.bind("<Configure>",update_scroll)
side_list.update()

# side_list.pack(fill="none",side="right", expand=1, pady=2, padx=2, anchor="ne")


headline = ctk.CTkLabel(scroll,text="Objects:",width=300).pack(fill="x", expand=1, pady=2, padx=2, anchor="n")

def update_side_list():
    create_object_menu()
    tkwin.after(250,update_side_list)

def create_object_menu():
    for i in object_list.get_list():
        if i.deleted:
            object_list.remove_from_list(i)
            scroll.update()
            
        elif (i.frame is None):
            i.set_frame(scroll)
            print("making menu "+i.name)
            scroll.update()

tkwin.update_idletasks()

tkwin.after(500,update_side_list)


tkwin.mainloop()
    