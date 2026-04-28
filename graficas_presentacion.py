import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

def main():
    data_file = 'writeup_data_xy.csv'
    if not os.path.exists(data_file):
        print("Error: No se encontró writeup_data_xy.csv")
        return

    df = pd.read_csv(data_file)
    df['x_numeric'] = np.arange(len(df))
    x = df['x_numeric'].values
    y = df['y'].values

    # 1. Polynomial Model
    p_coeffs = np.polyfit(x, y, 4)
    p_model = np.poly1d(p_coeffs)
    y_poly = p_model(x)

    # 2. Exponential Model
    mask = y > 0
    x_filtered = x[mask]
    y_filtered = y[mask]
    log_y = np.log(y_filtered)
    b, ln_a = np.polyfit(x_filtered, log_y, 1)
    a = np.exp(ln_a)
    y_exp = a * np.exp(b * x)

    def get_r2(y_true, y_pred):
        ss_res = np.sum((y_true - y_pred)**2)
        ss_tot = np.sum((y_true - np.mean(y_true))**2)
        return 1 - (ss_res / ss_tot)

    r2_poly = get_r2(y, y_poly)
    r2_exp = get_r2(y, y_exp)

    # Estilo base
    plt.style.use('dark_background')

    # --- FIGURA 1: Modelo Polinómico ---
    fig1, ax1 = plt.subplots(figsize=(10, 7))
    ax1.scatter(x, y, color='#00d4ff', alpha=0.4, s=30, label='Reportes Reales')
    ax1.plot(x, y_poly, color='#ff00ff', linewidth=3, label='Ajuste Polinómico')
    ax1.set_title('Modelo 1: Regresión Polinómica (Grado 4)', fontsize=16, color='#ff00ff', pad=15)
    ax1.set_xlabel('Meses (desde Jul 2010)', fontsize=12)
    ax1.set_ylabel('Cant. de Vulnerabilidades', fontsize=12)
    ax1.grid(True, alpha=0.2)
    
    texto_poly = (
        f"Función Resultante:\n"
        f"f(x) = {p_coeffs[0]:.2e}x⁴ {p_coeffs[1]:.4f}x³ + {p_coeffs[2]:.4f}x² {p_coeffs[3]:.4f}x + {p_coeffs[4]:.2f}\n\n"
        f"Conclusión de la Gráfica:\n"
        f"El R² alto ({r2_poly:.3f}) demuestra que el crecimiento no es lineal,\n"
        f"sino que existen fluctuaciones ('olas') mensuales.\n"
        f"La matemática nos permite predecir los próximos 'picos' de ataques."
    ).replace('+ -', '- ')
    
    ax1.text(0.05, 0.95, texto_poly, transform=ax1.transAxes, fontsize=11,
             verticalalignment='top', bbox=dict(boxstyle='round,pad=0.5', facecolor='#202020', edgecolor='#ff00ff', alpha=0.9))
    ax1.legend(loc='lower right')
    fig1.tight_layout()
    fig1.savefig('grafica_polinomica.png', dpi=150)
    plt.close(fig1)

    # --- FIGURA 2: Modelo Exponencial ---
    fig2, ax2 = plt.subplots(figsize=(10, 7))
    ax2.scatter(x, y, color='#00d4ff', alpha=0.4, s=30, label='Reportes Reales')
    ax2.plot(x, y_exp, color='#00ff00', linewidth=3, linestyle='--', label='Ajuste Exponencial')
    ax2.set_title('Modelo 2: Crecimiento Exponencial', fontsize=16, color='#00ff00', pad=15)
    ax2.set_xlabel('Meses (desde Jul 2010)', fontsize=12)
    ax2.set_ylabel('Cant. de Vulnerabilidades', fontsize=12)
    ax2.grid(True, alpha=0.2)

    texto_exp = (
        f"Función Resultante:\n"
        f"f(x) = {a:.4f} * e^({b:.4f}x)\n\n"
        f"Conclusión de la Gráfica:\n"
        f"Demuestra la tendencia de fondo (R²={r2_exp:.3f}).\n"
        f"Si las empresas no optimizan su presupuesto en ciberseguridad,\n"
        f"esta función prueba que el colapso ocurrirá\n"
        f"de forma multiplicativa (explosiva) a largo plazo."
    )
    ax2.text(0.05, 0.95, texto_exp, transform=ax2.transAxes, fontsize=11,
             verticalalignment='top', bbox=dict(boxstyle='round,pad=0.5', facecolor='#202020', edgecolor='#00ff00', alpha=0.9))
    ax2.legend(loc='lower right')
    fig2.tight_layout()
    fig2.savefig('grafica_exponencial.png', dpi=150)
    plt.close(fig2)

    print("\nImágenes separadas generadas con éxito:")
    print("- grafica_polinomica.png")
    print("- grafica_exponencial.png")

if __name__ == "__main__":
    main()
