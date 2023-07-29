import pymongo

server = pymongo.MongoClient("mongodb://localhost:27017")
database = server['web_db']
ticket_data_collection = database['ticket_data']
ticket_collection = database['ticket']

def reset_is_bought():
    '''Reset is_bought status in ticket_data collection'''
    global ticket_data_collection

    data = ticket_data_collection.find(
        {"is_bought": True},
        {"is_bought": 1}
    )

    id_list = []

    for i in data:
        id_list.append(i['_id'])

    #reset
    ticket_data_collection.update_many(
        {"_id": {"$in": id_list}},
        {"$set": {"is_bought": False}}
    )

def reset_checked():
    '''Reset checkin status in ticket collection'''
    global ticket_collection

    data = ticket_collection.find(
        {"checked": True},
        {"checked": 1}
    )

    id_list = []

    for i in data:
        id_list.append(i['_id'])

    #reset
    ticket_collection.update_many(
        {"_id": {"$in": id_list}},
        {"$set": {"checked": False}}
    )
