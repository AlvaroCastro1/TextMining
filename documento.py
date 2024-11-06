
import re
from googlesearch import search
import requests
from bs4 import BeautifulSoup
import os
import time

# Configuración de la búsqueda con más variaciones y temas más específicos
queries = [
    # "ChatGPT en aplicaciones prácticas", 
    # "Gemini IA Google", 
    # "Copilot Microsoft inteligencia artificial",
    # "modelos de IA generativa 2024",
    # "usos de ChatGPT en la industria",
    # "tecnología de Gemini y Google IA",
    # "Copilot en programación y desarrollo",
    # "deep learning en inteligencia artificial generativa",
    # "innovación en modelos de lenguaje grandes",
    # "aplicaciones de IA generativa en negocios",
    # "impacto de ChatGPT en la educación",
    # "Copilot en GitHub para desarrolladores",
    # "avances en modelos de deep learning",
    # "comparación de ChatGPT y Gemini",
    # "tecnología de Copilot en software",
    # "tendencias en inteligencia artificial generativa",
    # "machine learning aplicado a modelos de lenguaje",
    # "procesamiento de lenguaje natural con ChatGPT",
    # "modelos avanzados de deep learning en 2024",
    # "inteligencia artificial en generación de texto"
    # "inteligencia artificial en negocios", 
    # "impacto de inteligencia artificial en salud",
    # "inteligencia artificial y educación en 2024",
    # "automatización en inteligencia artificial",
    # "machine learning y big data",
    # "IA y tecnología en el hogar",
    # "avances en inteligencia artificial",
    # "cómo funciona la inteligencia artificial",
    # "inteligencia artificial en redes sociales",
    # "IA en la economía global"
    # "la IA nos va a sustituir",
    # "inteligencia artificical en los proximos años",
    # "origen de la inteligencia artificical",
    # "que es la inteligencia artificical",
    # "quien creo la inteligencia artificical",
    # "como programar alguna inteligencia artificical",
    # "inteligencia artificical de google",
    # "inteligencia artificical de amazon",
    # "chatgpt",
    # "gimini",
    # "para que sirve la inteligencia artificical",
    # "en donde se usa inteligencia artificical",
    # "quien puede usar inteligencia artificical",
    # "como usar inteligencia artificical",
    # "cosas que hace la inteligencia artificical por nosotros"
    # "inteligencia artificial", "impacto de inteligencia artificial",
    # "inteligencia artificial en educación", "IA en finanzas",
    # "automatización y IA", "machine learning y big data",
    # "tecnología en el hogar", "avances en inteligencia artificial 2024",
    # "inteligencia artificial en el trabajo", "IA en medicina",
    # "futuro de la inteligencia artificial", "IA en redes sociales",
    # "machine learning en negocios", "tecnología de IA 2024",
    # "innovación en inteligencia artificial", "IA en el medio ambiente",
    # "inteligencia artificial y privacidad", "inteligencia artificial y seguridad",
    # "aplicaciones de inteligencia artificial", "IA y transformación digital",
    # "ciberseguridad con IA", "inteligencia artificial en datos"
    # "implementaciones de ChatGPT en 2024",
    # "nuevas capacidades de Gemini IA",
    # "Microsoft Copilot en herramientas empresariales",
    # "impacto económico de la IA generativa",
    # "modelos de IA generativa en investigación médica",
    # "técnicas avanzadas en deep learning 2024",
    # "casos de uso de machine learning en industrias",
    # "Google Gemini vs OpenAI ChatGPT",
    # "Copilot de Microsoft y su evolución",
    # "aplicaciones de deep learning en análisis de datos",
    # "tendencias de inteligencia artificial en salud",
    # "IA generativa y derechos de autor",
    # "mejoras en algoritmos de machine learning",
    # "diferencias clave entre ChatGPT y otros modelos",
    # "uso de inteligencia artificial generativa en redes sociales",
    # "soluciones de IA para automatización industrial",
    # "cómo los modelos de lenguaje afectan la educación",
    # "IA y machine learning en la economía global",
    # "próximos desarrollos en IA generativa",
    # "tecnologías emergentes en deep learning"
    "ciberseguridad con IA", "inteligencia artificial en datos",
    "IA generativa en la creación de imágenes","nuevas herramientas de IA generativa 2024",
    "IA generativa y ética en la creación de contenido","IA generativa en marketing y publicidad",
    "generación de texto automático con IA","cómo funciona la IA generativa en videojuegos",
    "IA generativa en la industria cinematográfica","automatización creativa con IA generativa",
    "IA generativa en la personalización de contenido","retos y beneficios de la IA generativa en educación",
    "IA generativa y derechos de autor","mejores modelos de IA generativa en 2024",
    "IA generativa y el futuro de los empleos creativos","transformación de la producción audiovisual con IA",
    "generación de personajes y diálogos con IA","uso de IA generativa en videojuegos y experiencias interactivas"
]

num_results_per_query = 20  # Número de resultados por consulta
objetivo_documentos = 1200  # Meta de documentos

# Crear la carpeta donde se guardarán los archivos
SAVE_FOLDER = "noticias_guardadas"
os.makedirs(SAVE_FOLDER, exist_ok=True)

# Cargar los nombres de los archivos existentes
nombres_archivos_existentes = set(os.listdir(SAVE_FOLDER))
contador_documentos = len(nombres_archivos_existentes)

# Función para limpiar el nombre del archivo
def limpiar_nombre_archivo(nombre):
    return re.sub(r'[<>:"/\\|?*\x00-\x1F]', '_', nombre)[:50]  # Limita a 50 caracteres para evitar nombres muy largos

def extraer_contenido(url, query_text, result_index):
    global contador_documentos
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Obtener título y contenido
        titulo = soup.title.string if soup.title else f"noticia_{contador_documentos}"
        contenido = " ".join([p.get_text() for p in soup.find_all('p')])
        
        # Limpiar y verificar si el título ya existe
        nombre_archivo = f"{limpiar_nombre_archivo(titulo)}_{contador_documentos}.txt"
        if any(nombre_archivo.startswith(limpiar_nombre_archivo(titulo)) for nombre_archivo in nombres_archivos_existentes):
            print(f"Artículo duplicado: {titulo} (no se guardará)")
            return
        
        # Contar el número de palabras
        num_palabras = len(contenido.split())
        
        # Guardar el contenido en un archivo de texto si tiene al menos 200 palabras
        if num_palabras >= 200:
            nombre_archivo = f"{SAVE_FOLDER}/{limpiar_nombre_archivo(titulo)}_{contador_documentos}.txt"
            with open(nombre_archivo, "w", encoding="utf-8") as file:
                file.write(f"Título: {titulo}\n")
                file.write(f"URL: {url}\n")
                file.write(f"Número de palabras: {num_palabras}\n\n")
                file.write(contenido)

            # Agregar el archivo a la lista de existentes y aumentar el contador
            nombres_archivos_existentes.add(nombre_archivo)
            contador_documentos += 1
            print(f"Artículo guardado: {nombre_archivo} con {num_palabras} palabras (Total guardados: {contador_documentos})")
    except Exception as e:
        print(f"Error al procesar {url}: {e}")

# Realizar múltiples búsquedas hasta alcanzar la meta de documentos
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
