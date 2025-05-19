import numpy as np
from ase.io import read

class Atomo():
	"""
    Representa un átomo con un símbolo y una posición en el espacio 3D.

    Args:
		simbolo (str): Símbolo químico del átomo (ej. 'H', 'O', 'C').
		idx (int): indice del atomo.
		posicion (np.ndarray) : Coordenadas en 3D del átomo en un array de NumPy.
    """

	def __init__(self, simbolo, idx ,x,y,z):
		"""
        Constructor de la clase Atomo.

        Args:
			simbolo (str): Símbolo químico del átomo.
			idx (int): indice del atomo. 
			x (float): Coordenada en el eje X.
			y (float): Coordenada en el eje Y.
			z (float): Coordenada en el eje Z.
        """

		self.simbolo = simbolo
		self.idx = idx
		self.posicion = np.array([x,y,z])


class Molecula():
	"""
    Representa una molécula compuesta por múltiples átomos.

    Args:
		nombre (str): Nombre de la molécula.
		idx_list (np.ndarray): Lista de los indices de los atomos que conforman la molecula.
		atomos (np.ndarray): Lista de objetos Atomo que forman la molécula.
    """


	def __init__(self, nombre=None):
		"""
        Constructor de la clase Molecula.

        Args:
			nombre (str): Nombre identificador de la molécula.
        """

		self.nombre = nombre
		self.idx_list = np.array([])
		self.atomos = np.array([])

	def agregar_atomos(self,simbolo,idx, x,y,z):
		"""
        Agrega un átomo a la molécula.

        Args:
			simbolo (str): Símbolo químico del átomo.
			idx (int): indice del atomo.
			x (float): Coordenada en el eje X.
			y (float): Coordenada en el eje Y.
			z (float): Coordenada en el eje Z.
        """

		atomo = Atomo(simbolo,idx,x,y,z)
		self.idx_list = np.append(self.idx_list,atomo.idx) # Se agrega el indice del atomo agregado
		self.atomos = np.append(self.atomos, atomo)
		
		



def get_molecules(moleculas:list,cantidad_moleculas:list, file):
	'''Esta funcion tiene como proposito obtener las moleculas individuales de un archivo que pueda leer ASE.
	
	get_molecules va a buscar en el archivo todos los atomos correspondientes a las moleculas solicitadas y los va a asignar a dicha una nueva variable que va a contener dicha molecula, sin importar si existe repeticion por multiplicidad de moleculas iguales, todas seran contenidas por separado. Funciona bajo la suposicion de que el arreglo de los atomos es tal que se muestran primero todas las moleculas de un mismo tipo y luego las del siguente tipo.

	La función toma como referencia que los atomos de cada molecula (archivo i en moleculas) se encuentran en el mismo orden que en el archivo file, es decir si se tiene una molecula cuyo archivo va C00, en file se espera encontrar xxxxC00xxxxC00C00xxx siempre.

	Args:
		moleculas (list): Lista de todas las especies de moleculas que componen la mezcla deseada.
		cantidad_moleculas (list): Lista que contiene la cantidad de moleculas de cada especie en la mezcla. POSIBLEMENTE SE QUITE
		file (file): Archivo que contiene la mezcla a trabajar.

	Returns:
		almacenamiento (numpy.ndarray): Vector que contiene todos los objetos Moleculas.

	Example:
		>>> # DESPUES AGREGAR EJEMPLO

	'''
	mixture = read(file) # Se lee el archivo original que se desea analizar

	moleculas_list = np.empty(len(moleculas),dtype=object) # Lista de listas, cada lista dentro de esta corresponde a los atomos que conforman la molecula i de la lista de 
															#moleculas agregada.
	for i in range(len(moleculas)):
		aux = read(moleculas[i])
		moleculas_list[i] = list(aux.symbols) #np.array(aux.symbols)
	
	almacenamiento = [] # Aqui se almacena los datos de cada molecula individual.

	for i in range(len(moleculas_list)): # Para cada especie de molecula, se revisa todo el archivo de la mezcla por bloques de la cantidad de atomos de cada especie
		for j in range(len(mixture)):
			if (j== len(mixture) - len(moleculas_list[i])): 
			# Checkea si estamos en el primer atomo del ultimo grupo_i (el grupo_i viene de los grupos por especie de molecula en la mezcla) de la mezcla.
				if moleculas_list[i] == list(mixture.symbols[j:j+len(moleculas_list[i])]):
					aux_molecula = Molecula()
					for k in range(j,j+len(moleculas_list[i])):
						aux_molecula.agregar_atomos(mixture.symbols[k], # Simbolo
													k,					# Indice
													mixture[k].position[0], # posicion en x
													mixture[k].position[1], # posicion en y
													mixture[k].position[2]) # posicion en z
					almacenamiento.append(aux_molecula) # Luego de agregar todos los atomos de la molecula i, se agrega la molecula a almacenamiento
					break # Ya no hay mas moleculas de la especie i
				else: 
					break # Quedan moleculas pero no de la especie i
			elif moleculas_list[i] == list(mixture.symbols[j:j+len(moleculas_list[i])]):
				aux_molecula = Molecula()
				for k in range(j,j+len(moleculas_list[i])):
					aux_molecula.agregar_atomos(mixture.symbols[k], # Simbolo
												k,					# Indice
												mixture[k].position[0], # posicion en x
												mixture[k].position[1], # posicion en y
												mixture[k].position[2]) # posicion en z
				almacenamiento.append(aux_molecula) # Luego de agregar todos los atomos de la molecula i, se agrega la molecula a almacenamiento
	return almacenamiento
