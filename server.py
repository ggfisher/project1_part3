#!/usr/bin/env python2.7
import os
import datetime
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)

engine = create_engine('postgresql://jh3831:u8pvn@104.196.175.120:5432/postgres')

@app.before_request
def before_request():
  try:
    g.conn = engine.connect()
  except:
    print "uh oh, problem connecting to database"
    import traceback; traceback.print_exc()
    g.conn = None

@app.teardown_request
def teardown_request(exception):
  try:
    g.conn.close()
  except Exception as e:
    pass

@app.route('/')
def index():
  #print request.args
#  cursor = g.conn.execute("SELECT first_name, last_name, Free500 FROM swimmer, result where swimmer.swimmerid = result.swimmerid")
#  names = []
#  for result in cursor:
#     if (result[2] is not None): 
#         names.append(result)
#         print result[2]
#  cursor.close()

#  context = dict(data = names)

  return render_template("index.html")


@app.route('/select_swimmer')
def select_swimmer():
   return render_template('select_swimmer.html') 

@app.route('/listtimes', methods = ['POST', 'GET'])
def listtimes():
  if request.method == 'POST':

    try:
        swimmername = request.form['swimmername']
        eventtype = request.form['eventtype']
        
        if (swimmername == '') & (eventtype <> ''):
        	print '1'
        	cmd = "SELECT first_name, last_name, event, record FROM swimmer, result where swimmer.swimmerid = result.swimmerid and result.event like :event1 order by record asc"
        	cursor = g.conn.execute(text(cmd), event1 = eventtype)
        if (swimmername <> '') & (eventtype <> ''):
        	print '2'
        	cmd = "SELECT first_name, last_name, event, record FROM swimmer, result where swimmer.swimmerid = result.swimmerid and swimmer.first_name like :name1 and result.event like :event1 order by record asc"
        	cursor = g.conn.execute(text(cmd), name1 = swimmername, event1 = eventtype)
        if (eventtype == '') & (swimmername == ''):
			print '3'
			cmd = "SELECT first_name, last_name, event, record FROM swimmer, result where swimmer.swimmerid = result.swimmerid order by record asc"
			cursor = g.conn.execute(text(cmd))
        if (eventtype == '') & (swimmername <> ''):
			print '4'
			cmd = "SELECT first_name, last_name, event, record FROM swimmer, result where swimmer.swimmerid = result.swimmerid and swimmer.first_name like :name1 order by record asc"
			cursor = g.conn.execute(text(cmd), name1 = swimmername)

        names = [] 
        print cursor.rowcount
        
        for result in cursor:
            print result
            if (result[2] is not None):
                names.append(result)
        cursor.close()

        context = dict(data = names)   

    except:
      print 'this'
      g.conn.close();
    finally:
      print 'one'
  return render_template('/listswimtimes.html', **context)

@app.route('/select_pool')
def select_pool():
   return render_template('select_pool.html')

@app.route('/laneassign', methods = ['POST', 'GET'])
def laneassign():
  if request.method == 'POST':

    try:
        poollanes = request.form['poollanes']
        teamname = request.form['teamname']
        eventname = request.form['eventname']
        
        print poollanes
        print teamname
        print eventname
        cmd = "SELECT DISTINCT first_name, last_name, event, record FROM swimmer, result where swimmer.swimmerid = result.swimmerid and result.event = :event1 order by record asc"
        cursor = g.conn.execute(text(cmd), event1 = eventname)

        names = [] 
        print cursor.rowcount
        
        for result in cursor:
            print result
            if (result[2] is not None):
                names.append(result)
        cursor.close()

        cmd2 = "SELECT team_name FROM team WHERE team.teamid = :team1"
        cursor2 =  g.conn.execute(text(cmd2), team1 = teamname)
        
        teams = []
        #print cursor2[0]
        for result in cursor2:
        	print result[0]
        	if (result[0] is not None):
        		teams.append(result[0])
        cursor2.close()

        context = dict(data = names, team = teams, lanes = poollanes)   

    except:
      print 'this'
    finally:
      print 'one'
  return render_template('/lane_assignment.html', **context)


@app.route('/another')
def another():
  cursor = g.conn.execute("SELECT * FROM test")
  names = []
  for result in cursor:
    names.append(result)  # can also be accessed using result[0]
  cursor.close()
 
  return render_template("anotherfile.html", names = names)


@app.route('/add', methods=['POST'])
def add():
  name = request.form['name']
  cmd = 'INSERT INTO test(name) VALUES (:name1)';
  g.conn.execute(text(cmd), name1 = name, name2 = name);
  return redirect('/')


@app.route('/login')
def login():
    abort(401)
    this_is_never_executed()


if __name__ == "__main__":
  import click

  @click.command()
  @click.option('--debug', is_flag=True)
  @click.option('--threaded', is_flag=True)
  @click.argument('HOST', default='0.0.0.0')
  @click.argument('PORT', default=8111, type=int)
  def run(debug, threaded, host, port):
     HOST, PORT = host, port
     print "running on %s:%d" % (HOST, PORT)
     app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)


  run()
