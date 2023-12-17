# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/', methods=['GET'])
def login():
    return render_template('login.html')

@app.route('/esercizi', methods=['GET'])
def esercizi():
    
    import pyodbc
    import pandas as pd

    server = '192.168.40.16'
    database = 'zhao.filippo'
    username = 'zhao.filippo'
    password = 'xxx123##'
    driver= '{SQL Server}' # controllare che il driver ODBC sia installato sulla macchina in cui è in esecuzione l'interprete Python

              
    connectionString = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'
    conn = pyodbc.connect(connectionString) 

    sql_query = """
    SELECT * FROM Lotorto.Studente
    """

    df = pd.read_sql(sql_query, conn)
    email = request.args.get("email")
    password = request.args.get("password")

    sql_query2 = f"""
    SELECT Nome 
    FROM Lotorto.Studente
    WHERE Email = '{email}'
    """

    df2 = pd.read_sql(sql_query2, conn)
    nome = str(list(df2.Nome))
    if email in list(df.Email) and password in list(df.Pass):
        return render_template('esercizi.html', nome = nome)
    elif password not in list(df.Pass):
        return ('password non esistente')
    else:
        return ('dati non esistenti')

@app.route('/1', methods=['GET'])
def home():
    
    import pyodbc
    import pandas as pd

    server = '192.168.40.16'
    database = 'zhao.filippo'
    username = 'zhao.filippo'
    password = 'xxx123##'
    driver= '{SQL Server}' # controllare che il driver ODBC sia installato sulla macchina in cui è in esecuzione l'interprete Python

              
    connectionString = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'
    conn = pyodbc.connect(connectionString) 

    sql_query = """
    SELECT DISTINCT Lotorto.Videogioco.Titolo
    FROM Lotorto.Videogioco
    INNER JOIN Lotorto.Argomentazione 
    ON Lotorto.Argomentazione.ID_VIDEOGIOCO = Lotorto.Videogioco.ID_VIDEOGIOCO
    INNER JOIN Lotorto.Argomento
    ON Lotorto.Argomentazione.ID_ARGOMENTO = Lotorto.Argomento.ID_ARGOMENTO
    WHERE Lotorto.Argomento.Nome = 'Guerra'
    ORDER BY Lotorto.Videogioco.Titolo
    """
    
    df = pd.read_sql(sql_query, conn)
    return render_template('home.html', tabella = df.to_html())

@app.route('/2', methods=['GET'])
def query2():
    
    import pyodbc
    import pandas as pd

    server = '192.168.40.16'
    database = 'zhao.filippo'
    username = 'zhao.filippo'
    password = 'xxx123##'
    driver= '{SQL Server}' # controllare che il driver ODBC sia installato sulla macchina in cui è in esecuzione l'interprete Python

              
    connectionString = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'
    conn = pyodbc.connect(connectionString) 

    sql_query = """
    SELECT Lotorto.Studente.Cognome, sum(Lotorto.Moneta.Quantita) as monete
    FROM Lotorto.ClasseVirtuale
    INNER JOIN Lotorto.Partecipazione
    ON Lotorto.ClasseVirtuale.ID_CLASSE = Lotorto.Partecipazione.ID_CLASSE
    INNER JOIN Lotorto.Studente
    ON Lotorto.Studente.ID_STUDENTE = Lotorto.Partecipazione.ID_STUDENTE
    INNER JOIN Lotorto.Moneta
    ON Lotorto.Moneta.ID_STUDENTE = Lotorto.Studente.ID_STUDENTE
    INNER JOIN Lotorto.Videogioco 
    ON Lotorto.Videogioco.ID_VIDEOGIOCO = Lotorto.Moneta.ID_VIDEOGIOCO
    WHERE Lotorto.ClasseVirtuale.Nome = '4einformatica' and Lotorto.Videogioco.Titolo = 'Fortnite'
    GROUP BY Lotorto.Studente.Cognome
    ORDER BY sum(Lotorto.Moneta.Quantita) desc
    """
    df = pd.read_sql(sql_query, conn)
    
    import os
    import matplotlib.pyplot as plt


    x2 = df.Cognome
    y2 = df.monete
    fig, ax = plt.subplots(figsize = (10, 12))
    ax.bar(x2, y2)
    ax.set_title('classifica studenti')
    ax.set_xlabel('studenti')
    ax.set_ylabel('monete')
    dir = "static/images"
    file_name = "classifica.png"
    save_path = os.path.join(dir, file_name)
    plt.savefig(save_path, dpi = 150)
    return render_template('tabella.html', tabella = df.to_html())


@app.route('/3', methods=['GET'])
def query3():
    
    import pyodbc
    import pandas as pd

    server = '192.168.40.16'
    database = 'zhao.filippo'
    username = 'zhao.filippo'
    password = 'xxx123##'
    driver= '{SQL Server}' # controllare che il driver ODBC sia installato sulla macchina in cui è in esecuzione l'interprete Python

              
    connectionString = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'
    conn = pyodbc.connect(connectionString) 

    sql_query = """
    SELECT Lotorto.Videogioco.Titolo, COUNT(Lotorto.ClasseVirtuale.ID_CLASSE) as numeroClassi
    FROM Lotorto.ClasseVirtuale
    INNER JOIN Lotorto.Contiene
    ON Lotorto.Contiene.ID_CLASSE = Lotorto.ClasseVirtuale.ID_CLASSE
    INNER JOIN Lotorto.Videogioco
    ON Lotorto.Videogioco.ID_VIDEOGIOCO = Lotorto.Contiene.ID_VIDEOGIOCO
    GROUP BY Lotorto.Videogioco.Titolo
    """
    
    df = pd.read_sql(sql_query, conn)
    return render_template('home.html', tabella = df.to_html())


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)

