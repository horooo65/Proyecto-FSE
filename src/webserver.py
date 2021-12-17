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
# webserver.py
# Inicia un servidor web personalizado y maneja todas las solicitudes.
#
## ## ###############################################

# Future imports (Python 2.7 compatibility)
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import sys
import json
import magic
from controlfunciones import *
from http.server import BaseHTTPRequestHandler, HTTPServer
import socket# import time

def get_local_ip():
	hostname = socket.gethostname()
	local_ip = socket.gethostbyname(hostname)
	return local_ip

# Nombre o dirección IP del sistema anfitrión del servidor web
# address = "localhost"
address = get_local_ip()
# Puerto en el cual el servidor estará atendiendo solicitudes HTTP
# El default de un servidor web en produción debe ser 80
port = 8888

class WebServer(BaseHTTPRequestHandler):
	"""Sirve cualquier archivo encontrado en el servidor"""
	def _serve_file(self, rel_path):
		if not os.path.isfile(rel_path):
			self.send_error(404)
			return
		self.send_response(200)
		mime = magic.Magic(mime=True)
		self.send_header("Content-type", mime.from_file(rel_path))
		self.end_headers()
		with open(rel_path, 'rb') as file:
			self.wfile.write(file.read())

	"""Sirve el archivo de interfaz de usuario"""
	def _serve_ui_file(self):
		if not os.path.isfile("index.html"):
			err = "user_interface.html not found."
			self.wfile.write(bytes(err, "utf-8"))
			print(err)
			return
		try:
			with open("index.html", "r") as f:
				content = "\n".join(f.readlines())
		except:
			content = "Error reading index.html"
		self.wfile.write(bytes(content, "utf-8"))

	def _parse_post(self, json_obj):
		if not 'action' in json_obj or not 'value' in json_obj:
			return
		switcher = {
			'current_temp'     : temperatura_actual,
			'greenhouse_temperature': cambio_temperatura,
			'radiator_power': cambio_watts_radiador,
			'ventilator_power': cambio_watts_ventilador,
			'irrigation_status': estatus_irrigacion,
			'irrigation_program_fi': programacion_irrigacion_fi,
			'irrigation_program_ff': programacion_irrigacion_ff,
			'temperature_program_fi': programacion_temperatura_fi,
			'temperature_program_ff': programacion_temperatura_ff
		}
		func = switcher.get(json_obj['action'], None)
		if func:
			print('\tCall{}({})'.format(func, json_obj['value']))
			result = func(json_obj['value'])
			return result
		return None

	"""do_GET controla todas las solicitudes recibidas vía GET, es
	decir, páginas. Por seguridad, no se analizan variables que lleguen
	por esta vía"""
	def do_GET(self):
		# Revisamos si se accede a la raiz.
		# En ese caso se responde con la interfaz por defecto
		if self.path == '/':
			# 200 es el código de respuesta satisfactorio (OK)
			# de una solicitud
			self.send_response(200)
			# La cabecera HTTP siempre debe contener el tipo de datos mime
			# del contenido con el que responde el servidor
			self.send_header("Content-type", "text/html")
			# Fin de cabecera
			self.end_headers()
			# Por simplicidad, se devuelve como respuesta el contenido del
			# archivo html con el código de la página de interfaz de usuario
			self._serve_ui_file()
		# En caso contrario, se verifica que el archivo exista y se sirve
		else:
			self._serve_file(self.path[1:])

	def _set_headers(self):
		self.send_response(200)
		self.send_header('Content-type', 'application/json')
		self.end_headers()

	"""do_POST controla todas las solicitudes recibidas vía POST, es
	decir, envíos de formulario. Aquí se gestionan los comandos para
	la Raspberry Pi"""
	def do_POST(self):
		if self.path == '/':
			# Primero se obtiene la longitud de la cadena de datos recibida
			content_length = int(self.headers.get('Content-Length'))
			if content_length < 1:
				return
			# Después se lee toda la cadena de datos
			post_data = self.rfile.read(content_length)
			# Finalmente, se decodifica el objeto JSON y se procesan los datos.
			# Se descartan cadenas de datos mal formados
			try:
				jobj = json.loads(post_data.decode("utf-8"))
				response = self._parse_post(jobj)
				self._set_headers()
				if response:
					self.wfile.write(str.encode(response))
			except:
				self.send_response(400)
				self.send_header('Content-type', 'application/json')
				self.end_headers()
				self.wfile.write(str.encode('{"message":"Bad request"}'))

def main():
	# Inicializa una nueva instancia de HTTPServer con el
	# HTTPRequestHandler definido en este archivo
	webServer = HTTPServer((address, port), WebServer)
	print("Servidor iniciado")
	print ("\tAtendiendo solicitudes en http://{}:{}".format(address, port))
	try:
		# Mantiene al servidor web ejecutándose en segundo plano
		webServer.serve_forever()
	except KeyboardInterrupt:
		# Maneja la interrupción de cierre CTRL+C
		pass
	except:
		print(sys.exc_info())
	# Detiene el servidor web cerrando todas las conexiones
	webServer.server_close()
	# Reporta parada del servidor web en consola
	print("Server stopped.")

# Punto de anclaje de la función main
if __name__ == "__main__":
	main()
