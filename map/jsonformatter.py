import json
import random

with open('./maps.json',encoding="utf-8") as json_file:
    data = json.load(json_file)
    
levelBgColors={
    "1": (29,43,83),
    "2": (29,43,83),
    "3": (29,43,83),
    "4": (29,43,83),
    "5": (29,43,83),
    "6": (29,43,83),
    "7": (29,43,83),
    "8": (29,43,83),
    "9": (29,43,83),
    "10":(29,43,83),
    "11":(29,43,83),
    "12":(29,43,83),
    "13":(29,43,83),
    "14":(29,43,83),
    "15":(29,43,83),
    "16":(29,43,83),
    "17":(29,43,83),
    "18":(29,43,83),
    "19":(29,43,83),
    "20":(29,43,83),
    "21":(29,43,83),
    "22":(29,43,83),
    "23": (255,119,168),
    "24": (255,119,168),
    "25": (255,119,168),
    "26": (255,119,168),
    "27": (255,119,168),
    "28": (255,119,168),
    "29": (255,119,168),
    "30": (255,119,168),
    "31": (255,119,168),

    "debug":(29,43,83),
    "new":(29,43,83)
}
newJson = {}
for level in data:
    newJson[level] = {}
    newJson[level]["level"] = data[level]["level"]
    newJson[level]["size"] = data[level]["size"]
    newJson[level]["bgcolor"] = data[level]["bgcolor"]
    newJson[level]["particles"] = {}
    newJson[level]["particles"]["cloud"] = [15, levelBgColors[level]]
    newJson[level]["particles"]["snow"] = random.randint(25,50)

with open('./newMaps.json', 'w',encoding="utf-8") as outfile:
    outfile.write(json.dumps(newJson,indent=4,ensure_ascii=False))
