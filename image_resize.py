from PIL import Image, ExifTags
import os
from random import shuffle
import math

def get_width_height():
    folders = ['./pics/oil_pics', './pics/no_oil_pics']
    min_width = 1e11
    min_height = 1e11

    for folder in folders:
        for filename in os.listdir(folder):
            input_path = os.path.join(folder, filename)
            with Image.open(input_path) as img:
                exif = img._getexif()
                if exif is not None:
                    orientation_tag = next(
                        (key for key, value in ExifTags.TAGS.items() if value == "Orientation"), None
                    )
                    if orientation_tag and orientation_tag in exif:
                        orientation = exif[orientation_tag]
                        if orientation == 3:  # Rotated 180 degrees
                            img = img.rotate(180, expand=True)
                        elif orientation == 6:  # Rotated 270 degrees (90 CW)
                            img = img.rotate(270, expand=True)
                        elif orientation == 8:  # Rotated 90 degrees (90 CCW)
                            img = img.rotate(90, expand=True)

                min_width = min(img.width, min_width)
                min_height = min(img.height, min_height)


    return (min_width, min_height)


def reduce_image_quality_and_size(input_folder, max_width=800, max_height=800):
    """
    Reduces the resolution of all images in a folder.

    Args:
        input_folder (str): Path to the folder containing images.
        max_width (int): Maximum width of the output images.
        max_height (int): Maximum height of the output images.

    Returns:
        None
    """
    output_folder = f'{input_folder}_resized'
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        input_path = os.path.join(input_folder, filename)
        
        # Check if the file is an image
        try:
            with Image.open(input_path) as img:
                exif = img._getexif()
                if exif is not None:
                    orientation_tag = next(
                        (key for key, value in ExifTags.TAGS.items() if value == "Orientation"), None
                    )
                    if orientation_tag and orientation_tag in exif:
                        orientation = exif[orientation_tag]
                        if orientation == 3:  # Rotated 180 degrees
                            img = img.rotate(180, expand=True)
                        elif orientation == 6:  # Rotated 270 degrees (90 CW)
                            img = img.rotate(270, expand=True)
                        elif orientation == 8:  # Rotated 90 degrees (90 CCW)
                            img = img.rotate(90, expand=True)
                # Resize the image while maintaining the aspect ratio
                img.thumbnail((max_width, max_height))
                
                # Convert to RGB if not already in this mode
                img = img.convert("RGB")
                
                output_path = os.path.join(output_folder, filename)
                img.save(output_path, "JPEG")
                print(f"Processed: {filename}")
        except Exception as e:
            print(f"Skipped {filename}: {e}")


def fill_training_folders(max_width=800, max_height=800):
    """
    Fills the trainings image folders with resized images

    Args:
        max_width (int): Maximum width of the output images.
        max_height (int): Maximum height of the output images.

    Returns:
        None
    """
    source_folders = ['./pics/oil_pics', './pics/no_oil_pics']
    
    for idx, folder in enumerate(source_folders):
        has_oil = idx == 0
        images = []

        for filename in os.listdir(folder):
            input_path = os.path.join(folder, filename)
            
            # Check if the file is an image
            try:
                with Image.open(input_path) as img:
                    exif = img._getexif()
                    if exif is not None:
                        orientation_tag = next(
                            (key for key, value in ExifTags.TAGS.items() if value == "Orientation"), None
                        )
                        if orientation_tag and orientation_tag in exif:
                            orientation = exif[orientation_tag]
                            if orientation == 3:  # Rotated 180 degrees
                                img = img.rotate(180, expand=True)
                            elif orientation == 6:  # Rotated 270 degrees (90 CW)
                                img = img.rotate(270, expand=True)
                            elif orientation == 8:  # Rotated 90 degrees (90 CCW)
                                img = img.rotate(90, expand=True)
                    # img.thumbnail((max_width, max_height))
                    img.resize((max_width, max_height))
                    
                    # Convert to RGB if not already in this mode
                    img = img.convert("RGB")

                    images.append((filename, img))
                    
                    print(f"Processed: {filename}")
            except Exception as e:
                print(f"Skipped {filename}: {e}")

        shuffle(images)

        # split into train, val, test (80, 10, 10)
        train_end_dex = math.floor(len(images) * .8 // 1)
        train = images[:train_end_dex]
        
        val_end_dex = train_end_dex + math.floor(len(images) * .1 // 1)
        val = images[train_end_dex:val_end_dex]

        test = images[val_end_dex:]

        for imgs, location in [(train, 'train'), (val, 'val'), (test, 'test')]:
            sub_dir = 'oil' if has_oil else 'no_oil'
            output_folder = f'./oil_detection_training/data/{location}/{sub_dir}'
            for fn, img in imgs:
                output_path = os.path.join(output_folder, fn)
                img.save(output_path, "JPEG")




# Usage
# input_folder = "./test_pics"  # Replace with your folder path
# reduce_image_quality_and_size(input_folder, max_width=100, max_height=100)
# print(get_width_height())
# result is 1078 x 888 pixels
# folders = ['./pics/oil_pics', './pics/no_oil_pics']


# reduce_image_quality_and_size(folders[1], max_width=1078, max_height=888)

fill_training_folders()