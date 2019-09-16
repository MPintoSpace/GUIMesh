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
import Volumes

#Add FreeCAD directory to os path
def Find_FreeCAD_Dir():
        import tkFileDialog
        import sys
        import os.path
        path_to_FreeCAD=tkFileDialog.askdirectory()
        #Check if directory is correct
        if((os.path.isfile(path_to_FreeCAD+"/bin/FreeCAD.PYD")==True) or (os.path.isfile(path_to_FreeCAD+"/lib/FreeCAD.so")==True)):
            sys.path.append(path_to_FreeCAD+"/bin")
            sys.path.append(path_to_FreeCAD+"/lib")
            return 1
        else:
            return 0

#Add FreeCAD directory to os path
def Load_STEP_File(doc_status,material):
    import tkFileDialog
    import FreeCAD
    import Import
    import FreeCADGui
    import Draft
    import Part
    #prepares and opens STEP file with FreeCADs
    path_to_file = tkFileDialog.askopenfilename()
    if( path_to_file[-5:]==".STEP" or path_to_file[-5:]==".step"or path_to_file[-4:]==".stp"):
        if (doc_status):    #If a file was already open the document associated with it must be closed
            FreeCAD.closeDocument("Unnamed")
            print "Previous document closed"
        FreeCAD.newDocument("Unnamed")
        FreeCAD.setActiveDocument("Unnamed")
        try: 
            Import.insert(path_to_file,"Unnamed") #FreeCAD attempts to open file - If the format is wrong it will be detected
            print "File read successfuly"
            list_of_objects=[]
            for obj in FreeCAD.ActiveDocument.Objects:
                list_of_objects.append(Volumes.Volume(obj,material,0.1,1));
            return list_of_objects
        except:
            print "Error reading file. Format might be incorrect."
            return 0
    else:
        print "Error with file extension"
        return 0
