# !/usr/bin/env python3
# ## ###############################################
#
# Autores: 
# Acosta Hernández Horacio Emmanuel
# Juárez Munguía Brandon Jesús
# Medina Cruz Josué Emanuel
# License: MIT
#
# ## ###############################################
#
# controlfunciones.py
# Controla los leds en en el GPIO así como los mensajes
#
## ## ###############################################

# Future imports (Python 2.7 compatibility)
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import json

# Simulator functions
from controlleds import *
from random import random
import json
from datetime import datetime

last_error = random()
LOG_FILE = './temp.log'

def get_data():
    with open('values.json') as f:
        data = json.load(f)
    return data

def set_data(data: dict):
    with open("values.json", "w") as f:
        json.dump(data, f)

def pid(target_value, current_value):
    """ Se efectua el cálculo del PID"""
    global last_error
    kp= 0.5
    kd = 0.2
    error = int(target_value) - current_value
    derivative = error - last_error
    control_variable = (kp*error) + kd*derivative
    current_value += control_variable
    last_error = error
    return current_value

def cambio_watts_ventilador(targeted_ventilator_power):
    """ Ajusta la potencia del ventilador """
    targeted_ventilator_power = int(targeted_ventilator_power)
    t = registro_log()
    m1 = 'Inicia proceso de ajuste en ventilador ({}).'.format(t)
    print(m1)
    log_temp(m1)
    focoactualizacion()
    focoventilador()
    m2 = 'Potencia del ventilador se ajustará a: {}'.format(targeted_ventilator_power)
    print(m2)
    log_temp(m2)
    current_ventilator_power = get_data()["current_ventilator_power"]
    new_ventilator_powe= pid(targeted_ventilator_power, current_ventilator_power)
    m3 = 'Potencia final después del cambio: {}'.format(new_ventilator_powe)
    print(m3)
    log_temp(m3)
    data = get_data()
    data["current_ventilator_power"] = round(new_ventilator_powe)
    set_data(data)
    response = {}
    return json.dumps(response)

def cambio_watts_radiador(targeted_radiator_power):
    """ Ajusta la potencia del rediador """
    targeted_radiator_power = int(targeted_radiator_power)
    t = registro_log()
    m1 = 'Inicia proceso de ajuste en radiador ({}).'.format(t)
    print(m1)
    log_temp(m1)
    focoactualizacion()
    focoradiador()
    m2 = 'Potencia del radiador se ajustará a: {}'.format(targeted_radiator_power)
    print(m2)
    log_temp(m2)
    current_radiator_power = get_data()["current_radiator_power"]
    new_radiator_power= pid(targeted_radiator_power, current_radiator_power)
    m3 = 'Potencia final después del cambio: {}'.format(new_radiator_power)
    print(m3)
    log_temp(m3)
    data = get_data()
    data["current_radiator_power"] = round(new_radiator_power)
    set_data(data)
    response = {}
    return json.dumps(response)

def cambio_temperatura(target_temperature):
    """ Ajusta la temperatura del invernadero """
    target_temperature = int(target_temperature)
    t = registro_log()
    m1 = 'Inicia proceso de ajuste en la Temperatura ({}).'.format(t)
    print(m1)
    log_temp(m1)
    focoactualizacion()
    focotemperatura()
    m2 = 'Aproximacion de temperatura correspondiente a : {}'.format(target_temperature)
    print(m2)
    log_temp(m2)
    #Formulas obtenidas a partir de bibliografica registrada
    current_temperature = get_data()["current_temperature"]
    new_temperature = pid(target_temperature, current_temperature)
    m3 = 'Temperatura final despues del cambio es: {}'.format(new_temperature)
    print(m3)
    log_temp(m3)
    data = get_data()
    data["current_temperature"] = round(new_temperature)
    set_data(data)
    response = {}
    return json.dumps(response)

def estatus_irrigacion(value):
    """ Verifica si el sistema de irrigación está prendido """
    if value == 'on':
        focoactualizacion()
        t = registro_log()
        m1 = 'Sistema de irrigación encendido ({})'.format(t)
        print(m1)
        log_temp(m1)
        
    else:
        focoactualizacion()
        t = registro_log()
        m2 = 'Sistema de irrigación apagado ({}).'.format(t)
        print(m2)
        log_temp(m2)
    m3 = "==================================================================="
    log_temp(m3)

def programacion_irrigacion_fi(fecha):
    """ Ajusta la fecha inicial de programación para la irrigación """
    focoactualizacion()
    t = registro_log()
    m1 = 'Inicia proceso para programación de irrigación ({}).'.format(t)
    print (m1)
    log_temp(m1)
    m2 = 'Inicio de la programación de irrigación: {}'.format(fecha)
    print (m2)
    log_temp(m2)

def programacion_irrigacion_ff(fecha):
    """ Ajusta la fecha final de programación para la irrigación """
    focoactualizacion()
    m3 = 'Fin de la programación de irrigación: {}'.format(fecha)
    print (m3)
    log_temp(m3)
    m4 = "==================================================================="
    log_temp(m4)

def programacion_temperatura_fi(fecha):
    """ Ajusta la fecha inicial de programación para la temperatura """
    focoactualizacion()
    t = registro_log()
    m1 = 'Inicia proceso para programación de temperatura ({})'.format(t)
    print(m1)
    log_temp(m1)
    m2 = 'Inicio de la programación de temperatura: {}'.format(fecha)
    print(m2)
    log_temp(m2)

def programacion_temperatura_ff(fecha):
    """ Ajusta la fecha final de programación para la irrigación """
    focoactualizacion()
    m3 = 'Fin de la programación de temperatura:  {}'.format(fecha)
    print(m3)
    log_temp(m3)
    m4 = "==================================================================="
    log_temp(m4)

def temperatura_actual(_=None):
    """ Muestra la temperatura actual """
    response = {}
    current_temperature = get_data()["current_temperature"]
    m1 = 'Temperatura actual es: {}'.format(current_temperature)
    print(m1)
    log_temp(m1)
    m2 = "==================================================================="
    log_temp(m2)
    response[str(datetime.now())] = current_temperature
    return json.dumps(response)

def log_temp(logs):
    """ Registra los movimientos en un archivo llamado temp.log"""
    try:
        with open(LOG_FILE, 'a') as fp:
            fp.write('{}\n'.format(logs))
    except:
        return

def registro_log():
    """ Obtiene la fecha actual para los logs """
    tiempo = datetime.now()
    tiempo_format = tiempo.strftime('%d/%m/%Y %H:%M:%S')
    return tiempo_format
