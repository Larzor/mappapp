from geopy.distance import Geodesic
import tkintermapview as tmap
from tkintermapview.canvas_path import CanvasPath
from tkintermapview.canvas_polygon import CanvasPolygon
from tkintermapview.canvas_position_marker import CanvasPositionMarker as Mapmarker
from typing import Literal
from frames import ToggledFrame
import customtkinter as ctk
import tkinter as tk
import math
import sys


class Scenario_object:
    def __init__(self,typ:Literal["truck","poi","static object"], mapp:tmap.TkinterMapView,rot:tk.Tk):
        self.typ = typ
        self.mapp = mapp
        self.rot = rot
        # self.length = 9.2
        # self.width = 2.65
        self.angle = 0.0
        self.position = None
        self.marker:CanvasMarkerNew=None
        # self.angle_arrow = None
        self.polygon:CanvasPolygon = None
        self.points:list[tuple][float]=[]
        self.name = "grej"
        
        self.frame = None
        self.deleted = False

    def set_frame(self, main_frame):
        self.frame = ObjectFrame(main_frame,self)
        main_frame.update()
    
    def set_position(self,pos:tuple[float]):

        self.position = pos
        if self.marker is None:
        
            marker:CanvasMarkerNew=self.set_mapp_marker(self.position[0],self.position[1],text=self.name)
            
            self.set_marker(marker)
             
        if self.typ == "static object" and len(self.points) > 2:
            self.draw_polygon()
            
        self.marker.set_position(pos[0],pos[1])
        if self.frame is not None:
            self.frame.update_x_frame()
            self.frame.update_y_frame()
    
    def draw_polygon(self,finished=False):
        if self.polygon == None:
            if finished:
                self.polygon = self.mapp.set_polygon(self.points,outline_color = "black",
                 fill_color= "grey",
                 border_width= 2)
            else:
                self.polygon = self.mapp.set_polygon(self.points)
        self.polygon.draw()

    
    def set_mapp_marker(self, deg_x: float, deg_y: float, text: str = None, **kwargs) -> Mapmarker:
        
        marker = CanvasMarkerNew(self.mapp, (deg_x, deg_y), text=text, **kwargs)
        
        marker.draw()
        self.mapp.canvas_marker_list.append(marker)
        self.mapp.update()
        return marker
    
    def set_marker(self,marker):
        self.marker:CanvasMarkerNew=marker
        self.marker.poi = self # I dunno about this, but I'll try it...

    def set_x(self,x:float):
        position = (x,self.position[1])
        self.set_position(position)

    def set_y(self,y:float):
        position = (self.position[0],y)
        self.set_position(position)
        
        
    def set_angle(self,angle:float):
        self.angle = angle
        self.marker.set_angle(self.angle)
        if self.frame is not None:
            self.frame.update_angle_frame()
    

    def set_name(self,name:str):
        self.name = name
        if self.marker != None:
            self.marker.text = self.name
        if self.frame != None:
            self.frame.frame.set_text(self.name)

