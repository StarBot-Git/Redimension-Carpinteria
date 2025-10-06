import os
from pathlib import Path
import pythoncom
import win32com.client as win32

HEADERS_PROPS = ["Pieza", "Material", "Material Canto", "A1", "A2", "L1", "L2"]

def faces_by_tag(doc, tag: str):
    """Devuelve lista de entidades (faces/proxies) con iLogicEntityName == tag en un PartDocument."""
    am = doc.AttributeManager
    try:
        objs = am.FindObjects("iLogicEntityNameSet", "iLogicEntityName", tag)
        return [o for o in objs]  # puede ser vacío
    except:
        # Fallback: buscar por set+attr y filtrar por value
        try:
            objs = am.FindObjects("iLogicEntityNameSet", "iLogicEntityName")
        except:
            return []
        res = []
        for o in objs:
            try:
                val = o.AttributeSets.Item("iLogicEntityNameSet").Item("iLogicEntityName").Value
                if str(val) == tag:
                    res.append(o)
            except:
                pass
        return res

def collect_part_paths(asm_doc):
    """Recorre el ensamble (recursivo) y devuelve rutas únicas de todas las piezas .ipt."""
    seen = set()
    def walk(doc):
        try:
            refs = doc.ReferencedDocuments
        except:
            refs = []
        for r in refs:
            try:
                f = r.FullFileName
            except:
                continue
            if not f:
                continue
            ext = Path(f).suffix.lower()
            if ext == ".ipt":
                seen.add(f)
            elif ext == ".iam":
                walk(r)
    walk(asm_doc)
    return sorted(seen)

def extract_props_from_part(doc):
    """Extrae Material, Material Canto y banderas A1/A2/L1/L2 de un PartDocument ya abierto."""
    # Material
    try:
        material = doc.ComponentDefinition.Material.Name
    except:
        material = ""

    # User Defined Property: "Material Canto"
    mat_canto = ""
    try:
        udp = doc.PropertySets.Item("Inventor User Defined Properties")
        mat_canto = udp.Item("Material Canto").Value

    except:
        pass

    # Tags presentes
    tags = ["A1", "A2", "L1", "L2"]
    presentes = {t: (len(faces_by_tag(doc, t)) > 0) for t in tags}

    pieza = Path(doc.FullFileName).stem if getattr(doc, "FullFileName", "") else doc.DisplayName

    return {
        "Pieza": pieza,
        "Material": material,
        "Material Canto": mat_canto or "No especificado",
        "A1": 1 if presentes["A1"] else 0,
        "A2": 1 if presentes["A2"] else 0,
        "L1": 1 if presentes["L1"] else 0,
        "L2": 1 if presentes["L2"] else 0,
    }

def extract_properties_table_from_assembly(asm_path: str) -> list[dict]:
    """
    Abre el .iam (si no está abierto), recorre todas las .ipt referenciadas y
    devuelve list[dict] con HEADERS_PROPS.
    """
    pythoncom.CoInitialize()
    inv = win32.Dispatch("Inventor.Application")
    # No forzamos visible; déjalo como tengas tu instancia principal
    # inv.Visible = False

    docs = inv.Documents

    # Abrir assembly si no está abierto
    asm_doc = None
    opened_asm_here = False
    for i in range(1, docs.Count + 1):
        d = docs.Item(i)
        if getattr(d, "FullFileName", "").lower() == asm_path.lower():
            asm_doc = d
            break
    if asm_doc is None:
        asm_doc = docs.Open(asm_path)
        opened_asm_here = True

    # Recolectar rutas de piezas
    part_paths = collect_part_paths(asm_doc)

    rows = []
    opened_here = []  # docs que abrimos aquí para luego cerrarlos

    try:
        for p in part_paths:
            # Buscar si la pieza ya está abierta
            part_doc = None
            for i in range(1, docs.Count + 1):
                d = docs.Item(i)
                if getattr(d, "FullFileName", "").lower() == p.lower():
                    part_doc = d
                    break
            if part_doc is None:
                part_doc = docs.Open(p)
                opened_here.append(part_doc)

            rows.append(extract_props_from_part(part_doc))
    finally:
        # Cerrar piezas que abrimos aquí
        for d in opened_here:
            try:
                d.Close(True)  # True = save changes; usa False si no quieres guardar
            except:
                pass
        # Cerrar ensamblado si lo abrimos aquí
        if opened_asm_here:
            try:
                asm_doc.Close(True)
            except:
                pass

    return rows

# ===== Ejemplo de uso =====
if __name__ == "__main__":
    asm_path = r"C:\Users\autom\OneDrive\Carpintería\Modelos Produccion\PRUEBA\Escritorios Oficina\Escritorio oficina.iam"
    data = extract_properties_table_from_assembly(asm_path)
    # `data` es list[dict] con keys HEADERS_PROPS, listo para tu tabla
    for row in data:
        print(row)

