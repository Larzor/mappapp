from scen_objects import Scenario_object, Object_list
import tkinter as tk
from tkinter import filedialog
import re

def create_file():
    file = filedialog.asksaveasfile()

def save_file(objlist:Object_list):
    string_list = []
    for i in objlist.object_list:
        if i.typ == "truck":
            strng = """

            """

# Gör förenklad version av nedanstpende:

# class File_read_object():
#     def __init__(self,variable=None,clsfun=None,stringg=None):
#         self.variable = variable
#         self.classorfunction = clsfun
#         self.stringg:str = stringg
#         self.latitude = None
#         self.longitude = None
#         self.heading = None
    
#     def set_variable(self,variab):
#         self.variable = variab
    
#     def set_clsfun(self,clsfun):
#         self.classorfunction = clsfun

# class File_read():
#     def __init__(self):
#         self.file = None
#         self.contents:str = None
#         self.list_of_stuff:list[File_read_object] = None



# This was an attempt at reading a scenario-file:

    # def read_scenario_file(self):
    #     self.file = filedialog.askopenfile(initialdir="scenarios", title="load scenario")

    #     self.contents:str = self.file.read()
    #     self.contents = self.contents.replace("\n","")
    #     self.find_defined()
    
    # def find_defined(self,contents=None):
    #     cont = contents or self.contents
        
    #     listan = re.findall("(\w+(| )=(| )(Position\([^\)]+))",cont)
    #     print(listan)

    #     self.list_of_stuff = [File_read_object(stringg=i[0]) for i in listan]
    #     print(*(i.stringg for i in self.list_of_stuff))
    #     for i in self.list_of_stuff:
    #         i.variable = re.search("(\w+(| )=)",i.stringg).group().replace("=","").strip()
    #         print(i.variable)
        
        



        # self.list_of_stuff = [File_read_object(string=i) for i in range(len(self.contents)) if self.contents.startswith("=",i)]


# fr:File_read = File_read()
# stri = """    foreign_object =Position(latitude=59.16244816,
#             longitude=17.62475461,
#             heading=120
#         )
#     hello
#     point_of_interest= Position(
#             latitude = ght,
#             longitude=eff,
#             heading=120)"""


# fr.find_defined(stri)

# print(*(i.variable for i in fr.list_of_stuff))


