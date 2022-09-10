from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__) 
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
db = SQLAlchemy(app)

class Mood(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mood = db.Column(db.String(2), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return "<Task %r>" % self.id


@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        mood = request.form["rating"]
        description = request.form["description"]
        new_mood = Mood(mood=mood, description=description)

        try:
            db.session.add(new_mood)
            db.session.commit()
            return redirect("/")

        except: 
            return "There was an issue adding your task"

    else:
        moods = Mood.query.order_by(Mood.date_created).all()
        return render_template("index.html", moods=moods)

@app.route("/delete/<int:id>")
def delete(id):
    row_to_delete = Mood.query.get_or_404(id)

    try:
        db.session.delete(row_to_delete)
        db.session.commit()
        return redirect("/")
    except:
        return "There was a problem deleting that row"

@app.route("/update/<int:id>", methods=["POST", "GET"])
def update(id):
    mood = Mood.query.get_or_404(id)

    if request.method == "POST":
        mood.rating = request.form["rating"]
        mood.description = request.form["description"]
        try:
            db.session.commit()
            return redirect("/")
        except:
            return "There was an issue updating this row"

    else:
        return render_template("update.html", mood=mood)


if __name__ == "__main__":
    app.run(debug=True)

print(__name__)