import pymongo

class Database():
    """
    Arguments:
        :param connection_string {str}
        :param db_name {str}: name of the initial collection
    """
    def __init__(self, connection_string="mongodb://localhost:27017", db_name="vgu", initial_collection='career_fair') -> None:
        self.database = pymongo.MongoClient(connection_string)[db_name]
        self.customer_collection = self.database[initial_collection]
    
    def checkin(self, code: str) -> dict:
        """
        Called when a ticket is scanned by the checkin module. Return the data of that ticket code or None if the ticket is already checked in.

        Arguments:
            :param code {str}: code of the ticket
        
        Raise:
            AssertionError -> if a ticket code has field checked_in=True

        Return:
            None if ticket is already checked in
            
            or
            
            dict -> data associated to the ticket
        """

        condition = {
            'code': code,
            "checked_in": {"$exists": False}
        }

        ticket_existence = self.customer_collection.count_documents({'code': code})
        assert ticket_existence == 1, f"Ticket code {code} does not exist!"

        ticket = self.customer_collection.find_one(condition)

        if ticket == None:
            return None
        
        # add checked_in=True for this ticket
        self.customer_collection.update_one({'_id': ticket['_id']}, {"$set": {"checked_in": True}})

        return ticket
    
    def uncheck_all(self) -> int:
        filter = {
            "checked_in": True
        }

        update = {
            "$unset": {"checked_in": ""}
        }

        update_result = self.customer_collection.update_many(filter, update)

        return update_result.modified_count
