import matplotlib.pyplot as plt
import numpy as np

# Función para graficar la fuerza cortante real por piso
# Esta función toma como entrada los pisos y la fuerza cortante real y genera un gráfico de barras
def graficar_fuerza_cortante_real(pisos, Vreal):
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.barh(pisos, Vreal, color='darkred', edgecolor='black')
    ax.set_title('Fuerza Cortante Real por Piso', fontsize=14, fontweight='bold')
    ax.set_xlabel('Fuerza (ton)')
    ax.set_ylabel('Piso')
    ax.invert_yaxis()
    ax.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    return fig

# Función para graficar las combinaciones modales
# Esta función toma como entrada los pisos y las fuerzas cortantes calculadas por diferentes métodos de combinación modal
def graficar_combinaciones_modales(pisos, Vsum_abs, Vrcsc, Vmc_h, Vreal):
    fig, axs = plt.subplots(2, 2, figsize=(12, 12))
    colores = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']  # Azul, Naranja, Verde, Rojo
    data_titles = [('Vsum_abs', Vsum_abs), ('Vrcsc', Vrcsc), ('Vmc_h', Vmc_h), ('Vreal', Vreal)]

    for ax, (title, data), color in zip(axs.flat, data_titles, colores):
        ax.barh(pisos, data, color=color, edgecolor='black', linewidth=1.5)
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.set_xlabel('Cortante (ton)', fontsize=12)
        ax.set_ylabel('Piso', fontsize=12)
        ax.invert_yaxis()
        ax.grid(True, linestyle='--', alpha=0.6)

    plt.tight_layout()
    return fig
