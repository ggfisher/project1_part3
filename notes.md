engine = create_engine('postgresql://jh3831:u8pvn@104.196.175.120:5432/postgres')


I added several items this morning:
(1) I added a select_swimmer.html page
    this page has a form action that calls "listtimes" method in server.py
    It is just a framework - it includes multiple inputs that we may or may not need
(2) I added:

@app.route('/select_swimmer')
def select_swimmer():
   return render_template('select_swimmer.html') 

@app.route('/listtimes', methods = ['POST', 'GET'])
def listtimes():
  if request.method == 'POST':
    try:
        swimmername = request.form['nm']
        cmd = "SELECT * FROM test WHERE name = 'grace hopper'"
        #print cmd
        cursor = g.conn.execute(text(cmd))
        names = []
        for result in cursor:
          names.append(result)
        cursor.close()
    except:
      print 'this'
    finally:
      print 'one'
  #return redirect('/')
  return render_template('/anotherfile.html', names = names)

******* If I hard code a user in the database for the SELECT FROM it works.  If I try and pass in the swimmername from the form for some reason it does not work.  I kept this a try: except: finally: block in case we want to add our input checking in this definition.

Hopefully this makes sense.  I have tried to trouble shoot it multiple ways but no luck.  Hopefully you can figure this part out,
