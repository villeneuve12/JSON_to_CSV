#####################################################
#               JSON_to_CSV.py
#       By        : Régis Villeneuve, ÉTS
#       Date      : November 26, 2019
#
#       This script, parse through a directory for
#       ".jpg.json" files and extract the information
#        into a .CSV to easily store into a database
#
#####################################################

import csv
import json
#import numpy as np
import os

#Function to calculate area of a polygon
def PolygonArea(corners):
    n = len(corners) # of corners
    area = 0.0
    for i in range(n):
        j = (i + 1) % n
        area += corners[i][0] * corners[j][1]
        area -= corners[j][0] * corners[i][1]
    area = abs(area) / 2.0
    return area

#Set our directory in which we will be working in
directory = '' #Lien vers répertoire


# Open CSV file in Write mode
f = csv.writer(open('test.csv',"w"), lineterminator='')

# Write CSV Header
f.writerow(["inputfile", "descriptionf","tagsf","height","width",
            "presEstomac","areaEstomac",
            "presContaFecal","areaContaFecal",
            "presContaLiquide","areaContaLiquide",
            "presContaSolide","areaContaSolide",
            "presContaEtiquette",
            "presPlateauVide",
            "presPlateauOk"
            "\n"])

#Parse through our directory for .jpg.json files and append to list
for filename in os.listdir(directory):
    if filename.endswith(".json"):
        #Extract Filename
        base = os.path.basename(directory + filename)
        id = os.path.splitext(base)[0]

        #Read JSON
        p = open(directory + filename, 'r')
        info = p.read()

        #Convert Jsonlist string to list
        info = json.loads(info)

        #Get number of objects in our list
        nbobjects = len(info["objects"])

        #Initialize our lists
        dataEstomac = ["Estomac", 0, 0]
        dataContaFecal = ["Contamination Fecale",0,0]
        dataContaLiquide = ["Contamination Liquide",0,0]
        dataContaSolide = ["Contamination Solide",0,0]
        dataContaEtiquette = ["Contamination Etiquette",0]
        dataPlateauVide = ["Plateau Vide",0]
        dataPlateauOk = ["Plateau Ok",0]
        classlist = []

        #Append our data to our classlist
        classlist.append(dataEstomac)
        classlist.append(dataContaFecal)
        classlist.append(dataContaLiquide)
        classlist.append(dataContaSolide)
        classlist.append(dataContaEtiquette)
        classlist.append(dataPlateauVide)
        classlist.append(dataPlateauOk)

        add_mask = 0

        if add_mask == 1:
            classlist[0][0] = classlist[0][0] + "_maskrcnn"
            classlist[1][0] = classlist[0][0] + "_maskrcnn"
            classlist[2][0] = classlist[0][0] + "_maskrcnn"
            classlist[3][0] = classlist[0][0] + "_maskrcnn"
            classlist[4][0] = classlist[0][0] + "_maskrcnn"
            classlist[5][0] = classlist[0][0] + "_maskrcnn"

        #Write first 5 lines
        f.writerow([id,
                    info["description"],
                    info["tags"],
                    info["size"]["height"],
                    info["size"]["width"],
                    ""])

        #Initialize our objectlist
        objectlist = [""]

        #For Each number of different classes
        for j in range(nbobjects):

            #Assign classTitle to classname variable
            classname = info["objects"][j]["classTitle"]

            #Get number coordinate list from "Exterior" and get area
            corners = info["objects"][j]["points"]["exterior"]
            area = PolygonArea(corners)

            #Estomac
            if classname in classlist[0][0]:
                classlist[0][1] += 1
                classlist[0][2] += area

            #Contamination Fecale
            if classname in classlist[1][0]:
                classlist[1][1] += 1
                classlist[1][2] += area

            #Contamination Liquide
            if classname in classlist[2][0]:
                classlist[2][1] += 1
                classlist[2][2] += area

            #Contamination Solide
            if classname in classlist[3][0]:
                classlist[3][1] += 1
                classlist[3][2] += area

            #Contamination Etiquette
            if classname in classlist[4][0]:
                classlist[4][1] += 1

            #Plateau Vide
            if classname in classlist[5][0]:
                classlist[5][1] += 1

        #Plateau OK (si pas contamination & pas vide)
        if (classlist[0][1]>0) & ((classlist[1][1] + classlist[2][1] + classlist[3][1] + classlist[4][1] + classlist[5][1]) == 0) :
            classlist[6][1] += 1

        #Write in CSV file all information for each object
        f.writerow([classlist[0][1],
                    classlist[0][2],
                    classlist[1][1],
                    classlist[1][2],
                    classlist[2][1],
                    classlist[2][2],
                    classlist[3][1],
                    classlist[3][2],
                    classlist[4][1],
                    classlist[5][1],
                    classlist[6][1]
                   ])

        #End line with \n
        f.writerow("\n")
    else:
        continue
