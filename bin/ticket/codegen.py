import random
import string, csv
import pandas as pd

def generate_ticket_code(ticket_info: dict, quantity=10, length=6, seed='presto'):
    """Generate a unique ticket code of specified length
    and return a list of ticket codes
    
    dict ticket_info: contains all ticket classes and their corresponding required quantity
    quantity: number of tickets need to be generated
    length: length of ticket code (default 6)
    seed: seed for random generator (default presto)"""
    # Initializing

    #raise exception if ticket_classes quantity does not match the predefined quantity
    if sum(ticket_info.values()) != quantity:
        raise Exception('Quantity error!')
    
    #class field
    ticket_classes = []

    for ticket_class in ticket_info.keys():
        num = ticket_info[ticket_class]
        class_list = [ticket_class] * num
        ticket_classes = ticket_classes + class_list

    tickets = list()  # Create an empty list for tickets
    random.seed(seed)
    characters = string.ascii_uppercase + string.digits
    
    for i in range(quantity):
        ticket_code = ''.join(random.choice(characters) for _ in range(length))
        tickets.append(ticket_code)

    # print(f'{len(tickets)} code(s) created successfully!')

    result = list(zip(tickets, ticket_classes))

    #create data, this could be separated into another function 
    header = ['code', 'class']

    with open('code.csv', 'w') as f:
        writer = csv.writer(f)
        
        writer.writerow(header)

        for i in result:
            writer.writerow(i)
    
    #hàm vẫn trả về tickets như thường, nhưng mà sau này sẽ xài file csv nên mày có thể dựa theo đó chỉnh lại output của hàm này. Có thể là không trả gì hết, hàm gen bên Gen sẽ tự extract csv và return code

    return tickets