import sys
import glob
import os
from PIL import Image, UnidentifiedImageError
from PIL.ExifTags import TAGS
import ffmpeg
import shutil
from tqdm import tqdm


            
def has_date(filepath):
    returned_value = False
    is_photo = False
    try:
        this_image = Image.open(filepath)
        is_photo = True
    except UnidentifiedImageError as err:
        is_photo = False
    
    if is_photo:    
        exifdata = this_image.getexif()
        for tag_id in exifdata:
            tag = TAGS.get(tag_id, tag_id)
            data = exifdata.get(tag_id)
            if tag in ["DateTime"] and data:
                returned_value = True
                break
    else:
        try:
            exifdata = ffmpeg.probe(filepath)['streams']
            for exifitem in exifdata:
                if "creation_time" in exifitem.get('tags', {}):
                    returned_value = True
                    break
        except Exception as err:
            return False
    return returned_value

def scan_files(folder_path: str) -> list:
    files = []
    for root, dirs, listed_files in os.walk(folder_path):
        for subpath in dirs:
            returned_files = scan_files(f"{root}\\{subpath}")
            [files.append(x) for x in returned_files]
        for file in listed_files:
            files.append(f"{root}\\{file}")
    return files


def check_inputs(input_folder, output_folder):
    if not os.path.exists(input_folder):
        raise RuntimeError(f"The folder specified ({input_folder}) does not exist")
    if not os.path.isdir(input_folder):
        raise RuntimeError(f"The folder specified ({input_folder}) is not a folder")
    if not os.path.exists(output_folder):
        print(f"Creating output folder {output_folder}")
        os.mkdir(output_folder)
    if not os.path.exists(output_folder):
        raise RuntimeError(f"The folder specified ({output_folder}) is not a folder")


def remove_unnecessary(files_list) -> list:
    parsed_list = []
    for file in files_list:
        extension = os.path.splitext(file)[1]
        if extension not in [".json", ".html", ".pamp"]:
            parsed_list.append(file) 
    return parsed_list


def populate_extensions(file_list) -> list:
    extensions = []
    for file in file_list:
        extension = os.path.splitext(file)[1]
        if extension not in extensions:
            extensions.append(extension)
    return extensions


def scan_file_dates(files_list) -> tuple:
    files_with_dates = []
    files_without_dates = []
    print("Looking for date metadata in files...")
    for i in tqdm (range(len(files_list)), desc="Analyzing..."):
        file_path = files_list[i]
        if has_date(file_path):
            files_with_dates.append(file_path)
        else:
            files_without_dates.append(file_path)
    return files_with_dates, files_without_dates


def move_files(files_list, destination) -> list:
    left_files = []
    if not os.path.exists(destination):
        os.mkdir(destination)
    for i in tqdm (range(len(files_list)), desc="Moving..."):
        file = files_list[i]
        try:
            shutil.move(file, destination)
        except Exception as err:
            left_files.append(file)
    return left_files


def main():
    args = sys.argv
    if len(args) < 3:
        raise RuntimeError("You must provide an input folder and an output folder")
    input_folder = args[1]
    output_folder = args[2]
    check_inputs(input_folder, output_folder)
    folder_dates_output = f"{output_folder}\\files_with_dates"
    folder_no_dates_output = f"{output_folder}\\files_without_dates"
    remaining_files = []
    
    # Get all files
    files_list: list = scan_files(input_folder)
    
    # Remove unnecessary files (.json, .html)
    files_list: list = remove_unnecessary(files_list)
    
    extensions: list = populate_extensions(files_list)
    print(f"Found {len(files_list)} files with extensions: {', '.join(extensions)}")
    
    files_with_dates, files_without_dates = scan_file_dates(files_list)
    
    print(f"Found {len(files_with_dates)}/{len(files_list)} files with dates")
    input(f"Press enter to move {len(files_with_dates)} files to {folder_dates_output}: ")
    remain = move_files(files_with_dates, folder_dates_output)
    print(f"{len(remain)} files were not moved.")
    [remaining_files.append(x) for x in remain]
    
    
    print(f"Found {len(files_without_dates)}/{len(files_list)} files WITHOUT dates")
    input(f"Press enter to move {len(files_without_dates)} files to {folder_no_dates_output}: ")
    remain = move_files(files_without_dates, folder_no_dates_output)
    [remaining_files.append(x) for x in remain]
    remaining_files_list = "\n".join(remaining_files)
    
    print(f"The following files were not moved:\n\n{remaining_files_list}")
    

if __name__ in ['__main__']:
    main()