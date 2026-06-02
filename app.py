from flask import Flask, render_template, request, session, redirect
import sqlite3

app = Flask(__name__)
app.secret_key = "songman_secret_key"

cart = []

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


@app.route("/pay")
def pay():
    return render_template("pay.html")


@app.route("/detail/<int:product_id>")
def detail(product_id):


    products = {
        1: {
            "name": "오버핏 반팔 셔츠",
            "price": "49,000원",
            "image": "img1.jpg"
        },

        2: {
            "name": "와이드 데님 팬츠",
            "price": "59,000원",
            "image": "img2.jpg"
        },

        3: {
            "name": "미니멀 블레이저",
            "price": "89,000원",
            "image": "img3.jpg"
        },
        4: {
            "name": "오버핏 셔츠",
            "price": "39,000원",
            "image": "img4.jpg"
        },

        5: {
            "name": "미니멀 니트",
            "price": "49,000원",
            "image": "img5.jpg"
        },

        6: {
            "name": "반팔 티셔츠",
            "price": "29,000원",
            "image": "img6.jpg"
        },
        7: {
            "name": "와이드 슬랙스",
            "price": "49,000원",
            "image": "img7.jpg"
        },

        8: {
            "name": "데님 팬츠",
            "price": "59,000원",
            "image": "img8.jpg"
        },

        9: {
            "name": "조거 팬츠츠",
            "price": "35,000원",
            "image": "img9.jpg"
        }       
                    }

    product = products[product_id]

    return render_template(
        "detail.html",
        product=product,
        product_id=product_id
    )


@app.route("/add_cart/<int:product_id>")
def add_cart(product_id):

    products = {
        1: {
            "name": "오버핏 반팔 셔츠",
            "price": "49,000원",
        },

        2: {
            "name": "와이드 데님 팬츠",
            "price": "59,000원",
        },

        3: {
            "name": "미니멀 블레이저",
            "price": "89,000원",
        },
        4: {
            "name": "오버핏 셔츠",
            "price": "39,000원",
        },

        5: {
            "name": "미니멀 니트",
            "price": "49,000원",
        },

        6: {
            "name": "반팔 티셔츠",
            "price": "29,000원",
        },
        7: {
            "name": "와이드 슬랙스",
            "price": "49,000원",
        },

        8: {
            "name": "데님 팬츠",
            "price": "59,000원",
        },

        9: {
            "name": "조거 팬츠츠",
            "price": "35,000원",
        }       
    }

    cart.append(products[product_id])

    return redirect("/cart")

@app.route("/cart")
def cart_page():

    return render_template(
        "cart.html",
        cart=cart
    )

if __name__ == "__main__":
    app.run(debug=True)