import os

def extract_filenames(file_paths):
    filenames = []
    for file_path in file_paths:
        filename = os.path.basename(file_path)
        filenames.append(filename)
    return filenames


# extract filepaths from the directory
file_paths = []
for root, directories, files in os.walk('static/highres_images'):
    for filename in files:
        filepath = os.path.join(root, filename)
        file_paths.append(filepath)

filenames = extract_filenames(file_paths)

for filename in filenames:
    print(filename)