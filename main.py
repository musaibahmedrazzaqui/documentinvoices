from doctr.io import DocumentFile
from doctr.models import ocr_predictor
import json
import easygui
file_path = easygui.fileopenbox(title="Select an Image File", filetypes=["*.png", "*.jpg"])
if file_path is None:
    exit()  # Exit if the user cancels the file selection
print("{file_path} recieved." )
model = ocr_predictor(pretrained=True)

# Use easygui to open a file selection dialog

doc = DocumentFile.from_images(file_path)
result = model(doc)
json_output = result.export()

# Save JSON data to feed.json
json_file_path = "feed.json"
with open(json_file_path, 'w') as json_file:
    json.dump(json_output, json_file, indent=4)

print(f"JSON data has been saved to {json_file_path}")
# Read the JSON data from test.json
with open('feed.json', 'r') as json_file:
    json_data = json.load(json_file)

# Open a text file for writing
with open('results.txt', 'w') as txt_file:
    # Initialize a dictionary to store words grouped by y coordinates
    words_by_y = {}

    # Iterate through pages
    for page in json_data['pages']:
        # Iterate through blocks in each page
        for block in page['blocks']:
            # Iterate through lines in each block
            for line in block['lines']:
                # Sort words by their y0 coordinate
                words_in_line = sorted(line['words'], key=lambda w: w['geometry'][0][1])

                # Initialize a list to store words with the same y coordinates
                words_with_equal_y = []

                # Iterate through words in the line
                for word in words_in_line:
                    y_coord = round(word['geometry'][0][1], 2)  # Round y coordinate to 1 decimal place
                    if y_coord not in words_by_y:
                        words_by_y[y_coord] = []
                    words_by_y[y_coord].append(word)

    # Sort the words by y coordinate and write them to the text file with y coordinates
    sorted_y_coords = sorted(words_by_y.keys())
    for y_coord in sorted_y_coords:
        words_with_equal_y = words_by_y[y_coord]
        line_text = ' '.join(f'{w["value"]}' for w in words_with_equal_y)
        txt_file.write(line_text + '\n\n')

print("The results are saved in the root folder as results.txt")
