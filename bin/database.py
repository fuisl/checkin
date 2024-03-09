from string import ascii_uppercase
import pymongo

class GenerateTicketInfo():
    def __init__(self, ticket_info, codes, rows, seats_per_row):
        self.ticket_info = ticket_info
        self.codes = codes
        self.rows = rows
        self.seats_per_row = seats_per_row
        self.vvip_seat_ids = self.__generate_vvip_ids()

    def __generate_vvip_ids(self):
        return [f'vvip{i}' for i in range(self.ticket_info['vvip'])]

    def __generate_cinema_seats(self, row_num, seats_per_row):
        '''
        Generate seat ids in regular real-life cinemas. An uppercase letter + a number, depend on number of rows and seats per row.  
        '''
        assert row_num > 0 and seats_per_row > 0, "Invalid number of seats per row/col"

        result_seats = []

        for letter in ascii_uppercase[:row_num]:
            seat_ids = [f'{letter}{number}' for number in range(seats_per_row)]
            result_seats.extend(seat_ids)

        return result_seats
    
    def __distribute_seat_ids(self):
        def separate_center_rear_ids(seat_ids, start_col_id=7, end_col_id=20):
            assert start_col_id>=0 and end_col_id>start_col_id

            rear_ids = []
            center_ids = []

            for id in seat_ids:
                if int(id[1:]) >= start_col_id and int(id[1:]) <= end_col_id:
                    center_ids.append(id)
                    continue

                rear_ids.append(id)

            return center_ids, rear_ids
        
        def separate_center_vip_norm_ids(seat_ids, start_row_letter='B', end_row_letter='E'):
            first_letter_index = ascii_uppercase.find(start_row_letter.upper())
            second_letter_index = ascii_uppercase.find(end_row_letter.upper())
            assert first_letter_index!=-1 and second_letter_index!=-1, "Invalid input row letters"
            assert second_letter_index > first_letter_index

            norm_center_ids = []
            vip_ids = []

            for id in seat_ids:
                if id[0] in ascii_uppercase[first_letter_index:second_letter_index+1]:
                    vip_ids.append(id)
                    continue

                norm_center_ids.append(id)

            return vip_ids, norm_center_ids

        seat_ids = self.__generate_cinema_seats(self.rows, self.seats_per_row)
        center_ids, self.norm_rear_ids = separate_center_rear_ids(seat_ids)
        self.vip_ids, self.norm_center_ids = separate_center_vip_norm_ids(center_ids)

    def __generate_tickets_with_seats(self):
        self.__distribute_seat_ids()
        tickets_dict = {
            "vvip" : self.vvip_seat_ids,
            "vip" : self.vip_ids,
            "norm_center" : self.norm_center_ids,
            "norm_rear" : self.norm_rear_ids
        }

        return tickets_dict
    
    def generate_tickets(self):
        tickets_dict = self.__generate_tickets_with_seats()
        quantity_by_class = [len(i) for i in tickets_dict.values()]
        assert len(self.codes) == sum(quantity_by_class), "The quantity of codes and generated tickets must be equal"
        
        result_ticket_list = []
        code_index = 0

        for ticket_class in tickets_dict.keys():
            ticket_num = self.ticket_info[ticket_class]
            
            for i, code in enumerate(self.codes[code_index:ticket_num+code_index]):
                ticket = {
                    "_id": code,
                    "class": ticket_class.upper(),
                    "seat": tickets_dict[ticket_class][i],
                    "is_bought": False
                }

                result_ticket_list.append(ticket)

            code_index += ticket_num

        return result_ticket_list

class Database():
    def __init__(self, generated_tickets_info, connection_string="mongodb://localhost:27017", db_name="checkin_presto", initial_collection='tickets'):
        assert len(generated_tickets_info) > 0, "No ticket info"

        self.initial_collection = initial_collection
        self.database = pymongo.MongoClient(connection_string)[db_name]
        self.ticket_collection = self.database['tickets']
        self.generated_tickets_info = generated_tickets_info

    def create_databse(self):
        assert self.initial_collection not in self.database.list_collection_names(), "Collection already existed."

        print(f"Creating database with {len(self.generated_tickets_info)} tickets in '{self.initial_collection}' collection.")
        self.ticket_collection.insert_many(self.generated_tickets_info)