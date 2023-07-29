from PIL import Image, ImageDraw, ImageFont
from server import User, Ticket
user_id = "10422062"

user_collection = User()
ticket_collection = Ticket()

find_info_from_user = user_collection.get_user(user_id)
find_info_from_ticket = [i for i in list(ticket_collection.get_ticket_by_id(user_id))]
ticket_num = len(find_info_from_ticket)

if find_info_from_user != {}:
    name = find_info_from_user['name']

    for ticket in find_info_from_ticket:
        ticket_class = ticket['class']

        template = Image.open('font_and_imageTemplate/ticket.png')

        image_text = ImageDraw.Draw(template)

        myFont = ImageFont.truetype('font_and_imageTemplate/PPTelegraf-Regular.otf', 40)

        image_text.text((130, 500), user_id, font=myFont, fill=(0, 0, 0))
        image_text.text((495, 500), ticket_class, font=myFont, fill=(0, 0, 0))
        image_text.text((820, 500), name, font=myFont, fill=(0, 0, 0))

        template.show()