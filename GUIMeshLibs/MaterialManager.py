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
#Libraries
import sys
import Tkinter as tk
import tkFileDialog
import tkSimpleDialog
import tkMessageBox
import os.path
import time
import math
from Materials import *


##############################################
#################Buttons######################
##############################################

##############################################
#########Load materials in database###########
##############################################
def Pressed_Load_Mats_Dir():
    global MatManager_Element_List
    global MatManager_Material_List
    global mylist_mat_db

    #Temporary name list to check if new material is not on current database
    temp_name_list=[]
    for i in MatManager_Element_List:
        temp_name_list.append(i.Name)

    for i in MatManager_Material_List:
        temp_name_list.append(i.Name)

    New_Mats_List=Load_Materials()#See Materials Library
    if (New_Mats_List!=0):
        if len(New_Mats_List)==0:
            print "No materials found in Database"
            tkMessageBox.showinfo("Error", '"No materials found in Database.') 
        for i in New_Mats_List:
            if i.Name in temp_name_list:
                print "Error: "+i.Name+" is already used."
            else:
                MatManager_Material_List.append(i)
                mylist_mat_db.insert(tk.END, i.Name)
    else:
        tkMessageBox.showinfo("Error", '"Materials" folder not found.')
    
##############################################
##########Delete session database#############
##############################################
def Pressed_Delete_Mats():
    global MatManager_Material_List
    global mylist_mat_db
    for i in MatManager_Material_List:
        del i
    mylist_mat_db.delete(0, tk.END)
    MatManager_Material_List=[]
    print "Number of Materials:",len(MatManager_Material_List)

##########################################
#####Save Session Materials in Folder#####
##########################################
def Pressed_Save_Mats():
    global MatManager_Material_List
    success=Save_Materials(MatManager_Material_List) #See Material Library
    if (success==0):
        tkMessageBox.showinfo("Error", '"Materials" folder not found.')
        
##########################################
########Load a Material from File#########
##########################################
def Pressed_Load_Mat():
    global MatManager_Material_List
    global MatManager_Element_List
    global mylist_mat_db

    #Temporary name list to check if new material is not on current database
    temp_name_list=[]
    for i in MatManager_Element_List:
        temp_name_list.append(i.Name)
    for i in MatManager_Material_List:
        temp_name_list.append(i.Name)
        
    try:
        path_to_material = tkFileDialog.askopenfilename()
    except ValueError:
        return 0

    newmat=Load_Material(path_to_material)#See Material Library
    if newmat==0:
        print "Error: Material was not loaded."
    else:
        if newmat.Name in temp_name_list:
            print "Error: "+i.Name+" is already used."
            tkMessageBox.showinfo("Error", "Error: "+i.Name+" is already used.")    
        else:
            MatManager_Material_List.append(newmat)
            mylist_mat_db.insert(tk.END, newmat.Name)
            print "Material loaded successfully."
            
