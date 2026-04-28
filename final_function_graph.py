import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

def main():
    data_file = 'writeup_data_xy.csv'
    df = pd.read_csv(data_file)
    x_actual = np.arange(len(df))
    y_actual = df['y'].values

    # Final Polynomial Coefficients from previous fit
    # f(x) = (9.46e-06)x^4 + (-2.80e-03)x^3 + (2.71e-01)x^2 + (-8.74e+00)x^1 + (6.02e+01)
    p_coeffs = [9.46e-06, -2.80e-03, 2.71e-01, -8.74e+00, 60.2]
    f_final = np.poly1d(p_coeffs)

    # Extended timeline for projection (next 12 months)
    x_extended = np.arange(0, len(df) + 13)
    y_final = f_final(x_extended)

    # Aesthetics
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(14, 8), dpi=120)
    
    # Plot components
    ax.scatter(x_actual, y_actual, color='#00d4ff', alpha=0.3, s=15, label='Datos Históricos')
    
    # Glow effect for the main line
    ax.plot(x_extended, y_final, color='#ff00ff', linewidth=5, alpha=0.2)
    ax.plot(x_extended, y_final, color='#ff00ff', linewidth=2, label='Función Final f(x)')
    
    # Vertical line for "Today" (end of data)
    today_x = len(df) - 1
    ax.axvline(x=today_x, color='white', linestyle='--', alpha=0.5)
    ax.text(today_x + 1, ax.get_ylim()[1]*0.1, 'Proyección 2026', color='white', rotation=0, fontsize=10)

    # Labels and titles
    ax.set_title('Modelo Matemático Final: Proyección de Crecimiento', fontsize=18, pad=20, fontweight='bold')
    ax.set_xlabel('Meses (desde Julio 2010)', fontsize=12)
    ax.set_ylabel('Cantidad de Writeups', fontsize=12)
    
    # Grid
    ax.grid(True, linestyle=':', alpha=0.3)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    plt.legend(frameon=False, fontsize=11)
    plt.tight_layout()
    
    output_file = 'final_model_viz.png'
    plt.savefig(output_file)
    print(f"Final visualization saved as {output_file}")

if __name__ == "__main__":
    main()
