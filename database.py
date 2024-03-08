from string import ascii_uppercase

def generate_cinema_seats(row_num, seats_per_row):
    '''
    Generate seat ids in regular real-life cinemas. An uppercase letter + a number, depend on number of rows and seats per row.  
    '''
    assert row_num > 0 and seats_per_row > 0, "Invalid number of seats per row/col"

    result_seats = []

    for letter in ascii_uppercase[:row_num]:
        seat_ids = [f'{letter}{number}' for number in range(seats_per_row)]
        result_seats.extend(seat_ids)

    return result_seats