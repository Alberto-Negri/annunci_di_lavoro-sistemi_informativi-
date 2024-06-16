###CODICE PER APPLICAZIONE SENZA COMPILAZIONE DA RIGa DI COMANDO

import os
import sqlite3
import numpy as np
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

# Funzioni per interfaccia grafica

def connect_db():
    paths = simpledialog.askstring("Input", "Per favore inserire il percorso in cui è salvato il database (togliere gli ""):")
    #paths="C:\\Users\\alber\\OneDrive\\Desktop\\done\\sistemi informativi\\database_skills.db"
    if not paths:
        messagebox.showerror("Errore", "Percorso non fornito.")
        return

    if not os.path.isfile(paths):
        messagebox.showerror("Errore", "File non trovato. Verificare il percorso e riprovare.")
        return
    
    try:
        global conn, cursor
        conn = sqlite3.connect(paths)
        cursor = conn.cursor()
        messagebox.showinfo("Successo", "Connessione al database riuscita.")
    except sqlite3.Error as e:
        messagebox.showerror("Errore", f"Errore di connessione al database: {e}")

def import_table(tab):
    cursor.execute(f"SELECT * FROM {tab}")
    data_tab = cursor.fetchall()
    data_tab = np.array(data_tab)
    return data_tab

def load_data():
    try:
        global skills_conversion, skills_transversal, skills_digital, skills_professional
        global digit11, digit12, digit13, digit14, digit15, digit17, digit18, digit19

        skills_conversion = import_table("skills_conversion")
        skills_transversal = import_table("skills_transversal")
        skills_digital = import_table("skills_digital")
        skills_professional = import_table("skills_professional")
        
        def replace_spaces_with_underscore(skills_list):
            return [skill.replace(' ', '_') for skill in skills_list]
        skills_professional = replace_spaces_with_underscore(skills_professional[:,0])
        skills_digital = replace_spaces_with_underscore(skills_digital[:,0])
        skills_transversal = replace_spaces_with_underscore(skills_transversal[:,0])

        tables = {}
        for i in [1, 2, 3, 4, 5, 7, 8, 9]:
            table_name = f"Digit1{i}_skills"
            tables[table_name] = import_table(table_name)
        

            # Uso del dizionario per selezionare la tabella corretta
        
        messagebox.showinfo("Successo", "Dati caricati con successo.")
    except Exception as e:
        messagebox.showerror("Errore", f"Errore nel caricamento dei dati: {e}")
digit1_input = None
def ottieni_selezione_professione():
    professione_window = tk.Toplevel(root)
    professione_window.title("Seleziona Professione")
    tk.Label(professione_window, text="Scegli una professione:").pack()

    for codice, professione in professioni.items():
        tk.Radiobutton(professione_window, text=professione, variable=selected_professione, value=codice).pack(anchor=tk.W)

    def conferma_selezione():
        global digit1_input
        digit1_input = selected_professione.get()
        professione_window.destroy()

    tk.Button(professione_window, text="Conferma", command=conferma_selezione).pack()

    root.wait_window(professione_window)
    return digit1_input

def ottieni_selezione_skills_punteggi():
    skill_window = tk.Toplevel(root)
    skill_window.title("Seleziona Skills e Punteggi")

    skill_selections = []
    punteggio_selections = []
    
    def select_skills(skills_disponibili, skills_selezionate, punteggi):
        for i in range(3):
            skill_var = tk.StringVar()
            skill_menu = ttk.Combobox(skill_window, textvariable=skill_var, values= skills_disponibili)
            skill_menu.pack()
            punteggio_var = tk.IntVar(value=1)
            punteggio_menu = ttk.Combobox(skill_window, textvariable=punteggio_var, values=list(range(1, 6)))
            punteggio_menu.pack()
            skill_selections.append((skill_var, punteggio_var))
            punteggio_selections.append(punteggio_var)
            skills_selezionate.append(skill_var)
            punteggi.append(punteggio_var)
    
    
    
    tk.Label(skill_window, text="Skills professionali disponibili:").pack()

    select_skills(skills_professional, professional_skills_selezionate, punteggi_1)
    
    tk.Label(skill_window, text="Skills digitali disponibili:").pack()
    select_skills(skills_digital, digital_skills_selezionate, punteggi_2)
    
    tk.Label(skill_window, text="Skills trasversali disponibili:").pack()
    select_skills(skills_transversal, transversal_skills_selezionate, punteggi_3)

    tk.Button(skill_window, text="Conferma", command=skill_window.destroy).pack()

    root.wait_window(skill_window)

    skills_selezionate = [var.get() for var, _ in skill_selections]
    punteggi = [var.get() for var in punteggio_selections]
    return skills_selezionate, punteggi

