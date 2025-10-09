# -*- coding: utf-8 -*-
"""
Generador de combinaciones (Proveedor 2)
Material × Acabado × Sustrato(ST/RH) × Calibre([9,12,15,18,25,30,36])
Guarda Excel: materiales_texturas_proveedor2.xlsx
"""

from itertools import product
from pathlib import Path
import pandas as pd

# === Configuración general ===
FINISHES = ["Luna", "Amazona", "Terra", "Mate", "Poro", "PRIMAEXTI", "PRIMAFORZA"]
SUSTRATOS = ["ST", "RH"]
CALIBRES = [9, 12, 15, 18, 25, 30, 36]

# === Materiales (lista completa según tu foto) ===
MATERIALES = [
    "Andino","Flormorado","Ika","Kanua","Sapán","Tauarí","Brooklyn Oak","Cocuy","Iguaque","Majuy",
    "Roble Cenizo","Rovere Arena","Rustic Sand","Sikuani","Tambo","Taroa","Tumaco","Ártico",
    "Bacatá","Bareque","Chircal","Candelaria","Creta","Humo","Jayka","Maku","Sukta","Yalaa",
    "Volcánico","Checua","Suesca","Tausa","Tihua","London","Glazé","Malí","Wengue","Cedro"
]

# === Disponibilidad de acabados por material ===
# Rellena la lista con los acabados disponibles de cada material.
# Ejemplos ya puestos (ajusta si algo difiere); el resto queda [] para completar rápido.
AVAIL = {
    "Andino":       ["Amazona"],              # ejemplo
    "Flormorado":   ["Amazona","PRIMAFORZA"], # ejemplo
    "Ika":          ["Amazona","PRIMAFORZA"], # ejemplo
    "Kanua":        ["Amazona","PRIMAFORZA"],              # ejemplo
    "Sapán":        ["Poro"],                       # completa
    "Tauarí":       ["Amazona"],              # ejemplo
    "Brooklyn Oak": ["Amazona"],              # ejemplo
    "Cocuy":        ["Amazona","PRIMAEXTI"],                       # completa
    "Iguaque":      ["Luna"],                       # completa
    "Majuy":        ["Poro", "PRIMAEXTI"],                       # completa
    "Roble Cenizo": ["Amazona","PRIMAEXTI"],       # ejemplo
    "Rovere Arena": ["Amazona","PRIMAEXTI","PRIMAFORZA"],              # ejemplo
    "Rustic Sand":  ["Amazona"],              # ejemplo
    "Sikuani":      ["Poro", "PRIMAEXTI"],                       # completa
    "Tambo":        ["Amazona","PRIMAEXTI"],              # ejemplo
    "Taroa":        ["Amazona"],                       # completa
    "Tumaco":       ["Poro", "PRIMAEXTI"],                       # completa
    "Ártico":       ["Mate", "PRIMAFORZA"],              # ejemplo
    "Bacatá":       ["Amazona"],      # ejemplo
    "Bareque":      ["Terra"],                       # completa
    "Chircal":      ["Amazona"],                       # completa
    "Candelaria":   ["Mate"],                       # completa
    "Creta":        ["Luna"],                       # completa
    "Humo":         ["Luna","PRIMAEXTI","PRIMAFORZA"],              # ejemplo
    "Jayka":        ["Amazona"],                       # completa
    "Maku":         ["Amazona"],                       # completa
    "Sukta":        ["Mate"],                       # completa
    "Yalaa":        ["Amazona"],                       # completa
    "Volcánico":    ["Amazona"],                       # completa
    "Checua":       ["Luna", "PRIMAEXTI"],              # ejemplo
    "Suesca":       ["Luna", "PRIMAEXTI"],              # ejemplo
    "Tausa":        ["Luna", "PRIMAEXTI", "PRIMAFORZA"],              # ejemplo
    "Tihua":        ["Luna", "PRIMAFORZA"],              # ejemplo
    "London":       ["Luna", "PRIMAEXTI"],                       # completa
    "Glazé":        ["Poro"],                       # completa
    "Malí":         ["Poro"],                       # completa
    "Wengue":       ["Poro"],                       # completa
    "Cedro":        ["Poro"],                       # completa
}

# === Validación rápida (evita typos) ===
unknown_materials = set(AVAIL.keys()) - set(MATERIALES)
if unknown_materials:
    raise ValueError(f"Materiales en AVAIL no están en MATERIALES: {sorted(unknown_materials)}")

for mat, acabados in AVAIL.items():
    unknown_finishes = set(acabados) - set(FINISHES)
    if unknown_finishes:
        raise ValueError(f"Acabados inválidos para {mat}: {sorted(unknown_finishes)}. Válidos: {FINISHES}")

# === Generar todas las combinaciones ===
rows = []
for material in MATERIALES:
    acabados = AVAIL.get(material, [])
    for acabado, sustrato, calibre in product(acabados, SUSTRATOS, CALIBRES):
        rows.append({
            "Material": material,
            "Acabado": acabado,
            "Sustrato": sustrato,
            "Calibre": calibre,
            "Costo unidad": ""  # queda vacío para diligenciar
        })

df = pd.DataFrame(rows, columns=["Material", "Acabado", "Sustrato", "Calibre", "Costo unidad"])

# === Guardar a Excel ===
out = Path("materiales_texturas_proveedor2.xlsx")
df.to_excel(out, index=False)
print(f"✅ Archivo creado: {out.resolve()}")
print(f"   Totales -> filas: {len(df)} | materiales con data: {sum(bool(v) for v in AVAIL.values())} / {len(MATERIALES)}")

