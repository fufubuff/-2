
from PIL import Image

def white_to_transparent_except_center(image_path, output_path):
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
                # Change white pixels outside the center region to transparent
                if item[0] > 200 and item[1] > 200 and item[2] > 200:  # Adjusting the RGB values which are close to white
                    new_data.append((255, 255, 255, 0))  # Setting the white to transparent
                else:
                    new_data.append(item)  # Leave other colors unchanged

    # Update the image data
    img.putdata(new_data)
    img.save(output_path, "PNG")  # Save as PNG to maintain transparency

# Usage example
white_to_transparent_except_center('tiles/frozen.png', 'tiles/frozen2.png')
