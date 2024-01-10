import sqlite3  #importo il packages utile per db SQlite
import numpy #pacchetto per matrici può risultare utile in caso eseguire il comando pip install numpy dalla cmd
paths=input("per favore inserire il percorso in cui è salvato il database(se da windows potrebbe richiedere doppio \ )")
conn = sqlite3.connect(paths) #mi connetto al database
cursor = conn.cursor()

def import_table (tab):
    cursor.execute(f"SELECT * FROM {tab}")
    data_tab=cursor.fetchall() #restituisce le righe come una lista di tuple
    data_tab=numpy.array(data_tab) # lo metto come matrice
    return data_tab

#importo tutto il database sotto forma di matrici

skills_conversion=import_table("skills_conversion")
skills_transversal=import_table("skills_transversal")
skills_digital=import_table("skills_digital")
skills_professional=import_table("skills_professional")
digit11=import_table("Digit11_skills")
digit12=import_table("Digit12_skills")
digit13=import_table("Digit13_skills")
digit14=import_table("Digit14_skills")
digit15=import_table("Digit15_skills")
digit17=import_table("Digit17_skills")
digit18=import_table("Digit18_skills")
digit19=import_table("Digit19_skills")



conn.close()



#creo un dizionario in cui sono presenti tutte le professioni e le categorie
professioni = {
    "0": 'Forze Armate',
    "1": 'Dirigenti',
    "2": 'Professioni intellettuali e scientifiche',
    "3": 'Professioni tecniche intermedie',
    "4": 'Impiegati di ufficio',
    "5": 'Professioni nelle attività commerciali e nei servizi',
    "6": 'Personale specializzato addetto all’agricoltura, alle foreste e alla pesca',
    "7":  'Artigiani e operai specializzati',
    "8": 'Conduttori di impianti e macchinari e addetti al montaggio',
    "9": 'Professioni non qualificate',
}
def ottieni_selezione_professione():
    print("Scegli una professione:")
    for codice, professione in professioni.items():
      print(f"{codice}: {professione}")

    codice_selezionato = input("Inserisci il codice della professione scelta: ")

    while codice_selezionato=="0" or codice_selezionato=="6":
        print("Questi codici non sono stati registrati nel nostro database ")
        codice_selezionato = input("Inserisci un codice diverso per cambiare gruppo professionale, per favore: ")

    while codice_selezionato not in professioni:
        print("questo codice non è presente, per favore inserire un codice valido")
        codice_selezionato = input("Inserisci il codice della professione scelta: ")
        while codice_selezionato=="0" or codice_selezionato=="6":
                print("Questi codici non sono stati registrati nel nostro database ")
                codice_selezionato = input("Inserisci un codice diverso per cambiare gruppo professionale, per favore: ")

    return codice_selezionato
digit1_input = ottieni_selezione_professione()
print("Hai scelto il gruppo professionale:" + professioni[digit1_input] )

