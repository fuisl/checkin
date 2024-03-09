from string import ascii_uppercase
import pymongo

# Don't need to understand the GenerateTicketInfo, just input the right quantity of codes and matching quantity per class for ticket_info. The main procedure from scratch is written in the Database docstring.

class GenerateTicketInfo():
    """This class is tailored to our current task and seats planning. If adopted for other projects, this class should be re-written to generate a tailor-made generator for different seats distribution.
    
    Arguments:
        :param ticket_info {dict}: quantity per class, format {class: quantity}
        :param codes {list}: codes that will be used for qrcodes generation
        :param rows {int}: number of seat rows
        :param seats_per_row {int}
    """

    def __init__(self, ticket_info, codes, rows, seats_per_row) -> None:
        self.ticket_info = ticket_info
        self.codes = codes
        self.rows = rows
        self.seats_per_row = seats_per_row
        self.vvip_seat_ids = self.__generate_vvip_ids()

    def __generate_vvip_ids(self) -> list:
        """
        Return seat ids for VVIP class, format 'vvip{number(0->vvip_quantity)}'
        """
        return [f'vvip{i}' for i in range(self.ticket_info['vvip'])]

    def __generate_cinema_seats(self) -> list:
        """
        Generate seat ids in regular real-life cinemas, format '{uppercase letter}{number}', {number} depends on number of rows and seats per row.  
        """
        assert self.rows > 0 and self.seats_per_row > 0, "Invalid number of seats per row/col"

        result_seats = []

        for letter in ascii_uppercase[:self.rows]:
            seat_ids = [f'{letter}{number}' for number in range(self.seats_per_row)]
            result_seats.extend(seat_ids)

        return result_seats
    
    def __distribute_seat_ids(self) -> None:
        """
        Distribute generated seat ids to theirs classes.
        """

        def separate_center_rear_ids(seat_ids, start_col_id=7, end_col_id=20) -> tuple:
            """Separate seat ids of the center section and rear section. (start_col_id < end_col_id)
            Argument:
                :param seat_ids {list}: all generated codes
                :param start_col_id {int}
                :param end_col_id {int}
            Return:
                tuple -> (seat ids of center section, seat ids of rear section)
            """
            assert start_col_id>=0 and end_col_id>start_col_id

            rear_ids = []
            center_ids = []

            for id in seat_ids:
                if int(id[1:]) >= start_col_id and int(id[1:]) <= end_col_id:
                    center_ids.append(id)
                    continue

                rear_ids.append(id)

            return center_ids, rear_ids
        
        def separate_center_vip_norm_ids(seat_ids, start_row_letter='B', end_row_letter='E') -> tuple:
            """Separate seat ids vip class and standard_center section. (start_row_letter < end_row_letter in ascii)
            Argument:
                :param seat_ids {list}: codes of center section
                :param start_row_letter {str}
                :param end_row_letter {int}
            Return:
                tuple -> (seat ids of vip, seat ids of standard_center)
            """
            assert len(start_row_letter) == 1 and len(end_row_letter) == 1, "Start and end letters should only have length 1"

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

        seat_ids = self.__generate_cinema_seats()
        center_ids, self.norm_rear_ids = separate_center_rear_ids(seat_ids)
        self.vip_ids, self.norm_center_ids = separate_center_vip_norm_ids(center_ids)

    def __generate_tickets_with_seats(self) -> dict:
        """
        Generate all tickets with class and seat id. Format {class: seat_ids}
        """
        self.__distribute_seat_ids()
        tickets_dict = {
            "vvip" : self.vvip_seat_ids,
            "vip" : self.vip_ids,
            "norm_center" : self.norm_center_ids,
            "norm_rear" : self.norm_rear_ids
        }

        return tickets_dict
    
    def generate_tickets(self) -> list:
        """
        Generate tickets data for input to database.
        Return:
            list -> [
                {
                _id: code,
                class: class,
                seat: seat_id,
                is_bought: False
                },...
            ]
        """
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
    """
    A class for interacting with database. The simple use from scratch should be: Gen in gen.py for codes -> GenerateTicketInfo for input data -> Database for connection -> Database.create_database() to create the initial collection of tickets.
    Arguments:
        :param generated_tickets_info {list}: list of dictionaries of all generated ticket data by GenerateTicketInfo class.
        :param connection_string {str}
        :param db_name {str}: name of the initial collection
    """
    def __init__(self, generated_tickets_info, connection_string="mongodb://localhost:27017", db_name="checkin_presto", initial_collection='tickets') -> None:
        assert len(generated_tickets_info) > 0, "No ticket info"

        self.initial_collection = initial_collection
        self.database = pymongo.MongoClient(connection_string)[db_name]
        self.ticket_collection = self.database['tickets']
        self.generated_tickets_info = generated_tickets_info

    def create_database(self) -> None:
        """Create the initial collection"""
        assert self.initial_collection not in self.database.list_collection_names(), "Collection already existed."

        print(f"Creating database with {len(self.generated_tickets_info)} tickets in '{self.initial_collection}' collection.")
        self.ticket_collection.insert_many(self.generated_tickets_info)