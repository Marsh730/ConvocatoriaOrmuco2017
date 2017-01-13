from flask import Flask, render_template, json, request
from flask.ext.mysql import MySQL


app = Flask(__name__)
mysql = MySQL()

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'm730'
app.config['MYSQL_DATABASE_DB'] = 'Company'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


@app.route("/")
def main():
    return render_template('index.html')

@app.route('/SignUp' ,methods=['POST'])
def SignUp():
    print "entro"
    try:
        print "entro2"
        _name = request.form['inputName']
        _color = request.form['inputColor']
        _animal = request.form['inputAnimal']
        

        if _name and _color and _animal:
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('procedimiento',(_name,_color,_animal))
            data = cursor.fetchall()
        
            if len(data) is 0:
                conn.commit()
                return json.dumps({'message':'Good!'})
            else:
                return json.dumps({'error':str(data[0])})
            
        else:
            return json.dumps({'html' : '<span> Incomplete </span>'})

    except Exception as e:
        return json.dumps({'error':str(e)})
    finally:
        cursor.close()
        conn.close()   

if __name__ == "__main__":
    app.run()
