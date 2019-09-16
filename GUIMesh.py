#########################################################################################################
#    GUIMesh v1                                                                                         #
#                                                                                                       #
#    Copyright (c) 2018  Marco Gui Alves Pinto mail:mgpinto11@gmail.com                                 #
#                                                                                                       #
#    This program is free software: you can redistribute it and/or modify                               #
#    it under the terms of the GNU General Public License as published by                               #
#    the Free Software Foundation, either version 3 of the License, or                                  #
#    (at your option) any later version.                                                                #
#                                                                                                       #
#    This program is distributed in the hope that it will be useful,                                    #
#    but WITHOUT ANY WARRANTY; without even the implied warranty of                                     #
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the                                      #
#    GNU General Public License for more details.                                                       #
#                                                                                                       #
#    You should have received a copy of the GNU General Public License                                  #
#    along with this program.  If not, see <https://www.gnu.org/licenses/>                              #
#                                                                                                       #
#########################################################################################################

#################################################################
##########################Libraries##############################
#################################################################
import sys
import os.path
import time
import math
    
try: 
    import Tkinter as tk
    import tkFileDialog
    import tkSimpleDialog
    import tkMessageBox
except:
    print "Could not import Tkinter. It might not be installed or the instalation  might have a different name."

try:
    from GUIMeshLibs import Materials, MaterialManager, Volumes, LoadOP, WriteGDML
except:
    print "Could not load GUIMesh libraries. Please check if the folder GUIMeshLibs exists and if the files are there."

#################################################################
######################Pressed Find FreeCAD#######################
#################################################################
def Pressed_Find_FreeCAD_Dir():
    global FreeCAD_status
    print "Pressed Find FreeCAD Dir"
    #Import FreeCAD - essential to the whole program
    try:
        import FreeCAD
        FreeCAD_status="FreeCAD loaded"
        label_FreeCAD_path.configure(text=FreeCAD_status)
        tkMessageBox.showinfo("Success", "FreeCAD loaded.")
        print "FreeCAD loaded."
    except:
        r=LoadOP.Find_FreeCAD_Dir() #Load FreeCAD path to python - See LoadOP library
        if r:
            FreeCAD_status="FreeCAD loaded"
            label_FreeCAD_path.configure(text=FreeCAD_status)
            tkMessageBox.showinfo("Success", "FreeCAD loaded.")
            print "FreeCAD is now loaded"
        else:
            tkMessageBox.showinfo("Warning", "There was an error loading FreeCAD.")
            print "There was an error loading FreeCAD."
    root.update()

#################################################################
#########################Pressed Read STEP#######################
#################################################################
def Pressed_Read_STEP():
    global STEP_file_status
    global mylist_names
    global list_of_objects
    global Element_List
    global file_status
    global FreeCAD_status
    print "Pressed Read STEP"
    #Requires FreeCAD to be loaded
    if (FreeCAD_status=="FreeCAD loaded"):
        STEP_file_status="Opening file..."
        label_STEP_path.configure(text=STEP_file_status)
        temp_list_of_objects=LoadOP.Load_STEP_File(file_status,Element_List[13])#Load STEP with FreeCAD library - See LoadOP library
        #Check if loading was done properly
        if (temp_list_of_objects==0):
                tkMessageBox.showinfo("Error", "File format or extension is incorrect.")
                print "Error: File format or extension is incorrect."
                STEP_file_status="Error opening file"
                label_STEP_path.configure(text=STEP_file_status)
                file_status=0
        #Creates new object list
        else:
            list_of_objects=temp_list_of_objects #Replace previous object list (if there was one)
            temp_list_of_objects=0
            file_status=1
            tkMessageBox.showinfo("Success", "STEP file loaded.")
            print "STEP file loaded."
            STEP_file_status="STEP file loaded"
            label_STEP_path.configure(text=STEP_file_status)
            mylist_names.delete(0, tk.END)
            for i in list_of_objects:
                mylist_names.insert(tk.END,i.VolumeCAD.Label)
    else:
        tkMessageBox.showinfo("Error", "FreeCAD not found.")
        
