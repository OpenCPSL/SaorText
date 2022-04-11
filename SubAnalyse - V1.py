# -*- coding: utf-8 -*-
"""
Created on Fri Apr  8 23:25:41 2022

@author: OpenCPSL
License: GPLv3
"""

import ass
import re

# ---------------------
# ----- Functions -----
# ---------------------

# Takes a colour in ASS/EDU BGR format and returns a friendly name, or RGB code.
def colour_name(subColour, RGB=False):
    
    RGBtoName = {"000000": "black", "FFFFFF": "white", \
                 "FF0000": "red", "00FF00": "green", "0000FF": "blue", \
                 "FFFF00": "yellow", "FF00FF": "magenta", "00FFFF": "cyan"}
    
    colourBGR = subColour.split('&')[1][1:]
    colourRGB = colourBGR[4:6] + colourBGR[2:4] + colourBGR[0:2]
    
    if RGB == True:
        return colourRGB
    else:
        try:
            return RGBtoName[colourRGB]
        except:
            return colourRGB
    
    
# Splits the subtitles by colour, returns list with colour value
def colour_split(subText, subTime):
    
    defColour  = "&HFFFFFF&"  # White, as per EBU Teletext default colour, in BGR format
    defColName = colour_name(defColour) 
    
    # RegEx to find subtitle colour - r'{\\.?c&\w+&}'
    colourSearch = re.findall(r'{\\.?c&\w+&}', subText)

    splitText = list()
    if len(colourSearch) > 0:
       
        for colour in colourSearch:
            
            colourName = colour_name(colour)
            
            try:
                inputText  = splitText[-1]["text"]
                prevColour = splitText[-1]["colour"] 
            except:
                inputText = subText
                

            if len(splitText) < 1:
                text = inputText.split(colour, 1)[0]
                if len(text) > 0:
                    splitText.append({"colour": defColName, "time": subTime, "text": text})
                splitText.append({"colour": colourName, "time": subTime, "text": inputText.split(colour, 1)[1]})
            
            else:
                splitText[-1] = ({"colour": prevColour, "time": subTime, "text": inputText.split(colour, 1)[0]})
                splitText.append({"colour": colourName, "time": subTime, "text": inputText.split(colour, 1)[1]})
    
    else:
        splitText.append({"colour": defColName, "time": subTime, "text": subText})
        
    return splitText


# ----------------
# ----- MAIN -----
# ----------------

if __name__ == "__main__":
    
    # Step 1: Load in Subtitle file
    # ---------------------------------------
    fileIn = "test2222.ass"
    
    with open(fileIn, encoding='utf_8_sig') as f:
        doc = ass.parse(f)
    


    # Step 2: Find the unique subtitles
    # ---------------------------------------
    
    # A naive approach is to assume that the top subtitle is "good" and then 
    # check for a change.  Since subtitles get created additively, need to check
    # if previous subtitle is contained in present subtitle.
    # 
    # N.B. This method is known to have issues if there are two unique lines.
    
    subList = list()
    prevText = "~~~~~"
    subNo = 0
    
    for eventNo in range(0,len(doc.events)):
    #for eventNo in range(0,500):                   # Shorter range for debug
        newSub = dict()        
        
        # Use the first (top) line of subtitle text only
        text  = doc.events[eventNo].text.replace('\h',' ').split('\\N')[0]
        start = doc.events[eventNo].start
        end   = doc.events[eventNo].end
        
        # Check if previous line is in present line
        try:
            textIndex = text.index(prevText)
        except:
            #print(eventNo, start, text)
            newSub = {"subNo": subNo, "eventNo": eventNo, "start": start, "text": text}
            subList.append(newSub)
            subNo += 1
            pass       
        
        prevText = text
        
    # Step 3: Strip out all the position information  
    # -------------------------------------------------    
    replace = {r'{\\an\d}':''}      # RegEx to find markup for subtitle position - r'{\\an\d}'  
    for sub in subList:              
        for key in replace:
            sub["text"] = re.sub(key, replace[key], sub["text"])
            
        
    # Step 4: Split the subtitles by colour
    # ------------------------------------------------- 
    subListColour = list()    
    for sub in subList:
        splitText = colour_split(sub["text"], sub["start"])
        
        for row in splitText:
            
            row["eventNo"] = sub["eventNo"]
            row["subNo"]   = sub["subNo"]
            subListColour.append(row)           
    
    
    # Step 5: Make the transcript
    # ------------------------------------------------- 
    transcript = ""
    prevColour = ""
    
    for sub in subListColour:
        colour  = sub["colour"]
        
        # On new colour, make new paragraph
        if colour != prevColour:            
            transcript += "\n\n[" + str(sub["time"]) + "],[" + str(sub["eventNo"]) + "]"
            transcript += "\n[" + colour + "] "
        
        transcript += sub["text"]        
        prevColour = colour
        
    print(transcript)
    