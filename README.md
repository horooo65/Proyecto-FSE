# Proyecto Final de Fundamentos de Sistemas Embebidos

La finalidad del siguiente trabajo es presentar un control de invernadero
modificando los parámetros principales (temperatura, potencia de radiador
y potencia de ventilador)

## Instalación

Se recomienda instalar las dependencias requeridas por el simulador usando pip:
```
sudo apt install python3-tk
pip install --user -r requirements.txt
```

## Uso
En python se inicializa el servidor con el siguiente comando:

```
python3 webserver.py
```

En el navegador, para acceder al servicio como cliente se debe acceder con la 
dirección devuelta a través de la terminal (e.j. http://127.0.1.1:8888)


## License
[MIT](https://choosealicense.com/licenses/mit/)