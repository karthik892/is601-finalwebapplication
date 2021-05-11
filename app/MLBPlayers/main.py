from flask import Blueprint, render_template, Response, redirect, request

from flask_login import login_required, current_user

from . import mysql

import json

main = Blueprint('main', __name__)

@main.route('/', methods=['GET'])
@login_required
def index():
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM mlb_players')
    result = cursor.fetchall()
    return render_template('index.html', title='Home', mlb=result)

@main.route("/chart_stats", methods=['GET'])
@login_required
def chartStatsPage():
    return render_template('chart_stats.html', title='Chart Stats')

@main.route('/api/mlb_chart', methods=['GET'])
@login_required
def api_mlb_stats() -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('select team, count(*) as count from mlb_players group by team')
    result = cursor.fetchall()
    json_result = json.dumps(result)
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp

@main.route('/view/<int:mlb_id>', methods=['GET'])
@login_required
def record_view(mlb_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM mlb_players WHERE id= %s', mlb_id)
    result = cursor.fetchall()
    return render_template('view.html', title='View Form', mlb=result[0])

@main.route('/edit/<int:mlb_id>', methods=['GET'])
@login_required
def form_edit_get(mlb_id):
    print(mlb_id)
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM mlb_players WHERE id= %s', mlb_id)
    result = cursor.fetchall()
    return render_template('edit.html', title='Edit Form', mlb=result[0])

@main.route('/edit/<int:mlb_id>', methods=['POST'])
@login_required
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

@main.route('/new', methods=['GET'])
@login_required
def form_insert_get():
    return render_template('new.html', title='New City Form')

@main.route('/new', methods=['POST'])
@login_required
def form_insert_post():
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('fldName'), request.form.get('fldTeam'), request.form.get('fldPosition'),
                 request.form.get('fldWeight'), request.form.get('fldHeight'),
                 request.form.get('fldAge'))
    sql_insert_query = """INSERT INTO mlb_players (`Name`, `Team`, `Position`, `Height_inches`, `Weight_lbs`, `Age`) VALUES (%s, %s,%s, %s,%s, %s) """
    cursor.execute(sql_insert_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)

@main.route('/delete/<int:city_id>', methods=['GET'])
@login_required
def form_delete_post(city_id):
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM mlb_players WHERE id = %s """
    cursor.execute(sql_delete_query, city_id)
    mysql.get_db().commit()
    return redirect("/", code=302)


@main.route('/api/mlb/<int:mlb_id>', methods=['GET'])
@login_required
def api_mlb_view(mlb_id) -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM mlb_players WHERE id=%s', mlb_id)
    result = cursor.fetchall()
    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp

@main.route('/api/mlb/<int:mlb_id>', methods=['PUT'])
@login_required
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

@main.route('/api/mlb/new', methods=['POST'])
@login_required
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

@main.route('/api/mlb/<int:mlb_id>', methods=['DELETE'])
@login_required
def api_delete(mlb_id) -> str:
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM mlb_players WHERE id = %s """
    cursor.execute(sql_delete_query, mlb_id)
    mysql.get_db().commit()
    resp = Response(status=200, mimetype='application/json')
    return resp