#################################################################
#########################Pressed World Size######################
#################################################################
#######Save new world size - default is 1 m * 1 m *1 m
def Save_World_Button(x,y,z,top):
    global world_dimensions
    print world_dimensions[0], world_dimensions[1], world_dimensions[2]
    try:
        float(x.get())
        float(y.get())
        float(z.get())
    except:
        tkMessageBox.showinfo("Error", "All variables must be float values larger than 0.")
        return 0
    world_dimensions[0]=abs(float(x.get()))
    world_dimensions[1]=abs(float(y.get()))
    world_dimensions[2]=abs(float(z.get()))
    top.destroy()
    print world_dimensions[0], world_dimensions[1], world_dimensions[2]

########interface to select new world size
def Pressed_World_Size():
    global world_dimensions
    print "Pressed_World_Size"
    #Create small interface to assign world size values
    top = tk.Tk()
    top.attributes('-topmost', 'true')
    E1_label = tk.Message( top, text="X",width=int(500),font=("Helvetica", 15),anchor='w',fg="black")
    E1_label.grid(row=0,column=0)
    E1 = tk.Entry(top, bd =5)
    E1.grid(row=1, column=0)
    E2_label = tk.Message( top, text="Y",width=int(500),font=("Helvetica", 15),anchor='w',fg="black")
    E2_label.grid(row=0,column=1)
    E2 = tk.Entry(top, bd =5)
    E2.grid(row=1, column=1)   
    E3_label = tk.Message( top, text="Z",width=int(500),font=("Helvetica", 15),anchor='w',fg="black")
    E3_label.grid(row=0,column=2)
    E3 = tk.Entry(top, bd =5)
    E3.grid(row=1, column=2)
    units_label = tk.Message( top, text="m3",width=int(500),font=("Helvetica", 15),anchor='w',fg="black")
    units_label.grid(row=1,column=3)
    save_world_button=tk.Button(top, text="Save",bd=5,relief="raised",width=8,height=1,bg="red",command=lambda : Save_World_Button(E1,E2,E3,top))
    save_world_button.grid(row=0,column=3)
    top.mainloop()

#################################################################
#############Save object properties into a csv file.#############
#################################################################
def Pressed_Save_Properties():
    global list_of_objects
    print "Pressed Save Properties"
    Volumes.SaveVolumeProperties(list_of_objects)#Save csv file with volume properties - See Volumes Library
    
#################################################################
#############Load object properties into a csv file##############
#################################################################
#Even if there are errors (material for instance) all correct information is loaded
def Pressed_Load_Properties():
    global list_of_objects
    global Element_List
    global Material_List
    print "Pressed Load Properties"
    Volumes.LoadVolumeProperties(list_of_objects,Element_List,Material_List)#Load csv file with volume properties - See Volumes Library

#################################################################
################Material Manager - New window####################
#################################################################
def Pressed_Material_Manager():
    global Element_List
    global Material_List
    print "Pressed Material Manager"
    MaterialManager.Draw_MatManager(Element_List,Material_List) #See MaterialManager library - Changes Material List
    
#################################################################
############################Write GDML###########################
#################################################################
def Pressed_Write_GDML():
    global list_of_objects
    global world_dimensions
    print "Pressed_Write_GDML STEP Mesh"
    if len(list_of_objects)>0:
        WriteGDML.Write_Files(list_of_objects, world_dimensions)#See WriteGDML library
    else:
        tkMessageBox.showinfo("Error", "There are no volumes to mesh.")

