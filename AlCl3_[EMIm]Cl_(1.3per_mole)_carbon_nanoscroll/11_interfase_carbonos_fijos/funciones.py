import numpy as np
import pandas as pd
from ase.io import read, write
import re

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


	def __init__(self):
		"""
		Constructor de la clase Molecula.

		Args:
			nombre (str): Nombre identificador de la molécula.
		"""

		self.nombre = ''
		self.idx_list = [] #np.array([],dtype=int)
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
		self.idx_list.append(atomo.idx) #self.idx_list = np.append(self.idx_list,atomo.idx) # Se agrega el indice del atomo agregado
		self.atomos = np.append(self.atomos, atomo)

		self.nombre +=f"{atomo.simbolo}"
		
		



def get_molecules(moleculas:list, file):
	'''Esta funcion tiene como proposito obtener las moleculas individuales de un archivo que pueda leer ASE.
	
	get_molecules va a buscar en el archivo todos los atomos correspondientes a las moleculas solicitadas y los va a asignar a dicha una nueva variable que va a contener dicha molecula, sin importar si existe repeticion por multiplicidad de moleculas iguales, todas seran contenidas por separado. Funciona bajo la suposicion de que el arreglo de los atomos es tal que se muestran primero todas las moleculas de un mismo tipo y luego las del siguente tipo.

	La función toma como referencia que los atomos de cada molecula (archivo i en moleculas) se encuentran en el mismo orden que en el archivo file, es decir si se tiene una molecula cuyo archivo va C00, en file se espera encontrar xxxxC00xxxxC00C00xxx siempre.

	Args:
		moleculas (list): Lista de todas las especies de moleculas que componen la mezcla deseada.
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

def get_data(moleculas:list , file):
	"""
	Esta función va a obtener la data disponible de las posiciones de cada elemento dentro de un archivo que pueda leer ASE y lo pondra en un dataframe de pandas.

	La función obtendrá, por ahora, la posición de cada elemento de un archivo de simulación legible por ASE y generará un dataframe de pandas con la información de atomos individuales y moleculas presentes. Se plantea proximamente agregar que retorne una lista de dataframes donde cada dataframe contenga información diferente ordenada de la misma manera por ejemplo, fuerzas, velocidades, ...

	Args:
		moleculas (list): Lista de todas las especies de moleculas que componen la mezcla deseada.
		file (file): Archivo que contiene la mezcla a trabajar.

	Returns:
		dataframe (pandas.dataframe): Data frame que contiene toda la información referente a la posición en un espacio tridimensional de cada átomo individual de una mezcla y las moleculas formadas en ella. Las columnas corresponden corresponden a los atomos/moleculas y a la componente de un sistema de referencia tridimensional a la que le pertenece la coordenada y las fijas serán los frames de la simulación.

	Example:
		>>> # DESPUES AGREGAR EJEMPLO
	"""
	frames = read(file, index=':') # Se lee el archivo original que se desea analizar y todos los frames del mismo

	molecules_idx = get_molecules(moleculas, file)

	n_frames = len(frames) # Numero de frames del archivo
	n_atoms = len(frames[0]) # Se asume un numero constante de atomos
	n_molecules = len(molecules_idx) # Numero de moleculas en el archivo

	# Creando una matriz vacia para almacenar la informacion

	data = np.empty((n_frames, (n_atoms+n_molecules)*3))

	# Guardar informacion de los atomos individuales
	for i, frame in enumerate(frames):
		data[i][:n_atoms*3] = frame.get_positions().flatten()

	# Guardar informacion de las moleculas presentes
	for i in range(n_frames):
		for j, mol in enumerate(molecules_idx):
			cm = frames[i].get_center_of_mass(scaled=False, indices=mol.idx_list)
			start = n_atoms*3 + j*3
			data[i, start:start+3] = cm

	# Titulos de las columnas del dataframe
	titulos = []

	for i in range(n_atoms+n_molecules):
		if i < n_atoms:
			titulos += [f"{frames[0][i].symbol}_x_{i+1}", f"{frames[0][i].symbol}_y_{i+1}", f"{frames[0][i].symbol}_z_{i+1}"]
		elif i >= n_atoms:
			titulos += [f"{molecules_idx[i-n_atoms].nombre}_x_{i-n_atoms+1}", f"{molecules_idx[i-n_atoms].nombre}_y_{i-n_atoms+1}", f"{molecules_idx[i-n_atoms].nombre}_z_{i-n_atoms+1}"] 
	
	df = pd.DataFrame(data, columns=titulos)
	return df



from ase.io import read, write
import glob
import os

def unir_pwouts_en_trayectoria(nombre_salida:str="trayectoria_continua.traj", carpetas:list=None):
	"""
	Une todos los pw.out.* de múltiples carpetas en una sola trayectoria continua.
	
	Args:
		nombre_salida (str): nombre del archivo .traj resultante.
		carpetas (list): lista de carpetas donde buscar pw.out.*, si None busca 'outputs_*'.

	Returns:
		nombre_salida.traj: Un archivo que contiene la informacion de output files individuales.
	"""
	
	# Si no se pasan carpetas, detecta todas las que empiecen con outputs_
	if carpetas is None:
		carpetas = sorted([d for d in os.listdir('.') if d.startswith("outputs_")])

	print(f"Carpetas detectadas: {carpetas}\n")

	todas_las_imagenes = []
	es_primer_archivo_global = True  # Para no borrar el primer frame del primer archivo total

	for carpeta in carpetas:
		archivos = sorted(glob.glob(f"{carpeta}/pw.out.*"))
		print(f"\nProcesando carpeta: {carpeta} ({len(archivos)} archivos encontrados)")

		for i, f in enumerate(archivos):
			try:
				imgs = read(f, index=':')

				# Si no es el primer archivo global → borrar primer frame
				if not es_primer_archivo_global:
					imgs = imgs[1:]

				# Después del primer archivo, desactivar bandera
				es_primer_archivo_global = False  

				todas_las_imagenes.extend(imgs)
				print(f"   {f}: {len(imgs)} frames añadidos")

			except Exception as e:
				print(f"   Error leyendo {f}: {e}")

	# Guardar trayectoria
	write(nombre_salida, todas_las_imagenes)
	print(f"\nTrayectoria final con {len(todas_las_imagenes)} frames guardada en '{nombre_salida}'")

	return todas_las_imagenes



def read_kinetic_energy_and_temperature(file):
	"""
	Extrae la temperatura instantánea y la energía cinética de cada paso de una
	simulación de dinámica molecular (MD) realizada con Quantum ESPRESSO.

	La función lee un archivo de salida (`pw.out`) de Quantum ESPRESSO que contiene
	una simulación de dinámica molecular y extrae:
	- La energía cinética instantánea (Ekin)
	- La temperatura instantánea del sistema

	Estos valores se obtienen directamente del texto del archivo de salida mediante
	expresiones regulares y se asocian implícitamente a cada paso de la simulación.
	El número de temperaturas y energías cinéticas extraídas se valida contra el
	número de pasos reconstruidos por ASE a partir de las posiciones atómicas.

	La función asume que:
	- El archivo corresponde a una simulación MD (`md`, `vc-md`, `nvt`, `npt`)
	- La temperatura instantánea se imprime una vez por paso MD
	- La temperatura inicial ("Starting temperature") es ignorada

	Args:
		file (str): Ruta al archivo de salida de Quantum ESPRESSO (`pw.out`)
					que contiene la simulación de dinámica molecular.

	Returns:
		kinetic_energy (numpy.ndarray):
			Arreglo unidimensional que contiene la energía cinética instantánea
			de cada paso MD, en unidades de Rydberg (Ry), tal como las imprime
			Quantum ESPRESSO.

		Temperature (numpy.ndarray):
			Arreglo unidimensional que contiene la temperatura instantánea del
			sistema en cada paso MD, en Kelvin (K).

	Raises:
		ValueError:
			Si el número de pasos reconstruidos por ASE no coincide con el número
			de temperaturas o energías cinéticas extraídas del archivo de salida.

	Example:
		>>> from ase.io import read
		>>> kinetic_energy, Temperature = read_T_Temp("pw.out")
		>>> print(Temperature[0])
		289.68
		>>> print(kinetic_energy.shape)
		(500,)
	"""

	"""
	Extracts the instantaneous temperature and kinetic energy from each step of a
	molecular dynamics (MD) simulation performed with Quantum ESPRESSO.

	This function reads a Quantum ESPRESSO output file (`pw.out`) corresponding to
	a molecular dynamics simulation and extracts:
	- The instantaneous kinetic energy (Ekin)
	- The instantaneous temperature of the system

	These quantities are parsed directly from the text output using regular
	expressions and are implicitly associated with each MD step. The number of
	extracted temperatures and kinetic energies is validated against the number of
	MD steps reconstructed by ASE from the atomic positions.

	The function assumes that:
	- The file corresponds to an MD simulation (`md`, `vc-md`, `nvt`, `npt`)
	- The instantaneous temperature is printed once per MD step
	- The initial "Starting temperature" entry is ignored

	Args:
		file (str): Path to the Quantum ESPRESSO output file (`pw.out`)
					containing the molecular dynamics simulation.

	Returns:
		kinetic_energy (numpy.ndarray):
			One-dimensional array containing the instantaneous kinetic energy
			for each MD step, in Rydberg units (Ry), as printed by Quantum ESPRESSO.

		Temperature (numpy.ndarray):
			One-dimensional array containing the instantaneous system temperature
			for each MD step, in Kelvin (K).

	Raises:
		ValueError:
			If the number of MD steps reconstructed by ASE does not match the number
			of temperatures or kinetic energies extracted from the output file.

	Example:
		>>> from ase.io import read
		>>> kinetic_energy, Temperature = read_T_Temp("pw.out")
		>>> print(Temperature[0])
		289.68
		>>> print(kinetic_energy.shape)
		(500,)
	"""


	# Leer pasos MD desde ASE
	atoms_list = read(file, index=":")
	nsteps = len(atoms_list)

	# Listas temporales
	kinetic_energy = []
	Temperature = []

	# Regex
	kinetic_energy_pattern = re.compile(r"^\s*kinetic energy.*=\s*([0-9.+-Ee]+)")
	
	Temperature_pattern = re.compile(r"^\s*temperature\s*=\s*([0-9.+-Ee]+)\s*K")

	# Leer el archivo UNA vez
	with open(file, "r") as f:
		for line in f:
			ke_match = kinetic_energy_pattern.search(line)
			if ke_match:
				kinetic_energy.append(float(ke_match.group(1)))

			T_match = Temperature_pattern.search(line)
			if T_match:
				Temperature.append(float(T_match.group(1)))

	# Convertir a numpy
	kinetic_energy = np.array(kinetic_energy)
	Temperature = np.array(Temperature)

	
	# Chequeo de consistencia (MUY importante)
	if not (len(kinetic_energy) == len(Temperature) == nsteps):
		raise ValueError(
			f"Inconsistencia:\n"
			f"  pasos ASE = {nsteps}\n"
			f"  Ekin QE   = {len(kinetic_energy)}\n"
			f"  Temp QE   = {len(Temperature)}"
		)

	return kinetic_energy, Temperature


def attach_data_to_atoms(file):
	"""
	Asocia datos termodinámicos provenientes de un archivo de salida de Quantum ESPRESSO
	a cada frame atómico leído con Atomic Simulation Environment (ASE).

	La función lee un archivo de salida (`pw.out`) de Quantum ESPRESSO que contiene una
	simulación de dinámica molecular (MD). Para cada frame atómico reconstruido por ASE,
	se asocian como metadatos:
	- La temperatura instantánea del sistema
	- La energía cinética instantánea

	Estos valores se almacenan en el diccionario `atoms.info` de cada objeto `Atoms`,
	permitiendo su posterior análisis y postprocesado sin necesidad de recalcular
	propiedades termodinámicas.

	La función asume que:
	- El archivo corresponde a una simulación MD de Quantum ESPRESSO
	- Existe una temperatura y una energía cinética por cada paso MD
	- Los datos termodinámicos han sido correctamente parseados desde el output

	Args:
		file (str): Ruta al archivo de salida de Quantum ESPRESSO (`pw.out`)
					que contiene la simulación de dinámica molecular.

	Returns:
		atoms_frames (list[ase.Atoms]):
			Lista de objetos `Atoms`, donde cada elemento representa un paso de la
			simulación MD y contiene en `atoms.info` los campos:
			- `"temperature"`: temperatura instantánea en Kelvin (K)
			- `"kinetic_energy"`: energía cinética instantánea en Rydberg (Ry)

	Raises:
		ValueError:
			Si el número de frames atómicos no coincide con el número de temperaturas
			o energías cinéticas extraídas del archivo de salida.

	Example:
		>>> from ase.io import read
		>>> atoms_md = attach_data_to_atoms("pw.out")
		>>> print(atoms_md[0].info["temperature"])
		289.68
		>>> print(atoms_md[0].info["kinetic_energy"])
		0.012345
	"""

	"""
	Attach thermodynamic data extracted from a Quantum ESPRESSO output file
	to each atomic frame read by Atomic Simulation Environment (ASE).

	This function reads a Quantum ESPRESSO output file (`pw.out`) containing a
	molecular dynamics (MD) simulation. For each atomic frame reconstructed by ASE,
	the following thermodynamic quantities are attached as metadata:
	- Instantaneous system temperature
	- Instantaneous kinetic energy

	These values are stored in the `atoms.info` dictionary of each `Atoms` object,
	enabling further analysis and post-processing without recomputing thermodynamic
	properties.

	The function assumes that:
	- The file corresponds to a Quantum ESPRESSO MD simulation
	- There is one temperature and one kinetic energy value per MD step
	- Thermodynamic data have been correctly parsed from the output file

	Args:
		file (str): Path to the Quantum ESPRESSO output file (`pw.out`)
					containing the molecular dynamics simulation.

	Returns:
		atoms_frames (list[ase.Atoms]):
			A list of `Atoms` objects, where each element represents one MD step and
			contains the following entries in `atoms.info`:
			- `"temperature"`: instantaneous temperature in Kelvin (K)
			- `"kinetic_energy"`: instantaneous kinetic energy in Rydberg (Ry)

	Raises:
		ValueError:
			If the number of atomic frames does not match the number of extracted
			temperatures or kinetic energies.

	Example:
		>>> from ase.io import read
		>>> atoms_md = attach_data_to_atoms("pw.out")
		>>> print(atoms_md[0].info["temperature"])
		289.68
		>>> print(atoms_md[0].info["kinetic_energy"])
		0.012345
	"""

	atoms_frames = read(file, index=":")
	num_frames = len(atoms_frames)
	kinetic_energies, temperatures = read_kinetic_energy_and_temperature(file)
	

	if not (len(atoms_frames) == len(temperatures) == len(kinetic_energies)):
		raise ValueError(
			f"Inconsistencia de tamaños: "
			f"Atoms={len(atoms_frames)}, T={len(temperatures)}, Ekin={len(kinetic_energies)}"
		)
	
	for i, atoms in enumerate(atoms_frames):
		atoms.info["temperature"] = temperatures[i]   # K
		atoms.info["kinetic_energy"] = kinetic_energies[i]      # Ry (QE units)

	return atoms_frames


from pathlib import Path
import re

def glob_numeric(base, folder: str | Path = ".") -> list[Path]:
	"""
	Busca archivos en una carpeta que coincidan con un patrón tipo *glob* donde
	la parte numérica se encuentra en la posición indicada por el carácter '*',
	y devuelve las rutas ordenadas numéricamente según dicho valor.

	La función permite localizar archivos cuyo nombre contiene una parte
	numérica embebida en cualquier posición del nombre, siempre que dicha
	posición sea indicada mediante el comodín '*' en el patrón base. El
	ordenamiento se realiza de forma estrictamente numérica, evitando el
	ordenamiento lexicográfico estándar del sistema de archivos.

	Args:
		base (str): Patrón base del nombre del archivo, donde el carácter '*'
			indica la posición de la parte numérica. Por ejemplo:
			- "hola_*_prueba.txt"
			- "hola_prueba.txt_*"
		carpeta (str | pathlib.Path): Ruta a la carpeta donde se buscarán los
			archivos. Por defecto se utiliza el directorio actual.

	Returns:
		list[pathlib.Path]: Lista de rutas a los archivos encontrados, ordenados
		numéricamente de menor a mayor según la parte numérica del nombre.

	Example:
		>>> from pathlib import Path
		>>> archivos = glob_numerico("hola_*_prueba.txt", carpeta="datos")
		>>> for f in archivos:
		...     print(f.name)
		hola_1_prueba.txt
		hola_2_prueba.txt
		hola_10_prueba.txt
	"""


	"""
	Searches for files in a directory that match a *glob*-like pattern where the
	numeric part is located at the position indicated by the '*' character, and
	returns the file paths sorted numerically according to that value.

	This function allows locating files whose names contain an embedded numeric
	component at an arbitrary position, provided that this position is specified
	using the '*' wildcard in the base pattern. The resulting files are sorted
	using a true numeric ordering, avoiding the default lexicographic ordering
	of the filesystem.

	Args:
		base (str): Base filename pattern where the '*' character indicates the
			position of the numeric part. Examples:
			- "hola_*_prueba.txt"
			- "hola_prueba.txt_*"
		carpeta (str | pathlib.Path): Path to the directory where the files will
			be searched. Defaults to the current working directory.

	Returns:
		list[pathlib.Path]: List of paths to the matching files, sorted in ascending
		numerical order based on the numeric part of the filename.

	Example:
		>>> from pathlib import Path
		>>> files = glob_numerico("hola_prueba.txt_*", carpeta="data")
		>>> for f in files:
		...     print(f.name)
		hola_prueba.txt_1
		hola_prueba.txt_5
		hola_prueba.txt_20
	"""
	
	folder = Path(folder)

	# Convertir patrón glob a regex capturando el número
	regex = re.escape(base).replace(r"\*", r"(\d+)")
	patron = re.compile(rf"^{regex}$")

	encontrados = []

	for f in folder.iterdir():
		if not f.is_file():
			continue

		m = patron.match(f.name)
		if m:
			numer = int(m.group(1))
			encontrados.append((numer, f))

	encontrados.sort(key=lambda x: x[0])
	return [f for _, f in encontrados]


def joint_simulation(output_file: str = "joint_simulation.traj", **kwargs):
	"""
	Une múltiples simulaciones de Quantum ESPRESSO en una única trayectoria de ASE.

	Esta función permite combinar salidas de simulaciones (por ejemplo, cálculos
	SCF, relajaciones o dinámica molecular) provenientes de Quantum ESPRESSO en
	un solo archivo de trayectoria compatible con ASE. Los archivos pueden ser
	proporcionados explícitamente o encontrados dentro de carpetas especificadas.
	La función se encarga de leer los archivos, adjuntar la información relevante
	(energía, fuerzas, etc.) y descartar frames iniciales redundantes en archivos
	subsecuentes para mantener la continuidad de la simulación.

	Args:
		output_file (str): Nombre del archivo de salida donde se escribirá la
			trayectoria conjunta. Por defecto es "joint_simulation.traj".
		**kwargs: Argumento con nombre que especifica el origen de los datos.
			Debe proporcionarse exactamente uno de los siguientes:
			
			- files (list[str | pathlib.Path]): Lista explícita de archivos de
			  salida de Quantum ESPRESSO a unir.
			- folders (list[str | pathlib.Path]): Lista de carpetas que contienen
			  archivos de salida de Quantum ESPRESSO. Los archivos dentro de cada
			  carpeta se buscan y ordenan numéricamente usando el patrón
			  "pw.out.*".

	Raises:
		ValueError: Si no se proporciona ningún argumento con nombre.
		ValueError: Si se proporciona más de un argumento con nombre.
		ValueError: Si el argumento con nombre no es válido.

	Returns:
		None: La función escribe directamente la trayectoria combinada en el
		archivo especificado por `output_file`.

	Example:
		>>> files = [
		...     "outputs_1/pw.out.27896",
		...     "outputs_1/pw.out.27972",
		...     "outputs_1/pw.out.28046"
		... ]
		>>> joint_simulation(
		...     output_file="combined.traj",
		...     files=files
		... )

		>>> folders = ["run_1", "run_2"]
		>>> joint_simulation(
		...     output_file="combined_from_folders.traj",
		...     folders=folders
		... )
	"""

	"""
	Joins multiple Quantum ESPRESSO simulations into a single ASE trajectory.

	This function combines outputs from Quantum ESPRESSO simulations (such as
	SCF calculations, relaxations, or molecular dynamics runs) into a single
	ASE-compatible trajectory file. Input data can be provided either as an
	explicit list of files or as a list of folders containing simulation outputs.
	The function reads each file, attaches relevant physical data (energy,
	forces, etc.), and discards redundant initial frames from subsequent files
	to preserve simulation continuity.

	Args:
		output_file (str): Name of the output file where the combined trajectory
			will be written. Defaults to "joint_simulation.traj".
		**kwargs: Keyword argument specifying the source of the data. Exactly one
			of the following must be provided:
			
			- files (list[str | pathlib.Path]): Explicit list of Quantum ESPRESSO
			  output files to be joined.
			- folders (list[str | pathlib.Path]): List of directories containing
			  Quantum ESPRESSO output files. Files inside each folder are searched
			  and numerically ordered using the pattern "pw.out.*".

	Raises:
		ValueError: If no keyword argument is provided.
		ValueError: If more than one keyword argument is provided.
		ValueError: If an invalid keyword argument is supplied.

	Returns:
		None: The function writes the combined trajectory directly to the file
		specified by `output_file`.

	Example:
		>>> files = [
		...     "outputs_1/pw.out.27896",
		...     "outputs_1/pw.out.27972",
		...     "outputs_1/pw.out.28046"
		... ]
		>>> joint_simulation(
		...     output_file="combined.traj",
		...     files=files
		... )

		>>> folders = ["run_1", "run_2"]
		>>> joint_simulation(
		...     output_file="combined_from_folders.traj",
		...     folders=folders
		... )
	"""

	valid_kwargs = {"files", "folders"}

	# Validar kwargs
	if not kwargs:
		raise ValueError(
			"No keyword arguments provided. Use 'files' or 'folders'."
		)

	if len(kwargs) != 1:
		raise ValueError(
			"Provide exactly one keyword argument: 'files' or 'folders'."
		)

	key = next(iter(kwargs))
	if key not in valid_kwargs:
		raise ValueError(
			f"Invalid keyword argument '{key}'. Valid options are 'files' or 'folders'."
		)

	run_output = []

	# ----------------------------------
	# Caso 1: lista explícita de archivos
	# ----------------------------------
	if key == "files":
		files = kwargs["files"]

		for i , file in enumerate(files):
			
			frames = attach_data_to_atoms(file)

			if i > 0:
				frames = attach_data_to_atoms(file)
				frames = frames[2:]  # Descartar primeros 2 frames

			print(f"Processing file: {file} ---- {len(frames)} frames")
			run_output.extend(frames)

	# ----------------------------------
	# Caso 2: lista de carpetas
	# ----------------------------------
	elif key == "folders":
		folders = kwargs["folders"]

		for folder in folders:
			print(f"\nProcessing folder: {folder}")
			folder_files = glob_numeric(base="pw.out.*", folder=folder)

			for i, f in enumerate(folder_files):
				
				frames = attach_data_to_atoms(f)

				# Descartar primeros 2 frames excepto del primer archivo en todas las carpetas
				if i > 0:
					frames = frames[2:]
				
				print(f"Processing file: {f.name} ---- {len(frames)} frames")
				run_output.extend(frames)
			
			print(f"Total frames on {folder} folder: {len(run_output)}")
		
		print(f"\nTotal frames in joint simulation: {len(run_output)}")

	write(output_file, run_output)
	return run_output