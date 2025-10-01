import os
import win32com.client    

class test():
    def load_inventor_model(self, model_path):
        print(f"Cargando modelo de Inventor desde: {model_path}")

            # === Conexion con Inventor ===

        self.inventor = win32com.client.Dispatch("Inventor.Application")
        self.inventor.Visible = False  # No mostrar la ventana de Inventor inicialmente

        # === Apertura Skeleton Part ===

        skeleton_path = f"{model_path}\\Skeleton Part.ipt"

        if os.path.exists(skeleton_path):
            print(f"✅ Skeleteon abierto")
            skeleton_doc = self.inventor.Documents.Open(skeleton_path)
        else:
            print(f"❌ No se encontró el archivo Skeleton del modelo")
            return
        
        params = skeleton_doc.ComponentDefinition.Parameters
        

        print("Parámetros del modelo:")
        for param in params:
            print(f"- {param.Name}: {param.Value} {param.Units}")

        # === Abrir Ensamble CUERPO ===
        asm_path = f"{model_path}\\ENSAMBLE CUERPO.iam"
        if os.path.exists(asm_path):
            asmDoc = self.inventor.Documents.Open(asm_path)
            print("✅ Ensamble CUERPO abierto")
        else:
            print("❌ No se encontró el archivo de ensamble")
            return

        # === Mostrar Inventor y traerlo al frente ===
        self.inventor.Visible = True
        #self.inventor.ActiveWindow.Activate()

        # Guardar y cerrar un documento
        # skeleton_doc.Close(False)  # True = guardar cambios, False = no guardar

        # # Cerrar Inventor completo
        # self.inventor.Quit()
        # self.inventor = None
        
prueba = test()
prueba.load_inventor_model(f"C:\\Users\\autom\\OneDrive\\Carpintería\\Modelos Produccion\\PRUEBA\\COMODA 3 CAJONES")
            
        