##########################################
#######Pressed Create Material############
##########################################
####Save Material Button
def Save_Material(name,density,elements,fractions):
    global MatManager_Element_List 
    global MatManager_Material_List
    global mylist_mat_db
    global top
    #Check if Material information is correct (same as in Material libraries - should make one general function for this at some point)
    ele_db_names=["G4_H", "G4_He", "G4_Li", "G4_Be", "G4_B", "G4_C", "G4_N", "G4_O", "G4_F", "G4_Ne", "G4_Na", "G4_Mg", "G4_Al", "G4_Si", "G4_P", "G4_S", "G4_Cl", "G4_Ar", "G4_K", "G4_Ca", "G4_Sc", "G4_Ti", "G4_V", "G4_Cr", "G4_Mn", "G4_Fe", "G4_Co", "G4_Ni", "G4_Cu", "G4_Zn", "G4_Ga", "G4_Ge", "G4_As", "G4_Se", "G4_Br", "G4_Kr", "G4_Rb", "G4_Sr", "G4_Y", "G4_Zr", "G4_Nb", "G4_Mo", "G4_Tc", "G4_Ru", "G4_Rh", "G4_Pd", "G4_Ag", "G4_Cd", "G4_In", "G4_Sn", "G4_Sb", "G4_Te", "G4_I", "G4_Xe", "G4_Cs", "G4_Ba", "G4_La", "G4_Ce", "G4_Pr", "G4_Nd", "G4_Pm", "G4_Sm", "G4_Eu", "G4_Gd", "G4_Tb", "G4_Dy", "G4_Ho", "G4_Er", "G4_Tm", "G4_Yb", "G4_Lu", "G4_Hf", "G4_Ta", "G4_W", "G4_Re", "G4_Os", "G4_Ir", "G4_Pt", "G4_Au", "G4_Hg", "G4_Tl", "G4_Pb", "G4_Bi", "G4_Po", "G4_At", "G4_Rn", "G4_Fr", "G4_Ra", "G4_Ac", "G4_Th", "G4_Pa", "G4_U", "G4_Np", "G4_Pu", "G4_Am", "G4_Cm", "G4_Bk", "G4_Cf","G4_A-150_TISSUE", "G4_ACETONE", "G4_ACETYLENE", "G4_ADENINE", "G4_AIR", "G4_ALANINE", "G4_ALUMINUM_OXIDE", "G4_AMBER", "G4_AMMONIA", "G4_ANILINE", "G4_ANTHRACENE", "G4_B-100_BONE", "G4_BAKELITE", "G4_BARIUM_FLUORIDE", "G4_BARIUM_SULFATE", "G4_BENZENE", "G4_BERYLLIUM_OXIDE", "G4_BGO", "G4_BONE_COMPACT_ICRU", "G4_BONE_CORTICAL_ICRP", "G4_BORON_CARBIDE", "G4_BORON_OXIDE", "G4_BUTANE", "G4_N-BUTYL_ALCOHOL", "G4_C-552", "G4_CADMIUM_TELLURIDE", "G4_CADMIUM_TUNGSTATE", "G4_CALCIUM_CARBONATE", "G4_CALCIUM_FLUORIDE", "G4_CALCIUM_OXIDE", "G4_CALCIUM_SULFATE", "G4_CALCIUM_TUNGSTATE", "G4_CARBON_DIOXIDE", "G4_CARBON_TETRACHLORIDE", "G4_CELLULOSE_CELLOPHANE", "G4_CELLULOSE_BUTYRATE", "G4_CELLULOSE_NITRATE", "G4_CERIC_SULFATE", "G4_CESIUM_FLUORIDE", "G4_CESIUM_IODIDE", "G4_CHLOROBENZENE", "G4_CHLOROFORM", "G4_CYCLOHEXANE", "G4_1,2-DICHLOROBENZENE", "G4_DICHLORODIETHYL_ETHER", "G4_1,2-DICHLOROETHANE", "G4_DIETHYL_ETHER", "G4_N,N-DIMETHYL_FORMAMIDE", "G4_DIMETHYL_SULFOXIDE", "G4_ETHANE", "G4_ETHYL_ALCOHOL", "G4_ETHYL_CELLULOSE", "G4_ETHYLENE", "G4_EYE_LENS_ICRP", "G4_FERRIC_OXIDE", "G4_FERROBORIDE", "G4_FERROUS_OXIDE", "G4_FERROUS_SULFATE", "G4_FREON-12", "G4_FREON-12B2", "G4_FREON-13", "G4_FREON-13B1", "G4_FREON-13I1", "G4_GADOLINIUM_OXYSULFIDE", "G4_GALLIUM_ARSENIDE", "G4_GEL_PHOTO_EMULSION", "G4_Pyrex_Glass", "G4_GLASS_LEAD", "G4_GLASS_PLATE", "G4_GLUCOSE", "G4_GLUTAMINE", "G4_GLYCEROL", "G4_GUANINE", "G4_GYPSUM", "G4_N-HEPTANE", "G4_N-HEXANE", "G4_KAPTON", "G4_LANTHANUM_OXYBROMIDE", "G4_LANTHANUM_OXYSULFIDE", "G4_LEAD_OXIDE", "G4_LITHIUM_AMIDE", "G4_LITHIUM_CARBONATE", "G4_LITHIUM_FLUORIDE", "G4_LITHIUM_HYDRIDE", "G4_LITHIUM_IODIDE", "G4_LITHIUM_OXIDE", "G4_LITHIUM_TETRABORATE", "G4_M3_WAX", "G4_MAGNESIUM_CARBONATE", "G4_MAGNESIUM_FLUORIDE", "G4_MAGNESIUM_OXIDE", "G4_MAGNESIUM_TETRABORATE", "G4_MERCURIC_IODIDE", "G4_METHANE", "G4_METHANOL", "G4_MIX_D_WAX", "G4_MS20_TISSUE", "G4_MUSCLE_STRIATED_ICRU", "G4_MUSCLE_WITH_SUCROSE", "G4_MUSCLE_WITHOUT_SUCROSE", "G4_NAPHTHALENE", "G4_NITROBENZENE", "G4_NITROUS_OXIDE", "G4_NYLON-8062", "G4_NYLON-6/6", "G4_NYLON-6/10", "G4_NYLON-11_RILSAN", "G4_OCTANE", "G4_PARAFFIN", "G4_N-PENTANE", "G4_PHOTO_EMULSION", "G4_PLASTIC_SC_VINYLTOLUENE", "G4_PLUTONIUM_DIOXIDE", "G4_POLYACRYLONITRILE", "G4_POLYCARBONATE", "G4_POLYCHLOROSTYRENE", "G4_POLYETHYLENE", "G4_MYLAR", "G4_PLEXIGLASS", "G4_POLYOXYMETHYLENE", "G4_POLYPROPYLENE", "G4_POLYSTYRENE", "G4_TEFLON", "G4_POLYTRIFLUOROCHLOROETHYLENE", "G4_POLYVINYL_ACETATE", "G4_POLYVINYL_ALCOHOL", "G4_POLYVINYL_BUTYRAL", "G4_POLYVINYL_CHLORIDE", "G4_POLYVINYLIDENE_CHLORIDE", "G4_POLYVINYLIDENE_FLUORIDE", "G4_POLYVINYL_PYRROLIDONE", "G4_POTASSIUM_IODIDE", "G4_POTASSIUM_OXIDE", "G4_PROPANE", "G4_lPROPANE", "G4_N-PROPYL_ALCOHOL", "G4_PYRIDINE", "G4_RUBBER_BUTYL", "G4_RUBBER_NATURAL", "G4_RUBBER_NEOPRENE", "G4_SILICON_DIOXIDE", "G4_SILVER_BROMIDE", "G4_SILVER_CHLORIDE", "G4_SILVER_HALIDES", "G4_SILVER_IODIDE", "G4_SODIUM_CARBONATE", "G4_SODIUM_IODIDE", "G4_SODIUM_MONOXIDE", "G4_SODIUM_NITRATE", "G4_STILBENE", "G4_SUCROSE", "G4_TERPHENYL", "G4_TETRACHLOROETHYLENE", "G4_THALLIUM_CHLORIDE", "G4_TISSUE_SOFT_ICRU-4", "G4_TISSUE-METHANE", "G4_TISSUE-PROPANE", "G4_TITANIUM_DIOXIDE", "G4_TOLUENE", "G4_TRICHLOROETHYLENE", "G4_TRIETHYL_PHOSPHATE", "G4_TUNGSTEN_HEXAFLUORIDE", "G4_URANIUM_DICARBIDE", "G4_URANIUM_MONOCARBIDE", "G4_URANIUM_OXIDE", "G4_UREA", "G4_VALINE", "G4_VITON", "G4_WATER", "G4_WATER_VAPOR", "G4_XYLENE", "G4_GRAPHITE"]
    newmat_elements_list=[]
    temp_name_list=[]
    for i in MatManager_Element_List:
        temp_name_list.append(i.Name)
    for i in MatManager_Material_List:
        temp_name_list.append(i.Name)
    if name.get() in temp_name_list:
        print "Error: "+name.get()+" is already used."
        tkMessageBox.showinfo("Error", "Error: "+name.get()+" is already used.") 
        return 0
    check_fractions=0.0
    try:
        float(density.get())<=0
        for i in range(0,len(elements)):
            try:
                float(fractions[i].get())>0
                check_fractions+=float(fractions[i].get())
                if elements[i].get() in ele_db_names:
                    newmat_elements_list.append(elements[i].get())
                    newmat_elements_list.append(fractions[i].get())
                else:
                    print "Chosen Element: "+elements[i].get()+" not in DB."
                    tkMessageBox.showinfo("Error", "Chosen Element: "+elements[i].get()+" not in DB.") 
                    return 0
            except ValueError:
                print "Error: Fraction #"+str(i+1)+" not a float."
                tkMessageBox.showinfo("Error", "Error: Fraction #"+str(i+1)+"not a float.") 
                return 0
    except ValueError:
        print "Error: Material density either not a float or <1."
        tkMessageBox.showinfo("Error","Material density either not a float or <1.") 
        return 0
    if(check_fractions==1.0):
        newmat=Material(name.get(),float(density.get()),len(elements),newmat_elements_list)
        MatManager_Material_List.append(newmat)
        mylist_mat_db.insert(tk.END, newmat.Name)
        top.destroy()
    else:
        print "Error: Element fraction sum different than 1."
        tkMessageBox.showinfo("Error","Error: Element fraction sum different than 1.")
        return 0