class ObjectFrame:
    def __init__(self, main_frame, mapobject:Scenario_object):
        self.main_frame = main_frame
        self.obj = mapobject
        self.frame = None
        self.angle_frame = None
        self.angle_label:tk.Label = None
        self.print_frame = None

        self.x_frame = None
        self.y_frame = None
        self.x_label:tk.Label = None
        self.y_label:tk.Label = None
        self.set_frame()

    def set_frame(self):
        self.frame = ToggledFrame(self.main_frame, text=self.obj.name)
        self.frame.pack(fill="x", expand=1, pady=2, padx=2, side="top")
        
        self.show_change_name()
        self.show_coordinates()
        self.show_angle()
        self.show_print_object()
        self.show_delete()
    
    def show_print_object(self):
        self.print_frame=ctk.CTkFrame(self.frame.sub_frame)
        self.print_frame.pack(fill="x", expand=1, pady=2, padx=2, anchor="n")
        ctk.CTkButton(self.print_frame,text="print object",width=10,command=self.printobj).pack(side="left")
    
    def printobj(self):
        print(self.obj.typ)
        print(self.obj.name)
    
        if self.obj.typ == "truck":
            printstring = f"""def create_cloudias(self):
                self.truck = self.create_cloudia(
                    Position({self.obj.angle}, {self.obj.position[1]}, {self.obj.position[0]}), '{self.obj.name}', time_scale=1.0)"""
        if self.obj.typ == "static object":
            printstring = f"static_object = StaticObject(name='{self.obj.name}',position=({self.obj.position[0]},{self.obj.position[1]}) ,polygons=[{self.obj.points}])"
        if self.obj.typ == "poi":
            printstring = f"point_of_interest = Position(latitude={self.obj.position[0]},longitude={self.obj.position[1]},heading={self.obj.angle})"
        print(printstring)
        

    def show_angle(self):
        self.angle_frame=ctk.CTkFrame(self.frame.sub_frame)
        self.angle_frame.pack(fill="x", expand=1, pady=2, padx=2, anchor="n")
        self.angle_label:tk.Label = tk.Label(self.angle_frame, text=f"angle: {round(self.obj.angle,2)}°")
        self.angle_label.pack(side="left",fill="x", expand=1)
        self.update_angle_frame()

    def update_angle_frame(self):
        if self.angle_label is not None:

            self.angle_label.config(text=f"angle: {round(self.obj.angle,2)}°")
    
    def update_x_frame(self):
        if self.x_label is not None:

            self.x_label.config(text=f"Lat: {self.obj.position[0]}")

    def update_y_frame(self):
        if self.y_label is not None:

            self.y_label.config(text=f"Lon: {self.obj.position[1]}")
        

    
    def show_delete(self):
        delframe = ctk.CTkFrame(self.frame.sub_frame)
        delframe.pack(fill="x", expand=1, pady=2, padx=2, anchor="n")
        ctk.CTkButton(delframe,text="delete",command=self.remove_self,fg_color="red").pack(side="right",fill="x", expand=1)
    
    def show_change_name(self):
        frame = ctk.CTkFrame(self.frame.sub_frame)
        frame.pack(fill="x", expand=1, pady=2, padx=2, anchor="n")
        ctk.CTkLabel(frame, text=f"change name").pack(side="left",fill="x", expand=1)
        self.name_var=tk.StringVar()
        tk.Entry(frame,textvariable=self.name_var).pack(side="left")
        ctk.CTkButton(frame,text="",width=20,command=self.change_name_input).pack(side="left")
    
    def change_name_input(self):
        name = self.name_var.get()
        self.obj.set_name(name)

    def show_coordinates(self):
        self.x_frame = ctk.CTkFrame(self.frame.sub_frame)
        self.x_frame.pack(fill="x", expand=1, pady=2, padx=2, side="top")
        self.x_label = tk.Label(self.x_frame, text=f"X: {self.obj.position[0]}")
        self.x_label.pack(side="left",fill="x", expand=1)

        self.y_frame = ctk.CTkFrame(self.frame.sub_frame)
        self.y_frame.pack(fill="x", expand=1, pady=2, padx=2, side="top")
        self.y_label = tk.Label(self.y_frame, text=f"Y: {self.obj.position[1]}")
        self.y_label.pack(side="left",fill="x", expand=1)

    def remove_self(self):
        if self.obj.polygon != None:
            self.obj.polygon.delete()
        self.frame.pack_forget()
        self.obj.deleted = True
        self.obj.marker.delete()

class Measurement:
    def __init__(self):
        self.angle = None
        self.length = None
        self.coords = None
class Map_Line:
    def __init__(self, start_coords, start_map_coords) -> None:
        self.start = start_coords
        self.start_map_coords = start_map_coords
        self.end = None
        self.end_map_coords = None
    
    def set_start(self, coords):
        self.start = coords
    
    def set_end(self, coords, map_coords):
        self.end = coords
        self.end_map_coords = map_coords
    
