from googlesearch import search
import requests
from bs4 import BeautifulSoup
import os
import time

# Lista expandida de términos de búsqueda
queries = [
    "inteligencia artificial", "impacto de inteligencia artificial",
    "inteligencia artificial en educación", "IA en finanzas",
    "automatización y IA", "machine learning y big data",
    "tecnología en el hogar", "avances en inteligencia artificial 2024",
    "inteligencia artificial en el trabajo", "IA en medicina",
    "futuro de la inteligencia artificial", "IA en redes sociales",
    "machine learning en negocios", "tecnología de IA 2024",
    "innovación en inteligencia artificial", "IA en el medio ambiente",
    "inteligencia artificial y privacidad", "inteligencia artificial y seguridad",
    "aplicaciones de inteligencia artificial", "IA y transformación digital",
    "ciberseguridad con IA", "inteligencia artificial en datos"
]
num_results_per_query = 20  # Número de resultados por consulta
objetivo_documentos = 900  # Meta de documentos

# Crear la carpeta donde se guardarán los archivos
SAVE_FOLDER = "noticias_guardadas"
os.makedirs(SAVE_FOLDER, exist_ok=True)

# Contador de documentos guardados, inicia desde el último guardado
contador_documentos = len(os.listdir(SAVE_FOLDER))

def extraer_contenido(url, query_text, result_index):
    global contador_documentos
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Obtener título y contenido
        titulo = soup.title.string if soup.title else f"noticia_{contador_documentos}"
        contenido = " ".join([p.get_text() for p in soup.find_all('p')])
        
        # Contar el número de palabras
        num_palabras = len(contenido.split())
        
        # Guardar el contenido en un archivo de texto si tiene al menos 200 palabras
        if num_palabras >= 200:
            nombre_archivo = f"{SAVE_FOLDER}/{titulo[:50].replace(' ', '_')}_{contador_documentos}.txt"
            with open(nombre_archivo, "w", encoding="utf-8") as file:
                file.write(f"Título: {titulo}\n")
                file.write(f"URL: {url}\n")
                file.write(f"Número de palabras: {num_palabras}\n\n")
                file.write(contenido)

            contador_documentos += 1
            print(f"Artículo guardado: {nombre_archivo} con {num_palabras} palabras (Total guardados: {contador_documentos})")
    except Exception as e:
        print(f"Error al procesar {url}: {e}")

# Realizar múltiples búsquedas hasta alcanzar la meta de 900 documentos
for query_text in queries:
    if contador_documentos >= objetivo_documentos:
        break  # Detener el proceso si se alcanza la meta
    print(f"\nEjecutando búsqueda para: {query_text}")
    try:
        for result_index, enlace in enumerate(search(query_text, num_results=num_results_per_query, lang='es')):
            if contador_documentos >= objetivo_documentos:
                break
            print(f"Procesando: {enlace}")
            extraer_contenido(enlace, query_text, result_index)
            time.sleep(1)  # Pausa entre solicitudes
    except Exception as e:
        print(f"Error en la búsqueda para '{query_text}': {e}")
        continue  # Continuar con la siguiente consulta

    # Pausa más larga entre cada consulta para evitar sobrecargar Google
    time.sleep(5)

print(f"\nProceso completado. Total de documentos guardados: {contador_documentos}")
