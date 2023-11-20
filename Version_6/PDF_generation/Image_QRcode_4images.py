from PIL import Image
import os

# Define the A4 size
a4_width = 2480
a4_height = 3508
num_columns = 2
num_rows = 2
images_per_a4 = num_columns * num_rows

# Calculate the size of individual cells
cell_width = a4_width // num_columns
cell_height = a4_height // num_rows

# Calculate the size of individual images
image_width = 1200
image_height = 1350

# Directory containing the images
image_dir = os.path.join(os.path.dirname(__file__), "./PDF_generation/QR_codes")

# Get a list of all image files
image_list = [filename for filename in os.listdir(image_dir) if filename.lower().endswith(('.png', '.jpg', '.jpeg'))]

Name_of_file = 1
# Iterate through the image list in sets of 4 and create A4 images
for i in range(0, len(image_list), images_per_a4):
    # Create a new A4-sized image
    a4_image = Image.new("RGB", (a4_width, a4_height), 'white')
    
    # Iterate over the images in the current set of 4
    for j in range(images_per_a4):
        if i + j < len(image_list):
            img_path = image_list[i + j]
            img = Image.open(os.path.join(image_dir, img_path))
            img = img.resize((image_width, image_height), Image.ANTIALIAS)
            
            # Calculate the position to paste the image at the center of the cell
            cell_x = (j % num_columns) * cell_width
            cell_y = (j // num_columns) * cell_height
            x_offset = cell_x + (cell_width - image_width) // 2
            y_offset = cell_y + (cell_height - image_height) // 2
            
            a4_image.paste(img, (x_offset, y_offset))
    
    # Save the A4 image
    output_filename = f"{Name_of_file}.jpg"
    Name_of_file += 2
    a4_image.save(os.path.join(os.path.dirname(__file__), f"./PDF_generation/{output_filename}"))
