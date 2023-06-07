from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import or_



app = Flask(__name__)

# /// = relative path, //// = absolute path
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Pojistenec(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jmeno = db.Column(db.String(100))
    prijmeni = db.Column(db.String(100))
    datum_narozeni = db.Column(db.Date)
    pojistka = db.Column(db.String(100))


@app.route("/")
def home():
    pojistenci = Pojistenec.query.all()
    return render_template("base.html", pojistenci=pojistenci)

@app.route("/add", methods=["POST"])
def add():
    jmeno = request.form.get("jmeno") # vytáhnout ostatní hodnoty
    prijmeni = request.form.get("prijmeni")
    datum_narozeni = datetime.strptime(request.form.get("datum_narozeni"), "%Y-%m-%d") # datetime.strptime(request.form.get("datum_narozeni"), "%Y-%m-%d") request.form.get("datum_narozeni")
    pojistka = request.form.get("pojistka")


    novy_pojistenec =Pojistenec(jmeno=jmeno, prijmeni=prijmeni, datum_narozeni=datum_narozeni, pojistka=pojistka)
    # doplnit ostatní argumenty

    db.session.add(novy_pojistenec)
    db.session.commit()
    return redirect(url_for("home"))


@app.route("/databaze")
def databaze():
    databaze_pojistenci = Pojistenec.query.all()
    return render_template("databaze.html",databaze=databaze_pojistenci)


@app.route("/delete/<int:id>")

def delete(id):
    novy_pojistenec = Pojistenec.query.get(id)

    if novy_pojistenec:
        db.session.delete(novy_pojistenec)
        db.session.commit()
        return redirect(url_for("home"))
    else:
        return "Pojištenec nenalezen"


@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        search_query = request.form.get("search_query")
        search_results = Pojistenec.query.filter(
            or_(
                Pojistenec.jmeno.ilike(f"%{search_query}%"),
                Pojistenec.prijmeni.ilike(f"%{search_query}%"),
                Pojistenec.datum_narozeni.ilike(f"%{search_query}%"),
                Pojistenec.pojistka.ilike(f"%{search_query}%")
            )
        ).all()
        return render_template("search.html", search_results=search_results, search_query=search_query)
    return render_template("search.html")


@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    novy_pojistenec = Pojistenec.query.get(id)

    if request.method == "POST":
        pojistka = request.form.get("pojistka")
        novy_pojistenec.pojistka = pojistka
        db.session.commit()
        return redirect(url_for("home"))

    return render_template("edit.html", pojistenec=novy_pojistenec)



if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(debug=True)
