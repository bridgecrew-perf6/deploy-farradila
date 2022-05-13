from flask import Flask, render_template, request, session, url_for, redirect
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired

app = Flask(__name__)

app.secret_key = 'prediksi'

app.config['MYSQL_HOST'] = 'sql.promaydo.net'
app.config['MYSQL_USERNAME'] = 'promaydo_faradila'
app.config['MYSQL_PASSWORD'] = 'faradila@123'
app.config['MYSQL_DB'] = 'promaydo_faradila'

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] ='sistemprediksi2022@gmail.com'
app.config['MAIL_PASSWORD'] = 'SistemPrediksi2022'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mysql = MySQL(app)
mail = Mail(app)
s = URLSafeTimedSerializer('Thisisasecret')

@app.route('/', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        curl.execute('SELECT * FROM user WHERE email = %s AND password = %s', (email, password))
        user = curl.fetchone()
        if user:
            session['loggedin'] = True
            session['id_user'] = user['id_user']
            session['email'] = user['email']
            session['username'] = user['username']
            session['fix'] = user['confirmed']
            if user['confirmed'] == 1:
                session["role"] = user["level"]
                if user["level"] == "user":
                    return redirect(url_for('index'))
                else:
                    return redirect(url_for('index'))
            else:
                msg = 'Please confirm your email address'
                return redirect(url_for('login', msg=msg))
            return 'Logged in successfully!'
        else:
            msg = 'Please fill out the form !'

    return render_template('login.html', msg=msg)

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id_user', None)
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/register', methods = ['GET', 'POST'])
def register():
    msg = ''
    psn = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        level = request.form['level']
        confirmed = False

        curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        curl.execute('SELECT * FROM user WHERE username = %s', (username,))
        user = curl.fetchone()
        if user:
            psn = 'Account already exists !'
        elif not re.match(r'[^@]+@[student]+\.[polinema]+\.[ac]+\.[id]+', email):
            psn = 'Invalid email address! Please use institutional account.'
        elif not re.match(r'[A-Za-z0-9]+', username):
            psn = 'Username must contain only characters and numbers !'
        elif not username or not password or not email or not level:
            psn = 'Please fill out the form !'
        else:
            curl.execute('INSERT INTO user VALUES (NULL, %s, %s, %s, %s, %s)', (username, email, password, level, confirmed,))
            mysql.connection.commit()

            token = s.dumps(email, salt='email-confirm')
            msg = Message('Confirm Email', sender='sistemprediksi2022@gmail.com', recipients=[email])
            link = url_for('confirm_email', token=token, _external=True)
            msg.body = "To activate your account, please click the link below: {} \n".format(link) + "\nThis link will expire in 1 hour, so please confirm as soon as possible."\
                                                                                                     "\n\nThank You, \nSistem Prediksi Kesiapan Operasional Pesawat Tempur"
            msg.subject = "Please, confirm your email address"
            mail.send(msg)

            psn = 'You have successfully registered! Check your email address.'
            return render_template('login.html', psn=psn)

    elif request.method == 'POST':
        psn = 'Please fill out the form !'
    return render_template('register.html', msg=msg, psn=psn)

@app.route('/confirm_email/<token>')
def confirm_email(token):
    try:
        email = s.loads(token, salt='email-confirm', max_age=3600)
    except SignatureExpired:
        return '<h2>The token is experied!</h2>'

    confirmed = True

    if confirmed > 0:
        curl = mysql.connection.cursor()
        curl.execute("UPDATE user SET confirmed=%s WHERE email=%s", (confirmed, email))
        mysql.connection.commit()
        return redirect(url_for('login'))
    else:
        return 'Invalid confirmation email, please try again!'
    return 'Try Again'

@app.route('/index')
def index():
    if 'loggedin' in session:
        query_kesiapan = "SELECT * FROM kesiapan"
        query_admin = "SELECT COUNT(*) FROM user"
        cur = mysql.connection.cursor()
        cur.execute(query_kesiapan)
        dataKesiapan = cur.fetchall()
        cur.execute(query_admin)
        pengguna = cur.fetchall()
        cur.close()
        return render_template('index.html', dataKesiapan=len(dataKesiapan), pengguna=pengguna[0], username=session['username'])
    return redirect(url_for('login'))

@app.route('/dataKesiapan')
def dataKesiapan():
    if 'loggedin' in session:
        th = request.args.get('tahun')
        query = "SELECT * FROM kesiapan"
        if (th):
            query = "SELECT * FROM kesiapan WHERE tahun=" + str(th)
        curl = mysql.connection.cursor()
        curl.execute(query)
        kesiapanData = curl.fetchall()
        curl.close()
        return render_template('dataKesiapan.html', data=kesiapanData)
    return redirect(url_for('login'))

@app.route('/tambahKesiapan', methods=['POST'])
def tambahKesiapan():
    tahun = request.form['tahun']
    bulan = request.form['bulan']
    nilai_kekuatan = request.form['nilai_kekuatan']
    nilai_pemeliharaan = request.form['nilai_pemeliharaan']
    nilai_kesiapan = request.form['nilai_kesiapan']
    curl = mysql.connection.cursor()
    curl.execute("INSERT INTO kesiapan(tahun, bulan, nilai_kekuatan, nilai_pemeliharaan, nilai_kesiapan) VALUES (%s, %s, %s, %s, %s)", (tahun, bulan, nilai_kekuatan, nilai_pemeliharaan, nilai_kesiapan))
    mysql.connection.commit()
    curl.close()
    return redirect(url_for('dataKesiapan'))

@app.route('/ubahKesiapan', methods=['POST'])
def ubahKesiapan():
    id_kesiapan = request.form['id_kesiapan']
    tahun = request.form['tahun']
    bulan = request.form['bulan']
    nilai_kekuatan = request.form['nilai_kekuatan']
    nilai_pemeliharaan = request.form['nilai_pemeliharaan']
    nilai_kesiapan = request.form['nilai_kesiapan']
    curl = mysql.connection.cursor()
    curl.execute("UPDATE kesiapan SET tahun=%s, bulan=%s, nilai_kekuatan=%s, nilai_pemeliharaan=%s, nilai_kesiapan=%s WHERE id_kesiapan=%s", (tahun, bulan, nilai_kekuatan, nilai_pemeliharaan, nilai_kesiapan, id_kesiapan))
    mysql.connection.commit()
    return redirect(url_for('dataKesiapan'))

@app.route('/hapusKesiapan/<string:id_kesiapan>', methods=['GET'])
def hapusKesiapan(id_kesiapan):
    curl = mysql.connection.cursor()
    curl.execute("DELETE FROM kesiapan WHERE id_kesiapan=%s", [id_kesiapan])
    mysql.connection.commit()
    return redirect(url_for('dataKesiapan'))

@app.route('/prediksi')
def prediksi():
    if 'loggedin' in session:
        query = "SELECT * FROM kesiapan"
        curl = mysql.connection.cursor()
        curl.execute(query)
        kesiapanData = curl.fetchall()
        curl.close()
        return render_template('prediksi.html', data=kesiapanData)
    return redirect(url_for('login'))

@app.route('/persamaan')
def persamaan():
    th = request.args.get('th')
    query = "SELECT * FROM kesiapan"
    if (th):
        thSebelum = int(th)
        query = "SELECT * FROM kesiapan WHERE tahun=" + str(thSebelum)
        query2 = "SELECT * FROM kesiapan WHERE tahun=" + str(th)

    curl = mysql.connection.cursor()
    curl.execute(query)
    kesiapanData = curl.fetchall()
    curl.execute(query2)
    kesiapanData2 = curl.fetchall()
    curl.close()

    n = len(kesiapanData)
    X1 = sum(c[3] for c in kesiapanData)
    X2 = sum(c[4] for c in kesiapanData)
    Y = sum(c[5] for c in kesiapanData)
    X1Kuadrat = sum(c[3] * c[3] for c in kesiapanData)
    X2Kuadrat = sum(c[4] * c[4] for c in kesiapanData)
    Y2 = sum(c[5] * c[5] for c in kesiapanData)
    X1X2 = sum(c[3] * c[4] for c in kesiapanData)
    X1Y = sum(c[3] * c[5] for c in kesiapanData)
    X2Y = sum(c[4] * c[5] for c in kesiapanData)

    x1Kuadrat = X1Kuadrat - ((X1 * X1) / n)
    x2Kuadrat = X2Kuadrat - ((X2 * X2) / n)
    yKuadrat = Y2 - ((Y * Y) / n)
    x1y = X1Y - ((X1 * Y) / n)
    x2y = X2Y - ((X2 * Y) / n)
    x1x2 = X1X2 - ((X1 * X2) / n)

    # mencari nilai b1
    tempB1 = ((x2Kuadrat * x1y) - (x1x2 * x2y))
    b1 = tempB1 / ((x1Kuadrat * x2Kuadrat) - (x1x2 * x1x2))

    # mencari nilai b2
    tempB2 = ((x1Kuadrat * x2y) - (x1x2 * x1y))
    b2 = tempB2 / ((x1Kuadrat * x2Kuadrat) - (x1x2 * x1x2))

    # mencari nilai a
    a = (Y / n) - b1 * (X1 / n) - b2 * (X2 / n)

    return render_template('persamaan.html', data=kesiapanData2, a=a, b1=b1, b2=b2, tahun=th, data2=kesiapanData)

@app.route('/modelTerbaik')
def modelTerbaik():
    th = request.args.get('th')
    query = "SELECT * FROM kesiapan WHERE tahun=2019"
    query2 = "SELECT * FROM kesiapan WHERE tahun=2023"

    curl = mysql.connection.cursor()
    curl.execute(query)
    kesiapanData = curl.fetchall()
    curl.execute(query2)
    kesiapanData2 = curl.fetchall()
    curl.close()

    n = len(kesiapanData)
    X1 = sum(c[3] for c in kesiapanData)
    X2 = sum(c[4] for c in kesiapanData)
    Y = sum(c[5] for c in kesiapanData)
    X1Kuadrat = sum(c[3] * c[3] for c in kesiapanData)
    X2Kuadrat = sum(c[4] * c[4] for c in kesiapanData)
    Y2 = sum(c[5] * c[5] for c in kesiapanData)
    X1X2 = sum(c[3] * c[4] for c in kesiapanData)
    X1Y = sum(c[3] * c[5] for c in kesiapanData)
    X2Y = sum(c[4] * c[5] for c in kesiapanData)

    x1Kuadrat = X1Kuadrat - ((X1 * X1) / n)
    x2Kuadrat = X2Kuadrat - ((X2 * X2) / n)
    yKuadrat = Y2 - ((Y * Y) / n)
    x1y = X1Y - ((X1 * Y) / n)
    x2y = X2Y - ((X2 * Y) / n)
    x1x2 = X1X2 - ((X1 * X2) / n)

    # mencari nilai b1
    tempB1 = ((x2Kuadrat * x1y) - (x1x2 * x2y))
    b1 = tempB1 / ((x1Kuadrat * x2Kuadrat) - (x1x2 * x1x2))

    # mencari nilai b2
    tempB2 = ((x1Kuadrat * x2y) - (x1x2 * x1y))
    b2 = tempB2 / ((x1Kuadrat * x2Kuadrat) - (x1x2 * x1x2))

    # mencari nilai a
    a = (Y / n) - b1 * (X1 / n) - b2 * (X2 / n)

    return render_template('modelTerbaik.html', data=kesiapanData2, a=a, b1=b1, b2=b2, tahun=th, data2=kesiapanData)

@app.route('/modelTerakhir')
def modelTerakhir():
    th = request.args.get('th')
    query = "SELECT * FROM kesiapan WHERE tahun=2022"
    query2 = "SELECT * FROM kesiapan WHERE tahun=2023"

    curl = mysql.connection.cursor()
    curl.execute(query)
    kesiapanData = curl.fetchall()
    curl.execute(query2)
    kesiapanData2 = curl.fetchall()
    curl.close()

    n = len(kesiapanData)
    X1 = sum(c[3] for c in kesiapanData)
    X2 = sum(c[4] for c in kesiapanData)
    Y = sum(c[5] for c in kesiapanData)
    X1Kuadrat = sum(c[3] * c[3] for c in kesiapanData)
    X2Kuadrat = sum(c[4] * c[4] for c in kesiapanData)
    Y2 = sum(c[5] * c[5] for c in kesiapanData)
    X1X2 = sum(c[3] * c[4] for c in kesiapanData)
    X1Y = sum(c[3] * c[5] for c in kesiapanData)
    X2Y = sum(c[4] * c[5] for c in kesiapanData)

    x1Kuadrat = X1Kuadrat - ((X1 * X1) / n)
    x2Kuadrat = X2Kuadrat - ((X2 * X2) / n)
    yKuadrat = Y2 - ((Y * Y) / n)
    x1y = X1Y - ((X1 * Y) / n)
    x2y = X2Y - ((X2 * Y) / n)
    x1x2 = X1X2 - ((X1 * X2) / n)

    # mencari nilai b1
    tempB1 = ((x2Kuadrat * x1y) - (x1x2 * x2y))
    b1 = tempB1 / ((x1Kuadrat * x2Kuadrat) - (x1x2 * x1x2))

    # mencari nilai b2
    tempB2 = ((x1Kuadrat * x2y) - (x1x2 * x1y))
    b2 = tempB2 / ((x1Kuadrat * x2Kuadrat) - (x1x2 * x1x2))

    # mencari nilai a
    a = (Y / n) - b1 * (X1 / n) - b2 * (X2 / n)

    return render_template('modelTerakhir.html', data=kesiapanData2, a=a, b1=b1, b2=b2, tahun=th, data2=kesiapanData)

@app.route('/grafik')
def grafik():
    th = request.args.get('th')
    query = "SELECT * FROM kesiapan"
    if (th):
        thSesudah = int(th) + 1
        query = "SELECT * FROM kesiapan WHERE tahun=" + str(thSesudah)
        query2 = "SELECT * FROM kesiapan WHERE tahun=" + str(th)
    curl = mysql.connection.cursor()
    curl.execute(query)
    kesiapanData = curl.fetchall()
    curl.execute(query2)
    kesiapanData2 = curl.fetchall()
    curl.close()

    n = len(kesiapanData)
    X1 = sum(c[3] for c in kesiapanData2)
    X2 = sum(c[4] for c in kesiapanData2)
    Y = sum(c[5] for c in kesiapanData2)
    X1Kuadrat = sum(c[3] * c[3] for c in kesiapanData2)
    X2Kuadrat = sum(c[4] * c[4] for c in kesiapanData2)
    Y2 = sum(c[5] * c[5] for c in kesiapanData2)
    X1X2 = sum(c[3] * c[4] for c in kesiapanData2)
    X1Y = sum(c[3] * c[5] for c in kesiapanData2)
    X2Y = sum(c[4] * c[5] for c in kesiapanData2)

    x1Kuadrat = X1Kuadrat - ((X1 * X1) / n)
    x2Kuadrat = X2Kuadrat - ((X2 * X2) / n)
    yKuadrat = Y2 - ((Y * Y) / n)
    x1y = X1Y - ((X1 * Y) / n)
    x2y = X2Y - ((X2 * Y) / n)
    x1x2 = X1X2 - ((X1 * X2) / n)

    # mencari nilai b1
    tempB1 = ((x2Kuadrat * x1y) - (x1x2 * x2y))
    b1 = tempB1 / ((x1Kuadrat * x2Kuadrat) - (x1x2 * x1x2))

    # mencari nilai b2
    tempB2 = ((x1Kuadrat * x2y) - (x1x2 * x1y))
    b2 = tempB2 / ((x1Kuadrat * x2Kuadrat) - (x1x2 * x1x2))

    # mencari nilai a
    a = (Y / n) - b1 * (X1 / n) - b2 * (X2 / n)

    bulan = [row[2] for row in kesiapanData]
    value = [row[5] for row in kesiapanData]
    value2 = [(a + (b1*row[3]) + (b2*row[4])) for row in kesiapanData]

    pe = [((abs(row[5] - abs(a + (b1 * row[3]) + (b2 * row[4]))) / row[5]) * 100) for row in kesiapanData]

    return render_template('grafik.html', data=kesiapanData2, a=a, b1=b1, b2=b2, tahun=th, data2=kesiapanData, value=value, bulan=bulan, value2=value2, pe=pe)

@app.route('/grafikModelTerbaik')
def grafikModelTerbaik():
    th = request.args.get('th')
    query = "SELECT * FROM kesiapan WHERE tahun=2019"
    query2 = "SELECT * FROM kesiapan WHERE tahun=2023"

    curl = mysql.connection.cursor()
    curl.execute(query)
    kesiapanData = curl.fetchall()
    curl.execute(query2)
    kesiapanData2 = curl.fetchall()
    curl.close()

    n = len(kesiapanData2)
    X1 = sum(c[3] for c in kesiapanData)
    X2 = sum(c[4] for c in kesiapanData)
    Y = sum(c[5] for c in kesiapanData)
    X1Kuadrat = sum(c[3] * c[3] for c in kesiapanData)
    X2Kuadrat = sum(c[4] * c[4] for c in kesiapanData)
    Y2 = sum(c[5] * c[5] for c in kesiapanData)
    X1X2 = sum(c[3] * c[4] for c in kesiapanData)
    X1Y = sum(c[3] * c[5] for c in kesiapanData)
    X2Y = sum(c[4] * c[5] for c in kesiapanData)

    x1Kuadrat = X1Kuadrat - ((X1 * X1) / n)
    x2Kuadrat = X2Kuadrat - ((X2 * X2) / n)
    yKuadrat = Y2 - ((Y * Y) / n)
    x1y = X1Y - ((X1 * Y) / n)
    x2y = X2Y - ((X2 * Y) / n)
    x1x2 = X1X2 - ((X1 * X2) / n)

    # mencari nilai b1
    tempB1 = ((x2Kuadrat * x1y) - (x1x2 * x2y))
    b1 = tempB1 / ((x1Kuadrat * x2Kuadrat) - (x1x2 * x1x2))

    # mencari nilai b2
    tempB2 = ((x1Kuadrat * x2y) - (x1x2 * x1y))
    b2 = tempB2 / ((x1Kuadrat * x2Kuadrat) - (x1x2 * x1x2))

    # mencari nilai a
    a = (Y / n) - b1 * (X1 / n) - b2 * (X2 / n)

    bulan = [row[2] for row in kesiapanData2]
    value = [(a + (b1 * row[3]) + (b2 * row[4])) for row in kesiapanData2]

    return render_template('grafikModelTerbaik.html', data=kesiapanData2, a=a, b1=b1, b2=b2, tahun=th, data2=kesiapanData,
                           value=value, bulan=bulan)

@app.route('/grafikModelTerakhir')
def grafikModelTerakhir():
    th = request.args.get('th')
    query = "SELECT * FROM kesiapan WHERE tahun=2022"
    query2 = "SELECT * FROM kesiapan WHERE tahun=2023"

    curl = mysql.connection.cursor()
    curl.execute(query)
    kesiapanData = curl.fetchall()
    curl.execute(query2)
    kesiapanData2 = curl.fetchall()
    curl.close()

    n = len(kesiapanData2)
    X1 = sum(c[3] for c in kesiapanData)
    X2 = sum(c[4] for c in kesiapanData)
    Y = sum(c[5] for c in kesiapanData)
    X1Kuadrat = sum(c[3] * c[3] for c in kesiapanData)
    X2Kuadrat = sum(c[4] * c[4] for c in kesiapanData)
    Y2 = sum(c[5] * c[5] for c in kesiapanData)
    X1X2 = sum(c[3] * c[4] for c in kesiapanData)
    X1Y = sum(c[3] * c[5] for c in kesiapanData)
    X2Y = sum(c[4] * c[5] for c in kesiapanData)

    x1Kuadrat = X1Kuadrat - ((X1 * X1) / n)
    x2Kuadrat = X2Kuadrat - ((X2 * X2) / n)
    yKuadrat = Y2 - ((Y * Y) / n)
    x1y = X1Y - ((X1 * Y) / n)
    x2y = X2Y - ((X2 * Y) / n)
    x1x2 = X1X2 - ((X1 * X2) / n)

    # mencari nilai b1
    tempB1 = ((x2Kuadrat * x1y) - (x1x2 * x2y))
    b1 = tempB1 / ((x1Kuadrat * x2Kuadrat) - (x1x2 * x1x2))

    # mencari nilai b2
    tempB2 = ((x1Kuadrat * x2y) - (x1x2 * x1y))
    b2 = tempB2 / ((x1Kuadrat * x2Kuadrat) - (x1x2 * x1x2))

    # mencari nilai a
    a = (Y / n) - b1 * (X1 / n) - b2 * (X2 / n)

    bulan = [row[2] for row in kesiapanData2]
    value = [(a + (b1 * row[3]) + (b2 * row[4])) for row in kesiapanData2]

    return render_template('grafikModelTerakhir.html', data=kesiapanData2, a=a, b1=b1, b2=b2, tahun=th, data2=kesiapanData,
                           value=value, bulan=bulan)

@app.route('/pengguna')
def pengguna():
    if 'loggedin' in session:
        curl = mysql.connection.cursor()
        curl.execute("SELECT * FROM user")
        admin = curl.fetchall()
        curl.close()
        return render_template('pengguna.html', data=admin)
    return redirect(url_for('login'))

@app.route('/tambahPengguna', methods=['POST', 'GET'])
def tambahPengguna():
    msg = ''
    psn = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        level = request.form['level']
        confirmed = False

        curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        curl.execute('SELECT * FROM user WHERE username = %s', (username,))
        user = curl.fetchone()
        if user:
            psn = 'Account already exists !'
        elif not re.match(r'[^@]+@[student]+\.[polinema]+\.[ac]+\.[id]+', email):
            psn = 'Invalid email address! Please use institutional account.'
        elif not re.match(r'[A-Za-z0-9]+', username):
            psn = 'Username must contain only characters and numbers !'
        elif not username or not password or not email or not level:
            psn = 'Please fill out the form !'
        else:
            curl.execute('INSERT INTO user VALUES (NULL, %s, %s, %s, %s, %s)',
                         (username, email, password, level, confirmed,))
            mysql.connection.commit()

            token = s.dumps(email, salt='email-confirm')
            msg = Message('Confirm Email', sender='sistemprediksi2022@gmail.com', recipients=[email])
            link = url_for('confirm_email', token=token, _external=True)
            msg.body = "To activate your account, please click the link below: {} \n".format(
                link) + "\nThis link will expire in 1 hour, so please confirm as soon as possible." \
                        "\n\nThank You, \nSistem Prediksi Kesiapan Operasional Pesawat Tempur"
            msg.subject = "Please, confirm your email address"
            mail.send(msg)

            psn = 'You have successfully registered! Check your email address.'
            return redirect(url_for('pengguna', psn=psn))

    elif request.method == 'POST':
        psn = 'Please fill out the form !'
    return redirect(url_for('pengguna', msg=msg))

@app.route('/ubahPengguna', methods=['POST', 'GET'])
def ubahPengguna():
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'level' in request.form:
        id_user = request.form['id_user']
        username = request.form['username']
        password = request.form['password']
        level = request.form['level']

        curl = mysql.connection.cursor()
        curl.execute('UPDATE user SET username=%s, password=%s, level=%s WHERE id_user=%s', (username, password, level, id_user))
        mysql.connection.commit()
    return redirect(url_for('pengguna'))

@app.route('/hapusPengguna/<string:id_user>', methods=['GET'])
def hapusPengguna(id_user):
    curl = mysql.connection.cursor()
    curl.execute("DELETE FROM user WHERE id_user=%s", [id_user])
    mysql.connection.commit()
    return redirect(url_for('pengguna'))

if __name__ == '__main__':
    app.run()