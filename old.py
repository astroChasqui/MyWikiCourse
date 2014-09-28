import os
import sqlite3
from flask import Flask, url_for, render_template, request, session, flash,\
                  redirect


app = Flask(__name__)
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'mywikicourse.db'),
                       DEBUG=True,
                       SECRET_KEY="development key",
                       USERNAME='admin',
                       PASSWORD='default'))


@app.route("/")
def courses():
    return render_template("courses.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        if request.form["username"] != app.config["USERNAME"]:
            error = "Invalid username"
        elif request.form["password"] != app.config["PASSWORD"]:
            error = "Invalid password"
    else:
        session["logged_in"] = True
        flash("You were logged in")
        return redirect(url_for("courses"))
    return render_template("login.html", error=error)

@app.route("/logout")
def logout():
    session.pop("logged_in", None)
    flash("You were logged out")
    return redirect(url_for("courses"))


from collections import OrderedDict
import wikipedia

@app.route("/course")
def course():

    hd = {"title"   : "The Solar System",
          "summary" : ("Solar System", "")}
    hd["text"] = getwikitext(hd["summary"][0], hd["summary"][1])

    sects = OrderedDict()
    sects["Meh! Mercury"] = ["Mercury_(planet)", "Naked-eye viewing"]
    sects["*Venus"] = ["Venus", ""]
    sects["Earth: out planet"] = ["Earth", ""]
    sects["Mars"] = ["Mars", ""]
    sects["Gas giant Jupiter"] = ["Jupiter", "Atmosphere"]
    sects["Pluto: no longer a planet!"] = ["Pluto", "Classification"]

    sects_text = {}
    for sect in sects.keys():
        sects_text[sect] = getwikitext(sects[sect][0], sects[sect][1])

    return render_template("course.html",
                           hd=hd, sects=sects, sects_text=sects_text
                          )

def getwikitext(page, section):
    wp = wikipedia.page(page)
    if section != "":
        return wp.section(section).split("\n")
    else:
        return wp.summary.split("\n")


if __name__ == "__main__":
  app.run()
