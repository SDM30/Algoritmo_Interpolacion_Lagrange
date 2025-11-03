# Instrucciones de Ejecución - Windows

## Ejecutar código fuente

1. Crear entorno virtual:

   ```bash
   python -m venv venv
   ```

2. Activar el entorno virtual:

   ```bash
   venv\Scripts\activate.bat
   ```

3. Instalar dependencias:

   ```bash
   pip install -r requirements.txt
   ```

4. Ejecutar el programa:

   ```bash
   python main.py
   ```

## Crear ejecutable

1. Crear entorno virtual:

   ```bash
   python -m venv venv
   ```

2. Activar el entorno virtual:

   ```bash
   venv\Scripts\activate.bat
   ```

3. Instalar dependencias:

   ```bash
   pip install -r requirements.txt
   ```

4. Instalar PyInstaller (si no está incluido en `requirements.txt`):

   ```bash
   pip install pyinstaller
   ```

5. Generar el ejecutable con PyInstaller:

   ```bash
   pyinstaller --onedir --add-data "in\[2025-3] ANUM - Proyecto Final - Estudiantes.xlsx;in" --distpath . --name runnable_program main.py
   ```

6. Ejecutar con parámetros (OPCIONAL):

    Si se ejecuta sin parametros se toma el país 20, el asignado al autor del programa

   ```bash
   .\dist\main.exe -f ".\in\[2025-3] ANUM - Proyecto Final - Estudiantes.xlsx" "País 16"
   ```

7. Ejecutar sin parámetros:

   ```
   Explorador de archivos -> Algoritmo_Interpolacion_Lagrange -> dist -> main.exe
   ```
