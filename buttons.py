from dataclasses import dataclass
import tkinter as tk
import customtkinter as ctk
import geopy.distance as geodist
import tkintermapview as tmap
import pyproj
from scen_objects import Map_Line, Scenario_object, Object_list, Measurement, CanvasMarkerNew as mapmarker
from frames import ToggledFrame
from file_handling import save_file

class Elements:
    def __init__(self, root:tk.Tk, mapp:tmap.TkinterMapView,object_list):
        self.root = root
        self.mapp = mapp

        self.map_coords = mapp.get_position()
        self.line = None
        self.angle = None
        self.mouse_pos = None
        self.temp=None
        self.poi=None
        self.objlist:Object_list = object_list
        self.measure = Measurement()
    
    def read_button(self):
        pass
        # .read_scenario_file()
    
    def save_button(self):
        pass
    # Kanske ska göra en till fil med allt relaterat till filhantering.

    def measure_button(self):
        self.mapp.delete(self.temp)
        self.mapp.canvas.config(cursor="cross")
        self.reset_marker()
        self.root.bind("<Button-1>",self.measure_distance)
        return
    
    def coord_button(self):
        self.mapp.delete(self.temp)

        self.mapp.canvas.config(cursor="cross")
        
        self.root.bind("<Button-1>",self.coords)
        # self.mapp.bind("<Button-1>",self.unbind_left)
        # coord1 = self.mapp.add_left_click_map_command(self.left_click_event)

    def truck_button(self):
        self.mapp.delete(self.temp)
        self.mapp.canvas.config(cursor="cross")
        self.root.bind("<Button-1>",self.place_truck)
    
    def poi_button(self):
        self.mapp.delete(self.temp)
        self.mapp.canvas.config(cursor="cross")
        self.root.bind("<Button-1>",self.place_poi)
        # self.root.bind("<Button-1>",self.measure_angle)
    
    def statobj_button(self):
        
        self.mapp.delete(self.temp)
        self.mapp.canvas.config(cursor="cross")
        self.root.bind("<Button-1>",self.place_statobj)
    
    def place_statobj(self, event):
        
        self.place_thing("static object", event)
    
    def place_poi(self, event):
        self.place_thing("poi",event)
    
    def place_thing(self,typ,event):
        
        poi = Scenario_object(typ,self.mapp,self.root)
        self.objlist.add_object(poi)
        self.poi = poi
        poi.set_position(self.mapp.convert_canvas_coords_to_decimal_coords(event.x,event.y))
        # marker=self.mapp.set_marker(poi.position[0],poi.position[1])
        # poi.set_marker=marker
        
        self.poi.marker.angle_command = self.remeasure_angle
        self.poi.marker.command = self.repos_poi
        self.poi.marker.text_command = self.activate_poi
        self.poi.set_position((0,0)) # This is a massive workaround to make the marker clickable immediately. As long as there's no test track at the north pole, I think we're good.
        self.poi.set_position(self.mapp.convert_canvas_coords_to_decimal_coords(event.x,event.y))
        self.poi.marker.draw()
        self.mapp.canvas.update()
        if self.poi.typ == "static object":
            # self.poi.points.append(self.mapp.convert_canvas_coords_to_decimal_coords(event.x,event.y))
            self.place_poly_points(event)
        else:
            self.measure_angle(event)
    
    def activate_poi(self, marker:mapmarker):
        self.poi = marker.poi
        self.root.bind("<Button-1>",self.reactivate_poi)
    
    def reactivate_poi(self,event):
        self.poi.frame.frame.toggle()
        # self.poi.frame.frame.update()
        self.reset_tool()

    
    def place_poly_points(self,event):
        
        self.root.bind("<Button-1>",self.poly_point)
        self.root.bind("<space>",self.finish_polygon)
    
    def finish_polygon(self,event=None):
        self.temp.delete()
        self.reset_tool()
        self.poi.polygon.delete()
        self.poi.polygon=None
        self.poi.draw_polygon(finished=True)
    
    def poly_point(self,event):
        # self.start_line(event)
        
        self.mapp.config(cursor="cross")
        self.poi.points.append(self.mapp.convert_canvas_coords_to_decimal_coords(event.x,event.y))
        if len(self.poi.points) > 0:
            
            self.start_line(event)
            self.poi.draw_polygon()
    
    def repos_poi(self, marker:mapmarker):
        # marker.map_widget.canvas.itemconfigure(marker.big_circle, fill="blue", outline="blue")
        self.poi = marker.poi
        
        
        self.root.bind("<Motion>",self.start_repos)
    
    def start_repos(self,event):
        self.mapp.canvas.config(cursor="cross")
        self.root.bind("<Button-1>",self.reposition)
    
    def reposition(self,event):
        self.poi.set_position(self.mapp.convert_canvas_coords_to_decimal_coords(event.x,event.y))
        self.reset_tool()

    
    def remeasure_angle(self, marker:mapmarker):
        self.poi = marker.poi
        self.start_line(marker)
        self.root.bind("<Button-1>",self.preunmeasure)
    def preunmeasure(self,event):
        self.root.bind("<Button-1>",self.unmeasure)
    
    def measure_angle(self, event):
        self.start_line(event)
        self.root.bind("<Button-1>",self.unmeasure)
        
    
    def unmeasure(self,event):
        # try:
        self.mapp.delete(self.temp)
        
        point1 = self.line.start_map_coords
        print(event.x,event.y)
        # point2 = self.line.end_map_coords
        point2 = self.mapp.convert_canvas_coords_to_decimal_coords(event.x,event.y)

        
        geod = pyproj.Geod(ellps="WGS84")
        print(f"point1{point1}")
        print(f"point2{point2}")

        heading,_,distance = geod.inv(point1[0],point1[1],point2[0],point2[1], return_back_azimuth=False)
        
        print(round(heading,2))
        print(round(distance,2))
        self.angle = heading
        if self.poi is not None:
            self.poi.set_angle(self.angle)
            print(self.poi.angle)
            self.poi.marker.draw() # Det här är den senaste punkten, vilket inte nödvändigtvis är den jag vill ändra på. Tror att jag fixat det nu.
        self.reset_tool()
        # except:
        #     print("fail")
    
    # def click_command(self, marker):
    #     self.poi.marker.delete()
    #     lat=self.poi.marker.position[0]
    #     lon=self.poi.marker.position[1]
    #     self.mapp.canvas_marker_list.append(self.mapp.set_marker(lat, lon, marker_color_circle="blue"))
    #     print(self.poi.marker.text)
    
    def place_truck(self,event):
        self.place_thing("truck",event)
    
    def reset_tool(self,event=None):
        self.root.bind("<Button-1>","")
        self.root.bind("<Button-2>","")
        self.root.bind("<Motion>","")
        self.mapp.canvas.config(cursor="arrow")
    
    def reset_marker(self):
        self.poi = None
    
    def coords(self, event):
        self.map_coords = self.mapp.convert_canvas_coords_to_decimal_coords(event.x,event.y)
        print(event)
        print(self.map_coords)
        self.reset_tool()
    
    def left_click_coordinates(self,coordinates_tuple):
        self.map_coords = coordinates_tuple
        
    def measure_distance(self, event):
        # self.root.bind("<Button-1>",self.start_line,"+")
        self.start_line(event)
        self.root.bind("<Button-1>",self.unmeasure)
    
    def start_line(self,event):
        self.map_coords = self.mapp.convert_canvas_coords_to_decimal_coords(event.x,event.y)
        self.mouse_pos = (event.x,event.y)
        
        self.line = Map_Line(self.mouse_pos, self.map_coords)
        self.root.bind("<Motion>",self.line_end)

    def mouse_finder(self,event):
        self.mouse_pos = (event.x,event.y)

    def meters_to_points(self):
        tenmeters=geodist.Distance(10/1000)
        fourmeters=geodist.Distance(4/1000)
        
    
    def line_end(self,event):
        self.mapp.delete(self.temp)
        x1,y1=self.line.start_map_coords
        self.line.set_end((event.x,event.y), self.mapp.convert_canvas_coords_to_decimal_coords(event.x,event.y))
        x2,y2=self.line.end_map_coords
        
        self.temp=self.mapp.set_path(((x1,y1),(x2,y2)),width=2, color="black")
