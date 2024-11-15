# settings/__init__.py

from .production import *

try:
	from .local import *
except:
	pass