import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
# Nazarov O.I 529
# Вхідні параметри
n = 500  # Довжина сигналу у відліках
Fs = 1000  # Частота дискретизації (Гц)
F_max = 15  # Максимальна частота сигналу (Гц)

# Генерація випадкового сигналу
random_signal = np.random.normal(0, 10, n)

# Визначення відліків часу
time = np.arange(n) / Fs

# Розрахунок параметрів фільтру
cutoff_freq = F_max / (Fs / 2)  # Визначення частоти відсіву
filter_order = 3  # Порядок фільтру
sos = signal.butter(filter_order, cutoff_freq, 'low', output='sos')  # Розрахунок коефіцієнтів фільтру

# Фільтрація сигналу
filtered_signal = signal.sosfiltfilt(sos, random_signal)

# Побудова графіку сигналу
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(time, filtered_signal, linewidth=1)
ax.set_xlabel('Час, с', fontsize=14)
ax.set_ylabel('Амплітуда', fontsize=14)
plt.title('Фільтрований сигнал', fontsize=14)
plt.savefig('./figures/filtered_signal.png', dpi=600)  # Збереження графіку
plt.show()

# Розрахунок спектру сигналу
spectrum = np.fft.fft(filtered_signal)
spectrum = np.abs(np.fft.fftshift(spectrum))
freq = np.fft.fftfreq(n, 1/Fs)
freq = np.fft.fftshift(freq)

# Побудова графіку спектру
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(freq, spectrum, linewidth=1)
ax.set_xlabel('Частота, Гц', fontsize=14)
ax.set_ylabel('Амплітуда', fontsize=14)
plt.title('Спектр сигналу', fontsize=14)
plt.savefig('./figures/signal_spectrum.png', dpi=600)  # Збереження графіку
plt.show()

#...