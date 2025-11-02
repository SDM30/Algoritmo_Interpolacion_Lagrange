"""
Preprocesamiento: organiza los datos para usar en la interpolación
y crea la gráfica de año población
"""
import os
import matplotlib.pyplot as plt 
import math
from interpolation_algorithm_module import lagrange_interpolation, interpolate_by_list
from dataclasses import dataclass

plt.switch_backend("Agg")

@dataclass
class PopulPoint:
    year: int
    population: float
    interpolated: bool
    
def merge_interpolation_points(x_i, population_i, x, population_aprox):
    points = [PopulPoint(year, population, False) for year, population in zip(x_i, population_i)]
    known_years = {point.year for point in points}
    for year, population in zip(x, population_aprox):
        if year not in known_years:
            points.append(PopulPoint(year, population, True))
            known_years.add(year)
    points.sort(key=lambda point: point.year)
    return points

def program_menu(data):
    years = data["Año"].tolist()
    populations = data["Población"].tolist()
    print(years)
    print(populations)
    
    # Find years with unknown population
    x_i = []
    population_i = []
    x_opt = []
    for i in range(len(years)):
        if not math.isnan(populations[i]):
            x_i.append(years[i])
            population_i.append(populations[i])
        else:
            x_opt.append(years[i])

            
    # Show a menu to pick only one unknown year or all
    while True:
        print("\n=== Missing Population Data Menu ===")
        for idx, year in enumerate(x_opt, start=1):
            print(f"{idx}. Year {year}")
        print(f"{len(x_opt) + 1}. Fill ALL missing years")
        print(f"{len(x_opt) + 2}. Exit")

        try:
            usr_in = int(input("\nSelect an option: "))
        except ValueError:
            print("Please enter a valid number.")
            continue

        if usr_in == len(x_opt) + 2:
            print("Exiting menu...")
            break

        elif usr_in == len(x_opt) + 1:
            print("Filling all missing years...")
            print(interpolate_by_list(x_i,population_i,x_opt))
            population_aprox = interpolate_by_list(x_i,population_i,x_opt)
            points = merge_interpolation_points(x_i,population_i,x_opt,population_aprox)
            plot_aprox(points)
            # Call your interpolation or calculation function here
            # e.g. interpolate_all(x_i, population_i, x_opt)
            break

        elif 1 <= usr_in <= len(x_opt):
            selected_year = x_opt[usr_in - 1]
            print(f"→ Selected year: {selected_year}")
            print(lagrange_interpolation(x_i, population_i, selected_year))
            # You could process only this one year here
            # e.g. interpolate_single(selected_year, x_i, population_i)
            break

        else:
            print("Invalid option. Try again.")        

def plot_points(ax, known_points, estimated_points):
    years_known, pops_known = zip(*((p.year, p.population) for p in known_points)) if known_points else ([], [])
    years_est, pops_est = zip(*((p.year, p.population) for p in estimated_points)) if estimated_points else ([], [])
    combined = sorted(known_points + estimated_points, key=lambda p: p.year)
    if combined:
        years_all, pops_all = zip(*((p.year, p.population) for p in combined))
        ax.plot(years_all, pops_all, "-", color="blue", linewidth=1, alpha=0.6)
    if years_known:
        ax.plot(years_known, pops_known, "o", label="Datos")
    if years_est:
        ax.plot(years_est, pops_est, "s", color="orange", label="Interpolados")

def plot_aprox(points):
    known = [p for p in points if not p.interpolated]
    estimated = [p for p in points if p.interpolated]

    fig, (ax_left, ax_right) = plt.subplots(
        1, 2, figsize=(10, 4), sharey=False, constrained_layout=True
    )

    # Datos completos
    plot_points(ax_left, known, estimated)
    ax_left.set_title("Con outlier")
    ax_left.set_xlabel("Año")
    ax_left.set_ylabel("Población")
    ax_left.legend()

    # Filtra el outlier (ajusta el umbral a tus datos)
    threshold = -1e9
    filtered_known = [p for p in known if p.population > threshold]
    filtered_estimated = [p for p in estimated if p.population > threshold]
    plot_points(ax_right, filtered_known, filtered_estimated) 
    ax_right.set_title("Sin outlier")
    ax_right.set_xlabel("Año")
    ax_right.legend()

    plt.suptitle("Evolución poblacional")
    output_dir = "out"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "evolucion_poblacional.png")
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
