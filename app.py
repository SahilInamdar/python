from flask import Flask, render_template, request
from flask_mysqldb import MySQL
import os

app = Flask(__name__)

# MySQL configuration
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST', 'mysql')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER', 'root')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD', 'my-secret-pw')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB', 'my_database')

mysql = MySQL(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            # Fetch form data
            userDetails = request.form
            name = userDetails.get('name')
            email = userDetails.get('email')

            # Validate input
            if not name or not email:
                return 'Name and email are required', 400

            # Insert data into database
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO users(name, email) VALUES(%s, %s)", (name, email))
            mysql.connection.commit()
            cur.close()

            return 'success'
        except Exception as e:
            return 'An error occurred: {}'.format(str(e)), 500
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0")

