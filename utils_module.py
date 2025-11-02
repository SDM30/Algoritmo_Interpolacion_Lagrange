"""
Preprocesamiento: organiza los datos para usar en la interpolación
y crea la gráfica de año población
"""
import os
import matplotlib.pyplot as plt 
import math
import pandas as pd

from interpolation_algorithm_module import lagrange_interpolation, interpolate_by_list
from dataclasses import dataclass
from matplotlib.ticker import ScalarFormatter

plt.switch_backend("Agg")

@dataclass
class PopulPoint:
    year: int
    population: float
    interpolated: bool
    
def output_aprox(points):
    """Genera un archivo de Excel con las estimaciones calculadas."""
    estimated = [p for p in points if p.interpolated]
    years_est, population_est = zip(*((p.year, p.population) for p in estimated)) if estimated else ([], [])
    rows = pd.DataFrame({
        "Año": years_est,
        "Población": population_est
    })
    out_file = pd.DataFrame(rows)
    out_file.to_excel("out/poblacion.xlsx", index= False, sheet_name="Población estimada")
    
    
    
def merge_interpolation_points(x_i, population_i, x, population_aprox):
    """Combina los datos originales con las aproximaciones manteniendo el orden cronológico."""
    points = [PopulPoint(year, population, False) for year, population in zip(x_i, population_i)]
    known_years = {point.year for point in points}
    for year, population in zip(x, population_aprox):
        if year not in known_years:
            points.append(PopulPoint(year, population, True))
            known_years.add(year)
    points.sort(key=lambda point: point.year)
    return points

def program_menu(data):
    """Controla la interacción con el usuario para seleccionar los valores a interpolar."""
    years = data["Año"].tolist()
    populations = data["Población"].tolist()
    
    x_i = []
    population_i = []
    x_opt = []
    for i in range(len(years)):
        if not math.isnan(populations[i]):
            x_i.append(years[i])
            population_i.append(populations[i])
        else:
            x_opt.append(years[i])

            
    while True:
        print("\n=== Algoritmo de Interpolación ===")
        for idx, year in enumerate(x_opt, start=1):
            print(f"{idx}. Año {year}")
        print(f"{len(x_opt) + 1}. Estimar para todos los datos faltantes.")
        print(f"{len(x_opt) + 2}. Salir.")

        try:
            usr_in = int(input("\nSeleccione un opción: "))
        except ValueError:
            print("Ingrese una opción valida.")
            continue

        if usr_in == len(x_opt) + 2:
            print("Saliendo del programa...")
            break

        elif usr_in == len(x_opt) + 1:
            print("Estimando para los años faltantes...")
            population_aprox = interpolate_by_list(x_i,population_i,x_opt)
            points = merge_interpolation_points(x_i,population_i,x_opt,population_aprox)
            plot_aprox(points)
            output_aprox(points)
            print("""En la carpeta out/ se ha creado un archivo con las estimaciones para cada uno de los años faltantes y una grafica año-población""")
            input("Presiona Enter para continuar…")
            

        elif 1 <= usr_in <= len(x_opt):
            selected_year = x_opt[usr_in - 1]
            print(f"Año seleccionado: {selected_year}")
            population_est = lagrange_interpolation(x_i, population_i, selected_year)
            print(f"Población estimada: {population_est}")
            input("Presiona Enter para continuar…")
            

        else:
            print("Ingrese una opción valida.")        

def plot_points(ax, known_points, estimated_points):
    """Traza los puntos conocidos e interpolados sobre el eje recibido."""
    years_known, population_known = zip(*((p.year, p.population) for p in known_points)) if known_points else ([], [])
    years_est, population_est = zip(*((p.year, p.population) for p in estimated_points)) if estimated_points else ([], [])
    combined = sorted(known_points + estimated_points, key=lambda p: p.year)
    if combined:
        years_all, pops_all = zip(*((p.year, p.population) for p in combined))
        ax.plot(years_all, pops_all, "-", color="blue", linewidth=2, alpha=0.6)
    if years_known:
        ax.plot(years_known, population_known, "o", label="Datos")
    if years_est:
        ax.plot(years_est, population_est, "s", color="orange", label="Datos estimados")

def plot_aprox(points):
    """Construye las gráficas comparativas y guarda la imagen resultante en disco."""
    known = [p for p in points if not p.interpolated]
    estimated = [p for p in points if p.interpolated]

    fig, (ax_left, ax_right) = plt.subplots(
        1, 2, figsize=(10, 4), sharey=False, constrained_layout=True
    )

    plot_points(ax_left, known, estimated)
    ax_left.set_title("Con outlier")
    ax_left.set_xlabel("Año")
    ax_left.set_ylabel("Población")
    ax_left.legend()

    threshold = -1e9
    filtered_known = [p for p in known if p.population > threshold]
    filtered_estimated = [p for p in estimated if p.population > threshold]
    plot_points(ax_right, filtered_known, filtered_estimated) 
    ax_right.set_title("Sin outlier")
    ax_right.set_xlabel("Año")
    ax_right.legend()
        
    formatter = ScalarFormatter(useOffset=False)
    formatter.set_scientific(False)

    ax_left.yaxis.set_major_formatter(formatter)
    ax_right.yaxis.set_major_formatter(formatter)

    plt.suptitle("Año-Población")
    output_dir = "out"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "evolucion_poblacional.png")
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
