import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

# Вхідні параметри
n = 500
Fs = 1000
F_max = 15

# Генерація випадкового сигналу
random_signal = np.random.normal(0, 10, n)

# Визначення відліків часу
time = np.linspace(0, n / Fs, n)

# Фільтрація сигналу
b, a = signal.butter(3, F_max / (Fs / 2), 'low')
filtered_signal = signal.filtfilt(b, a, random_signal)

# Побудова графіку сигналу
plt.figure(figsize=(10, 6))
plt.plot(time, filtered_signal, linewidth=1)
plt.xlabel('Час, с', fontsize=14)
plt.ylabel('Амплітуда', fontsize=14)
plt.title('Фільтрований сигнал', fontsize=14)
plt.savefig('./figures/filtered_signal.png', dpi=600)
plt.show()

# Розрахунок спектру сигналу
spectrum = np.fft.fft(filtered_signal)
spectrum = np.abs(np.fft.fftshift(spectrum))
freq = np.fft.fftfreq(n, 1/Fs)
freq = np.fft.fftshift(freq)

# Побудова графіку спектру
plt.figure(figsize=(10, 6))
plt.plot(freq, spectrum, linewidth=1)
plt.xlabel('Частота, Гц', fontsize=14)
plt.ylabel('Амплітуда', fontsize=14)
plt.title('Спектр сигналу', fontsize=14)
plt.savefig('./figures/signal_spectrum.png', dpi=600)
plt.show()
#кінець коду