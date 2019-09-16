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
import Materials
import tkSimpleDialog
import tkFileDialog
import tkMessageBox

#Volume class - Volumes have all properties from STEP, an assigned material, mesh precision (MMD) and a write variable option
class Volume():
    def __init__(self,myvolume,mymaterial,myMMD,myGDMLoption):
        self.VolumeCAD=myvolume
        self.VolumeMaterial=mymaterial
        self.VolumeMMD=myMMD
        self.VolumeGDMLoption=myGDMLoption

#Save Volume Properties Function - Writes a CSV file with information of all loaded volumes to edit outsite of GUIMesh
def SaveVolumeProperties(list_of_objects):
    filename=tkSimpleDialog.askstring("","Please type a filename: ")
    f=open(filename+".csv",'w')
    for i in list_of_objects:
            f.write(str(i.VolumeCAD.Label)+";"+ str(i.VolumeMaterial.Name)+";"+ str(i.VolumeMMD)+";"+ str(i.VolumeGDMLoption)+"\n")
            print i.VolumeCAD.Label, i.VolumeMaterial.Name, i.VolumeMMD, i.VolumeGDMLoption
    f.close()

#Load Volume Properties Function - Reads a CSV file with information of all loaded volumes. Several tests are made to make sure all information is correct
def LoadVolumeProperties(list_of_objects,Element_List,Material_List):
    #Read CXV
    path_to_file = tkFileDialog.askopenfilename()
    print "Checking file extension..."
    if (path_to_file[-4:]==".csv"):
        print "File extension is correct."
        properties_csv_file=open(str(path_to_file),"r")
        properties=properties_csv_file.readlines()
        properties_csv_file.close()
        print "Checking number of lines..."
        #Check if number of lines is correct - one per volume
        if (len(properties)==len(list_of_objects)):
            print "Number of lines is correct."
            counter=0
            #Evaluate line content, one at a time
            for line in properties:
                properties_list = line.split(';')
                Volume_Label=properties_list[0]
                new_material_name=properties_list[1]
                new_MMD=properties_list[2]
                new_GDMLoption=properties_list[3][0]
                print "Evaluating line "+str(counter+1)+":"
                #Check if Name in line corresponds to Volume label
                if Volume_Label==list_of_objects[counter].VolumeCAD.Label:
                    print "Volume name is correct:",Volume_Label
                    #Check if Material exists
                    check_mat=0
                    for ele in Element_List:
                        if new_material_name==ele.Name:
                            list_of_objects[counter].VolumeMaterial=ele
                            check_mat=1
                    if check_mat==0:
                        for mat in Material_List:
                            if new_material_name==mat.Name:
                                list_of_objects[counter].VolumeMaterial=mat
                                check_mat=1
                        if check_mat==0:
                            print "Material not found - moving on to the next line."
                        else:
                            print "Material found:",new_material_name
                    else:
                        print "Material found:",new_material_name
                    #Check if MMD value is valid
                    try:
                        float(new_MMD)
                        list_of_objects[counter].VolumeMMD=float(new_MMD)
                        print "MMD value is correct:", new_MMD
                        #Check if GDMLoption value is valid
                        try:
                            int(new_GDMLoption)
                            if int(new_GDMLoption)!=0:
                                new_GDMLoption=1
                            list_of_objects[counter].VolumeGDMLoption=int(new_GDMLoption)
                            print "GDMLoption value is correct:", new_GDMLoption
                        except:
                            print "GDML option must be an integer - moving on to the next line."
                    except:
                        print "MMD not a float - moving on to the next line."
                else:
                    print "Name does not match the volume"
                counter+=1
            tkMessageBox.showinfo("Message", "Load complete. Check log for errors.")

        else:
            tkMessageBox.showinfo("Warning", "Your list has incorrect size")
    else:
        tkMessageBox.showinfo("Error", "Must be csv file.")