def calcola_lavoro_perfetto():
    input_data = np.array(skills_punt).T
    ninput = input_data.shape[0]
    nskill = skills_conversion.shape[0]

    for i in range(ninput):
        for j in range(nskill):
            if input_data[i, 0] == skills_conversion[j, 1]:
                input_data[i, 0] = skills_conversion[j, 0]
    tables = {}
    for i in [11, 12, 13, 14, 15, 17, 18, 19]:
        table_name = f"Digit{i}_skills"
        tables[table_name] = import_table(table_name)
       
    input_to_table = {
            "1": "Digit11_skills",
            "2": "Digit12_skills",
            "3": "Digit13_skills",
            "4": "Digit14_skills",
            "5": "Digit15_skills",
            "7": "Digit17_skills",
            "8": "Digit18_skills",
            "9": "Digit19_skills"}
    
    table_key = input_to_table.get(digit1_input)

    if table_key:
            tabella = tables[table_key]
    else:
            tabella = None  # Gestisci il caso in cui l'input non è valido
    conn.close()

    tabella[:, 3] = np.char.replace(tabella[:, 3], ",", ".")
    tabella[:, 3] = tabella[:, 3].astype(float)

    ntab = tabella.shape[0]
    colonna_zeri = np.zeros(ntab)
    tabella = np.column_stack((tabella, colonna_zeri))

    for i in range(ninput):
        for j in range(ntab):
            if input_data[i, 0] == tabella[j, 2]:
                tabella[j, 4] = float(tabella[j, 3]) * int(input_data[i, 1])

    lavoro = {}
    for i in range(ntab):
        if tabella[i, 1] not in lavoro:
            lavoro[tabella[i, 1]] = float(tabella[i, 4])
        else:
            lavoro[tabella[i, 1]] += float(tabella[i, 4])

    massimo = max(lavoro.values())
    for chiave, valore in lavoro.items():
        if valore == massimo:
            lavoro_perfetto = chiave

    messagebox.showinfo("Lavoro Perfetto", f"Il lavoro migliore con le tue competenze è {lavoro_perfetto}")

# Dizionario delle professioni
professioni = {
    #"0": 'Forze Armate',
    "1": 'Dirigenti',
    "2": 'Professioni intellettuali e scientifiche',
    "3": 'Professioni tecniche intermedie',
    "4": 'Impiegati di ufficio',
    "5": 'Professioni nelle attività commerciali e nei servizi',
    #"6": 'Personale specializzato addetto all’agricoltura, alle foreste e alla pesca',
    "7": 'Artigiani e operai specializzati',
    "8": 'Conduttori di impianti e macchinari e addetti al montaggio',
    "9": 'Professioni non qualificate',
}

# Configurazione della finestra principale
root = tk.Tk()
root.title("Selezione Professione e Skills")
root.attributes('-fullscreen', True)
# Variabili globali
selected_professione = tk.StringVar(value="1")
professional_skills_selezionate = []
punteggi_1 = []
digital_skills_selezionate = []
punteggi_2 = []
transversal_skills_selezionate = []
punteggi_3 = []
skills_punt = []

def close_fullscreen(event):
    root.attributes('-fullscreen', False)

root.bind("<Escape>", close_fullscreen)
# Pulsanti e azioni
button_style = {"bg": "gray", "fg": "white", "font": ("Helvetica", 14), "padx": 10, "pady": 10}

tk.Button(root, text="Connetti al Database", command=connect_db, **button_style).pack()
tk.Button(root, text="Carica Dati", command=load_data,**button_style).pack()
tk.Button(root, text="Seleziona Professione", command=ottieni_selezione_professione,**button_style).pack()
tk.Button(root, text="Seleziona Skills e Punteggi", command=ottieni_selezione_skills_punteggi,**button_style).pack()
tk.Button(root, text="Calcola Lavoro Perfetto", command=calcola_lavoro_perfetto,**button_style).pack()

# Avvia l'applicazione
root.mainloop()
