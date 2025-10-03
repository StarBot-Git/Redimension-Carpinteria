import win32com.client as win32
import pythoncom

inv = win32.Dispatch("Inventor.Application")
inv.Visible = False  # o True si quieres ver

doc = inv.Documents.Open(r"C:\Users\autom\OneDrive\Carpintería\Modelos Produccion\PRUEBA\Escritorios Oficina\tapa cajon.ipt")  # PartDocument
prop_sets = doc.PropertySets
udp = doc.PropertySets.Item("Inventor User Defined Properties")
try:
    material_canto = udp.Item("Material Canto").Value
except:
    material_canto = ""

am = doc.AttributeManager

def faces_by_tag(tag: str):
    """Devuelve lista de entidades (faces/proxies) con iLogicEntityName == tag"""
    try:
        # Muchos builds soportan filtrar por valor directamente (set, attr, value)
        objs = am.FindObjects("iLogicEntityNameSet", "iLogicEntityName", tag)
        return [o for o in objs]  # puede ser vacío
    except:
        # Fallback: buscar por set+attr y filtrar a mano por value
        objs = am.FindObjects("iLogicEntityNameSet", "iLogicEntityName")
        res = []
        for o in objs:
            try:
                val = o.AttributeSets.Item("iLogicEntityNameSet").Item("iLogicEntityName").Value
                if str(val) == tag:
                    res.append(o)
            except:
                pass
        return res

presentes = {name: len(faces_by_tag(name)) > 0 for name in ["L1", "L2", "A1", "A2"]}

mat_name  = doc.ComponentDefinition.Material.Name

print("Material Canto:", material_canto)
print("Cantos marcados:", presentes)
print("Material:", mat_name)


# for body in comp_def.SurfaceBodies:
#     for face in body.Faces:
#         a_sets = face.AttributeSets
#         if a_sets.Count == 0:
#             #print("  (sin AttributeSets)")
#             continue
#         for aset in a_sets:
#             #print(f"  AttributeSet: {aset.Name}")
#             for att in aset:
#                 try:
#                     print(f"    - {att.Name} = {att.Value}")
#                 except:
#                     #print(f"    - {att.Name} (no imprimible)")
#                     pass

# # Recorre todos los sólidos y caras
# for body in comp_def.SurfaceBodies:
#     for face in body.Faces:
#         k = face_key(face)
#         print("\n--- FACE:", k, "---")
#         a_sets = face.AttributeSets
#         if a_sets.Count == 0:
#             print("  (sin AttributeSets)")
#             continue

#         for aset in a_sets:
#             print(f"  AttributeSet: {aset.Name}")
#             for att in aset:
#                 # Cada atributo tendrá .Name y .Value
#                 try:
#                     print(f"    - {att.Name} = {att.Value}")
#                 except:
#                     print(f"    - {att.Name} (tipo no imprimible)")

doc.Close(True)
inv.Quit()