#################################################################
#################Selected Volume Operations######################
#################################################################
#Change Material
def Pressed_Change_Material():
    global selected_volume_index
    global Element_List
    global Material_List
    print "Pressed_Change_Volume_Material"

    newMaterial=tkSimpleDialog.askstring('Material ', 'Select new Material');
    check_mat=0 #Check if Material exists
    for ele in Element_List:
        if newMaterial==ele.Name:
            check_mat=1
            if set_all_var.get()==0:#Selected volume
                list_of_objects[selected_volume_index].VolumeMaterial=ele
            else:#All volumes
                for i in list_of_objects:
                    i.VolumeMaterial=ele
    if check_mat==0:
        for mat in Material_List:
            if newMaterial==mat.Name:
                check_mat=1
                if set_all_var.get()==0: #Selected volume
                    list_of_objects[selected_volume_index].VolumeMaterial=mat
                else: #All volumes
                    for i in list_of_objects:
                        i.VolumeMaterial=mat
    if check_mat==0:
        tkMessageBox.showinfo("Error", "Material not found in database.")
        print "Material not found in database"
    else:
        print "New material:",newMaterial
        
#Change MMD
def Pressed_Change_MMD():
    global list_of_objects
    print "Pressed_Change_MMD"
    newMMD=tkSimpleDialog.askfloat('MMD ', 'Select new MMD value.');
    try:
        if float(newMMD)>0:
            print "MMD ok"
            if set_all_var.get()==0: #Selected volume
                global selected_volume_index
                list_of_objects[selected_volume_index].VolumeMMD=newMMD
            else: #All volumes
                for i in list_of_objects:
                    i.VolumeMMD=newMMD
        else:
            tkMessageBox.showinfo("Error", "MMD must be greater than 0.")
            print "Chosen value <= 0"
    except:
        tkMessageBox.showinfo("Error", "Value not a float.")
        print "Not a float or < 0"

#Change Write GDML option
def Pressed_Change_GDML_Option():
    global list_of_objects
    print "Pressed_Change_GDML_Option"
    newGDMLoption=tkSimpleDialog.askinteger('Write Option', 'Select Write Option.'); #>=1 write - <1 do not write
    if newGDMLoption<0:
        newGDMLoption=0
    else:
        newGDMLoption=1
    if set_all_var.get()==0: #Selected volume
        global selected_volume_index
        list_of_objects[selected_volume_index].VolumeGDMLoption=newGDMLoption
    else: #All volumes
        for i in list_of_objects:
            i.VolumeGDMLoption=newGDMLoption

#Select volume
def vol_info(evt):
    global vol_properties_menu
    global list_of_objects
    global selected_volume_index
    #Volume Name
    Vol_Name = tk.StringVar(vol_properties_menu)
    Vol_Name.set("") # default value
    Vol_Name_label = tk.Message( vol_properties_menu, textvariable=Vol_Name, width=int(500),font=("Helvetica", 15),anchor='w',fg="black")
    Vol_Name_label.place(relx=0.05,rely=0.05,relwidth=0.9,relheight=0.1)
    #Volume Material    
    Vol_Material = tk.StringVar(vol_properties_menu)
    Vol_Material.set("") # default value
    Vol_Material_label = tk.Message( vol_properties_menu, textvariable=Vol_Material,width=int(500),font=("Helvetica", 15),anchor='w',fg="black")
    Vol_Material_label.place(relx=0.05,rely=0.15,relwidth=0.9,relheight=0.1)
    #Volume Size
    Vol_Size = tk.StringVar(vol_properties_menu)
    Vol_Size.set("") # default value
    Vol_Size_label = tk.Message( vol_properties_menu, textvariable=Vol_Size,width=int(500),font=("Helvetica", 15),anchor='w',fg="black")
    Vol_Size_label.place(relx=0.05,rely=0.25,relwidth=0.9,relheight=0.1)
    #Volume Mass
    Vol_Mass = tk.StringVar(vol_properties_menu)
    Vol_Mass.set("") # default value
    Vol_Mass_label = tk.Message( vol_properties_menu, textvariable=Vol_Mass,width=int(500),font=("Helvetica", 15),anchor='w',fg="black")
    Vol_Mass_label.place(relx=0.05,rely=0.35,relwidth=0.9,relheight=0.1)
    #Volume MMD
    Vol_MMD = tk.StringVar(vol_properties_menu)
    Vol_MMD.set("") # default value
    Vol_MMD_label = tk.Message( vol_properties_menu, textvariable=Vol_MMD,width=int(500),font=("Helvetica", 15),anchor='w',fg="black")
    Vol_MMD_label.place(relx=0.05,rely=0.45,relwidth=0.45,relheight=0.1)
    #Volume GDML option
    Vol_GDML_option = tk.StringVar(vol_properties_menu)
    Vol_GDML_option.set("") # default value
    Vol_GDML_option_label = tk.Message( vol_properties_menu, textvariable=Vol_GDML_option,width=int(500),font=("Helvetica", 15),anchor='w',fg="black")
    Vol_GDML_option_label.place(relx=0.5,rely=0.45,relwidth=0.45,relheight=0.1)

    #Set Volume  Properties to display
    w = evt.widget
    selected_volume_index=index = int(w.curselection()[0]) #index
    Vol_Name.set("Name: "+list_of_objects[index].VolumeCAD.Label)
    Vol_Material.set("Material: "+list_of_objects[index].VolumeMaterial.Name)
    Vol_Size.set("Volume: "+str(list_of_objects[index].VolumeCAD.Shape.Volume/1000)+" cm3")
    Vol_Mass.set("Mass: "+str(list_of_objects[index].VolumeMaterial.Density*(list_of_objects[index].VolumeCAD.Shape.Volume/1000.))+" g")
    Vol_MMD.set("MMD: "+str(list_of_objects[index].VolumeMMD)+" mm")
    if list_of_objects[index].VolumeGDMLoption!=0:
        Vol_GDML_option.set("Write GDML: Yes")
    else:
        Vol_GDML_option.set("Write GDML: No")

