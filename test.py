import DButilities
Db = DButilities.DButilities()


data = Db.get_data("Businesses")
businesses = [user_info for user_id, user_info in data.items()]

for business in businesses:
    print(business["name"])