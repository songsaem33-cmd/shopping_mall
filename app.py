from flask import Flask, render_template, request, session, redirect
import sqlite3

app = Flask(__name__)
app.secret_key = "songman_secret_key"


# DB 생성
def create_table():
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        userid TEXT,
        email TEXT,
        password TEXT
    )
    """)

    conn.commit()
    conn.close()


create_table()


@app.route("/")
def home():

    userid = session.get("userid")

    return render_template(
        "index.html",
        userid=userid
    )
    

@app.route("/signup", methods=["GET", "POST"])
def signup():

    if request.method == "POST":

        userid = request.form["userid"]
        email = request.form["email"]
        password = request.form["password"]
        password_confirm = request.form["password_confirm"]

        if password != password_confirm:
            return "비밀번호가 일치하지 않습니다."

        conn = sqlite3.connect("database.db")
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO users(userid,email,password) VALUES(?,?,?)",
            (userid, email, password)
        )

        conn.commit()
        conn.close()

        return redirect("/login")

    return render_template("signup.html")


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        userid = request.form["userid"]
        password = request.form["password"]

        conn = sqlite3.connect("database.db")
        cur = conn.cursor()

        cur.execute(
            "SELECT * FROM users WHERE userid=? AND password=?",
            (userid, password)
        )

        user = cur.fetchone()

        print("조회결과:", user)

        conn.close()

        if user:
            session["userid"] = userid
            print("로그인 성공")
            return redirect("/")

        else:
            print("로그인 실패")
            return "아이디 또는 비밀번호가 틀렸습니다."

    return render_template("login.html")

@app.route("/logout")
def logout():

    session.pop("userid", None)

    return redirect("/")


@app.route("/top")
def top():
    return render_template("top.html")


@app.route("/pants")
def pants():
    return render_template("pants.html")


@app.route("/detail")
def detail():
    return render_template("detail.html")


@app.route("/pay")
def pay():
    return render_template("pay.html")


if __name__ == "__main__":
    app.run(debug=True)