class Object_list:
    def __init__(self):
        self.trucknum = 1
        self.poinum = 1
        self.statobjnum = 1
        self.object_list:list[Scenario_object] = []
        
    def add_object(self,obj:Scenario_object):
        if obj.typ == "truck": 
            name = f"truck {self.trucknum}"
            self.trucknum += 1
            print(self.trucknum)
        elif obj.typ == "poi":
            name = f"point {self.poinum}"
            self.poinum += 1
            print(self.poinum)
        else:
            name = f"static object {self.statobjnum}"
            self.statobjnum += 1

        obj.set_name(name)
        self.object_list.append(obj)
    
    def get_list(self):
        return self.object_list
    
    def remove_from_list(self, obj):
        self.object_list.remove(obj)
        
    


class CanvasMarkerNew(Mapmarker):
    def __init__(self,*args,angle_command=None,text_command=None,**kwargs):
        super().__init__(*args,**kwargs)
        self.angle_circle = None
        self.angle_line = None
        self.angle_command = angle_command
        self.text_command = text_command
        self.angle = 0
        self.x = None
        self.y = None
        self.poi:Scenario_object = None

    def delete(self):
        if self in self.map_widget.canvas_marker_list:
            self.map_widget.canvas_marker_list.remove(self)

        self.map_widget.canvas.delete(self.angle_line)
        self.map_widget.canvas.delete(self.angle_circle)
        self.map_widget.canvas.delete(self.polygon)
        self.map_widget.canvas.delete(self.big_circle)
        self.map_widget.canvas.delete(self.canvas_text)
        self.map_widget.canvas.delete(self.canvas_icon)
        self.map_widget.canvas.delete(self.canvas_image)

        self.polygon, self.big_circle, self.canvas_text, self.canvas_image, self.canvas_icon, self.angle_circle, self.angle_line = None, None, None, None, None, None, None
        self.deleted = True
        self.map_widget.canvas.update()
    
    def set_angle(self,angle):
        self.angle = angle
    
    def calculate_angle_line(self,pos_x,pos_y):
        angle_rad = math.radians(self.angle)
        point2_x = math.cos(angle_rad)*14 + pos_x
        point2_y = math.sin(angle_rad)*-14 + pos_y

        return point2_x,point2_y
    
    def mouse_enter(self, event=None):
    
        if sys.platform == "darwin":
            self.map_widget.canvas.config(cursor="pointinghand")
        elif sys.platform.startswith("win"):
            self.map_widget.canvas.config(cursor="hand2")
        else:
            self.map_widget.canvas.config(cursor="hand2")  # not tested what it looks like on Linux!

    def mouse_leave(self, event=None):
        
        self.map_widget.canvas.config(cursor="arrow")
    
    def text_click(self, event=None):
        if self.text_command is not None:
            self.text_command(self)

    def click(self, event=None):
        if self.command is not None:
            self.command(self)
    
    def angle_click(self,event=None):
        if self.angle_command is not None:
            self.clicked = True
            self.angle_command(self)

    
    def draw(self, event=None):
        canvas_pos_x, canvas_pos_y = self.get_canvas_pos(self.position)
        self.x = canvas_pos_x
        self.y = canvas_pos_y
        

        if not self.deleted:
            if 0 - 50 < canvas_pos_x < self.map_widget.width + 50 and 0 < canvas_pos_y < self.map_widget.height + 70:

                


                # draw icon image for marker
                if self.icon is not None:
                    if self.canvas_icon is None:
                        self.canvas_icon = self.map_widget.canvas.create_image(canvas_pos_x, canvas_pos_y,
                                                                               anchor=self.icon_anchor,
                                                                               image=self.icon,
                                                                               tag="marker")
                        if self.command is not None:
                            self.map_widget.canvas.tag_bind(self.canvas_icon, "<Enter>", self.mouse_enter)
                            self.map_widget.canvas.tag_bind(self.canvas_icon, "<Leave>", self.mouse_leave)
                            self.map_widget.canvas.tag_bind(self.canvas_icon, "<Button-1>", self.click)
                    else:
                        self.map_widget.canvas.coords(self.canvas_icon, canvas_pos_x, canvas_pos_y)

                # draw standard icon shape
                else:
                    if self.polygon is None:
                        self.polygon = self.map_widget.canvas.create_polygon(canvas_pos_x - 14, canvas_pos_y - 23,
                                                                             canvas_pos_x, canvas_pos_y,
                                                                             canvas_pos_x + 14, canvas_pos_y - 23,
                                                                             fill=self.marker_color_outside, width=2,
                                                                             outline=self.marker_color_outside, tag="marker")
                        if self.command is not None:
                            self.map_widget.canvas.tag_bind(self.polygon, "<Enter>", self.mouse_enter)
                            self.map_widget.canvas.tag_bind(self.polygon, "<Leave>", self.mouse_leave)
                            self.map_widget.canvas.tag_bind(self.polygon, "<Button-1>", self.click)
                    else:
                        self.map_widget.canvas.coords(self.polygon,
                                                      canvas_pos_x - 14, canvas_pos_y - 23,
                                                      canvas_pos_x, canvas_pos_y,
                                                      canvas_pos_x + 14, canvas_pos_y - 23)
                    if self.big_circle is None:
                        self.big_circle = self.map_widget.canvas.create_oval(canvas_pos_x - 14, canvas_pos_y - 45,
                                                                             canvas_pos_x + 14, canvas_pos_y - 17,
                                                                             fill=self.marker_color_circle, width=6,
                                                                             outline=self.marker_color_outside, tag="marker")
                        if self.command is not None:
                            self.map_widget.canvas.tag_bind(self.big_circle, "<Enter>", self.mouse_enter)
                            self.map_widget.canvas.tag_bind(self.big_circle, "<Leave>", self.mouse_leave)
                            self.map_widget.canvas.tag_bind(self.big_circle, "<Button-1>", self.click)
                    else:
                        
                        self.map_widget.canvas.coords(self.big_circle,
                                                      canvas_pos_x - 14, canvas_pos_y - 45,
                                                      canvas_pos_x + 14, canvas_pos_y - 17)
            # draw angle circle
                if self.angle_circle is None:
                    
                    self.angle_circle = self.map_widget.canvas.create_oval(canvas_pos_x - 14, canvas_pos_y - 14,
                                                                             canvas_pos_x + 14, canvas_pos_y + 14,
                                                                            width=3,
                                                                             outline="black", tag="button")
                    if self.angle_command is not None:
                            self.map_widget.canvas.tag_bind(self.angle_circle, "<Enter>", self.mouse_enter)
                            self.map_widget.canvas.tag_bind(self.angle_circle, "<Leave>", self.mouse_leave)
                            self.map_widget.canvas.tag_bind(self.angle_circle, "<Button-1>", self.angle_click)
                else:
                    
                    self.map_widget.canvas.coords(self.angle_circle,
                                                    canvas_pos_x - 14, canvas_pos_y - 14,
                                                    canvas_pos_x + 14, canvas_pos_y + 14)
                if self.angle is not None:
                    ang_x,ang_y = self.calculate_angle_line(canvas_pos_x,canvas_pos_y)
                    if self.angle_line is None:
                        
                        self.angle_line = self.map_widget.canvas.create_line(canvas_pos_x, canvas_pos_y,
                                                                                ang_x,ang_y,
                                                                                width=2,fill="black",
                                                                                tag="marker")

                    else:
                        
                        self.map_widget.canvas.coords(self.angle_line,
                                                        canvas_pos_x, canvas_pos_y,
                                                                                ang_x,ang_y)

                if self.text is not None:
                    if self.canvas_text is None:
                        self.canvas_text = self.map_widget.canvas.create_text(canvas_pos_x, canvas_pos_y + self.text_y_offset,
                                                                              anchor=tk.S,
                                                                              text=self.text,
                                                                              fill=self.text_color,
                                                                              font=self.font,
                                                                              tag=("marker_text"))
                        if self.text_command is not None:
                            self.map_widget.canvas.tag_bind(self.canvas_text, "<Enter>", self.mouse_enter)
                            self.map_widget.canvas.tag_bind(self.canvas_text, "<Leave>", self.mouse_leave)
                            self.map_widget.canvas.tag_bind(self.canvas_text, "<Button-1>", self.text_click)
                    else:
                        self.map_widget.canvas.coords(self.canvas_text, canvas_pos_x, canvas_pos_y + self.text_y_offset)
                        self.map_widget.canvas.itemconfig(self.canvas_text, text=self.text)
                else:
                    if self.canvas_text is not None:
                        self.map_widget.canvas.delete(self.canvas_text)

                if self.image is not None and self.image_zoom_visibility[0] <= self.map_widget.zoom <= self.image_zoom_visibility[1]\
                        and not self.image_hidden:

                    if self.canvas_image is None:
                        self.canvas_image = self.map_widget.canvas.create_image(canvas_pos_x, canvas_pos_y + (self.text_y_offset - 30),
                                                                                anchor=tk.S,
                                                                                image=self.image,
                                                                                tag=("marker", "marker_image"))
                    else:
                        self.map_widget.canvas.coords(self.canvas_image, canvas_pos_x, canvas_pos_y + (self.text_y_offset - 30))
                else:
                    if self.canvas_image is not None:
                        self.map_widget.canvas.delete(self.canvas_image)
                        self.canvas_image = None
            else:
                self.map_widget.canvas.delete(self.canvas_icon)
                self.map_widget.canvas.delete(self.polygon)
                self.map_widget.canvas.delete(self.canvas_text)
                self.map_widget.canvas.delete(self.big_circle)
                self.map_widget.canvas.delete(self.canvas_image)
                self.map_widget.canvas.delete(self.angle_circle)
                self.map_widget.canvas.delete(self.angle_line)
                self.canvas_text, self.polygon, self.big_circle, self.canvas_image, self.canvas_icon, self.angle_circle, self.angle_line = None, None, None, None, None, None, None

            self.map_widget.manage_z_order()





