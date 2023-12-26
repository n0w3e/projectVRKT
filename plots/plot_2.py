import matplotlib.pyplot as plt
import numpy as np

KSP_T = [60, 900, 1800, 2000, 3600, 5400]
KSP_D = [2344, 7407, 300_000, 500_000, 7_000_000, 40_000_000] 

# Функция для вычисления V_ср
def average_velocity(t):
    return 8 * t * (t / 1000)

# Создаем массив значений времени от 0 до 5400 секунд с определенным шагом
t_values = np.linspace(0, 5400, 100)

# Вычисляем соответствующие значения V_ср
V_cp_values = average_velocity(t_values)

# Строим график
plt.figure(figsize=(10, 6))
plt.plot(t_values, V_cp_values * t_values, label=r'мат модель')
plt.plot(KSP_T, KSP_D, label="KSP")

# Добавляем сетку
plt.grid(True, linestyle='--', alpha=0.7)

# Добавляем метки осей и легенду
plt.xlabel('Время (сек)')
plt.title('Дистанция за промежуток времени')
plt.ylabel("Расстояние (м)")
plt.legend()
# Отключаем научную нотацию для оси y
plt.ticklabel_format(style='plain', axis='y')

# Устанавливаем конкретные значения на осях
plt.xticks(np.arange(0, 5500, step=500))
plt.yticks(np.arange(0, 50_000_000, step=5_000_000))

# Отображаем график
plt.savefig("plot_2.png")
