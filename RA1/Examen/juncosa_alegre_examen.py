import random
#la funció randint de random, genera un numero desde el numero inicial fins al final, aquests dos els inclou
code = random.randint(1, 99)
code_str = str(code)
#Si code te 2 xifres agafem aquestes xifres per separat, si no agafem la xifra sencera.
if code > 9:
    code1 = code_str[0:1]
    code2 = code_str[1:2]
elif code < 10:
    code1 = code_str

trys = []
num_trys = 5
print("Benvingut al facilitador de codis 3000")
print("Si desitja sortir del programa escrigui la paraula 'exit'.")
print("")

#Introduim usuari i verfiquem
user = input("Siusplau, introdueix-hi el seu alias: ")
if user == "exit":
    print("Adeu, que tingui un bon robatori.")
while user == "":
    user = input("L'ailias no pot estar vuit, siusplau introudeix-lo un altre cop: ")

print("Benvingut " + user + ".")
print("Esta apunt de començar el programa, el programa podra verificar 5 codis abans de que salti l'alarma, queda avisat.")


while num_trys > 0:
    #CODI DE 2 XIFRES
    print("")
    if code > 9:
        try_code = input("Introdueixi un codi: ")
        if try_code == "exit":
            print("Adeu " + user + ", que tingui un bon robatori.")
            break
        while try_code == "":
            try_code = input("El codi no pot estar buit, vols que et pillin acas!? ")
        #Afegim el codi a la llista de codis probats
        trys.append(try_code)

        #Desglosem el codi en dues parts
        try_code1 = try_code[0:1]
        try_code2 = try_code[1:2]

        #Verifiquem si algun dels digits es igual al origial
        if try_code1 == code1 and try_code2 == code2:
            print("¡Codi encertat !" + code_str)
            print("¡Adeu " + user + " corre!")
            break
        elif try_code1 == code1 and try_code2 != code2:
            print("Codi proper al original")
        elif try_code1 != code1 and try_code2 == code2:
            print("Codi proper al original")
        elif try_code1 != code1 and try_code2 != code2:
            print("Codi fallit.")
    #CODI DE 1 XIFRA
    elif code < 10:
        try_code = input("Introdueixi un codi: ")
        if try_code == "exit":
            print("Adeu " + user + ", que tingui un bon robatori.")
            break
        while try_code == "":
            try_code = input("El codi no pot estar buit, vols que et pillin acas!? ")
        trys.append(try_code)

        try_code1 = try_code[0:1]
        try_code2 = try_code[1:2]

        #Verifiquem si algun dels digits es igual al origial
        if try_code1 == code_str:
            print("¡Codi encertat! " + code_str)
            print("¡Adeu " + user + " corre!")
            break
        elif try_code1 == code_str or try_code2 == code_str:
            print("Codi proper al original")
        elif try_code1 != code_str and try_code2 != code_str:
            print("Codi fallit.")

    num_trys -= 1
    print("Queden: " + str(num_trys) + " intents.")
    if num_trys < 3:
        print("Cuidado...")
    if num_trys == 1:
        print("¡Es l'ultim intent!")

if num_trys == 0:
    print("")
    print("¡Ha saltat l'alarma, CORRE!")
    print("Aquets han sigut els teus intents: ")
    print(trys)