import pymongo

class Server(object):
    def __init__(self):
        self.__server = pymongo.MongoClient("mongodb://localhost:27017")
        self._web_server = self.__server["web_db"]


class User(Server):
    '''Class for working with the user collection'''

    def __init__(self):
        super().__init__()
        self.__collection = self._web_server['user']
        

    def get_user(self, id: str) -> dict:
        '''
        Return user data having the matching id.

        Note: this method only find ONE document. An empty dict is returned if there is no matching value.
        '''
        user_collection = self.__collection

        result = user_collection.find_one({"_id": id})

        if result != None:
            return result
        else:
            print("No value found!")
            return {}

    def add_user(self, data: dict) -> bool:
        '''
        Add a new user to the collection. Return True if the process succeeded, False if there is already a document with the provided user_id.
        '''

        user_collection = self.__collection

        check_existence = self.get_user(id = data['_id'])

        if not bool(check_existence):
            user_collection.insert_one(data)
            return True
        else: 
            return False

    def get_all_id(self):
        user_collection = self.__collection
        all_ids = []

        user_ids = user_collection.find({},{"_id":1})
        
        for id in list(user_ids):
            all_ids.append(id["_id"])
        print(all_ids)
        return all_ids

class UserFace(Server):
    '''Class for working with the user_face collection'''
    def __init__(self):
        super().__init__()
        self.__collection = self._web_server['user_face']

    def get_face(self, id: str) -> dict:
        '''
        Return data of the matching id in the collection.
        '''
        face_collection = self.__collection

        result = face_collection.find_one({"_id": id})

        if result == None:
            print("No value found!")
            return {}
        else:
            return result
        
    def add_face(self, id: str, image_paths: list) -> None:
        '''
        Add new image paths to a new user. The system won't add more data if that user already have data in the collection and it will log out in CLI.
        '''
        face_collection = self.__collection

        insert_document = face_collection.find_one({"_id": id})

        if insert_document == None:
            
            face_collection.insert_one({
                "_id": id,
                "images": image_paths
            })

        else:
            print("Your images have been uploaded already!")
            print(f"You have uploaded {len(insert_document['images'])} images.")

class UserPassword(Server):
    '''Class for working with the user_password collection'''

    def __init__(self):
        super().__init__()
        self.__collection = self._web_server['user_password']

    def get_password(self, id: str) -> str:
        '''
        Return the password of the matching id. An empty string will be returned if no matching data is found.
        '''

        password_collection = self.__collection

        result = password_collection.find_one({"_id": id})

        print(result)

        if result == None:
            return ""
        else:
            return result['password']
        
    def set_password(self, id: str, hashed_password: str) -> None:
        '''
        Set password for new user.

        Warning! This method currently doesn't have any protection or data existence checking. The password should be controlled by the initial web interface rather than this method.  
        '''

        password_collection = self.__collection

        password_collection.insert_one({
            "_id": id,
            "password": hashed_password
        })

class Ticket(Server):
    '''Class for working with the ticket collection'''

    def __init__(self):
        super().__init__()
        self.__collection = self._web_server['ticket']

    def get_ticket_by_id(self, id: str):
        '''Return a mongoDb cursor containing all matching tickets by user_id'''
        ticket_collection = self.__collection
        
        result = ticket_collection.find({"user_id": id})

        if result == None:
            print(f'No ticket found!')
            return {}
        else:
            return result
        
    def get_ticket_by_code(self, code: str) -> dict:
        '''Return a matching ticket'''
        ticket_collection = self.__collection

        result = ticket_collection.find_one({"_id": code})

        if result == None:
            print(f'No ticket found!')
            return {}
        else:
            return result
        
    def get_ticket_by_class(self, ticket_class: str):
        '''Return a mongoDb cursor containing all matching tickets by ticket class'''
        ticket_collection = self.__collection

        result = ticket_collection.find({"class": ticket_class})

        if result == None:
            print(f'No ticket found!')
            return {}
        else:
            return result

    def add_ticket(self, ticket_id: str, user_id: str, ticket_class: str) -> None:
        '''Update the collection with a list of bought tickets from a user'''
        ticket_collection = self.__collection
        ticket_collection.insert_one({
            "_id": ticket_id,
            "user_id": user_id,
            "class": ticket_class,
            "checked": False
        })

class TicketData(Server):
    def __init__(self):
        super().__init__()
        self.__ticket_data_collection = self._web_server['ticket_data']

    def buy_ticket(self, ticket_class: str, quantity: int) -> list:
        '''
        Get desired number of tickets and return their info
        '''

        all_available_tickets = self.__ticket_data_collection.find(
            {
                "class": ticket_class,
                "is_bought": False
        })

        # check if there are enough tickets
        # if all_available_tickets.count() < quantity:
        #     print("Not enough tickets!")
        #     return {}
        # else:
        tickets = list(all_available_tickets.limit(quantity))

        self.__update_ticket_purchase_status(tickets)

        return tickets

    def __update_ticket_purchase_status(self, tickets):
        '''
        Change chosen tickets is_bought status to True
        '''

        id_list = []
        for ticket in tickets:
            id_list.append(ticket['_id'])

        self.__ticket_data_collection.update_many(
            {"_id": {"$in": id_list}},
            {"$set": {"is_bought": True}}
        )