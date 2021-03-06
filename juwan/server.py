#!/usr/bin/env python2.7
import os
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)


engine = create_engine('postgresql://jh3831:u8pvn@104.196.175.120:5432/postgres')
##engine.execute("""DROP TABLE IF EXISTS test;""")
##engine.execute("""CREATE TABLE IF NOT EXISTS test (id serial, name text );""")
#engine.execute("""INSERT INTO test(name) VALUES ('grace hopper'), ('alan turing'), ('ada lovelace');""")


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
  print request.args
  
  cursor = g.conn.execute("SELECT * FROM swimmer")
  names = []
  for result in cursor:
    names.append(result['first_name'])  # can also be accessed using result[0]
  cursor.close()

  context = dict(data = names)

  return render_template("index.html", **context)


@app.route('/select_swimmer')
def select_swimmer():
   return render_template('select_swimmer.html') 

@app.route('/listtimes', methods = ['POST', 'GET'])
def listtimes():
  if request.method == 'POST':
    try:
        swimmername = request.form['nm']
        if not swimmername:
        	cmd = 'SELECT * FROM swimmer'
        else:
        	cmd = 'SELECT * FROM swimmer where first_name like :name1'
        print cmd
        cursor = g.conn.execute(text(cmd), name1 = swimmername)
        names = []
        for result in cursor:
          names.append(result)
        cursor.close()
    except:
      print 'this'
    finally:
      print 'one'
  return render_template('/anotherfile.html', names = names)


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
