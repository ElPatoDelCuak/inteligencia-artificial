

# ? 1 Que són?
#Els sets són grups d'elements unics i no ordentats. S'utilitzen {} per definir-los i es poden separar els elements amb comes.

# ? 2 Que fan?
#Els sets agrupen elements unics que permeten agrupar elements unics aixi que no permeten la duplicació d'elements.

# ? 3 Per que serveixen?
#Serveixen per agrupar elements unics, son utils per eliminar duplicats d'un array, verificar si un element existeix dins d'un array etc...

# ? 4 Quina diferencia tenen amb les llistes?
#Els sets no permeten elements duplicats i no tenen un ordre, els arrays en canvi si ho permeten i tenen un ordre.

# ? Exemples de creació:

gats = {"Gary", "Velcro", "Lucy"}
gossos = set(["Tom", "Maya", "Chloe"])
print("Els meus gats son:", gats)
print("Els meus gossos son:", gossos)

# ? 5) Utilitza tres mètodes, tant de tuples com de sets, que siguin vàlids. I fes algun càsting entre tuples, sets i llistes per veure el que passa.  
# ? Respon: Creus que són útils els sets? Per a fer el què? Les tuples en quin moment les utilitzaries?  

gats.add("Nina") # Afegir element
print("Aquests han sigut tots els meus gats:", gats)
gossos.remove("Tom") # Eliminar element
print("Aquests son els meus gossos femella:", gossos)
gats.pop() # Eliminar un element aleatori
print("Aquests son els meus gats després de perdre un:", gats)

# ? Casting

llista_gats = list(gats) # Set a llista
tupla_gossos = tuple(gossos) # Set a tupla
set_nou_gats = set(gats) # Set a set
print("Llista de gats:", llista_gats)
print("Tupla de gossos:", tupla_gossos)
print("Set nou de gats:", set_nou_gats)

# Jo si crec que els sets son útils, ja que al no permetre elements duplicats es poden fer servir per coses que necessitin elements únics, 
# com per verificar si un element existeix dins d'un array, eliminar duplicats d'un array etc...