import json

buisness = {
    
        "name": "test",
        "catagory": "food",
        "owner": "ori",
        "description": "pizza shop",
        "comments": [
        {
            "user_name": "ori",
            "content": "love it!"
        }
    ]
}




def Create_Buisness(name, catagory, owner, description, comments):
    buisness["name"] = name
    buisness["catagory"] = catagory
    buisness["owner"] = owner
    buisness["description"] = description
    buisness["comments"] = comments
    return buisness


def Show_db():
    with open("C:\\Users\\user\\Desktop\\SchoolProj\\SchoolProj-1\\DBes\\BuisnessUser.json", 'r') as file:
        data = json.load(file)
    return data


def write_to_db(buisness):
    data = Show_db()
    data[len(data)+1] = buisness
    with open("C:\\Users\\user\\Desktop\\SchoolProj\\SchoolProj-1\\DBes\\BuisnessUser.json", 'w') as file:
        json.dump(data, file, indent=4)


#comments = {"user_name": "Shalev", "content": "So delicius"}
#buisness3 = Create_Buisness(name="Pizzaria", catagory="food", owner="ori", description="xfgdchvjgbhknjm", comments=comments)

#write_to_db(buisness3)

def Delete_Buisness_by_name(name):
    data = Show_db()
    for id in list(data.keys()):
        if data[id]["name"] == name:
           del data[id]
    with open("C:\\Users\\user\\Desktop\\SchoolProj\\SchoolProj-1\\DBes\\BuisnessUser.json", 'w') as file:
        json.dump(data, file, indent=4)

        