class CanvasPathNew(CanvasPath):
    def draw(self,move=False):
        new_line_length = self.last_position_list_length != len(self.position_list)
        self.last_position_list_length = len(self.position_list)

        widget_tile_width = self.map_widget.lower_right_tile_pos[0] - self.map_widget.upper_left_tile_pos[0]
        widget_tile_height = self.map_widget.lower_right_tile_pos[1] - self.map_widget.upper_left_tile_pos[1]

        if move is True and self.last_upper_left_tile_pos is not None and new_line_length is False:
            x_move = ((self.last_upper_left_tile_pos[0] - self.map_widget.upper_left_tile_pos[0]) / widget_tile_width) * self.map_widget.width
            y_move = ((self.last_upper_left_tile_pos[1] - self.map_widget.upper_left_tile_pos[1]) / widget_tile_height) * self.map_widget.height

            for i in range(0, len(self.position_list)* 2, 2):
                self.canvas_line_positions[i] += x_move
                self.canvas_line_positions[i + 1] += y_move
        else:
            self.canvas_line_positions = []
            for position in self.position_list:
                canvas_position = self.get_canvas_pos(position, widget_tile_width, widget_tile_height)
                self.canvas_line_positions.append(canvas_position[0])
                self.canvas_line_positions.append(canvas_position[1])

        if not self.deleted:
            if self.canvas_line is None:
                self.map_widget.canvas.delete(self.canvas_line)
                self.canvas_line = self.map_widget.canvas.create_line(self.canvas_line_positions,
                                                                        width=self.width, fill=self.path_color,
                                                                        capstyle=tk.ROUND, joinstyle=tk.ROUND,
                                                                        tag="path")

                if self.command is not None:
                    self.map_widget.canvas.tag_bind(self.canvas_line, "<Enter>", self.mouse_enter)
                    self.map_widget.canvas.tag_bind(self.canvas_line, "<Leave>", self.mouse_leave)
                    self.map_widget.canvas.tag_bind(self.canvas_line, "<Button-1>", self.click)
            else:
                self.map_widget.canvas.coords(self.canvas_line, self.canvas_line_positions)
        else:
            self.map_widget.canvas.delete(self.canvas_line)
            self.canvas_line = None

        self.map_widget.manage_z_order()
        self.last_upper_left_tile_pos = self.map_widget.upper_left_tile_pos