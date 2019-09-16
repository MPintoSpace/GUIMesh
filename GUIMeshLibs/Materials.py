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
#Libaries
import os
import tkMessageBox

#Class Element - an Element has a name (from G4 NIST), a density and zero number of elements (used to differentiate them from created materials)
class Element:
	def __init__(self,myname,mydensity):
		self.Name=myname
		self.Density=mydensity
		self.Nelements=0
		
#Class Material - a Material has a name , a density, a number of elements, a list of elements (from the class Element) and a list with each element weight (fraction)
class Material:
	def __init__(self,myname,mydensity,nelements,myelements):
		self.Name=myname
		self.Density=mydensity
		self.Nelements=nelements
		self.Elements=[]
		self.ElementFractions=[]
		for i in range(0,nelements):
			self.Elements.append(myelements[i*2])
			self.ElementFractions.append(float(myelements[i*2+1]))
#Load elements function - It loads the NIST elements recognized by Geant4 to the available Materials
def Load_Elements():
        ele_db_names=["G4_H", "G4_He", "G4_Li", "G4_Be", "G4_B", "G4_C", "G4_N", "G4_O", "G4_F", "G4_Ne", "G4_Na", "G4_Mg", "G4_Al", "G4_Si", "G4_P", "G4_S", "G4_Cl", "G4_Ar", "G4_K", "G4_Ca", "G4_Sc", "G4_Ti", "G4_V", "G4_Cr", "G4_Mn", "G4_Fe", "G4_Co", "G4_Ni", "G4_Cu", "G4_Zn", "G4_Ga", "G4_Ge", "G4_As", "G4_Se", "G4_Br", "G4_Kr", "G4_Rb", "G4_Sr", "G4_Y", "G4_Zr", "G4_Nb", "G4_Mo", "G4_Tc", "G4_Ru", "G4_Rh", "G4_Pd", "G4_Ag", "G4_Cd", "G4_In", "G4_Sn", "G4_Sb", "G4_Te", "G4_I", "G4_Xe", "G4_Cs", "G4_Ba", "G4_La", "G4_Ce", "G4_Pr", "G4_Nd", "G4_Pm", "G4_Sm", "G4_Eu", "G4_Gd", "G4_Tb", "G4_Dy", "G4_Ho", "G4_Er", "G4_Tm", "G4_Yb", "G4_Lu", "G4_Hf", "G4_Ta", "G4_W", "G4_Re", "G4_Os", "G4_Ir", "G4_Pt", "G4_Au", "G4_Hg", "G4_Tl", "G4_Pb", "G4_Bi", "G4_Po", "G4_At", "G4_Rn", "G4_Fr", "G4_Ra", "G4_Ac", "G4_Th", "G4_Pa", "G4_U", "G4_Np", "G4_Pu", "G4_Am", "G4_Cm", "G4_Bk", "G4_Cf","G4_A-150_TISSUE", "G4_ACETONE", "G4_ACETYLENE", "G4_ADENINE", "G4_AIR", "G4_ALANINE", "G4_ALUMINUM_OXIDE", "G4_AMBER", "G4_AMMONIA", "G4_ANILINE", "G4_ANTHRACENE", "G4_B-100_BONE", "G4_BAKELITE", "G4_BARIUM_FLUORIDE", "G4_BARIUM_SULFATE", "G4_BENZENE", "G4_BERYLLIUM_OXIDE", "G4_BGO", "G4_BONE_COMPACT_ICRU", "G4_BONE_CORTICAL_ICRP", "G4_BORON_CARBIDE", "G4_BORON_OXIDE", "G4_BUTANE", "G4_N-BUTYL_ALCOHOL", "G4_C-552", "G4_CADMIUM_TELLURIDE", "G4_CADMIUM_TUNGSTATE", "G4_CALCIUM_CARBONATE", "G4_CALCIUM_FLUORIDE", "G4_CALCIUM_OXIDE", "G4_CALCIUM_SULFATE", "G4_CALCIUM_TUNGSTATE", "G4_CARBON_DIOXIDE", "G4_CARBON_TETRACHLORIDE", "G4_CELLULOSE_CELLOPHANE", "G4_CELLULOSE_BUTYRATE", "G4_CELLULOSE_NITRATE", "G4_CERIC_SULFATE", "G4_CESIUM_FLUORIDE", "G4_CESIUM_IODIDE", "G4_CHLOROBENZENE", "G4_CHLOROFORM", "G4_CYCLOHEXANE", "G4_1,2-DICHLOROBENZENE", "G4_DICHLORODIETHYL_ETHER", "G4_1,2-DICHLOROETHANE", "G4_DIETHYL_ETHER", "G4_N,N-DIMETHYL_FORMAMIDE", "G4_DIMETHYL_SULFOXIDE", "G4_ETHANE", "G4_ETHYL_ALCOHOL", "G4_ETHYL_CELLULOSE", "G4_ETHYLENE", "G4_EYE_LENS_ICRP", "G4_FERRIC_OXIDE", "G4_FERROBORIDE", "G4_FERROUS_OXIDE", "G4_FERROUS_SULFATE", "G4_FREON-12", "G4_FREON-12B2", "G4_FREON-13", "G4_FREON-13B1", "G4_FREON-13I1", "G4_GADOLINIUM_OXYSULFIDE", "G4_GALLIUM_ARSENIDE", "G4_GEL_PHOTO_EMULSION", "G4_Pyrex_Glass", "G4_GLASS_LEAD", "G4_GLASS_PLATE", "G4_GLUCOSE", "G4_GLUTAMINE", "G4_GLYCEROL", "G4_GUANINE", "G4_GYPSUM", "G4_N-HEPTANE", "G4_N-HEXANE", "G4_KAPTON", "G4_LANTHANUM_OXYBROMIDE", "G4_LANTHANUM_OXYSULFIDE", "G4_LEAD_OXIDE", "G4_LITHIUM_AMIDE", "G4_LITHIUM_CARBONATE", "G4_LITHIUM_FLUORIDE", "G4_LITHIUM_HYDRIDE", "G4_LITHIUM_IODIDE", "G4_LITHIUM_OXIDE", "G4_LITHIUM_TETRABORATE", "G4_M3_WAX", "G4_MAGNESIUM_CARBONATE", "G4_MAGNESIUM_FLUORIDE", "G4_MAGNESIUM_OXIDE", "G4_MAGNESIUM_TETRABORATE", "G4_MERCURIC_IODIDE", "G4_METHANE", "G4_METHANOL", "G4_MIX_D_WAX", "G4_MS20_TISSUE", "G4_MUSCLE_STRIATED_ICRU", "G4_MUSCLE_WITH_SUCROSE", "G4_MUSCLE_WITHOUT_SUCROSE", "G4_NAPHTHALENE", "G4_NITROBENZENE", "G4_NITROUS_OXIDE", "G4_NYLON-8062", "G4_NYLON-6/6", "G4_NYLON-6/10", "G4_NYLON-11_RILSAN", "G4_OCTANE", "G4_PARAFFIN", "G4_N-PENTANE", "G4_PHOTO_EMULSION", "G4_PLASTIC_SC_VINYLTOLUENE", "G4_PLUTONIUM_DIOXIDE", "G4_POLYACRYLONITRILE", "G4_POLYCARBONATE", "G4_POLYCHLOROSTYRENE", "G4_POLYETHYLENE", "G4_MYLAR", "G4_PLEXIGLASS", "G4_POLYOXYMETHYLENE", "G4_POLYPROPYLENE", "G4_POLYSTYRENE", "G4_TEFLON", "G4_POLYTRIFLUOROCHLOROETHYLENE", "G4_POLYVINYL_ACETATE", "G4_POLYVINYL_ALCOHOL", "G4_POLYVINYL_BUTYRAL", "G4_POLYVINYL_CHLORIDE", "G4_POLYVINYLIDENE_CHLORIDE", "G4_POLYVINYLIDENE_FLUORIDE", "G4_POLYVINYL_PYRROLIDONE", "G4_POTASSIUM_IODIDE", "G4_POTASSIUM_OXIDE", "G4_PROPANE", "G4_lPROPANE", "G4_N-PROPYL_ALCOHOL", "G4_PYRIDINE", "G4_RUBBER_BUTYL", "G4_RUBBER_NATURAL", "G4_RUBBER_NEOPRENE", "G4_SILICON_DIOXIDE", "G4_SILVER_BROMIDE", "G4_SILVER_CHLORIDE", "G4_SILVER_HALIDES", "G4_SILVER_IODIDE", "G4_SODIUM_CARBONATE", "G4_SODIUM_IODIDE", "G4_SODIUM_MONOXIDE", "G4_SODIUM_NITRATE", "G4_STILBENE", "G4_SUCROSE", "G4_TERPHENYL", "G4_TETRACHLOROETHYLENE", "G4_THALLIUM_CHLORIDE", "G4_TISSUE_SOFT_ICRU-4", "G4_TISSUE-METHANE", "G4_TISSUE-PROPANE", "G4_TITANIUM_DIOXIDE", "G4_TOLUENE", "G4_TRICHLOROETHYLENE", "G4_TRIETHYL_PHOSPHATE", "G4_TUNGSTEN_HEXAFLUORIDE", "G4_URANIUM_DICARBIDE", "G4_URANIUM_MONOCARBIDE", "G4_URANIUM_OXIDE", "G4_UREA", "G4_VALINE", "G4_VITON", "G4_WATER", "G4_WATER_VAPOR", "G4_XYLENE", "G4_GRAPHITE"]
        ele_db_dens=[8.37E-05, 0.000166322, 0.534, 1.848, 2.37, 2, 0.0011652, 0.00133151, 0.00158029, 0.000838505, 0.971, 1.74, 2.699, 2.33, 2.2, 2, 0.00299473, 0.00166201, 0.862, 1.55, 2.989, 4.54, 6.11, 7.18, 7.44, 7.874, 8.9, 8.902, 8.96, 7.133, 5.904, 5.323, 5.73, 4.5, 0.0070721, 0.00347832, 1.532, 2.54, 4.469, 6.506, 8.57, 10.22, 11.5, 12.41, 12.41, 12.02, 10.5, 8.65, 7.31, 7.31, 6.691, 6.24, 4.93, 0.00548536, 1.873, 3.5, 6.154, 6.657, 6.71, 6.9, 7.22, 7.46, 5.243, 7.9004, 8.229, 8.55, 8.795, 9.066, 9.321, 6.73, 9.84, 13.31, 16.654, 19.3, 21.02, 22.57, 22.42, 21.45, 19.32, 13.546, 11.72, 11.35, 9.747, 9.32, 9.32, 0.00900662, 1, 5, 10.07, 11.72, 15.37, 18.95, 20.25, 19.84, 13.67, 13.51, 14, 10,1.127,0.7899,0.0010967,1.35,0.00120479,1.42,3.97,1.1,0.000826019,1.0235,1.283,1.45,1.25,4.89,4.5,0.87865,3.01,7.13,1.85,1.85,2.52,1.812,0.00249343,0.8098,1.76,6.2,7.9,2.8,3.18,3.3,2.96,6.062,0.00184212,1.594,1.42,1.2,1.49,1.03,4.115,4.51,1.1058,1.4832,0.779,1.3048,1.2199,1.2351,0.71378,0.9487,1.1014,0.00125324,0.7893,1.13,0.00117497,1.1,5.2,7.15,5.7,1.024,1.12,1.8,0.95,1.5,1.8,7.44,5.31,1.2914,2.23,6.22,2.4,1.54,1.46,1.2613,1.58,2.32,0.68376,0.6603,1.42,6.28,5.86,9.53,1.178,2.11,2.635,0.82,3.494,2.013,2.44,1.05,2.958,3,3.58,2.53,6.36,0.000667151,0.7914,0.99,1,1.04,1.11,1.07,1.145,1.19867,0.00183094,1.08,1.14,1.14,1.425,0.7026,0.93,0.6262,3.815,1.032,11.46,1.17,1.2,1.3,0.94,1.4,1.19,1.425,0.9,1.06,2.2,2.1,1.19,1.3,1.12,1.3,1.7,1.76,1.25,3.13,2.32,0.00187939,0.43,0.8035,0.9819,0.92,0.92,1.23,2.32,6.473,5.56,6.47,6.01,2.532,3.667,2.27,2.261,0.9707,1.5805,1.234,1.625,7.004,1,0.00106409,0.00182628,4.26,0.8669,1.46,1.07,2.4,11.28,13.63,10.96,1.323,1.23,1.8,1,0.000756182,0.87,1.7]
        ele_db=[]
        for i in range (0,len(ele_db_names)):
                ele_db.append(Element(ele_db_names[i],ele_db_dens[i]))
        return ele_db