####Create material interface
def Pressed_Create_Mat():
    global MatManager_Material_List
    global sel_ele
    global top
    global MatManager_root

    for i in MatManager_Material_List:
        print i.Name
    total_elements=0.0
    n_comp=tkSimpleDialog.askinteger('Create Material ', 'Choose the number of elements.');
    if n_comp<1:
        tkMessageBox.showinfo("Error", "Error: Number of elements must be >0.") 
        return 0
    #new window
    top = tk.Toplevel(MatManager_root)
    top.attributes('-topmost', 'true')
    E1 = tk.Entry(top, bd =5)
    E1.grid(row=1, column=0)
    E2 = tk.Entry(top, bd =5)
    E2.grid(row=1, column=1)
    nm_name_label = tk.Label(top, text="New Material Name",font=("Helvetica",12)).grid(row=0,column=0)
    nm_dense_label = tk.Label(top, text="Material Density (g/cm3)",font=("Helvetica",12)).grid(row=0,column=1)
    

    blanck_label = tk.Label(top, text=" ").grid(row=2,column=0)
    blanck2_label = tk.Label(top, text="                    ").grid(row=0,column=2)
    n_elements_label = tk.Label(top, text='Number of elements: '+str(n_comp),font=("Helvetica",12)).grid(row=3,column=0,columnspan=2,sticky="W")

    entrys_name = []
    entrys_fraction = []
    labels_name = []
    labels_fraction = []
    for i in range(0,n_comp):
        labels_name.append(tk.Label(top, text="Element "+ str(i+1)+" name",font=("Helvetica",12)).grid(row=4+2*(i%8),column=2*(i/8),sticky="W"))
        entrys_name.append(tk.Entry(top, bd =5))
        entrys_name[i].grid(row=4+2*(i%8), column=2*(i/8)+1)
        labels_fraction.append(tk.Label(top, text="Element "+ str(i+1)+" fraction",font=("Helvetica",12)).grid(row=5+2*(i%8),column=2*(i/8),sticky="W"))
        entrys_fraction.append(tk.Entry(top, bd =5))
        entrys_fraction[i].grid(row=5+2*(i%8), column=2*(i/8)+1)

    for i in range (0,21):
        top.rowconfigure(i, weight=1) 
    save_mat_button=tk.Button(top, text="Save Material",bd=5,relief="raised",width=16,height=1,bg="red",command=lambda : Save_Material(E1,E2,entrys_name,entrys_fraction))
    if(n_comp>8):
        save_mat_button.grid(row=1, column=3)
    else:
        save_mat_button.grid(row=1, column=3)
    top.mainloop()

