from django.db import models

# Create your models here.
class Producto(object):

	def __init__(self, arg):
		super(Producto, self).__init__()
		self.arg = arg

class Casos(object):

	def __init__(self, arg):
		super(Casos, self).__init__()
		self.arg = arg

class Hoteles(object):

	def __init__(self, arg):
		super(Hoteles, self).__init__()
		self.arg = arg

class Vehiculos(object):

	def __init__(self, arg):
		super(Vehiculos, self).__init__()
		self.arg = arg

class Clima(object):

	def __init__(self, arg):
		super(Clima, self).__init__()
		self.arg = arg

class Incendio(object):

	def __init__(self, arg):
		super(Incendio, self).__init__()
		self.arg = arg

class Elecciones(object):

	def __init__(self, arg):
		super(Elecciones, self).__init__()
		self.arg = arg

class Actividades(object):

	def __init__(self, arg):
		super(Actividades, self).__init__()
		self.arg = arg
