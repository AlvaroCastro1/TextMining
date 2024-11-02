import os
import shutil
from collections import defaultdict

def process_and_move_duplicates(folder_path):
    # Crear carpeta "estos_no" si no existe
    target_folder = os.path.join(folder_path, "estos_no")
    os.makedirs(target_folder, exist_ok=True)

    # Diccionario para almacenar el contenido y el conteo de palabras de cada archivo
    file_data = {}
    duplicates = defaultdict(list)

    # Recorrer todos los archivos en la carpeta
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".txt"):
            file_path = os.path.join(folder_path, file_name)
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                word_count = len(content.split())

                # Solo considerar archivos con menos de 400 palabras
                if word_count < 400:
                    file_data[file_name] = (content, word_count)

    # Comparar archivos para encontrar duplicados
    for file1, (content1, _) in file_data.items():
        for file2, (content2, _) in file_data.items():
            if file1 != file2 and content1 == content2:
                duplicates[file1].append(file2)

    # Mover archivos duplicados a la carpeta "estos_no"
    moved_files = set()
    for file, dup_list in duplicates.items():
        if file not in moved_files:
            # Mover archivo original y sus duplicados
            shutil.move(os.path.join(folder_path, file), os.path.join(target_folder, file))
            moved_files.add(file)
            print(f"Movido: {file} a {target_folder}")

            for dup in set(dup_list):
                if dup not in moved_files:
                    shutil.move(os.path.join(folder_path, dup), os.path.join(target_folder, dup))
                    moved_files.add(dup)
                    print(f"Movido: {dup} a {target_folder}")

    if moved_files:
        print("\nArchivos duplicados con menos de 400 palabras se han movido a la carpeta 'estos_no'.")
    else:
        print("\nNo se encontraron archivos duplicados con menos de 400 palabras para mover.")

# Ruta a la carpeta que contiene los archivos .txt

folder_path = "noticias_guardadas"
process_and_move_duplicates(folder_path)

