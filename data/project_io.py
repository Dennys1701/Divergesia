
import json
from typing import List
from data.models import Paleta

def guardar_paleta_a_archivo(paleta: Paleta, path: str) -> None:
    
    data = paleta.to_dict()
    # Registrar la ruta en el propio objeto para futuros guardados automáticos
    paleta.archivo_guardado = path
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def cargar_paleta_desde_archivo(path: str) -> Paleta:
    
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    paleta = Paleta.from_dict(data)
    paleta.archivo_guardado = path
    return paleta

def guardar_coleccion_paletas(paletas: List[Paleta], path: str) -> None:
    
    data_list = []
    for p in paletas:
        data = p.to_dict()
        # No modificar p.archivo_guardado aquí, pues puede no corresponder a este archivo de colección
        data_list.append(data)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data_list, f, ensure_ascii=False, indent=2)

def cargar_coleccion_paletas(path: str) -> List[Paleta]:
   
    with open(path, 'r', encoding='utf-8') as f:
        data_list = json.load(f)
    paletas = []
    for data in data_list:
        pal = Paleta.from_dict(data)
        # No asignamos archivo_guardado individual aquí salvo que se decida
        paletas.append(pal)
    return paletas
