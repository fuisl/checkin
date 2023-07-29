from PIL import Image, ImageDraw, ImageFont
from server import User, Ticket
from pathlib import Path
import base64, io

def render_tickets(user_id: str, font_path: str = 'font_and_imageTemplate/PPTelegraf-Regular.otf', template_path: str = 'font_and_imageTemplate/ticket.png', qrcode_folder: str = '../bin/qrcodes'):
    def encode_images(image):
        data = io.BytesIO()
        image.save(data, "PNG")
        encoded_img_data = base64.b64encode(data.getvalue())
        return encoded_img_data.decode('utf-8')
    
    user_collection = User()
    ticket_collection = Ticket()

    ticket_images_list = []

    find_info_from_user = user_collection.get_user(user_id)
    find_info_from_ticket = [i for i in list(ticket_collection.get_ticket_by_id(user_id))]

    if find_info_from_user != {}:
        name = find_info_from_user['name']

        for ticket in find_info_from_ticket:
            qrcode_image_path = Path(qrcode_folder) / f'{ticket["_id"]}.png'
            qrcode_image = Image.open(qrcode_image_path)

            ticket_class = ticket['class']

            template = Image.open(template_path)

            image_text = ImageDraw.Draw(template)

            myFont = ImageFont.truetype(font_path, 40)

            image_text.text((130, 500), user_id, font=myFont, fill=(0, 0, 0))
            image_text.text((495, 500), ticket_class, font=myFont, fill=(0, 0, 0))
            image_text.text((820, 500), name, font=myFont, fill=(0, 0, 0))

            template.paste(qrcode_image, (1550, 120))

            ticket_images_list.append(encode_images(template))
    
    return ticket_images_list
