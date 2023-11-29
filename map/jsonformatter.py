import json

with open('./maps.json',encoding="utf-8") as json_file:
    data = json.load(json_file)
    
#json is of type    
# "1" :
    # [
    #     "f3ec56c4g4gch--a",
    #     "cf3c4gh--------a",
    #     "6cfb----------xa",
    #     "4gh---------zbbc",
    #     "fij---------mncc",
    #     "hkl-----------3c",
    #     "cfmmn----------a",
    #     "ch-------------a",
    #     "d--------------a",
    #     "h------------mnc",
    #     "-------y------ac",
    #     "-p-----1f-----a8",
    #     "---1f--3h--oooa7",
    #     "2e2cd--1foo2e2cc",
    #     "c56cdooac2ecc56c",
    #     "c78cc2eccc5cc78c"
    # ],
# Json need to be:
#     {
#    "1":{
#       "level":[
#          "f3ec56c4g4gch--a",
#          "cf3c4gh--------a",
#          "6cfb----------xa",
#          "4gh---------zbbc",
#          "fij---------mncc",
#          "hkl-----------3c",
#          "cfmmn----------a",
#          "ch-------------a",
#          "d--------------a",
#          "h------------mnc",
#          "-------y------ac",
#          "-p-----1f-----a8",
#          "---1f--3h--oooa7",
#          "2e2cd--1foo2e2cc",
#          "c56cdooac2ecc56c",
#          "c78cc2eccc5cc78c"
#       ],
#       "size":[
#          800,
#          800
#       ]
#    }
# }
newJson = {}
for level in data:
    newJson[level] = {}
    newJson[level]["level"] = data[level]
    newJson[level]["size"] = [800,800]

with open('./newMaps.json', 'w',encoding="utf-8") as outfile:
    outfile.write(json.dumps(newJson,indent=4,ensure_ascii=False))
