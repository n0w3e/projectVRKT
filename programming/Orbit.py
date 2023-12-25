import krpc
import time
import math


conn = krpc.connect(name='My project')

# Получение доступа к важным объектам и функциям
vessel = conn.space_center.active_vessel
ap = vessel.auto_pilot
control = vessel.control
initial_propellant_mass = vessel.mass


# Создание полезных переменных потока
altitude = conn.add_stream(getattr, vessel.flight(), 'mean_altitude')
apoapsis = conn.add_stream(getattr, vessel.orbit, 'apoapsis_altitude')
periapsis = conn.add_stream(getattr, vessel.orbit, 'periapsis_altitude')
surface_velocity_stream = conn.add_stream(getattr, vessel.flight(vessel.orbit.body.reference_frame), 'velocity')


# Получение объекта топливного бака
fuel_tank = vessel.parts.with_tag('rk-7')[0]

# Получение объекта ресурса LiquidFuel
liquid_fuel_resource = fuel_tank.resources.with_resource('LiquidFuel')[0]

# Получение текущего количества топлива
current_fuel = liquid_fuel_resource.amount


# Активация двигателя
control.throttle = 1
control.sas = True

print("Запуск двигателей прошел успешно, полет через:")
time.sleep(1)
print('3...')
time.sleep(1)
print('2...')
time.sleep(1)
print('1...')
control.activate_next_stage()

timing = time.time()

# Рассчет идеальной скорости ступенчатой ракеты
total_mass = vessel.mass
engine_thrust = sum([engine.thrust for engine in vessel.parts.engines])
specific_impulse = max([engine.specific_impulse for engine in vessel.parts.engines])
ideal_velocity = specific_impulse * 9.81 * vessel.available_thrust / total_mass * math.log((total_mass + vessel.resources.amount("LiquidFuel")) / total_mass)
velocity_origin = ideal_velocity // 10


print("Данные на 1 минуте \n")
print(f"Идеальная скорость ступенчатой ракеты(суммарная): {velocity_origin} м/с")
print("Время в секундах:", round(time.time() - timing))
print("Расстояние:", altitude(), "км\n")


times = 0
ideal_rocket = 0
while True:

    seconds = round(time.time() - timing)

    # Рассчет идеальной скорости ступенчатой ракеты
    total_mass = vessel.mass
    engine_thrust = sum([engine.thrust for engine in vessel.parts.engines])
    specific_impulse = max([engine.specific_impulse for engine in vessel.parts.engines])
    ideal_velocity = specific_impulse * 9.81 * vessel.available_thrust / total_mass * math.log((total_mass + vessel.resources.amount("LiquidFuel")) / total_mass)

    # Скорость ракеты
    surface_velocity = surface_velocity_stream()
    surface_speed = surface_velocity[0]**2 + surface_velocity[1]**2 + surface_velocity[2]**2
    surface_speed = surface_speed**0.5
    
    ideal_rocket += ideal_velocity // 10

    if 13 <= seconds <= 17:
        if times == 0:
            print(f"Данные на {seconds} минуте \n")
            print(f"Идеальная скорость ступенчатой ракеты(суммарная): {ideal_rocket} м/с")
            print("Расстояние:", altitude(), "км\n")
            times += 1

    if 500 <= surface_speed <= 550:
        if times == 1 and (28 <= seconds <= 32):
            print(f"Данные на {seconds} минуте \n")
            print(f"Идеальная скорость ступенчатой ракеты(суммарная): {ideal_rocket} м/с")
            print("Расстояние:", altitude(), "км\n")
            times += 1
        control.throttle = 0.55

    elif 30000 <= altitude() <= 50000:
        vessel.control.pitch = -1
        time.sleep(2.2)
        vessel.control.pitch = 0
    
    elif times == 2 and (58 <= seconds <= 62):
        print(f"Данные на {seconds} минуте \n")
        print(f"Идеальная скорость ступенчатой ракеты(суммарная): {ideal_rocket} м/с")
        print("Расстояние", altitude(), "км\n")
        times += 1
    
    elif (times == 3) and ((88 <= seconds <= 95)):
        print(f"Данные на {seconds} минуте \n")
        print(f"Идеальная скорость ступенчатой ракеты(суммарная): {ideal_rocket} м/с")
        print("Расстояние:", altitude(), "км\n")
        times += 1

    elif 50500 <= altitude() <= 60000:
        vessel.control.pitch = 0
        control.sas = True

    elif altitude() >= 60500 or current_fuel < 7:
        break

print("Выход в космос прошел успешно!")
control.activate_next_stage()

# Изменение тангажа ракеты к внутреннему радиальному вектору
control.sas = True
vessel.control.pitch = -1
time.sleep(4.8)
vessel.control.pitch = 0

print("Ракета идет к орбите")

while True:
    if (930000 <= apoapsis() <= 970000) and (120000 <= periapsis() <= 150000):
        break
    else:
        pass

control.sas = False
vessel.control.pitch = 0.05
time.sleep(0.5)
vessel.control.pitch = 0
control.sas = True
control.throttle = 0

# Выпуск спутника на орбиту
time.sleep(5)
control.activate_next_stage()
time.sleep(5)
control.activate_next_stage()
time.sleep(5)
control.antennas = True

print("Спутник успешно вышел на орбиту!")