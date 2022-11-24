#!/usr/bin/env python3
import sys

import pylab
import numpy as np
from scipy.signal import find_peaks
import uncertainties as unc
from scipy.optimize import curve_fit

# Definizione gaussiana: a=fattore moltiplicativo, x0=centro, sigma=varianza


def gauss_function(x, a, x0, sigma):
    return a*np.exp(-(x-x0)**2/(2*sigma**2))


def fit_gauss(x, y, dy, TF):
    # Parametri della gaussiana
    n = sum(y)  # the number of data
    mean = sum(x*y)/n  # note this correction
    sigma = np.sqrt(sum(y*(x-mean)**2)/n)  # note this correction

    # Calcolo parametri
    popt, pcov = curve_fit(gauss_function, x, y, p0=[
                           1, mean, sigma])  # , sigma = dy)

    # Valori
    a0, x0, sigma = popt
    da, dx, dsigma = np.sqrt(pcov.diagonal())
    chisq = (((y - gauss_function(x, a0, x0, sigma))/dy)**2).sum()
    ndof = len(x) - 2
    if TF:
        print("a = %f +- %f" % (a0, da))
        print("x0 = %f +- %f" % (x0, dx))
        print("sigma = %f +- %f" % (sigma, dsigma))
        print("err (dev. standard su x0) = %f +- %f" %
              (np.sqrt(np.abs(sigma)), np.sqrt(dsigma)))

        print("Chisquare/ndof = %f/%d, (Aspettative: %f vs. %f)" %
              (chisq, ndof, chisq/ndof, np.sqrt(8)))

        pylab.figure()
        pylab.errorbar(x, y, dy, linestyle='', color="black",
                       marker="o", label='Dati picco')
        pylab.plot(x, gauss_function(x, *popt), 'r-', label='Fit')
        pylab.rc("font", size=14)
        pylab.title("Fit", y=1.02)
        pylab.xlabel("Canale")
        pylab.ylabel("Occorrenze", labelpad=25)
        pylab.grid(color="gray")
        pylab.legend(loc='upper right')

    return (a0, da, x0, dx, sigma, dsigma)


# Vettore dei canali
x = np.linspace(0, 2047, 2048)

# Apertura file SEGNALE DI FONDO
yf1 = pylab.loadtxt(sys.path[0]+"/example_volume_data.txt",
                    skiprows=12, unpack=True, max_rows=2048)
dyf1 = np.sqrt(yf1)
tf = 74214  # Tempo vivo di acquisizione in [s]
yf = yf1/tf  # Riscalatura con il tempo di acquisizione
dyf = dyf1/tf  # Errori poissoniani nei conteggi degli eventi

# Riscalamento dati
# set parametri
m = 1.169
dm = 0.006
M = unc.ufloat(m, dm)
q = 17
dq = 4
Q = unc.ufloat(q, dq)
X0 = []
dX0 = []

xx = (x - q) / m  # Riscalamento tutti dati

# Plot riscalando nel tempo
pylab.figure(1)
pylab.errorbar(xx, yf, dyf, linestyle='', marker=".", color="blue")

# Plot dati grezzi
pylab.figure(1)
pylab.errorbar(xx, yf1, dyf, linestyle='', marker=".", color="blue")
pylab.xlabel("Energy [keV]")
pylab.ylabel("Occorrenze")
pylab.grid(color="gray", linestyle="--")

# Limiti picchi
AA = [1365, 1050, 856, 561, 323, 34]
BB = [1522, 1180, 1028, 665, 386, 224]
'''
A1=1365
B1=1522
A2=1050
B2=1180
A3=856
B3=1028
A4=561
B4=665
A5=323
B5=386
A6=34
B6=224
'''

for i in range(0, 5):

    print("Picco numero:", i+1)
    # MEtodo di covell con media ai limiti
    ml = 10
    # A1=int(1050*m+q)
    # B1=int(1180*m+q)
    A1 = int(AA[i]*m+q)
    B1 = int(BB[i]*m+q)
    N = B1-A1
    print("Limiti picco: %d,%d; Canali compresi: %d " % (A1, B1, N))

    # Individuazione picco
    y_peak = yf1[(A1):(B1)]
    dy_peak = dyf1[(A1):(B1)]
    x_peak = xx[(A1):(B1)]
    '''
    y_peak=yf[(A1):(B1)]
    dy_peak=dyf[(A1):(B1)]
    x_peak=xx[(A1):(B1)]
    '''

    # Plot in evidenza del picco
    pylab.figure(1)
    pylab.errorbar(x_peak, y_peak, dy_peak,
                   linestyle='', marker="o", color="red")

    # Conteggio eventi
    # Stima fondo
    Mi = (sum(yf1[(A1-ml):A1]))/ml
    Mf = (sum(yf1[B1:(B1+ml)]))/ml
    print('y degli estremi del picco', Mi, Mf)
    F = ((Mi+Mf)/2)*N
    dF = np.sqrt(sum(y_peak))

    # Somma totale conteggi sotto al picco
    S = sum(y_peak)
    dS = np.sqrt(S)

    # Conteggi netti con errore
    An = S-F
    dAn = np.sqrt(S+(F*N/(2*ml)))

    print("sommatoria y (Somma) =%f +-%f" % (S, dS))
    print("sommatoria del fondo fra a,b con una retta (Fondo) = %f +- %f" % (F, dF))
    print("differenza fra somma e fondo = VOLUME SEGNALE SENZA FONDO %f +- %f" % (An, dAn))

    # Controllo con t-student se è un picco
    t_s = 1.994  # sicuro al 95% con almeno 60 dati

    if An > t_s * dAn:  # se supera e'
        print("Il picco supera il test del t di Student, i conteggi sono maggiori di: %d" % (t_s*dAn))

        # Riscalo i dati togliendo il continum
        # NOTA: necessario per plottare il picco
        y_cont = (y_peak[N-1]-y_peak[0])/(x_peak[N-1]-x_peak[0])*x_peak + \
            (((x_peak[N-1]*y_peak[0])-(x_peak[0]*y_peak[N-1])) /
             (x_peak[N-1]-x_peak[0]))
        yp = y_peak-y_cont

        # Fit gaussiana
        # Note: a è l'ampiezza, x0 è la posizione del picco e sigma è la dev. standard
        # ampiezza
        a0, da, x0, dx0, sigma, dsigma = fit_gauss(x_peak, yp, dy_peak, True)
        X0 = np.append(X0, x0)
        dX0 = np.append(dX0, np.abs(sigma))

    else:
        print("Il picco non supera il test del t di Student")

print("Posizioini picchi:", X0)
print("Errori sulle posizioini:", np.sqrt(dX0))

pylab.figure(1)
pylab.title("Spettro del fondo e picchi individuati")
pylab.legend(["Fondo", "Picchi"], loc='upper right')
pylab.show()
