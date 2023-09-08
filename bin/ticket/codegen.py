import random
import string

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