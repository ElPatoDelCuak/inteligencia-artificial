

# ? 1 Que són?
# Les tuples són coleccions d'elements ordenats i inmutables, s'utilitzen () per definir-les i es poden separar els elements amb les comes.

# ? 2 Que fan?
# Les tuples agrupen elements que no deuen cambiar durant l'execució del programa, 


# ? 3 Per que serveixen?
# S'utilitzen per guardar dades que no han de canviar.
# També es poden utilitzar com a claus en diccionaris ja que són inmutables.

# ? 4 Quina diferencia tenen amb les llistes?
# no permet modificar, afegir o eliminar elements un cop creada en comparació amb els arrays.

# ? Exemples de creació:

gats = ("Gary", "Velcro", "Lucy")
gossos = tuple(["Tom", "Maya", "Chloe"])
print("Els meus gats son:", gats)
print("Els meus gossos son:", gossos)

# ? 5) Utilitza tres mètodes, tant de tuples com de sets, que siguin vàlids. I fes algun càsting entre tuples, sets i llistes per veure el que passa.  
# ? Respon: Creus que són útils els sets? Per a fer el què? Les tuples en quin moment les utilitzaries?  

print ("Comptar gossos Maya:", gossos.count("Maya")) # Comptar elements
print ("El nombre de gossos és:", len(gossos)) # Longitud de la tupla
print ("Index de Maya:", gossos.index("Chloe")) # Índex d'un element

# ? Casting

llista_gats = list(gats) # Tupla a llista
grup_gossos = set(gossos) # Tupla a set
tuplaNova_gats = tuple(gats) # Tupla a tupla
print("Llista de gats:", llista_gats)
print("Set de gossos:", grup_gossos)
print("Tupla nova de gats:", tuplaNova_gats)

# Les tuples les utilitzaria quan vulgui agrupar dades que no vui que canviin.