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
    def __init__(self, event_code:str):
        self.client = connect()  # get client
        self.event_code = event_code

        self.db = self.client['check-in']  # create new database

        self.db[event_code]  # create new event_code collection
        self.db["user_info"]
        self.db["ticket_info"]
        self.db["ticket"]

    # ticket_info
    def add_ticket_info(self, code: str):  # add 1 ticket info
        raise NotImplementedError
    
    def add_ticket_info(self, codes: list):  # add many ticket info
        raise NotImplementedError

    # user_info
    def add_user_info(self, csv_path: str):  # add many user info from csv file
        raise NotImplementedError

    def add_user_info(self, info: dict):  # add 1 user info
        raise NotImplementedError
    
    # ticket
    def assign_ticket(self, user_id: str, code: str):  # assign 1 ticket to 1 user
        raise NotImplementedError
    
    # event_code
    def register(self, csv_path: str):  # register many code to an event
        raise NotImplementedError

    def register(self, code: str):  # register 1 code to an event
        raise NotImplementedError
    
    def deregister(self, code: str):  # deregister 1 code from an event
        raise NotImplementedError

    def update(self, code: str):  # update status of ticket in an event
        raise NotImplementedError

if __name__ == "__main__":
    connect()