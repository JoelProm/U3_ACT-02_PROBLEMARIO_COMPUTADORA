import math
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def programa_esfuerzos():
    # --- A. INTRODUCCIÓN ---
    print("="*80)
    print("ALGORITMO PARA EL ANÁLISIS DE ESFUERZO NORMAL POR FLEXIÓN BIAXIAL")
    print("="*80)
    print("DESCRIPCIÓN:")
    print("Este algoritmo calcula el esfuerzo normal (σ) en puntos críticos y genera")
    print("un reporte visual con diagrama y tabla de resultados.")
    print("Fórmula: σ = -(Mx * y / Ix) + (My * x / Iy)")
    print("="*80)

    # --- B. SELECCIÓN DE CASO ---
    opcion = input("\n¿Qué caso de los tres quiere analizar (a, b o c)?: ").lower()

    # Cargas constantes según el problemario
    Mx = 100 
    My = 50  

    # Preparar la figura con dos columnas: una para el dibujo y otra para la tabla
    fig, (ax, ax_table) = plt.subplots(1, 2, figsize=(15, 8), gridspec_kw={'width_ratios': [1.2, 1]})
    seccion_path = []
    table_data = [] # Para almacenar los resultados de la tabla

    if opcion == 'a':
        print("\n--- CONFIGURACIÓN: CASO A (SECCIÓN EN L) ---")
        b = float(input("Ingrese el ancho b (m): "))
        h = float(input("Ingrese el alto h (m): "))
        t = float(input("Ingrese el espesor t (m): "))

        area = (t * h) + ((b - t) * t)
        xc = ((t * h * (t / 2)) + ((b - t) * t * (t + (b - t) / 2))) / area
        yc = ((t * h * (h / 2)) + ((b - t) * t * (t / 2))) / area
        ix = ((t * h**3) / 12 + (t * h) * (h / 2 - yc)**2) + (((b - t) * t**3) / 12 + ((b - t) * t) * (t / 2 - yc)**2)
        iy = ((h * t**3) / 12 + (t * h) * (t / 2 - xc)**2) + ((t * (b - t)**3) / 12 + ((b - t) * t) * (t + (b - t) / 2 - xc)**2)

        puntos = {
            'a': (-xc, h-yc), 'b': (t-xc, h-yc), 'c': (-xc, t-yc),
            'd': (t-xc, t-yc), 'e': (t-xc, t-yc), 'f': (t-xc, -yc),
            'g': (b-xc, t-yc), 'h': (-xc, -yc), 'i': (t-xc, -yc), 'j': (b-xc, -yc)
        }
        seccion_path = [[-xc, -yc], [b-xc, -yc], [b-xc, t-yc], [t-xc, t-yc], [t-xc, h-yc], [-xc, h-yc], [-xc, -yc]]

    elif opcion == 'b':
        print("\n--- CONFIGURACIÓN: CASO B (SECCIÓN EN I) ---")
        b = float(input("Ingrese el ancho b (m): "))
        h = float(input("Ingrese el alto h (m): "))
        t = float(input("Ingrese el espesor t (m): "))
        xc, yc = b / 2, h / 2
        ix = (b * h**3 / 12) - ((b - t) * (h - 2 * t)**3 / 12)
        iy = (2 * (t * b**3 / 12)) + ((h - 2 * t) * t**3 / 12)

        puntos = {
            'a': (-b/2, h/2), 'b': (0, h/2), 'c': (b/2, h/2),
            'd': (-b/2, h/2-t), 'e': (-t/2, h/2-t), 'f': (t/2, h/2-t),
            'g': (b/2, h/2-t), 'h': (-t/2, 0), 'i': (t/2, 0),
            'j': (-b/2, -h/2+t), 'k': (-t/2, -h/2+t), 'l': (t/2, -h/2+t),
            'm': (b/2, -h/2+t), 'n': (-b/2, -h/2), 'o': (b/2, -h/2)
        }
        seccion_path = [[-b/2, h/2], [b/2, h/2], [b/2, h/2-t], [t/2, h/2-t], [t/2, -h/2+t], [b/2, -h/2+t], [b/2, -h/2], [-b/2, -h/2], [-b/2, -h/2+t], [-t/2, -h/2+t], [-t/2, h/2-t], [-b/2, h/2-t], [-b/2, h/2]]

    elif opcion == 'c':
        print("\n--- CONFIGURACIÓN: CASO C (CIRCULAR HUECA) ---")
        r_int = float(input("Ingrese el radio interior (m): "))
        t = float(input("Ingrese el espesor t (m): "))
        r_ext = r_int + t
        ix = iy = (math.pi / 4) * (r_ext**4 - r_int**4)
        nombres = ['a','b','c','d','e','f','g','h']
        angs = [90, 90, 180, 180, 0, 0, 270, 270]
        radios = [r_ext, r_int, r_ext, r_int, r_int, r_ext, r_int, r_ext]
        puntos = {n: (r * math.cos(math.radians(a)), r * math.sin(math.radians(a))) for n, a, r in zip(nombres, angs, radios)}
        ax.add_patch(patches.Circle((0, 0), r_ext, color='green', alpha=0.3, fill=True))
        ax.add_patch(patches.Circle((0, 0), r_int, color='white', fill=True))

    else:
        print("Caso no reconocido.")
        return

    # --- C. CÁLCULO Y RECOLECCIÓN DE DATOS PARA LA TABLA ---
    for p, (x, y) in puntos.items():
        sigma = -(Mx * y / ix) + (My * x / iy)
        estado = "TENSIÓN" if sigma > 0 else "COMPRESIÓN"
        color_punto = 'blue' if sigma > 0 else 'red'
        
        # Guardar para la tabla visual
        table_data.append([p, f"{sigma:.2f}", estado])
        
        # Graficar en el diagrama
        ax.scatter(x, y, color=color_punto, s=100, zorder=5)
        ax.text(x, y, f' {p}', fontsize=10, fontweight='bold')

    # --- D. DIBUJO DE LA SECCIÓN Y EJES ---
    if opcion != 'c':
        ax.add_patch(patches.Polygon(seccion_path, closed=True, color='green', alpha=0.2, ec='black', lw=2))

    ax.axhline(0, color='black', linestyle='--', linewidth=0.8)
    ax.axvline(0, color='black', linestyle='--', linewidth=0.8)
    
    # Flechas de momentos (representativas)
    ax.annotate('', xy=(0.05, 0), xytext=(0, 0), arrowprops=dict(facecolor='red', width=2, headwidth=8))
    ax.text(0.05, 0.005, 'Mx', color='red', fontsize=12, fontweight='bold')
    ax.annotate('', xy=(0, 0.05), xytext=(0, 0), arrowprops=dict(facecolor='red', width=2, headwidth=8))
    ax.text(0.005, 0.05, 'My', color='red', fontsize=12, fontweight='bold')

    ax.set_aspect('equal')
    ax.set_title(f"DIAGRAMA DE ESFUERZOS - CASO {opcion.upper()}\n(Azul: Tensión | Rojo: Compresión)", fontsize=14)
    ax.grid(True, linestyle=':', alpha=0.5)

    # --- E. GENERACIÓN DE LA TABLA EN EL GRÁFICO ---
    ax_table.axis('off') # Ocultar ejes de la segunda columna
    column_labels = ["Punto", "Esfuerzo (Pa)", "Estado"]
    
    # Crear la tabla
    tabla_visual = ax_table.table(
        cellText=table_data, 
        colLabels=column_labels, 
        loc='center', 
        cellLoc='center'
    )
    
    # Estilo de la tabla
    tabla_visual.auto_set_font_size(False)
    tabla_visual.set_fontsize(11)
    tabla_visual.scale(1.1, 1.8) # Ajustar tamaño de celdas

    # Colorear las celdas de la columna 'Estado' para mayor claridad
    for i in range(len(table_data)):
        estado_val = table_data[i][2]
        color_celda = '#D6EAF8' if estado_val == "TENSIÓN" else '#FADBD8'
        tabla_visual[(i + 1, 2)].set_facecolor(color_celda)

    plt.tight_layout()
    print("\nDiagrama y Tabla generados exitosamente.")
    plt.show()

if __name__ == "__main__":
    programa_esfuerzos()