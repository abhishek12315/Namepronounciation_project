from PIL import Image
import os

# Define the Letter size
letter_width = int(8.5 * 96)  # Convert inches to pixels at 300 DPI
letter_height = int(11 * 96)

num_columns = 2
num_rows = 2
images_per_page = num_columns * num_rows

# Calculate the size of individual cells
cell_width = letter_width // num_columns
cell_height = letter_height // num_rows

# Calculate the size of individual images
image_width = int(4.25 * 96)  # Convert inches to pixels at 300 DPI
image_height = int(5.5 * 96)

# Directory containing the images
image_dir = os.path.join(os.path.dirname(__file__), "./QR_codes")

# Get a list of all image files
image_list = [filename for filename in os.listdir(image_dir) if filename.lower().endswith(('.png', '.jpg', '.jpeg'))]

Name_of_file = 1
# Iterate through the image list in sets of 4 and create Letter-sized images
for i in range(0, len(image_list), images_per_page):
    # Create a new Letter-sized image
    letter_image = Image.new("RGB", (letter_width, letter_height), 'white')
    
    # Iterate over the images in the current set of 4
    for j in range(images_per_page):
        if i + j < len(image_list):
            img_path = image_list[i + j]
            img = Image.open(os.path.join(image_dir, img_path))
            img = img.resize((image_width, image_height), Image.ANTIALIAS)
            
            # Calculate the position to paste the image at the center of the cell
            cell_x = (j % num_columns) * cell_width
            cell_y = (j // num_columns) * cell_height
            x_offset = cell_x + (cell_width - image_width) // 2
            y_offset = cell_y + (cell_height - image_height) // 2
            
            letter_image.paste(img, (x_offset, y_offset))
    
    # Save the Letter-sized image
    output_filename = f"{Name_of_file}.jpg"
    Name_of_file += 1
    letter_image.save(os.path.join(os.path.dirname(__file__), f"./PDF/{output_filename}"))
