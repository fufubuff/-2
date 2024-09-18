from PIL import Image
import os

def grey_to_transparent_except_center(image_path, output_path):
    # Load the image
    img = Image.open(image_path)
    img = img.convert("RGBA")  # Ensure it has an alpha channel
    width, height = img.size

    # Define the center region (50% of the image)
    center_x_start = width * 0.25
    center_x_end = width * 0.75
    center_y_start = height * 0.25
    center_y_end = height * 0.75

    # Get the data for all pixels
    datas = img.getdata()
    
    new_data = []
    for y in range(height):
        for x in range(width):
            index = y * width + x
            item = datas[index]
            # Check if the pixel is within the center region
            if center_x_start <= x <= center_x_end and center_y_start <= y <= center_y_end:
                # Keep all pixels in the center region unchanged
                new_data.append(item)
            else:
                # Change grey pixels outside the center region to transparent
                if abs(item[0] - 192) < 64 and abs(item[1] - 192) < 64 and abs(item[2] - 192) < 64:  # Assuming grey is close to (192, 192, 192)
                    new_data.append((255, 255, 255, 0))  # Setting the grey to transparent
                else:
                    new_data.append(item)  # Leave other colors unchanged

    # Update the image data
    img.putdata(new_data)
    img.save(output_path, "PNG")  # Save as PNG to maintain transparency

def process_folder(folder_path):
    """Process all image files in a folder to make their background transparent."""
    for filename in os.listdir(folder_path):
        if filename.endswith(('.png', '.jpg', '.jpeg')):  # Add more file types if necessary
            file_path = os.path.join(folder_path, filename)
            output_path = os.path.join(folder_path, 'transparent_' + filename)
            grey_to_transparent_except_center(file_path, output_path)
            print(f'Processed {filename}')

# Usage example
process_folder('tiles')