#################################################################
#####################Pressed Exit_Program########################
#################################################################
def Pressed_Exit_Program():
    root.destroy()

#####################################################################################
##################################Main###############################################
#####################################################################################
##################    
#Global variables#
##################
FreeCAD_status="FreeCAD not loaded"
STEP_file_status="No file has been loaded"
file_status=0
world_dimensions=[1.0,1.0,1.0] #in meters
list_of_objects=[]
list_of_names=[]
Element_List=Materials.Load_Elements()
Material_List=[]

#####################################################################################
#######################################Canvas########################################
#####################################################################################
#Window 
root = tk.Tk()
s_w = root.winfo_screenwidth()
s_h = root.winfo_screenheight()
p_w = s_w/1366.
p_h = s_h/768.
buttons_width=int(18*p_w)
buttons_height=int(2*p_h)
pos_x=0.1
pos_y=0.05
pos_y_os=0.115
font_size=20*p_h*p_w
#root.state("zoomed")
#Draw interface regions
button_menu=tk.Canvas(root,bd=5,bg="black")
button_menu.place(relx=0.01,rely=0.24,relwidth=0.12,relheight=0.59)
button_menu_rectangle=button_menu.create_rectangle(0, 0, 1000, 1000, fill="#ccccb3");
lists_menu=tk.Canvas(root,bd=5,bg="black")
lists_menu.place(relx=0.209,rely=0.24,relwidth=0.4015,relheight=0.59)
lists_menu.create_rectangle(0, 0, s_w, s_h, fill="#ccccb3");
vol_properties_menu=tk.Canvas(root, bd=5,bg="black")
vol_properties_menu.place(relx=0.7,rely=0.24,relwidth=0.295,relheight=0.59)
vol_properties_menu.create_rectangle(0, 0, s_w, s_h, fill="#ccccb3")
vol_properties_menu.create_rectangle(0, 0, s_w, s_h, fill="#ccccb3")
vol_properties_menu.create_rectangle(0, 0, s_w, s_h, fill="#ccccb3")
status_menu=tk.Canvas(root,bd=2,bg="red")
status_menu.place(relx=0.01,rely=0.892,relwidth=0.137, relheight=0.104)
status_menu.create_rectangle(0, 0, s_w, s_h, fill="#ccccb3")
#Draw Interface Labels
button_menu_label = tk.Label(root, text = "Menu",borderwidth=5,relief="solid",font=("Helvetica", int(14*p_w)),bg="#e0e0d1")
button_menu_label.place(relx=0.011 ,rely = 0.19,relwidth=0.118, relheight=0.05)
volume_menu_label = tk.Label(root, text = "Volume List",borderwidth=5,relief="solid",font=("Helvetica", int(14*p_w)),bg="#e0e0d1")
volume_menu_label.place(relx=0.21,rely = 0.19,relwidth=0.4, relheight=0.05)
edit_menu_label = tk.Label(root, text = "Volume Properties",borderwidth=5,relief="solid",font=("Helvetica", int(14*p_w)),bg="#e0e0d1")
edit_menu_label.place(relx=0.701,rely = 0.19,relwidth=0.292, relheight=0.05)
status_label = tk.Label(status_menu, text = "Status:", fg="red",font=("Helvetica", int(12*p_w)),bg="#ccccb3",bd=1)
status_label.place(relx= 0.08,rely = 0.05,relwidth=0.3, relheight=0.2)
label_FreeCAD_path = tk.Label(status_menu, font=("Helvetica", int(11*p_w)),text = FreeCAD_status,anchor="w",bg="#ccccb3",bd=1)
label_FreeCAD_path.place(relx= 0.025,rely = 0.355,relwidth=0.95, relheight=0.2)
label_STEP_path = tk.Label(status_menu, font=("Helvetica", int(11*p_w)),text = STEP_file_status,anchor="w",bg="#ccccb3",bd=1)
label_STEP_path.place(relx= 0.025,rely = 0.65,relwidth=0.9, relheight=0.2)
author_label = tk.Label(root, text = "Copyright (c) 2018  Marco Gui Alves Pinto\nmail: mgpinto11@gmail.com",fg="red",font=("Helvetica", int(12*p_w)),bd=1,anchor='e',justify="right")
author_label.place(relx= 0.65,rely = 0.94,relwidth=0.35, relheight=0.05)
logo_label = tk.Label(root, text = "GUI Mesh", fg="red",font=("Helvetica", int(40*p_w)),bd=1)
logo_label.place(relx= 0.25,rely = 0.02,relwidth=0.5, relheight=0.1)
description_label = tk.Label(root, text = "A Graphical User Interface to convert STEP files into GDML", fg="red",font=("Helvetica", int(20*p_w)),bd=1)
description_label.place(relx= 0.25,rely = 0.1,relwidth=0.55, relheight=0.05)
    
