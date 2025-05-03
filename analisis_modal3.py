import numpy as np

# CALCULO DE ACELERACIONES Y DESPLAZAMIENTOS ESPECTRALES

# Calculo de la constante C(T) segun tramo espectral
def calcular_C(T, Tp, TL):
    if T <= Tp:
        return 2.5
    elif Tp < T <= TL:
        return 2.5 * (Tp / T)
    else:
        return 2.5 * (Tp * TL / T**2)

# Calculo de la aceleración espectral Sa
def calcular_Sa(T, g, Z, U, S, R, Tp, TL):
    C = calcular_C(T, Tp, TL)
    return g * (Z * U * C * S) / R

# Calculo de la frecuencia angular W
def calcular_W(T):
    return 2 * np.pi / T

# Calculo del desplazamiento espectral
def calcular_desplazamiento_espectral(Sa, W):
    return Sa / W**2

# Calculo del factor de participación de masa
def calcular_factor_participacion_masa(modo, masas):
    M = np.diag(masas)
    m = masas.reshape(-1, 1)
    numerador = modo.T @ m
    denominador = modo.T @ M @ modo
    return numerador / denominador

# Calculo de la fuerza espectral
def realizar_calculos(pisos, masas, modos, periodos, g, Z, U, S, R, Tp, TL):
    Sa = np.array([calcular_Sa(T, g, Z, U, S, R, Tp, TL) for T in periodos])
    W = np.array([calcular_W(T) for T in periodos])
    desplazamientos = np.array([calcular_desplazamiento_espectral(Sa[i], W[i]) for i in range(len(periodos))])
    
    
    Gamma = np.array([calcular_factor_participacion_masa(modos[:, i], masas) for i in range(modos.shape[1])])
    U_hat = np.array([Sa[i] * Gamma[i] * modos[:, i] for i in range(len(periodos))])
    F = np.array([np.diag(masas) @ U_hat[i] for i in range(len(periodos))])
    
    # Calculo de la fuerza cortante sismica
    V = np.array([[np.sum(F[i, j:]) for j in range(len(pisos))] for i in range(len(periodos))])
    #Metodos de combinacion modal
    Vsum_abs = np.sum(np.abs(V), axis=0)
    Vrcsc = np.sqrt(np.sum(V**2, axis=0))
    Vmc_h = 0.25 * Vsum_abs + 0.75 * Vrcsc
    Vreal = 0.75 * Vmc_h * R

    return pisos, F, V, Vsum_abs, Vrcsc, Vmc_h, Vreal
