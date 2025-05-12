import numpy as np
from ase.io import read

def get_molecules(molecules:list, file):
	'''Esta funcion tiene como proposito obtener las moleculas individuales de un archivo que pueda leer ASE.
	
	get_molecules va a buscar en el archivo todos los atomos correspondientes a las moleculas solicitadas y los va a asignar a dicha una nueva variable que va a contener dicha molecula, sin importar si existe repeticion por multiplicidad de moleculas iguales, todas seran contenidas por separado. Funciona bajo la suposicion de que el arreglo de los atomos es tal que se muestran primero todas las moleculas de un mismo tipo y luego las del siguente tipo.

	'''
	all_atoms = read(file) # Se lee el archivo original que se desea analizar


	atoms_per_molecule = np.empty(len(molecules), dtype=object) # Se genera un numpy array para guardar los elementos que conforman cada molecula diferente del sistema

	# El siguiente ciclo le asigna una lista de los atomos que conforman cada molecula un lugar en el numpy array anterior
	for i in range(len(molecules)):
		atoms_per_molecule[i] = list(molecules[i].symbols.indices().keys())

	simbolos = all_atoms.get_chemical_symbols()
	posiciones = all_atoms.get_positions()

	for i in range(len(molecules)):
		for j in range(len(all_atoms)):
			pass


'''

Por ejemplo tener moleculas A, B y C

buscar en el archivo por grupos conformados de acuerdo a la cantidad de atomos de A, B y C (Por separado), donde esta la primerta molecula de cada tipo, a partir de ahi, juntar en grupitos.

Es decir, me posiciono en el indice del primer atomo de la primera molecula tipo A, y desde ahi voy formando grupitos de tama;o A para obtener todas las moleculas A, con el cuidado de que se deberia saber cuantas moleculas A hay en el archivo

De igual forma para las otras

'''