#####################################################################################
###############################Menu Buttons##########################################
#####################################################################################
#FreeCAD button
button_FreeCAD_path = tk.Button(button_menu, text = 'Find FreeCAD Dir',font=("Helvetica", int(12*p_w)), command = Pressed_Find_FreeCAD_Dir,bg="#e0e0d1")
button_FreeCAD_path.place(relx=0.1,rely=pos_y,relwidth=0.8, relheight=0.1)
#Read Step button
button_Read_STEP = tk.Button(button_menu, text = 'Read STEP', font=("Helvetica", int(12*p_w)), command = Pressed_Read_STEP,bg="#e0e0d1")
button_Read_STEP.place(relx=0.1,rely=(pos_y+pos_y_os),relwidth=0.8, relheight=0.1)
#Update Lists button
button_World_Size = tk.Button(button_menu, text = 'World Size', font=("Helvetica", int(12*p_w)), command = Pressed_World_Size,bg="#e0e0d1")
button_World_Size.place(relx=0.1,rely=(pos_y+pos_y_os*2),relwidth=0.8, relheight=0.1)
#Save Lists button
button_Save_Properties = tk.Button(button_menu, text = 'Save Properties',font=("Helvetica", int(12*p_w)), command = Pressed_Save_Properties,bg="#e0e0d1")
button_Save_Properties.place(relx=0.1,rely=(pos_y+pos_y_os*3),relwidth=0.8, relheight=0.1)
#Load Materials button
button_Load_Properties = tk.Button(button_menu, text = 'Load Properties',font=("Helvetica", int(12*p_w)), command = Pressed_Load_Properties,bg="#e0e0d1")
button_Load_Properties.place(relx=0.1,rely=(pos_y+pos_y_os*4),relwidth=0.8, relheight=0.1)
#Material manager button
button_Create_Material = tk.Button(button_menu, text = 'Material Manager',font=("Helvetica", int(12*p_w)), command = Pressed_Material_Manager,bg="#e0e0d1")
button_Create_Material.place(relx=0.1,rely=(pos_y+pos_y_os*5),relwidth=0.8, relheight=0.1)
#Write GDML button
button_Write_GDML = tk.Button(button_menu, text = 'Write GDML',font=("Helvetica", int(12*p_w)), command = Pressed_Write_GDML,bg="#e0e0d1")
button_Write_GDML.place(relx=0.1,rely=(pos_y+pos_y_os*6),relwidth=0.8, relheight=0.1)
#Exit button
button_exit = tk.Button(button_menu, text = 'Exit Program',font=("Helvetica", int(12*p_w)), command = Pressed_Exit_Program,bg="#e0e0d1")
button_exit.place(relx=0.1,rely=(pos_y+pos_y_os*7),relwidth=0.8, relheight=0.1)

