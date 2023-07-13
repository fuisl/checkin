import os
from barcode import Code128
from barcode.writer import ImageWriter
from PIL import Image

def gen(codes:list, folder_path='./barcodes/', transparent=False):
    """
    Generate barcode using Code 128 from a list of codes and
    export to a destinated folder, if not exist, automatically
    create one.

    If files exist, replace the duplicate files.

    (optional) Transparent barcode
    """
    folder_path = './'+folder_path+'/barcodes' if not(os.path.isdir(folder_path)) else folder_path+'/barcodes'
    try:
        os.mkdir(folder_path)
        print(f"Folder '{folder_path}' created successfully.")
    except:
        pass
    # (optional) font_path: path to font file to be used
    # Use PIL to set transparent (1) Switch mode to RGBA, (2) set alpha = 0 - 255, (3) 
    ren = ImageWriter(format='PNG', mode='RGBA')

    barcode_options = {'font_size':0,
                       'module_width':0.2,
                       'module_height':7,
                       'text_distance':3,
                       }
 
    for code in codes:
        with open(folder_path+code+'.png', 'wb') as f:
            Code128(code, writer=ren).write(f, options=barcode_options)

    if transparent:
        for code in codes:
            img = Image.open(folder_path+code+'.png')

            img = img.convert("RGBA")

            datas = img.getdata()
            new_data = []

            for item in datas:
                # Set the white pixels as transparent
                if item[:3] == (255, 255, 255):
                    new_data.append((255, 255, 255, 0))
                else:
                    new_data.append(item)

            img.putdata(new_data)

            img.save(folder_path+code+'.png', "PNG")

    print(f'{len(codes)} BarCodes created successfully!')