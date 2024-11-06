import os
import shutil
import difflib

def are_files_similar(file1_path, file2_path):
    with open(file1_path, 'r', encoding='utf-8') as f1, open(file2_path, 'r', encoding='utf-8') as f2:
        return f1.read() == f2.read()

def are_names_similar(name1, name2, threshold=0.8):
    ratio = difflib.SequenceMatcher(None, name1, name2).ratio()
    return ratio >= threshold

def move_to_estos_no(file_path, destination_folder):
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
    shutil.move(file_path, destination_folder)

def main(folder_path):
    destination_folder = os.path.join(folder_path, 'estos_no')
    files = [f.strip() for f in os.listdir(folder_path) if f.endswith('.txt')]

    for i in range(len(files)):
        file1_path = os.path.join(folder_path, files[i])
        for j in range(i + 1, len(files)):
            file2_path = os.path.join(folder_path, files[j])

            if os.path.exists(file1_path) and os.path.exists(file2_path):
                if (are_files_similar(file1_path, file2_path) or 
                    are_names_similar(files[i], files[j])):
                    move_to_estos_no(file1_path, destination_folder)
                    move_to_estos_no(file2_path, destination_folder)

if __name__ == "__main__":
    folder_path = input("Introduce la ruta de la carpeta: ")
    main(folder_path)