#Loads a Material from a txt file - Several tests are made to ensure format is correct and that it does not overlap with other material
def Load_Material(path_to_material):
        ele_db_names=["G4_H", "G4_He", "G4_Li", "G4_Be", "G4_B", "G4_C", "G4_N", "G4_O", "G4_F", "G4_Ne", "G4_Na", "G4_Mg", "G4_Al", "G4_Si", "G4_P", "G4_S", "G4_Cl", "G4_Ar", "G4_K", "G4_Ca", "G4_Sc", "G4_Ti", "G4_V", "G4_Cr", "G4_Mn", "G4_Fe", "G4_Co", "G4_Ni", "G4_Cu", "G4_Zn", "G4_Ga", "G4_Ge", "G4_As", "G4_Se", "G4_Br", "G4_Kr", "G4_Rb", "G4_Sr", "G4_Y", "G4_Zr", "G4_Nb", "G4_Mo", "G4_Tc", "G4_Ru", "G4_Rh", "G4_Pd", "G4_Ag", "G4_Cd", "G4_In", "G4_Sn", "G4_Sb", "G4_Te", "G4_I", "G4_Xe", "G4_Cs", "G4_Ba", "G4_La", "G4_Ce", "G4_Pr", "G4_Nd", "G4_Pm", "G4_Sm", "G4_Eu", "G4_Gd", "G4_Tb", "G4_Dy", "G4_Ho", "G4_Er", "G4_Tm", "G4_Yb", "G4_Lu", "G4_Hf", "G4_Ta", "G4_W", "G4_Re", "G4_Os", "G4_Ir", "G4_Pt", "G4_Au", "G4_Hg", "G4_Tl", "G4_Pb", "G4_Bi", "G4_Po", "G4_At", "G4_Rn", "G4_Fr", "G4_Ra", "G4_Ac", "G4_Th", "G4_Pa", "G4_U", "G4_Np", "G4_Pu", "G4_Am", "G4_Cm", "G4_Bk", "G4_Cf","G4_A-150_TISSUE", "G4_ACETONE", "G4_ACETYLENE", "G4_ADENINE", "G4_AIR", "G4_ALANINE", "G4_ALUMINUM_OXIDE", "G4_AMBER", "G4_AMMONIA", "G4_ANILINE", "G4_ANTHRACENE", "G4_B-100_BONE", "G4_BAKELITE", "G4_BARIUM_FLUORIDE", "G4_BARIUM_SULFATE", "G4_BENZENE", "G4_BERYLLIUM_OXIDE", "G4_BGO", "G4_BONE_COMPACT_ICRU", "G4_BONE_CORTICAL_ICRP", "G4_BORON_CARBIDE", "G4_BORON_OXIDE", "G4_BUTANE", "G4_N-BUTYL_ALCOHOL", "G4_C-552", "G4_CADMIUM_TELLURIDE", "G4_CADMIUM_TUNGSTATE", "G4_CALCIUM_CARBONATE", "G4_CALCIUM_FLUORIDE", "G4_CALCIUM_OXIDE", "G4_CALCIUM_SULFATE", "G4_CALCIUM_TUNGSTATE", "G4_CARBON_DIOXIDE", "G4_CARBON_TETRACHLORIDE", "G4_CELLULOSE_CELLOPHANE", "G4_CELLULOSE_BUTYRATE", "G4_CELLULOSE_NITRATE", "G4_CERIC_SULFATE", "G4_CESIUM_FLUORIDE", "G4_CESIUM_IODIDE", "G4_CHLOROBENZENE", "G4_CHLOROFORM", "G4_CYCLOHEXANE", "G4_1,2-DICHLOROBENZENE", "G4_DICHLORODIETHYL_ETHER", "G4_1,2-DICHLOROETHANE", "G4_DIETHYL_ETHER", "G4_N,N-DIMETHYL_FORMAMIDE", "G4_DIMETHYL_SULFOXIDE", "G4_ETHANE", "G4_ETHYL_ALCOHOL", "G4_ETHYL_CELLULOSE", "G4_ETHYLENE", "G4_EYE_LENS_ICRP", "G4_FERRIC_OXIDE", "G4_FERROBORIDE", "G4_FERROUS_OXIDE", "G4_FERROUS_SULFATE", "G4_FREON-12", "G4_FREON-12B2", "G4_FREON-13", "G4_FREON-13B1", "G4_FREON-13I1", "G4_GADOLINIUM_OXYSULFIDE", "G4_GALLIUM_ARSENIDE", "G4_GEL_PHOTO_EMULSION", "G4_Pyrex_Glass", "G4_GLASS_LEAD", "G4_GLASS_PLATE", "G4_GLUCOSE", "G4_GLUTAMINE", "G4_GLYCEROL", "G4_GUANINE", "G4_GYPSUM", "G4_N-HEPTANE", "G4_N-HEXANE", "G4_KAPTON", "G4_LANTHANUM_OXYBROMIDE", "G4_LANTHANUM_OXYSULFIDE", "G4_LEAD_OXIDE", "G4_LITHIUM_AMIDE", "G4_LITHIUM_CARBONATE", "G4_LITHIUM_FLUORIDE", "G4_LITHIUM_HYDRIDE", "G4_LITHIUM_IODIDE", "G4_LITHIUM_OXIDE", "G4_LITHIUM_TETRABORATE", "G4_M3_WAX", "G4_MAGNESIUM_CARBONATE", "G4_MAGNESIUM_FLUORIDE", "G4_MAGNESIUM_OXIDE", "G4_MAGNESIUM_TETRABORATE", "G4_MERCURIC_IODIDE", "G4_METHANE", "G4_METHANOL", "G4_MIX_D_WAX", "G4_MS20_TISSUE", "G4_MUSCLE_STRIATED_ICRU", "G4_MUSCLE_WITH_SUCROSE", "G4_MUSCLE_WITHOUT_SUCROSE", "G4_NAPHTHALENE", "G4_NITROBENZENE", "G4_NITROUS_OXIDE", "G4_NYLON-8062", "G4_NYLON-6/6", "G4_NYLON-6/10", "G4_NYLON-11_RILSAN", "G4_OCTANE", "G4_PARAFFIN", "G4_N-PENTANE", "G4_PHOTO_EMULSION", "G4_PLASTIC_SC_VINYLTOLUENE", "G4_PLUTONIUM_DIOXIDE", "G4_POLYACRYLONITRILE", "G4_POLYCARBONATE", "G4_POLYCHLOROSTYRENE", "G4_POLYETHYLENE", "G4_MYLAR", "G4_PLEXIGLASS", "G4_POLYOXYMETHYLENE", "G4_POLYPROPYLENE", "G4_POLYSTYRENE", "G4_TEFLON", "G4_POLYTRIFLUOROCHLOROETHYLENE", "G4_POLYVINYL_ACETATE", "G4_POLYVINYL_ALCOHOL", "G4_POLYVINYL_BUTYRAL", "G4_POLYVINYL_CHLORIDE", "G4_POLYVINYLIDENE_CHLORIDE", "G4_POLYVINYLIDENE_FLUORIDE", "G4_POLYVINYL_PYRROLIDONE", "G4_POTASSIUM_IODIDE", "G4_POTASSIUM_OXIDE", "G4_PROPANE", "G4_lPROPANE", "G4_N-PROPYL_ALCOHOL", "G4_PYRIDINE", "G4_RUBBER_BUTYL", "G4_RUBBER_NATURAL", "G4_RUBBER_NEOPRENE", "G4_SILICON_DIOXIDE", "G4_SILVER_BROMIDE", "G4_SILVER_CHLORIDE", "G4_SILVER_HALIDES", "G4_SILVER_IODIDE", "G4_SODIUM_CARBONATE", "G4_SODIUM_IODIDE", "G4_SODIUM_MONOXIDE", "G4_SODIUM_NITRATE", "G4_STILBENE", "G4_SUCROSE", "G4_TERPHENYL", "G4_TETRACHLOROETHYLENE", "G4_THALLIUM_CHLORIDE", "G4_TISSUE_SOFT_ICRU-4", "G4_TISSUE-METHANE", "G4_TISSUE-PROPANE", "G4_TITANIUM_DIOXIDE", "G4_TOLUENE", "G4_TRICHLOROETHYLENE", "G4_TRIETHYL_PHOSPHATE", "G4_TUNGSTEN_HEXAFLUORIDE", "G4_URANIUM_DICARBIDE", "G4_URANIUM_MONOCARBIDE", "G4_URANIUM_OXIDE", "G4_UREA", "G4_VALINE", "G4_VITON", "G4_WATER", "G4_WATER_VAPOR", "G4_XYLENE", "G4_GRAPHITE"]
        lines= open(path_to_material).read().split('\n')
        error_check=0
        #check if density is float > 0
        try:
                float(lines[1])<=0
                #check if number of elements is and integer > 0 and if number number of lines with element name and fraction is correct
                try:
                        int(lines[2])>0
                        if len(lines)!=(int(lines[2])*2+3):
                                print "Error: Number of Elements assigned different than expected."
                                error_check=1
                        else:
                                elements=[]
                                check_fractions=0.0
                                for i in range(3,len(lines)):
                                        elements.append(lines[i])
                                        #check if fraction is a float
                                        if(i%2==0):
                                                try:
                                                        check_fractions+=float(lines[i])
                                                except ValueError:
                                                        print "Error: Element fraction not a float."
                                                        error_check=1
                                        #check if element exists
                                        else:
                                                if lines[i] not in ele_db_names:
                                                        print "Error: Element not in database, please check the name."
                                                        error_check=1
                                if str(check_fractions)!="1.0": #string used to fix a bug
                                        error_check=1
                                        print "Error: Element fraction sum different than 1."
                except ValueError:
                        print "Error: Number of Elements is either < 1 or not an integer."
                        error_check=1
        except ValueError:
                print "Error: Material density either not a float or <1."
                error_check=1
                
        #Accept or not the material
        if error_check==0:
                print lines[0]+" was imported successfully."
                tkMessageBox.showinfo("Message", lines[0]+" was imported successfully.")
                return Material(lines[0], float(lines[1]),int(lines[2]),elements)
        else:
                print lines[0]+" was not imported due to format errors."
                return 0
        