##########################################
##########Pressed Exit Button#############
##########################################
def Pressed_Exit_Mat_Manager_Button():
    MatManager_root.destroy()

##########################################
##########Show Mat Properties#############
##########################################
def mat_info(evt):
    global Mat_Properties_Menu
    global MatManager_Element_List
    global MatManager_Material_List

    Mat_Name = tk.StringVar(Mat_Properties_Menu)
    Mat_Name.set("") # default value
    Mat_Density = tk.StringVar(Mat_Properties_Menu)
    Mat_Density.set("") # default value
    Mat_Name_label = tk.Message( Mat_Properties_Menu, textvariable=Mat_Name, relief="raised",bg="black",width=int(500),font=("Helvetica", 22),fg="red")
    Mat_Name_label.place(relx=0.05,rely=0.05,relwidth=0.9,relheight=0.15)
    Mat_Density_label = tk.Message( Mat_Properties_Menu, textvariable=Mat_Density,width=int(500),font=("Helvetica", 18),anchor='w')
    Mat_Density_label.place(relx=0.05,rely=0.225,relwidth=0.6,relheight=0.1)
    Mat_Elements_Frame = tk.Frame(Mat_Properties_Menu,width=10,height=20,)
    Mat_Elements_Frame.place(relx=0.05, rely=0.35,relwidth=0.9,relheight=0.6)
    Mat_Elements_label = tk.Message( Mat_Elements_Frame, text="Element",width=int(500),font=("Helvetica", 18))
    Mat_Elements_label.place(relx=0.00,rely=0.00,relwidth=0.5,relheight=0.1)
    Mat_Fraction_label = tk.Message( Mat_Elements_Frame, text="Fraction",width=int(500),font=("Helvetica", 18))
    Mat_Fraction_label.place(relx=0.5,rely=0.00,relwidth=0.5,relheight=0.1)
    
    # Note here that Tkinter passes an event object to onselect()
    w = evt.widget
    index = int(w.curselection()[0])
    value = w.get(index)

    Ele_labels=[]
    Frac_labels=[]
    for i in MatManager_Element_List:
        if value==i.Name:
            print i.Name, i.Density
            Mat_Name.set(i.Name)
            Mat_Density.set("Density: "+str(i.Density)+" g/cm3")
            return
    for i in MatManager_Material_List:
        if value==i.Name:
            print i.Name, i.Density, i.Nelements
            Mat_Name.set(i.Name)
            Mat_Density.set("Density: "+str(i.Density)+" g/cm3")
            HSF=0.1
            if i.Nelements>10:
                HSF=(1-0.105)/i.Nelements
            for j in range (0, i.Nelements):
                print i.Elements[j], i.ElementFractions[j]
                Ele_labels.append(tk.Message( Mat_Elements_Frame, text=str(i.Elements[j]),width=int(500),font=("Helvetica", 14)))
                Ele_labels[j].place(relx=0.00, rely=0.105+HSF*j,relwidth=0.5,relheight=HSF)
                
                Frac_labels.append(tk.Message( Mat_Elements_Frame, text=str(i.ElementFractions[j]),width=int(500),font=("Helvetica", 14)))
                Frac_labels[j].place(relx=0.5, rely=0.105+HSF*j,relwidth=0.5,relheight=HSF)
            return

