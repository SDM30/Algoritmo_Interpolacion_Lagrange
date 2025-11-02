import sys
import pandas as pd

from utils_module import program_menu, plot_aprox

def proccess_user_input():
    # TODO
    # Recive .xslx file and the sheet
    name = ""
    src_data = None
    years = []
    populations = []
    valid = False
    # default to Pais 20 and original file if not specified
    default_name = "in/[2025-3] ANUM - Proyecto Final - Estudiantes.xlsx"
    default_sheet = "País 20"

    if len(sys.argv) == 1:
        name = default_name
        sheet = default_sheet
        src_data = pd.read_excel(name, header= 1,sheet_name= sheet)
        valid = True
            
    elif sys.argv[1] == "-f" and len(sys.argv) == 4:
        name = sys.argv[2]
        sheet = sys.argv[3]
        src_data = pd.read_excel(name, header= 1,sheet_name= sheet)
        valid = True
        #print(src_data.head())
        
    elif sys.argv[1] == "-f" and len(sys.argv) == 3:
        name = sys.argv[2]
        src_data = pd.read_excel(name, header= 1)
        valid = True
        #TODO: Agregar error de archivo no encontrado 
        #print(src_data.head())
        
    else:
        # Ayuda
        print("""Formato de Entrada: El programa recibe archivos en formato .xlsx
        1. Para una hoja especifica los argumentos son:
            -f <archivo.xlsx> <Nombre de la hoja>
            Si no es necesario especificarla omita el último argumento """)
        return
    
    if valid:
        program_menu(src_data)
    
    # call interpolation algorithm
    # print result and crate plot
    
    print(sys.argv)
    # lagrangeInterpolation(year, population, 1990)
    pass


if __name__ == "__main__":
    proccess_user_input()