import os
import sqlite3 as sql
from flask import (Flask, render_template, request,
                   send_from_directory)

app = Flask(__name__)
BDD_PATH = "data/poubelle_metro.db"

@app.route('/', methods=['GET', 'POST'])
def index():
    results = None
    if request.method=='POST':
        with sql.connect(BDD_PATH) as conn:
            results = conn.execute('''
                SELECT type_poubelle AS Type, sum(nombre_par_type) AS Total
                FROM poubelle
                GROUP BY type_poubelle
                ORDER BY total DESC
                ''').fetchall()

    return render_template("index.html", results=results)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == '__main__':
   app.run(host='0.0.0.0')