""" """ 
x = 42
y = str(x)
print(y)
print(type(y))

x = "123"
y = 2
z = (int(x))*y
print (z)
print(type(z))


pi = 3.14
z = (int(pi))
print (z)
print(type(z))

u = 5
z =(float(u))
print (z)
print(type(z))

g = round(0.1+0.2,1)
print (g)
 
 x = 10
y = 20
resultat = (x+y)/100
print (resultat) 

x = 10
y = 3

print (x+y)
print (x-y)
print (x*y)
print (round(x/y,1))
print (x//y)
print (x%y)
print (x ** y)

pi = 3.14
z = (int(pi))
print (z)
print(type(z))

u = 5
z =(float(u))
print (z)
print(type(z))

g = round(0.1+0.2,1)
print (g)
 
tal1 = 0.1
tal2 = 0.2
tal1 = int(tal1 * 10)
tal2 = int(tal2 * 10)
print (tal1+tal2)

svar = (tal1+tal2) / 10
print (svar)



x = input("Skriv första talet: ")
y = input("Skriv andra talet: ")
summa = int(x) + int(y)
print(f"Summan är: {summa}")








x = 42
text = "Talet är: " + str(x)
print(text)



name = input("Vad heter du?")
age = input("Hur gammal är du")
print(f"Hej, {name}! Du är {age} år gammal.") """



""" x = 10
y = 5

print(x > 5 and y < 10)  # Output: True
print(x > 5 or y < 10)  # Output: 
print(x > 5 and y < 4)  # Output: 
print(x > 5 or y < 4)  # Output:

z = 3

print(x > 5 or y < 4 and z == 3)  # Output:
print(x > 5 or y < 4 and z != 3)  # Output:

print(x > 15 or y < 4 and z != 3)  # Output:


print(x > 5 and y < 5 and z == 3)  # Output:

# Överkurs
print(x > 5 and y <= 5 and z == 3)  # Output: """




try:
   x = int("femtusen")
   print (x)
except: 
   print ("ett fel uppstod1")

try:
   x = float("hej")
   print (x)
except ValueError: 
   print ("ett fel uppstod2")

try:
      y = bool("")
   print (y)
except ValueError: 
   print ("ett fel uppstod3")

try:
   y = str(0.1)
   
except: 
   print ("ett fel uppstod4")

   """ """ 
"""""
print (type(empty_list))
if empty_list == []:
    print("listan är tom")


my_list_numbers = [1,2,3,4,5,6,7,8,9,10]
print (my_list_numbers)
print(len(my_list_numbers))
my_list_numbers.pop(2)
empty_list = []    
"""


""" mixed_list = [1,2,"hejhej",True,3.14]
result = mixed_list [::2]
print (result)

number_list = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
result = number_list [0::3]
print (result)

reallyLongList = ["äpple", "banan", "körsbär", "druva", "apelsin", "päron", "kiwi", "mango", "passionsfrukt", "ananas"]
result = reallyLongList [::3]
print (result)


reallyLongList = ["äpple", "banan", "körsbär", "druva", "apelsin", "päron", "kiwi", "mango", "passionsfrukt", "ananas"] """ """

reallyLongLists = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22]
for index, number in enumerate(reallyLongLists):
    if number % 3 == 0:
        print(index,number)

reallyLongList = ["äpple", "banan", "körsbär", "druva", "apelsin", "päron", "kiwi", "mango", "passionsfrukt", "ananas"]
result = reallyLongList [2::3]
print (result)

reallyLongList = ["äpple", "banan", "körsbär", "druva", "apelsin", "päron", "kiwi", "mango", "passionsfrukt", "ananas"]
result = reallyLongList [2::3]
print (result) """






"""# Det förbestämda talet
hemligt_tal = 7

# Antal gissningar som tillåts
antal_gissningar = 5  # Kolla att denna rad finns

print("Gissa det hemliga talet mellan 1 och 10!")

# For-loop för att låta användaren gissa
for försök in range(1, antal_gissningar + 1):  # Använd rätt variabelnamn
    gissning = int(input(f"Försök {försök}: "))
    
    if gissning == hemligt_tal:
        print("Grattis! Du gissade rätt!")
        break  # Avbryter loopen om gissningen är korrekt
    elif gissning < hemligt_tal:
        print("Fel! Det hemliga talet är högre.")
    else:
        print("Fel! Det hemliga talet är lägre.")


else:
    print(f"Tyvärr, du har inga försök kvar. Det hemliga talet var {hemligt_tal}.")

    
 

produkt = {
"namn" : "Samsung",          
"pris" : 50000,           
"lager" : 50,           
 

 }

print(produkt["pris"])
produkt["lager"] = 35
produkt["kategori"] = "dator"
print(produkt)   
    
    
    person = {


"namn" : "anna",
"alder": 25,
"stad": "Stockholm",


}
person["land"] = "sverige"
person["stad"] = "Stenfors"
print(person)




produkt = [   
{
"kategori" : "dator",
"brand" : "Samsung",
"typ" : "laptop",
"pris" : "5050",
"butik" : "Whatever"

},

{
 "kategori": "telefon",
 "brand": "Apple",
 "typ": "iPhone",
 "pris": 9999,
 "butik": "MediaMarkt"
},
{
   "kategori": "dator",
   "brand": "Lenovo",
   "typ": "laptop",
   "pris": 7500,
   "butik": "NetOnNet"
 }, 
 ]
for produkter in produkt:
 print(*produkter.values())
print(type(person))

reallyLongList = ["äpple", "banan", "körsbär", "druva", "apelsin", "päron", "kiwi", "mango", "passionsfrukt", "ananas"]
print (len(reallyLongList))
for i, fruit in enumerate(reallyLongList):
 if (i+1) % 3 == 0:
  print(i,fruit) 

  x = True
y = False
print(type(x)) 

x = 10
if x > 5:
 print("x är större än 5") 

 name = input("Vad heter du?")
age = input("Hur gammal är du?")
stad = input ("Och i vilken stad bor du?")
print(f"Hej, {name}! Du är {age} år gammal, och bor i {stad}")

my_tuple = (1,2,3)
print (my_tuple) """