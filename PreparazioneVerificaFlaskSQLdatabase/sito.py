from flask import Flask, render_template, request
app = Flask(__name__)



@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')


@app.route('/esercizio1', methods=['GET'])
def esercizio1():
    import os
    import pandas as pd
    import matplotlib.pyplot as plt
    import sqlalchemy
    from sqlalchemy import create_engine
    import pyodbc
    SERVER = '5.172.64.20\sqlexpress'
    DATABASE = 'zhao.filippo'
    USERNAME = 'zhao.filippo'
    PASSWORD = 'xxx123##'
    connectionString = f'DRIVER={{SQL Server}};SERVER={SERVER};DATABASE={DATABASE};UID={USERNAME};PWD={PASSWORD}'
    conn = pyodbc.connect(connectionString)
    
    sql_query = """
    SELECT production.categories.category_name, COUNT(production.products.product_id) as numeroProdotti
    FROM production.products
    inner join production.categories on categories.category_id = products.category_id
    group by production.categories.category_name
    order by numeroProdotti DESC
    """
    
    from sqlalchemy.engine import URL
    connection_url = URL.create("mssql+pyodbc", query={"odbc_connect": connectionString})
    engine = create_engine(connection_url)
    connAlch = engine.connect()
    df = pd.read_sql(sql_query, connAlch)
    
    stringhe = df.category_name
    dati = df.numeroProdotti
    fig, ax = plt.subplots(figsize = (10, 12))
    ax.bar(stringhe, dati, color = ['red', 'black', 'blue'])
    ax.set_title('numero di prodotti per ogni categoria')
    ax.set_xlabel('categorie')
    ax.set_ylabel('numero prodotti')
    plt.xticks(rotation = 70)
    
    dir = "static/images"
    file_name = "es1.png"
    save_path = os.path.join(dir, file_name)
    plt.savefig(save_path, dpi = 150)
    return render_template('esercizi.html', tabella = df.to_html(), foto = file_name)

@app.route('/esercizio2', methods=['GET'])
def esercizio2():
    import os
    import pandas as pd
    import matplotlib.pyplot as plt
    import sqlalchemy
    from sqlalchemy import create_engine
    import pyodbc
    SERVER = '5.172.64.20\sqlexpress'
    DATABASE = 'zhao.filippo'
    USERNAME = 'zhao.filippo'
    PASSWORD = 'xxx123##'
    connectionString = f'DRIVER={{SQL Server}};SERVER={SERVER};DATABASE={DATABASE};UID={USERNAME};PWD={PASSWORD}'
    conn = pyodbc.connect(connectionString)
    
    sql_query = """
    SELECT production.categories.category_name, sum(sales.order_items.list_price * (1 - sales.order_items.discount) * sales.order_items.quantity) as ammontareTotale
    FROM production.products
    inner join production.categories on categories.category_id = products.category_id
    inner join sales.order_items on order_items.product_id = production.products.product_id
    group by production.categories.category_name
    order by ammontareTotale DESC
    """
    
    from sqlalchemy.engine import URL
    connection_url = URL.create("mssql+pyodbc", query={"odbc_connect": connectionString})
    engine = create_engine(connection_url)
    connAlch = engine.connect()
    df = pd.read_sql(sql_query, connAlch)
    
    stringhe = df.category_name
    dati = df.ammontareTotale
    plt.figure(figsize=(16, 8))
    plt.pie(dati, labels=stringhe, autopct=lambda p:  '{:.0f}'.format(p * (dati.sum()) / 100))

    
    dir = "static/images"
    file_name = "es2.png"
    save_path = os.path.join(dir, file_name)
    plt.savefig(save_path, dpi = 150)
    return render_template('esercizi.html', tabella = df.to_html(), foto = file_name)




if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)