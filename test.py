import json

buisness = {
    "id": 2,
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

with open("C:\\Users\\user\\Desktop\\SchoolProj\\SchoolProj-1\\DBes\\BuisnessUser.json", 'w') as file:
    json.dump(buisness, file)

with open("C:\\Users\\user\\Desktop\\SchoolProj\\SchoolProj-1\\DBes\\BuisnessUser.json", 'r') as file:
    data = json.load(file)
    print(data)