#####################################################################################
###################################Volume Lists######################################
#####################################################################################
frame_names = tk.Frame(lists_menu)
frame_names.place(relx=0.01, rely=0.02,relwidth=0.98,relheight=0.96)
scrollbar_names = tk.Scrollbar(frame_names)
scrollbar_names.pack( side = tk.RIGHT, fill = tk.Y )
mylist_names = tk.Listbox(frame_names, yscrollcommand = scrollbar_names.set,width=int(3000*p_w),height=int(3000*p_h),font=("Helvetica", int(12*p_w)))
mylist_names.pack( side = tk.LEFT, fill = tk.BOTH )
for i in range(len(list_of_names)):
   mylist_names.insert(tk.END, str(i+1)+". "+str(list_of_names[i]))
scrollbar_names.config( command = mylist_names.yview )
mylist_names.bind('<<ListboxSelect>>', vol_info)

#####################################################################################
###############################Property Buttons######################################
#####################################################################################
#Label
empty_label = tk.Message( vol_properties_menu, text="",width=int(500),font=("Helvetica", 15),anchor='w',fg="black")
empty_label.place(relx=0.05,rely=0.05,relwidth=0.9,relheight=0.5)
#Set all variable
set_all_var = tk.IntVar()
set_all_var.set(0)
set_all_check_button = tk.Checkbutton(vol_properties_menu, text="Set All", font=("Helvetica", 16),variable=set_all_var)
set_all_check_button.place(relx=0.05,rely=0.9,relwidth=0.15,relheight=0.05)
#Change Material
button_Change_Material = tk.Button(vol_properties_menu, text = 'Change Material',font=("Helvetica", int(12*p_w)), command = Pressed_Change_Material,bg="#e0e0d1")
button_Change_Material.place(relx=0.05,rely=0.6,relwidth=0.9, relheight=0.1)
#Change MMD
button_Change_MMD = tk.Button(vol_properties_menu, text = 'Change MMD',font=("Helvetica", int(12*p_w)), command = Pressed_Change_MMD,bg="#e0e0d1")
button_Change_MMD.place(relx=0.05,rely=0.7,relwidth=0.9, relheight=0.1)
#Change GDML Option
button_Change_GDML_Option = tk.Button(vol_properties_menu, text = 'Change GDML Option',font=("Helvetica", int(12*p_w)), command = Pressed_Change_GDML_Option,bg="#e0e0d1")
button_Change_GDML_Option.place(relx=0.05,rely=0.8,relwidth=0.9, relheight=0.1)

#####################################################################################
################################End of main loop#####################################
#####################################################################################
root.mainloop()
