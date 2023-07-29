import os
from barcode import Code128
from barcode.writer import ImageWriter
from PIL import Image
from pathlib import Path

def gen(codes:list, folder_path=None, transparent=False):
    """
    Generate barcode using Code 128 from a list of codes and
    export to a destinated folder, if not exist, automatically
    create one.

    If files exist, replace the duplicate files.

    :param codes: list of codes for generating
    :param folder_path: folder_path for exporting images
    :param transparent: set background transparent
    """
    folder_path = './barcodes/' if folder_path == None else folder_path
    path1 = Path(folder_path)  # folder path
    
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
        file_name = Path(code['_id']+'.png')
        file_path = path1.joinpath(file_name)

        with open(file_path, 'wb') as f:
            Code128(code, writer=ren).write(f, options=barcode_options)

    if transparent:
        for code in codes:
            file_name = Path(code+'.png')
            file_path = path1.joinpath(file_name)

            img = Image.open(file_path)

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

            img.save(file_path)

    print(f'{len(codes)} BarCodes created successfully!')