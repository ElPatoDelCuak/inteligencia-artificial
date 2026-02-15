import os
import pandas as pd
import requests
import time

CHARACTERS_API = "https://rickandmortyapi.com/api/character"

def fetch_all_characters():
    results = []
    url = CHARACTERS_API
    while url:
        resp = requests.get(url)
        resp.raise_for_status()
        data = resp.json()
        results.extend(data.get('results', []))
        url = data.get('info', {}).get('next')
        time.sleep(0.1)
    return results


def characters_to_dataframe(characters, explode_episodes=True):
    if not characters:
        return pd.DataFrame(columns=['id', 'name', 'status', 'species', 'gender', 'episode'])

    df = pd.DataFrame(characters)

    cols = ['id', 'name', 'status', 'species', 'gender', 'episode']
    for c in cols:
        if c not in df.columns:
            df[c] = pd.NA

    df = df[cols].copy()

    if explode_episodes:
        df = df.explode('episode').reset_index(drop=True)

    return df


if __name__ == '__main__':
    characters = fetch_all_characters()

    df = characters_to_dataframe(characters, explode_episodes=True)

    def set_id_as_index(df, inplace=True):
        if 'id' not in df.columns and 'id' not in df.index:
            raise KeyError("No se encontró la columna 'id'")
        if inplace:
            df.set_index('id', inplace=True)
            return df
        return df.set_index('id')

    set_id_as_index(df, inplace=True)

    base_dir = os.path.dirname(__file__)
    data_dir = os.path.join(base_dir, "..", "data")
    os.makedirs(data_dir, exist_ok=True)
    output_path = os.path.join(data_dir, "characters_exploded.csv")
    df.to_csv(output_path, encoding="utf-8")

    print(f"CSV guardado en {output_path}")
