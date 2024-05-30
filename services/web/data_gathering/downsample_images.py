from PIL import Image
import os

def downsample_image(input_path, output_path, target_size):
    # Open the input image
    image = Image.open(input_path)
    
    # Calculate the aspect ratio of the original image
    aspect_ratio = image.width / image.height
    
    # Calculate the target dimensions while preserving the aspect ratio
    if aspect_ratio > 1:
        target_width = target_size
        target_height = int(target_size / aspect_ratio)
    else:
        target_width = int(target_size * aspect_ratio)
        target_height = target_size
    
    # Perform downsampling on the image
    downsized_image = image.resize((target_width, target_height), Image.ANTIALIAS)
    
    # Save the downsized image
    downsized_image.save(output_path)

# downsample all images in a directory
for root, directories, files in os.walk('static/images'):
    for filename in files:
        input_path = os.path.join(root, filename)
        output_path = os.path.join('static/lowres_images/images', filename)
        downsample_image(input_path, output_path, 600)
