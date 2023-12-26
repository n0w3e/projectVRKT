import matplotlib.pyplot as plt
import numpy as np

KSP_T = [60, 900, 1600, 1700, 1800, 2700, 2800, 2900, 3600, 5400]
KSP_V = [10, 521, 1400, 1600, 1798, 3850, 4100, 4300, 6600, 16700]

# Функция для вычисления V_ср
def average_velocity(t):
    return 8 * t * (t / 1000)

# Создаем массив значений времени от 0 до 5400 секунд с определенным шагом
t_values = np.linspace(0, 5400, 100)

# Вычисляем соответствующие значения V_ср
V_cp_values = average_velocity(t_values)

# Строим график
plt.plot(t_values, V_cp_values, label=r'мат модель')
plt.plot(KSP_T, KSP_V, label="KSP")

# Добавляем сетку
plt.grid(True, linestyle='--', alpha=0.7)

# Добавляем метки осей и легенду
plt.xlabel('Время (сек)')
plt.ylabel('Средняя скорость')
plt.title('График зависимости V_ср от времени')
plt.legend()

# Отображаем график
plt.savefig("plot_1.png")
