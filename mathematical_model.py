import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

def main():
    data_file = 'writeup_data_xy.csv'
    if not os.path.exists(data_file):
        print("Data file not found.")
        return

    df = pd.read_csv(data_file)
    df['x_numeric'] = np.arange(len(df))
    x = df['x_numeric'].values
    y = df['y'].values

    # 1. Polynomial Model (Degree 4 to capture the bend)
    p_coeffs = np.polyfit(x, y, 4)
    p_model = np.poly1d(p_coeffs)
    y_poly = p_model(x)

    # 2. Exponential Model y = a * e^(b * x)
    # Filter y > 0 to use log
    mask = y > 0
    x_filtered = x[mask]
    y_filtered = y[mask]
    
    # ln(y) = ln(a) + bx
    log_y = np.log(y_filtered)
    b, ln_a = np.polyfit(x_filtered, log_y, 1)
    a = np.exp(ln_a)
    y_exp = a * np.exp(b * x)

    # Calculate R-squared for evaluation
    def get_r2(y_true, y_pred):
        ss_res = np.sum((y_true - y_pred)**2)
        ss_tot = np.sum((y_true - np.mean(y_true))**2)
        return 1 - (ss_res / ss_tot)

    r2_poly = get_r2(y, y_poly)
    r2_exp = get_r2(y, y_exp)

    # Aesthetics
    plt.style.use('dark_background')
    plt.figure(figsize=(12, 7))
    plt.scatter(x, y, color='#00d4ff', alpha=0.5, s=20, label='Datos reales')
    plt.plot(x, y_poly, color='#ff00ff', linewidth=2, label=f'Polinomial (R²={r2_poly:.3f})')
    plt.plot(x, y_exp, color='#00ff00', linewidth=2, linestyle='--', label=f'Exponencial (R²={r2_exp:.3f})')

    plt.title('Ajuste matemático de curvas para el volumen de escritura', fontsize=16)
    plt.xlabel('Meses transcurridos desde julio de 2010', fontsize=12)
    plt.ylabel('Escrituras por mes', fontsize=12)
    plt.legend()
    plt.grid(True, alpha=0.2)
    
    fit_path = 'model_fit.png'
    plt.savefig(fit_path)
    print(f"Fit chart saved as {fit_path}")

    # Output formulas
    print("\n--- Modelo matemático de curvas para el volumen de escritura ---")
    print(f"1. Modelo exponencial: f(x) = {a:.4f} * e^({b:.4f} * x)")
    print(f"   Donde x es el número de meses transcurridos desde julio de 2010.")
    
    # Polynomial formula string
    poly_str = "f(x) = "
    for i, c in enumerate(p_coeffs):
        pow = len(p_coeffs) - 1 - i
        if pow > 0:
            poly_str += f"({c:.2e})x^{pow} + "
        else:
            poly_str += f"({c:.2e})"
    print(f"2. Polynomial Model (Deg 4): {poly_str}")

if __name__ == "__main__":
    main()