##############################################
##############################################
##############Draw Mat Manager################
##############################################
##############################################
def Draw_MatManager(imported_Element_List,imported_Material_List):
    global MatManager_Element_List
    global MatManager_Material_List
    global MatManager_root
    global mylist_mat_db
    global mylist_ele_db
    global sel_ele
    global Mat_Name
    global Mat_Density
    global Mat_Properties_Menu
    global MatManager_root

    #Load session database into the manager
    MatManager_Element_List=imported_Element_List
    MatManager_Material_List=imported_Material_List

    #MatManager window
    MatManager_root = tk.Tk()
    s_w = MatManager_root.winfo_screenwidth()
    s_h = MatManager_root.winfo_screenheight()
    p_w = s_w/1800.
    p_h = s_h/800.
    buttons_width=int(18*p_w)
    buttons_height=int(2*p_h)
    pos_x=0.1
    pos_y=0.25
    pos_y_os=0.115
    font_size=20*p_h*p_w
    MatManager_root.state("zoomed")

    #Menu
    button_menu_label = tk.Label(MatManager_root, width=19-int(70./(font_size)),height=int(1*p_h), text = "Menu",borderwidth=5,relief="solid",font=("Helvetica", int(18*p_w)),bg="#e0e0d1")
    button_menu_label.place(relx=0.025 ,rely = 0.2,relwidth=0.15, relheight=0.05)
    MatManager_menu=tk.Canvas(MatManager_root, width=int(150*p_w),height=int(440*p_h),bd=5,bg="black")
    MatManager_menu.place(relx=0.025,rely=pos_y,relwidth=0.15,relheight=0.6)
    Load_Mats_Dir = tk.Button(MatManager_menu, text = 'Load Material DB', font=("Helvetica", int(16*p_w)),width=buttons_width,height=buttons_height, command = Pressed_Load_Mats_Dir,bg="#e0e0d1")
    Load_Mats_Dir.place(relx=0.05,rely=0.025,relwidth=0.9, relheight=0.15)
    Delete_Mats = tk.Button(MatManager_menu, text = 'Delete_Materials', font=("Helvetica", int(16*p_w)),width=buttons_width,height=buttons_height, command = Pressed_Delete_Mats,bg="#e0e0d1")
    Delete_Mats.place(relx=0.05,rely=0.185,relwidth=0.9, relheight=0.15)
    Save_Mats = tk.Button(MatManager_menu, text = 'Save Materials DB', font=("Helvetica", int(16*p_w)),width=buttons_width,height=buttons_height, command = Pressed_Save_Mats,bg="#e0e0d1")
    Save_Mats.place(relx=0.05,rely=0.345,relwidth=0.9, relheight=0.15)
    Load_Mat = tk.Button(MatManager_menu, text = 'Load Material', font=("Helvetica", int(16*p_w)),width=buttons_width,height=buttons_height, command = Pressed_Load_Mat,bg="#e0e0d1")
    Load_Mat.place(relx=0.05,rely=0.505,relwidth=0.9, relheight=0.15)
    Create_Mat = tk.Button(MatManager_menu, text = 'Create New Material', font=("Helvetica", int(16*p_w)),width=buttons_width,height=buttons_height, command = Pressed_Create_Mat,bg="#e0e0d1")
    Create_Mat.place(relx=0.05,rely=0.665,relwidth=0.9, relheight=0.15)
    Exit = tk.Button(MatManager_menu, text = 'Exit MatManager', font=("Helvetica", int(16*p_w)),width=buttons_width,height=buttons_height, command = Pressed_Exit_Mat_Manager_Button,bg="#e0e0d1")
    Exit.place(relx=0.05,rely=0.825,relwidth=0.9, relheight=0.15)


    #Scrolls
    Element_label = tk.Label(MatManager_root, width=19-int(70./(font_size)),height=int(1*p_h), text = "Element List",borderwidth=5,relief="solid",font=("Helvetica", int(18*p_w)),bg="#e0e0d1")
    Element_label.place(relx=0.2 ,rely = 0.2,relwidth=0.2, relheight=0.05)
    #Elements
    frame_ele_db = tk.Frame(MatManager_root,width=10,height=20)
    frame_ele_db.place(relx=0.2, rely=pos_y,relwidth=0.2,relheight=0.6)
    scrollbar_ele_db = tk.Scrollbar(frame_ele_db)
    scrollbar_ele_db.pack( side = tk.RIGHT, fill = tk.Y )
    mylist_ele_db = tk.Listbox(frame_ele_db, yscrollcommand = scrollbar_ele_db.set,width=int(15*p_w),height=int(27*p_h),font=("Helvetica", int(14*p_w)))
    mylist_ele_db.pack( side = tk.LEFT, fill = tk.BOTH )
    mylist_ele_db.place(relwidth=0.95,relheight=1)
    for i in MatManager_Element_List:
        mylist_ele_db.insert(tk.END, i.Name)
    scrollbar_ele_db.config( command = mylist_ele_db.yview )
    mylist_ele_db.bind('<<ListboxSelect>>', mat_info)
    #Materials
    Material_label = tk.Label(MatManager_root, width=19-int(70./(font_size)),height=int(1*p_h), text = "Material List",borderwidth=5,relief="solid",font=("Helvetica", int(18*p_w)),bg="#e0e0d1")
    Material_label.place(relx=0.4 ,rely = 0.2,relwidth=0.2, relheight=0.05)
    frame_mat_db = tk.Frame(MatManager_root,width=10,height=20)
    frame_mat_db.place(relx=0.4, rely=pos_y,relwidth=0.2,relheight=0.6)
    scrollbar_mat_db = tk.Scrollbar(frame_mat_db)
    scrollbar_mat_db.pack( side = tk.RIGHT, fill = tk.Y )
    mylist_mat_db = tk.Listbox(frame_mat_db, yscrollcommand = scrollbar_mat_db.set,width=int(15*p_w),height=int(27*p_h),font=("Helvetica", int(14*p_w)))
    mylist_mat_db.pack( side = tk.LEFT, fill = tk.BOTH )
    mylist_mat_db.place(relwidth=0.95,relheight=1)
    for i in MatManager_Material_List:
        mylist_mat_db.insert(tk.END, i.Name)
    scrollbar_mat_db.config( command = mylist_mat_db.yview )
    mylist_mat_db.bind('<<ListboxSelect>>', mat_info)

    #Mat Info Display
    Mat_Properties_label = tk.Label(MatManager_root, width=19-int(70./(font_size)),height=int(1*p_h), text = "Material Properties",borderwidth=5,relief="solid",font=("Helvetica", int(18*p_w)),bg="#e0e0d1")
    Mat_Properties_label.place(relx=0.675 ,rely = 0.2,relwidth=0.295, relheight=0.05)
    Mat_Properties_Menu=tk.Canvas(MatManager_root, width=int(340*p_w),height=int(440*p_h),bd=5,borderwidth=5,relief="solid",bg="#e0e0d1")
    Mat_Properties_Menu.place(relx=0.675,rely=pos_y,relwidth=0.295,relheight=0.59)

    #Labels
    cr_label = tk.Label(MatManager_root, text = "Copyright (c) 2018  Marco Gui Alves Pinto\nmail: mgpinto11@gmail.com",fg="red",font=("Helvetica", int(12*p_w)),bd=1,anchor='e',justify="right")
    cr_label.place(relx= 0.64,rely = 0.94,relwidth=0.35, relheight=0.05)
    Title_label = tk.Label(MatManager_root, text = "GUI Mesh", fg="red",font=("Helvetica", int(40*p_w)),bd=1)
    Title_label.place(relx= 0.25,rely = 0.02,relwidth=0.5, relheight=0.1)
    MatMan_Label = tk.Label(MatManager_root, text = "Material Manager", fg="red",font=("Helvetica", int(20*p_w)),bd=1)
    MatMan_Label.place(relx= 0.225,rely = 0.1,relwidth=0.55, relheight=0.05)
    MatManager_root.mainloop()
    
    return MatManager_Material_List #return a new Material List
