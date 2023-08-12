import random
import string

def generate_ticket_code(ticket_info: dict, length=6, seed='presto'):
    """Generate a unique ticket code of specified length
    and return a list of ticket codes
    
    :param dict ticket_info: contains all ticket classes and their corresponding required quantity.
        
    Example ticket_info dictionary:
    
        {
        'STANDARD': 5
        'VIP': 7
        'WAENDERLUSTE': 4
        }

    :param length: length of ticket code (default 6)
    :param seed: seed for random generator (default presto)"""
    # Initializing

    quantity = sum(ticket_info.values())  # Total number of tickets to be generated
    
    #class field
    ticket_classes = []

    for ticket_class in ticket_info.keys():
        num = ticket_info[ticket_class]
        class_list = [ticket_class] * num
        ticket_classes = ticket_classes + class_list

    tickets = list()  # Create an empty list for tickets
    random.seed(seed)
    characters = string.ascii_uppercase + string.digits  
    
    #generate and combine ticket data
    for i in range(quantity):
        ticket_code = ''.join(random.choice(characters) for _ in range(length))
        
        ticket_data = {
            "class": ticket_classes[i],
            "_id": ticket_code,
            "is_bought": False
        }

        tickets.append(ticket_data)
    if len(tickets) == quantity:
        print(f'{len(tickets)} code(s) created successfully!')

    return tickets  # Return the list of tickets data


def generate_ticket_code(quantity=10, length=6, seed='presto'):
    """Generate a unique ticket code of specified length
    and return a list of ticket codes
    
    :param quantity: number of tickets need to be generated
    :param length: length of ticket code (default 6)
    :param seed: seed for random generator (default presto)"""
    # Initializing
    tickets = list()  # Create an empty list for tickets
    random.seed(seed)
    characters = string.ascii_uppercase + string.digits

    for i in range(quantity):
        ticket_code = ''.join(random.choice(characters) for _ in range(length))
        tickets.append(ticket_code)

    print(f'{len(tickets)} code(s) created successfully!')

    return tickets  # Return the list of tickets codes