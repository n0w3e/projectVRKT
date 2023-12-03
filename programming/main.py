import krpc
import time
import math


conn = krpc.connect('Orbit')

# Получение доступа к важным объектам и функциям
vessel = conn.space_center.active_vessel
ap = vessel.auto_pilot
control = vessel.control
initial_propellant_mass = vessel.mass



altitude = conn.add_stream(getattr, vessel.flight(), 'mean_altitude')
apoapsis = conn.add_stream(getattr, vessel.orbit, 'apoapsis_altitude')
periapsis = conn.add_stream(getattr, vessel.orbit, 'periapsis_altitude')
surface_velocity_stream = conn.add_stream(getattr, vessel.flight(vessel.orbit.body.reference_frame), 'velocity')


# Активация двигателя
control.throttle = 1
control.sas = True

print("Запуск двигателей прошел успешно, полет через:")
time.sleep(0.5)
print('3...')
time.sleep(0.5)
print('2...')
time.sleep(0.5)
print('1...')
control.activate_next_stage()

current_propellant_mass = vessel.mass
fuel_savings = initial_propellant_mass - current_propellant_mass

print('Оценка экономии топлива:', fuel_savings)


while True:
    surface_velocity = surface_velocity_stream()
    surface_speed = surface_velocity[0]**2 + surface_velocity[1]**2 + surface_velocity[2]**2
    surface_speed = surface_speed**0.5
    if  500 <= surface_speed <= 550:
        control.throttle = 0.55
    elif 30000 <= altitude() <= 50000:
        control.sas = False
        vessel.control.pitch = -0.05
    elif 50500 <= altitude() <= 60000:
        vessel.control.pitch = 0
        control.sas = True
    elif altitude() >= 60500:
        break

print("Выход в космос прошел успешно!")
control.activate_next_stage()

control.sas = True
vessel.control.pitch = -1
time.sleep(4.8)
vessel.control.pitch = 0

print("Ракета идет к орбите")

while True:
    if (930000 <= apoapsis() <= 970000) and (130000 <= periapsis() <= 150000):
        break
    else:
        pass

control.sas = False
vessel.control.pitch = 0.05
time.sleep(0.5)
vessel.control.pitch = 0
control.sas = True
control.throttle = 0

time.sleep(5)
control.activate_next_stage()
time.sleep(5)
control.activate_next_stage()

time.sleep(5)
control.antennas = True