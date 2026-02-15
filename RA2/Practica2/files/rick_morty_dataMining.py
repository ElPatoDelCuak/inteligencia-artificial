import os
import pandas as pd
import requests

CHARACTERS_API = "https://rickandmortyapi.com/api/character"

base_dir = os.path.dirname(__file__)
data_dir = os.path.join(base_dir, "..", "data")
csv_path = os.path.join(data_dir, "characters_exploded.csv")

df = pd.read_csv(csv_path, encoding='utf-8')

characters = ["Mel Gibson", "Johnny Depp", "Pickle Rick"]

output_folder = os.path.join(data_dir, "images")
os.makedirs(output_folder, exist_ok=True)

def get_character_image_from_api(character_name):
    """Obtiene la URL de la imagen de un personaje desde la API"""
    try:
        resp = requests.get(f"{CHARACTERS_API}/?name={character_name}")
        resp.raise_for_status()
        data = resp.json()
        if data.get('results'):
            return data['results'][0].get('image')
    except Exception as e:
        print(f"Error al buscar {character_name} en la API: {e}")
    return None

for character in characters:
    character_df = df[df['name'] == character]

    if not character_df.empty:
        # Obtener la URL de imagen desde la API
        image_url = get_character_image_from_api(character)

        if image_url:
            resp = requests.get(image_url)
            if resp.status_code == 200:
                file_path = os.path.join(output_folder, f"{character.replace(' ', '_')}.jpg")
                with open(file_path, 'wb') as f:
                    f.write(resp.content)
                print(f"Imagen de {character} guardada en {file_path}")
            else:
                print(f"No se pudo descargar la imagen de {character}")
        else:
            print(f"No se encontró imagen para {character} en la API")
    else:
        print(f"{character} no se encuentra en el CSV")

print("")
print("======= Imagenes descargadas =======")
print("")

characters2 = ["Birdperson", "Squanchy", "Mr. Meeseeks"]

for character in characters2:

    appearances = df[df['name'] == character]

    count = appearances.shape[0]
    
    print(f"{character} ha aparecido {count} veces en la serie.")