from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask('__name__')
app.secret_key = "rural_secret_key"


def get_db():
    conn = sqlite3.connect("rural.db")
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        conn = get_db()
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO users(username,email,password) VALUES(?,?,?)",
            (username, email, password)
        )

        conn.commit()
        conn.close()

        return redirect('/login')

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']

        conn = get_db()
        cur = conn.cursor()

        cur.execute(
            "SELECT * FROM users WHERE email=? AND password=?",
            (email, password)
        )

        user = cur.fetchone()
        conn.close()

        if user:
            session['username'] = user['username']
            return redirect('/dashboard')

    return render_template('login.html')


@app.route('/dashboard')
def dashboard():

    if 'username' not in session:
        return redirect('/login')

    return render_template(
        'dashboard.html',
        username=session['username']
    )


@app.route('/smart_farming')
def smart_farming():
    return render_template('smart_farming.html')


@app.route('/water_awareness')
def water_awareness():
    return render_template('water_awareness.html')


@app.route('/sanitation')
def sanitation():
    return render_template('sanitation.html')


@app.route('/feedback', methods=['GET', 'POST'])
def feedback():

    if request.method == 'POST':

        username = session.get('username', 'Guest')
        message = request.form['message']

        conn = get_db()
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO feedback(username,message) VALUES(?,?)",
            (username, message)
        )

        conn.commit()
        conn.close()

        return redirect('/dashboard')

    return render_template('feedback.html')


@app.route('/admin')
def admin():

    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT * FROM feedback")
    feedbacks = cur.fetchall()

    conn.close()

    return render_template(
        'admin.html',
        feedbacks=feedbacks
    )


@app.route('/logout')
def logout():

    session.clear()
    return redirect('/')


if __name__ =='__main__':
    app.run(debug=True)
