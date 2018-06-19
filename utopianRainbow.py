from flask import Flask, render_template, url_for
app = Flask(__name__)
# app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/aboutus/")
def aboutus():
    return render_template("aboutus.html")

@app.route("/ngo/")
def ngo():
    return render_template("ngo.html")

@app.route("/fellowship")
def fellowship():
    return render_template("fellowship.html")

@app.route("/community")
def community():
    return render_template("community.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/chineseIndex")
def chineseIndex():
    return render_template("chineseIndex.html")

if __name__ == "__main__":
    app.run(debug=True)