from typing import List, Dict
import simplejson as json
from flask import Flask, Response, render_template, redirect, request
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor

app = Flask(__name__)
mysql = MySQL(cursorclass=DictCursor)

app.config['MYSQL_DATABASE_HOST'] = 'db'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config['MYSQL_DATABASE_DB'] = 'citiesData'
mysql.init_app(app)

@app.route('/', methods=['GET'])
def index():
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM mlb_players')
    result = cursor.fetchall()
    return render_template('index.html', title='Home', mlb=result)

@app.route('/view/<int:mlb_id>', methods=['GET'])
def record_view(mlb_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM mlb_players WHERE id= %s', mlb_id)
    result = cursor.fetchall()
    return render_template('view.html', title='View Form', mlb=result[0])

@app.route('/edit/<int:mlb_id>', methods=['GET'])
def form_edit_get(mlb_id):
    print(mlb_id)
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM mlb_players WHERE id= %s', mlb_id)
    result = cursor.fetchall()
    return render_template('edit.html', title='Edit Form', mlb=result[0])

@app.route('/edit/<int:mlb_id>', methods=['POST'])
def form_update_post(mlb_id):
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('fldName'), request.form.get('fldTeam'), request.form.get('fldPosition'),
                 request.form.get('fldWeight'), request.form.get('fldHeight'),
                 request.form.get('fldAge'), mlb_id)
    sql_update_query = """UPDATE mlb_players t SET t.Name = %s, t.Team = %s, t.Position = %s, t.Weight_lbs = 
    %s, t.Height_inches = %s, t.Age = %s WHERE t.id = %s """
    cursor.execute(sql_update_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)

@app.route('/new', methods=['GET'])
def form_insert_get():
    return render_template('new.html', title='New City Form')

@app.route('/new', methods=['POST'])
def form_insert_post():
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('fldName'), request.form.get('fldTeam'), request.form.get('fldPosition'),
                 request.form.get('fldWeight'), request.form.get('fldHeight'),
                 request.form.get('fldAge'))
    sql_insert_query = """INSERT INTO mlb_players (`Name`, `Team`, `Position`, `Height_inches`, `Weight_lbs`, `Age`) VALUES (%s, %s,%s, %s,%s, %s) """
    cursor.execute(sql_insert_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)

@app.route('/delete/<int:city_id>', methods=['GET'])
def form_delete_post(city_id):
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM mlb_players WHERE id = %s """
    cursor.execute(sql_delete_query, city_id)
    mysql.get_db().commit()
    return redirect("/", code=302)

@app.route('/api/mlb', methods=['GET'])
def api_mlb_list() -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM mlb_players')
    result = cursor.fetchall()
    json_result = json.dumps(result)
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp

@app.route('/api/mlb/<int:mlb_id>', methods=['GET'])
def api_mlb_view(mlb_id) -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM mlb_players WHERE id=%s', mlb_id)
    result = cursor.fetchall()
    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp

@app.route('/api/mlb/<int:mlb_id>', methods=['PUT'])
def api_mlb_save(mlb_id) -> str:
    cursor = mysql.get_db().cursor()
    content = request.json
    inputData = (content['fldName'], content['fldTeam'], content['fldPosition'],
                 content['fldWeight'], content['fldHeight'],
                 content['fldAge'], mlb_id)
    sql_update_query = """UPDATE mlb_players t SET t.Name = %s, t.Team = %s, t.Position = %s, t.Weight_lbs = 
    %s, t.Height_inches = %s, t.Age = %s WHERE t.id = %s """
    cursor.execute(sql_update_query, inputData)
    mysql.get_db().commit()
    resp = Response(status=200, mimetype='application/json')
    return resp

@app.route('/api/mlb/new', methods=['POST'])
def api_mlb_add() -> str:

    content = request.json

    cursor = mysql.get_db().cursor()
    inputData = (content['fldName'], content['fldTeam'], content['fldPosition'],
                 content['fldWeight'], content['fldHeight'],
                 content['fldAge'])
    sql_insert_query = """INSERT INTO mlb_players (`Name`, `Team`, `Position`, `Height_inches`, `Weight_lbs`, `Age`) VALUES (%s, %s,%s, %s,%s, %s) """
    cursor.execute(sql_insert_query, inputData)
    mysql.get_db().commit()
    resp = Response(status=201, mimetype='application/json')
    return resp

@app.route('/api/mlb/<int:mlb_id>', methods=['DELETE'])
def api_delete(mlb_id) -> str:
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM mlb_players WHERE id = %s """
    cursor.execute(sql_delete_query, mlb_id)
    mysql.get_db().commit()
    resp = Response(status=200, mimetype='application/json')
    return resp

if __name__ == '__main__':
    app.run(host='0.0.0.0')