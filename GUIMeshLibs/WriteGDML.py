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
import os
import Materials
import Volumes
import tkFileDialog
import tkMessageBox

#Write Mother.gdml file
def CreateMother(dir_path,object_list,world):
    #write headers and globals
    F=open(str(dir_path)+"/mother.gdml","w")
    F.write('<?xml version="1.0" encoding="UTF-8" ?>\n')
    F.write('<gdml xmlns:gdml="../schema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="../schema/gdml.xsd" >\n')
    F.write('<define>\n')
    F.write('<position name="center" x="0" y="0" z="0"/>\n')
    F.write('<rotation name="identity" x="0" y="0" z="0"/>\n')
    F.write('</define>\n')
    #write material information
    F.write('<materials>\n')  
    F.write('<element name="Vacuum_el"  formula="Hv" Z="1">\n')
    F.write('<atom value="1.008"/>\n')
    F.write('</element> \n')
    F.write('<material name="Vacuum_ref">\n')
    F.write('<D value="0.0000000000000000000001" unit="mg/cm3"/>\n')
    F.write('<fraction n="1.0" ref="Vacuum_el"/>\n')
    F.write('</material>\n')
    F.write('</materials>\n')
    #write solid information (world volume)
    F.write('<solids>\n')
    F.write('<box name="WorldBox" x="'+str(world[0])+'" y="'+str(world[1])+'" z="'+str(world[2])+'" lunit="m"/>\n')
    F.write('</solids>\n')
    #write structure
    F.write('<structure>\n')
    F.write('<volume name="World">\n')
    F.write('<materialref ref="Vacuum_ref"/>\n')
    F.write('<solidref ref="WorldBox"/>\n')
    for i in range(0,len(object_list)):
        if (object_list[i].VolumeGDMLoption==1):
            F.write('<physvol>\n')
            F.write('<file name="Volumes/'+str(object_list[i].VolumeCAD.Label)+str(i+1)+'.gdml"/>\n')
            F.write('<positionref ref="center"/>\n')
            F.write('<rotationref ref="identity"/>\n')
            F.write('</physvol>\n')
    F.write('</volume>\n')
    F.write('</structure>\n')
    F.write('<setup name="Default" version="1.0">\n')
    F.write('<world ref="World"/>\n')
    F.write('</setup>\n')
    F.write('</gdml>') 
    F.close()

     
####################Function to write individual volume GDML file#####################     
def CreateGDML(obj,vol_numb,path_to_mesh):
    import Mesh
    precision=obj.VolumeMMD   
    triangles = obj.VolumeCAD.Shape.tessellate(precision) #the number represents the precision of the tessellation #returns matrix with triangles vertices
    count=0
    gdml_name=str(obj.VolumeCAD.Label)+str(vol_numb) #gdml file name derives from volume label and number
    #write file
    F=open(str(path_to_mesh)+"/Volumes/"+gdml_name+".gdml","w")
    #write header
    F.write('<?xml version="1.0" encoding="UTF-8" standalone="no" ?>\n')
    F.write('<gdml xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://service-spi.web.cern.ch/service-spi/app/releases/GDML/schema/gdml.xsd">\n')
    #write position
    F.write(' <define>\n')
    for tri in triangles[0]:
        F.write(' <position name="'+gdml_name+'_v'+str(count)+'" unit="mm" x="'+str(tri[0])+'" y="'+str(tri[1])+'" z="'+str(tri[2])+'"/>\n')
        count=count+1	
    F.write(" </define>\n\n")
    #write material
    if obj.VolumeMaterial.Nelements!=0:    
        mat_state="solid"   
        F.write(' <materials>\n')
        F.write('   <material name="'+str(obj.VolumeMaterial.Name)+'" state="'+mat_state+'">\n')
        F.write('       <D unit="g/cm3" value="'+str(obj.VolumeMaterial.Density)+'"/>\n')        
        for i in range (0,obj.VolumeMaterial.Nelements):
            F.write('       <fraction n="'+str(obj.VolumeMaterial.ElementFractions[i])+'" ref="'+str(obj.VolumeMaterial.Elements[i])+'"/>\n')          
        F.write('   </material>\n')         
        F.write(' </materials>\n')
        
    #write solids
    F.write(" <solids>\n")
    F.write(' <tessellated aunit="deg" lunit="mm" name="'+gdml_name+'_solid">\n')
    count=0
    for tri in triangles[1]:
        F.write(' <triangular vertex1="'+gdml_name+'_v'+str(tri[0])+'" vertex2="'+gdml_name+'_v'+str(tri[1])+'" vertex3="'+gdml_name+'_v'+str(tri[2])+'"/>'+"\n")
        count+=3
    F.write(' </tessellated>\n')
    F.write(' <box lunit="mm" name="worldsolid" x="1000" y="1000" z="1000"/>\n')
    F.write(' </solids>'+"\n")
    #write structure
    F.write(' <structure>\n')
    F.write(' <volume name="'+gdml_name+'">\n')
    F.write(' <materialref ref="'+str(obj.VolumeMaterial.Name)+'"/>'+"\n")
    F.write(' <solidref ref="'+gdml_name+'_solid"/>'+"\n")
    F.write(' </volume>\n')
    F.write(' </structure>\n')
    F.write(' <setup name="Default" version="1.0">'+"\n")
    F.write(' <world ref="'+gdml_name+'"/>'+"\n")
    F.write(' </setup>'+"\n")
    F.write('</gdml>')
    F.close()

#Main function called to write all GDML files
def Write_Files(obj_list, world_list):
    write_dir=tkFileDialog.askdirectory()
    print write_dir
    # Create Volumes Directory (does not remove folders)
    try:
        os.mkdir(str(write_dir)+"/Volumes")
        print("Directory " , str(write_dir)+"/Volumes" ,  " Created ") 
    except:
        print("Directory " , str(write_dir)+"/Volumes" ,  " already exists")
    #Create mother gdml
    CreateMother(write_dir,obj_list,world_list,)
    #Create volume gdmls
    counter=1
    for obj in obj_list:
        if obj.VolumeGDMLoption==1:
            CreateGDML(obj,counter,write_dir)
        counter+=1
    tkMessageBox.showinfo("Message", 'GDML Files ready.')        
#Note: A number is added to each volumes label to avoid that two different volumes have the same name. This can be seen in the mother and in the volumes GDMLs