#Loads all Materials in txt form from the "Materials" folder. Each file format is tested. Returns a Maerial database
def Load_Materials():
        ele_db_names=["G4_H", "G4_He", "G4_Li", "G4_Be", "G4_B", "G4_C", "G4_N", "G4_O", "G4_F", "G4_Ne", "G4_Na", "G4_Mg", "G4_Al", "G4_Si", "G4_P", "G4_S", "G4_Cl", "G4_Ar", "G4_K", "G4_Ca", "G4_Sc", "G4_Ti", "G4_V", "G4_Cr", "G4_Mn", "G4_Fe", "G4_Co", "G4_Ni", "G4_Cu", "G4_Zn", "G4_Ga", "G4_Ge", "G4_As", "G4_Se", "G4_Br", "G4_Kr", "G4_Rb", "G4_Sr", "G4_Y", "G4_Zr", "G4_Nb", "G4_Mo", "G4_Tc", "G4_Ru", "G4_Rh", "G4_Pd", "G4_Ag", "G4_Cd", "G4_In", "G4_Sn", "G4_Sb", "G4_Te", "G4_I", "G4_Xe", "G4_Cs", "G4_Ba", "G4_La", "G4_Ce", "G4_Pr", "G4_Nd", "G4_Pm", "G4_Sm", "G4_Eu", "G4_Gd", "G4_Tb", "G4_Dy", "G4_Ho", "G4_Er", "G4_Tm", "G4_Yb", "G4_Lu", "G4_Hf", "G4_Ta", "G4_W", "G4_Re", "G4_Os", "G4_Ir", "G4_Pt", "G4_Au", "G4_Hg", "G4_Tl", "G4_Pb", "G4_Bi", "G4_Po", "G4_At", "G4_Rn", "G4_Fr", "G4_Ra", "G4_Ac", "G4_Th", "G4_Pa", "G4_U", "G4_Np", "G4_Pu", "G4_Am", "G4_Cm", "G4_Bk", "G4_Cf","G4_A-150_TISSUE", "G4_ACETONE", "G4_ACETYLENE", "G4_ADENINE", "G4_AIR", "G4_ALANINE", "G4_ALUMINUM_OXIDE", "G4_AMBER", "G4_AMMONIA", "G4_ANILINE", "G4_ANTHRACENE", "G4_B-100_BONE", "G4_BAKELITE", "G4_BARIUM_FLUORIDE", "G4_BARIUM_SULFATE", "G4_BENZENE", "G4_BERYLLIUM_OXIDE", "G4_BGO", "G4_BONE_COMPACT_ICRU", "G4_BONE_CORTICAL_ICRP", "G4_BORON_CARBIDE", "G4_BORON_OXIDE", "G4_BUTANE", "G4_N-BUTYL_ALCOHOL", "G4_C-552", "G4_CADMIUM_TELLURIDE", "G4_CADMIUM_TUNGSTATE", "G4_CALCIUM_CARBONATE", "G4_CALCIUM_FLUORIDE", "G4_CALCIUM_OXIDE", "G4_CALCIUM_SULFATE", "G4_CALCIUM_TUNGSTATE", "G4_CARBON_DIOXIDE", "G4_CARBON_TETRACHLORIDE", "G4_CELLULOSE_CELLOPHANE", "G4_CELLULOSE_BUTYRATE", "G4_CELLULOSE_NITRATE", "G4_CERIC_SULFATE", "G4_CESIUM_FLUORIDE", "G4_CESIUM_IODIDE", "G4_CHLOROBENZENE", "G4_CHLOROFORM", "G4_CYCLOHEXANE", "G4_1,2-DICHLOROBENZENE", "G4_DICHLORODIETHYL_ETHER", "G4_1,2-DICHLOROETHANE", "G4_DIETHYL_ETHER", "G4_N,N-DIMETHYL_FORMAMIDE", "G4_DIMETHYL_SULFOXIDE", "G4_ETHANE", "G4_ETHYL_ALCOHOL", "G4_ETHYL_CELLULOSE", "G4_ETHYLENE", "G4_EYE_LENS_ICRP", "G4_FERRIC_OXIDE", "G4_FERROBORIDE", "G4_FERROUS_OXIDE", "G4_FERROUS_SULFATE", "G4_FREON-12", "G4_FREON-12B2", "G4_FREON-13", "G4_FREON-13B1", "G4_FREON-13I1", "G4_GADOLINIUM_OXYSULFIDE", "G4_GALLIUM_ARSENIDE", "G4_GEL_PHOTO_EMULSION", "G4_Pyrex_Glass", "G4_GLASS_LEAD", "G4_GLASS_PLATE", "G4_GLUCOSE", "G4_GLUTAMINE", "G4_GLYCEROL", "G4_GUANINE", "G4_GYPSUM", "G4_N-HEPTANE", "G4_N-HEXANE", "G4_KAPTON", "G4_LANTHANUM_OXYBROMIDE", "G4_LANTHANUM_OXYSULFIDE", "G4_LEAD_OXIDE", "G4_LITHIUM_AMIDE", "G4_LITHIUM_CARBONATE", "G4_LITHIUM_FLUORIDE", "G4_LITHIUM_HYDRIDE", "G4_LITHIUM_IODIDE", "G4_LITHIUM_OXIDE", "G4_LITHIUM_TETRABORATE", "G4_M3_WAX", "G4_MAGNESIUM_CARBONATE", "G4_MAGNESIUM_FLUORIDE", "G4_MAGNESIUM_OXIDE", "G4_MAGNESIUM_TETRABORATE", "G4_MERCURIC_IODIDE", "G4_METHANE", "G4_METHANOL", "G4_MIX_D_WAX", "G4_MS20_TISSUE", "G4_MUSCLE_STRIATED_ICRU", "G4_MUSCLE_WITH_SUCROSE", "G4_MUSCLE_WITHOUT_SUCROSE", "G4_NAPHTHALENE", "G4_NITROBENZENE", "G4_NITROUS_OXIDE", "G4_NYLON-8062", "G4_NYLON-6/6", "G4_NYLON-6/10", "G4_NYLON-11_RILSAN", "G4_OCTANE", "G4_PARAFFIN", "G4_N-PENTANE", "G4_PHOTO_EMULSION", "G4_PLASTIC_SC_VINYLTOLUENE", "G4_PLUTONIUM_DIOXIDE", "G4_POLYACRYLONITRILE", "G4_POLYCARBONATE", "G4_POLYCHLOROSTYRENE", "G4_POLYETHYLENE", "G4_MYLAR", "G4_PLEXIGLASS", "G4_POLYOXYMETHYLENE", "G4_POLYPROPYLENE", "G4_POLYSTYRENE", "G4_TEFLON", "G4_POLYTRIFLUOROCHLOROETHYLENE", "G4_POLYVINYL_ACETATE", "G4_POLYVINYL_ALCOHOL", "G4_POLYVINYL_BUTYRAL", "G4_POLYVINYL_CHLORIDE", "G4_POLYVINYLIDENE_CHLORIDE", "G4_POLYVINYLIDENE_FLUORIDE", "G4_POLYVINYL_PYRROLIDONE", "G4_POTASSIUM_IODIDE", "G4_POTASSIUM_OXIDE", "G4_PROPANE", "G4_lPROPANE", "G4_N-PROPYL_ALCOHOL", "G4_PYRIDINE", "G4_RUBBER_BUTYL", "G4_RUBBER_NATURAL", "G4_RUBBER_NEOPRENE", "G4_SILICON_DIOXIDE", "G4_SILVER_BROMIDE", "G4_SILVER_CHLORIDE", "G4_SILVER_HALIDES", "G4_SILVER_IODIDE", "G4_SODIUM_CARBONATE", "G4_SODIUM_IODIDE", "G4_SODIUM_MONOXIDE", "G4_SODIUM_NITRATE", "G4_STILBENE", "G4_SUCROSE", "G4_TERPHENYL", "G4_TETRACHLOROETHYLENE", "G4_THALLIUM_CHLORIDE", "G4_TISSUE_SOFT_ICRU-4", "G4_TISSUE-METHANE", "G4_TISSUE-PROPANE", "G4_TITANIUM_DIOXIDE", "G4_TOLUENE", "G4_TRICHLOROETHYLENE", "G4_TRIETHYL_PHOSPHATE", "G4_TUNGSTEN_HEXAFLUORIDE", "G4_URANIUM_DICARBIDE", "G4_URANIUM_MONOCARBIDE", "G4_URANIUM_OXIDE", "G4_UREA", "G4_VALINE", "G4_VITON", "G4_WATER", "G4_WATER_VAPOR", "G4_XYLENE", "G4_GRAPHITE"]
        mat_db=[]
        if (os.path.isdir("Materials/")==False):
                print '"Materials" folder not found'
                return 0
        for filename in os.listdir("Materials"):
                print "Loading "+filename
                lines = open("Materials/"+filename).read().split('\n')
                #Check variable format
                error_check=0
                try:
                        float(lines[1])<0
                        try:
                                int(lines[2])>0
                                if len(lines)!=(int(lines[2])*2+3):
                                        print "Error: Number of Elements assigned different than expected."
                                        error_check=1
                                else:
                                        elements=[]
                                        check_fractions=0.0
                                        for i in range(3,len(lines)):
                                                elements.append(lines[i])
                                                if(i%2==0):
                                                        try:
                                                                check_fractions+=float(lines[i])
                                                        except ValueError:
                                                                print "Error: Element fraction not a float."
                                                                error_check=1
                                                else:
                                                        if lines[i] not in ele_db_names:
                                                                print "Error: Element not in database, please check the name."
                                                                error_check=1
                                        if str(check_fractions)!="1.0": #string used to fix a bug
                                                error_check=1
                                                print "Error: Element fraction sum different than 1."
                        except ValueError:
                                print "Error: Number of Elements is either < 1 or not an integer."
                                error_check=1
                except ValueError:
                        print "Error: Material density either not a float or <1."
                        error_check=1

                if (error_check==0):
                        print lines[0]+" was imported successfully."
                        mat_db.append(Material(lines[0], float(lines[1]),int(lines[2]),elements))
                else:
                        print lines[0]+" was not imported due to format errors."
        tkMessageBox.showinfo("Message", "Material Database loaded. Check log for errors.")
        print "Material Database loaded. Check log for errors."
        return mat_db

#Save the Material Database into the "Materials" Folder. 
def Save_Materials(Mat_List):
        if (os.path.isdir("Materials/")==False):
                print '"Materials" folder not found'
                return 0
        for i in Mat_List:
                print i.Name
                f=open("Materials/"+str(i.Name)+".txt","w")
                f.write(i.Name+"\n")
                f.write(str(i.Density)+"\n")
                f.write(str(i.Nelements)+"\n")
                for j in range(0, i.Nelements):
                        f.write(str(i.Elements[j])+"\n")
                        if(j<i.Nelements-1):
                                f.write(str(i.ElementFractions[j])+"\n")
                        else:
                                f.write(str(i.ElementFractions[j]))
                f.close()
        tkMessageBox.showinfo("Message", "Material Database saved.")
        print "Material Database saved."
