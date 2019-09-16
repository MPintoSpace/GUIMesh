# GUIMesh
Copyright (c) 2018  Marco Gui Alves Pinto  mail:mgpinto11@gmail.com

This program is distributed under the terms of the GNU General Public License 3

### Software Description
GUIMesh is a Graphical User Interface that converts STEP geometries to GDML format allowing
to import this geometries into Geant4

### Citation / Reference
GUIMesh is published in: https://doi.org/10.1016/j.cpc.2019.01.024. It has a full description of the program as well as all the tests done. You can request me the document via e-mail.
Please cite the paper if you found GUIMesh useful for your work.

### Dependencies
GUIMesh requires:

* UNIX distribution or Windows (R) 
* [Python 2.X](www.python.org) with TKinter extension
* [FreeCAD](www.freecadweb.org) v0.15 and 0.16
* [Geant4](https://geant4.web.cern.ch/) - although Geant4 is not necessary to run GUIMesh, its output are intended to be imported by it. Versions >10 are recomended.

Note: Since GUIMesh is a python script only its dependencies must be installed.

### File description
* GUIMesh.py - Main and only source code
* Documents - Folder with "GUIMesh User Manual.pdf", a guide on how to run GUIMesh found in the Documents directory
* GUIMeshLibs - folder containing libraries used in GUIMesh
* Materials - folder which should be used to save materials in a database
* STEP Files - folder with STEP geometries used in all tests
* COPYING - License disclosure

