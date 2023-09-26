import pandas as pd
from pymongo.mongo_client import MongoClient

def connect():
    # Connect to MongoDB Atlas

    uri = "mongodb+srv://fuisl:fv7MuQ7lpOlCQbRM@ori23.pdjh2im.mongodb.net/?retryWrites=true&w=majority"

    # Create a new client and connect to the server
    client = MongoClient(uri)

    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print("Pinged deployment. Successfully connected to MongoDB!")
    except Exception as e:
        print(e)

    return client

class Updater:
    '''
    Class for updating ticket status
    '''
    def __init__(self, event_code:str=None):
        """
        Updater for updating ticket status in an event on MongoDB Atlas.

        Parameter:
            :event_code: Event code/Event room/Session code.
        """
        self.client = connect()  # get client
        self.event_code = event_code

        self.db = self.client['check-in']  # create new database
        if event_code != None:
            self.db[event_code]  # create new event_code collection
        self.db["user_info"]
        self.db["ticket_info"]
        self.db["ticket"]

    # ticket_info
    def add_ticket_info_one(self, code: str):  # add 1 ticket info
        self.db['ticket_info'].insert_one({'code':code, 'path':'', 'status':False})
    
    def add_ticket_info_many(self, codes: list):  # add many ticket info
        self.db['ticket_info'].insert_many([{'code':code, 'path':'', 'status':False} for code in codes])

    # user_info
    def add_user_info(self, csv_path: str):  # add many user info from csv file
        df = pd.read_csv(csv_path)
        list_of_dict = df.to_dict('records')
        self.db["user_info"].insert_many(list_of_dict)

    def add_user_info(self, info: dict):  # add 1 user info
        """
        Add 1 user info to database.

        Must include id, name and email.

        info = {'user_id': '...',
                'name': '...',
                'email': '...'}
    
        """
        self.db["user_info"].insert_one(info)
    
    # ticket
    def assign_ticket(self, user_id: str):  # assign 1 ticket to 1 user
        codes = self.db['ticket_info'].find({'status':False}, {'code':1})  # get all unused code
        code = codes[0]['code']  # get 1 unused code
        self.db['ticket'].insert_one({'user_id':user_id, 'code':code})  # insert to ticket collection
        self.db['ticket_info'].update_one({'code':code}, {'$set':{'status':True}})  # update status of code to True

    def get_ticket_all(self):
        """
        return a cursor for all {user_id - code}
        """
        return self.db['ticket'].find({}, {'_id':0})

    # event_code
    def register_many(self, csv_path: str):  # register many code to an event from csv file of user_id
        fil = {'user_id':{'$in':pd.read_csv(csv_path)['user_id'].tolist()}}  # filter by user_id
        cursor = self.db['ticket'].find({fil}, {'code':1})  # get all code
        
        list_of_dict = list(cursor)
        normalized_df = pd.json_normalize(list_of_dict)
        df = pd.DataFrame(normalized_df)
        
        df['status'] = False  # add status column, default is False

        self.db[self.event_code].insert_many(df.to_dict('records'))  # insert to event_code collection

    def register_one(self, user_id: str):  # register 1 user_id to an event
        codes = self.db['ticket'].find({'user_id':user_id}, {'code':1})
        for c in codes:
            self.db[self.event_code].insert_one({'code':c['code'], 'status':False})
    
    def register_code(self, code: str):  # register 1 code to an event
        self.db[self.event_code].insert_one({'code':code, 'status':False})

    def deregister(self, user_id: str):  # deregister id from an event
        cursor = self.db['ticket'].find({'user_id':user_id}, {'code':1})
        condition = {'code':{'$in':list(cursor)}}
        self.db[self.event_code].delete_many(condition)

    def update(self, code: str):  # update status of ticket in an event
        self.db[self.event_code].update_one({'code':code}, {'$set':{'status':True}})

    def get_user_info(self, code):  # get user_info from code
        user = self.db['ticket'].find_one({'code':code}, {'user_id':1})
        
        info = self.db['user_info'].find({'user_id':user['user_id']}, {'_id':0})

        return list(info)[0]
    
    def count(self, code): # count number of scan with a ticket code.
        return self.db[self.event_code].update_one({'code':code}, {'$inc':{'count':1}})


if __name__ == "__main__":
    connect()