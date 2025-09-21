import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import sys
from pathlib import Path

def data_loading(ruta, nombre_archivo, sheet_name=None):
    """
    load_dataframe nos generará un dataframe para un determinado archivo

    Args:
        ruta (str): ruta donde está alojado el archivo.
        nombre_archivo (str): nombre del archivo con los datos.
        sheet_name (list, str o None, optional): hojas (Excel) que contiene el archivo. Defaults to None.

    Returns:
        df: dataframe con los datos que contenía el archivo.
    """
    try:
        # Comprobamos si existe el archivo que queremos cargar
        if not os.path.exists(ruta):
            print(f"El directorio {ruta} no existe")
            return None
        
        # Si la ruta es correcta, generamos la ruta completa
        archivo = os.path.join(ruta, nombre_archivo)

        # Comprobamos que existe
        if not os.path.exists(archivo):
            print(f"El archivo {archivo} no existe.")
            return None
        
        print(f"Cargando datos desde el archivo {archivo}...")
        extension = os.path.splitext(nombre_archivo)[1].lower()  # .lower() para consistencia

        # En caso de ser un archivo .csv
        if extension == '.csv':
            print(f"Se ha generado el dataframe con datos de {archivo}...")
            return pd.read_csv(archivo, index_col=0)

        # Si el archivo es Excel 
        elif extension == '.xlsx':
            # Leer el archivo Excel
            df_excel = pd.read_excel(archivo, sheet_name=sheet_name)
            
            # Si se especificaron hojas específicas o se leyeron todas 
            if isinstance(df_excel, dict):
                # Si hubiera múltiples hojas y se tuvieran que concatenar
                df_dicts = []
                for sn, df in df_excel.items():
                    # Añadimos una columna con el nombre de la hoja de origen
                    df = df.copy()
                    df['sheet_name'] = sn 
                    df_dicts.append(df)
                
                result_df = pd.concat(df_dicts, ignore_index=True)
                print(f"Se han concatenado {len(df_dicts)} hojas en un dataframe de {result_df.shape}")
                return result_df
                
            else:
                # Una sola hoja - devolver directamente
                print(f"Se ha generado el dataframe con datos de {archivo}...")
                return df_excel
                    
        else:
            print(f"Error: formato {extension} no soportado.")
            return None         

    except Exception as e:
        print(f"Error: {e}")
        return None
