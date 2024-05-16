from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///site.db"
db = SQLAlchemy(app)
migrate = Migrate(app, db)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(35), unique=False, nullable=False)


@app.route("/")
def hello():
    user_list = User.query.all()
    return render_template("index.html", user_list=user_list)

@app.route("/gunner/<int:user_id>")
def Gunner_details(user_id):
    user = User.query.get(user_id)
    return render_template("gunner_info.html", user=user)

@app.route("/add_gunner", methods=["POST", "GET"])
def AddGunner():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        user_obj = User(username=username, email=email)
        db.session.add(user_obj)
        db.session.commit()
        return redirect("/")
    else:
        return render_template("add_gunner.html")

    

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)