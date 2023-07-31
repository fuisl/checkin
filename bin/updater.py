import pymongo
from time_tracking import increase_checkin_by_one

class Server(object):
    def __init__(self):
        self.__server = pymongo.MongoClient("mongodb://localhost:27017")
        self._database = self.__server['web_db']

class Updater(Server):
    '''
    Class for updating ticket status
    '''
    def __init__(self):
        super().__init__()
        self._ticket_collection = self._database['ticket']

    def _get_ticket_relevant_info(self, key: str, get_by_id: bool) -> list:
        '''
        Private method. Return a list of matching documents involving both user and ticket collections.
        :param key: is either the user id or the ticket code
        :param get_by_id: defined pipeline for aggregation. True for getting data by user id, False for getting data by ticket code
        '''
        pipeline = []
        if get_by_id:
            pipeline = [
                {
                    "$lookup": {
                        "from": "user",
                        "localField": "user_id",
                        "foreignField": "_id",
                        "as": "User"
                    }
                },
                {
                    "$unwind": "$User"
                },
                {#difference
                    "$match": {
                        "User._id": key
                    }
                },
                {
                    "$project": {
                        "customer_id": "$User._id",
                        "name": "$User.name",
                        "gender": "$User.gender",
                        "checked": 1,
                        "class": 1,
                        "code_qr": 1
                    }
                }
            ]

        else:
            pipeline = [
                {
                    "$lookup": {
                        "from": "user",
                        "localField": "user_id",
                        "foreignField": "_id",
                        "as": "User"
                    }
                },
                {
                    "$unwind": "$User"
                },
                {#difference
                    "$match": {
                        "_id": key
                    }
                },
                {
                    "$project": {
                        "customer_id": "$User._id",
                        "name": "$User.name",
                        "gender": "$User.gender",
                        "checked": 1,
                        "class": 1,
                        "code_qr": 1
                    }
                }
            ]
            
        ticket_info = self._ticket_collection.aggregate(pipeline)
        return list(ticket_info)
    
class FaceUpdater(Updater):
    def __init__(self):
        super().__init__()

    def update(self, id: str):
        '''
        Used for checkin with face recognition. 
        :param id: user id
        '''
        get_ticket = self._get_ticket_relevant_info(key=id, get_by_id=True)
        if get_ticket:
            ticket_status = get_ticket[0]['checked']

        if ticket_status:
            print('This ticket has been checked in!')
        else:
            increase_checkin_by_one()
            self._ticket_collection.update_one(
                {"user_id": id},
                {"$set": {"checked": True}}
            )
    
    def get_info(self, id: str):
        '''
        Used for getting user info by id.
        :param id: user id
        '''
        get_ticket = self._get_ticket_relevant_info(key=id, get_by_id=True)
        if get_ticket:
            return get_ticket[0]

class CodeUpdater(Updater):
    def __init__(self):
        super().__init__()

    def update(self, ticket_code: str):
        '''
        Used for code scanned checkin.
        :param ticket_code: the literal code (encoded after scanned) of the ticket
        '''
        get_ticket = self._get_ticket_relevant_info(key=ticket_code, get_by_id=False)
        if get_ticket:
            ticket_status = get_ticket[0]['checked']
        else:
            print('Invalid ticket!')
            return

        #check validity
        if ticket_status:
            print('This ticket has been checked in!')
        else:
            increase_checkin_by_one()
            self._ticket_collection.update_one(
                {"_id": ticket_code},
                {"$set": {"checked": True}}
            )

    def get_info(self, ticket_code: str):
        '''
        Used for getting user info by id.
        :param id: user id
        '''
        get_ticket = self._get_ticket_relevant_info(key=ticket_code, get_by_id=False)
        if get_ticket:
            return get_ticket[0]

class Observer(Server):
    '''
    Class used for observing database. Should be called after committing any changes.
    '''
    def __init__(self):
        super().__init__()
        self.__user_collection = self._database['user']
        self.__ticket_collection = self._database['ticket']
    
    def show_data(self) -> list:
        pipeline = [
                {
                    "$lookup": {
                        "from": "user",
                        "localField": "user_id",
                        "foreignField": "_id",
                        "as": "User"
                    }
                },
                {
                    "$unwind": "$User"
                },
                {
                    "$project": {
                        "_id": 0,
                        "code": "$_id",
                        "customer_id": "$User._id",
                        "name": "$User.name",
                        "gender": "$User.gender",
                        "checked": 1,
                        "class": 1,
                        "code_qr": 1
                    }
                }
            ]
        
        result = self.__ticket_collection.aggregate(pipeline)
        return list(result)

class TicketCode(Server):
    '''
    Class to work with ticket_data collection
    '''
    def __init__(self):
        super().__init__()
        self.__ticket_data_collection = self._database['ticket_data']

    def create_tickets(self, data: list):
        self.__ticket_data_collection.insert_many(data)