def ottieni_selezione_skills_punteggi():
    # elenco delle skills disponibili
    professional_skills_disponibili = skills_professional[:,0]
    digital_skills_disponibili = skills_digital[:,0]
    transversal_skills_disponibili = skills_transversal[:,0]
    professional_skills_selezionate = []
    punteggi_1 = []
    digital_skills_selezionate = []
    punteggi_2 = []
    transversal_skills_selezionate = []
    punteggi_3 = []
    numeri_validi=[1,2,3,4,5]
    print("Scegli 3 skills per ogni type e assegna un punteggio da 1 a 5 a ciascuna:")
    print("Skills professionali disponibili:")
    for skill in professional_skills_disponibili:
        print(skill)
    for i in range(3):       #Eseguo 3 volte il ciclo
        skill_selezionata = input("Inserisci il nome di una skill: ")
        while skill_selezionata not in professional_skills_disponibili:
            print("inserire inserire una skill valida")
            skill_selezionata = input("Inserisci il nome di una skill: ")
        professional_skills_selezionate.append(skill_selezionata)
        punteggio = float(input(f"Assegna un punteggio in base al tuo livello della skill selezionata da 1(minimo) a 5(massimo) '{skill_selezionata}': "))
        while punteggio not in numeri_validi:
            punteggio=float(input("per favore inserire un numero da 1 a 5:"))
        punteggio=int(punteggio)
        punteggi_1.append(punteggio)

    print("Skills digitali disponibili:")
    for skill in digital_skills_disponibili:
        print(skill)
    for i in range(3):       #Eseguo 3 volte il ciclo
        skill_selezionata = input("Inserisci il nome di una skill: ")
        while skill_selezionata not in digital_skills_disponibili:
            print("inserire inserire una skill valida")
            skill_selezionata = input("Inserisci il nome di una skill: ")
        digital_skills_selezionate.append(skill_selezionata)
        punteggio = float(input(f"Assegna un punteggio in base al tuo livello della skill selezionata da 1(minimo) a 5(massimo)'{skill_selezionata}': "))
        while punteggio not in numeri_validi:
            punteggio=float(input("per favore inserire un numero da 1 a 5:"))
        punteggio=int(punteggio)
        punteggi_2.append(punteggio)

    print("Skills trasversali disponibili:")
    for skill in transversal_skills_disponibili:
        print(skill)
    for i in range(3):       #Eseguo 3 volte il ciclo
        skill_selezionata = input("Inserisci il nome di una skill: ")
        while skill_selezionata not in transversal_skills_disponibili:
            print("inserire inserire una skill valida")
            skill_selezionata = input("Inserisci il nome di una skill: ")
        transversal_skills_selezionate.append(skill_selezionata)
        punteggio = float(input(f"Assegna un punteggio in base al tuo livello della skill selezionata da 1(minimo) a 5(massimo) '{skill_selezionata}': "))
        while punteggio not in numeri_validi:
            punteggio=float(input("per favore inserire un numero da 1 a 5:"))
        punteggio=int(punteggio)
        punteggi_3.append(punteggio)
    skills_selezionate=professional_skills_selezionate + digital_skills_selezionate + transversal_skills_selezionate
    punteggi=punteggi_1+punteggi_2+punteggi_3
    return skills_selezionate, punteggi

skills_punt = ottieni_selezione_skills_punteggi()
print(f"Skill e punteggi: {skills_punt}")

input=numpy.array(skills_punt).T #devo ottenere una matrice e alla fine la traspongo perchè array lo fa per riga
ninput=input.shape[0]
nskill=skills_conversion.shape[0]
for i in range(ninput):
    for j in range(nskill):
        if input[i,0]==skills_conversion[j,1]:
            input[i,0]=skills_conversion[j,0]



if (digit1_input=="1"):
    tabella=digit11
elif (digit1_input=="2"):
    tabella=digit12
elif (digit1_input=="3"):
    tabella=digit13
elif (digit1_input=="4"):
    tabella=digit14
elif (digit1_input=="5"):
    tabella=digit15
elif (digit1_input=="7"):
    tabella=digit17
elif (digit1_input=="8"):
    tabella=digit18
elif (digit1_input=="9"):
    tabella=digit19

tabella[:,3] =numpy.char.replace(tabella[:,3],",", ".") # il database purtroppo ha le virgole al posto dei punti per separare i decimali converto
tabella[:,3] = tabella[:,3].astype(float) #lo rendo un numero

ntab=tabella.shape[0]  # numero di righe in un oggetto numpy
ninput=input.shape[0]


colonna_zeri=numpy.zeros(ntab) #creo una colonna di zeri lunga qunato le righe della tabella
tabella=numpy.column_stack((tabella,colonna_zeri)) #aggiungo la colonna di zeri alla tabella . concatenando le tuple

for i in range(ninput):
  for j in range(ntab):
    if (input[i,0]==tabella[j,2]):  #inserisco any in quanto è una matrice numpy e non posso applicare una normale condizione con ==
      tabella[j,4]=float(tabella[j, 3])*int(input[i,1])

lavoro={}

for i in range(ntab):
    if tabella[i,1] not in lavoro:
        lavoro[tabella[i,1]]=float(tabella[i,4])
    else:
        lavoro[tabella[i,1]]=lavoro[tabella[i,1]]+float(tabella[i,4])
massimo=max(lavoro.values())
for chiave,valore in lavoro.items():
    if valore==massimo:
        lavoro_perfetto=chiave



print(f"il lavoro migliore con le tue competenze è {lavoro_perfetto}")
