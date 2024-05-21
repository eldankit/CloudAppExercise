from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import boto3
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///site.db"
db = SQLAlchemy(app)
migrate = Migrate(app, db)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(35), unique=False, nullable=False)


s3_client = boto3.client('s3')
S3_BUCKET = 'eldan-arsenal-buk1'
S3_KEY = 'Arsenal_FC.png'

def generate_presigned_url(bucket_name, object_key, expiration=3600):
    try:
        response = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': bucket_name, 'Key': object_key},
                                                    ExpiresIn=expiration)
    except Exception as e:
        print(e)
        return None
    return response

@app.route("/")
def hello():
    user_list = User.query.all()
    logo_url = generate_presigned_url(S3_BUCKET, S3_KEY)
    return render_template("index.html", user_list=user_list, logo_url=logo_url)

@app.route("/gunner/<int:user_id>")
def Gunner_details(user_id):
    user = User.query.get(user_id)
    logo_url = generate_presigned_url(S3_BUCKET, S3_KEY)
    return render_template("gunner_info.html", user=user, logo_url=logo_url)

@app.route("/hello")
def Gunner_hello():
    username = request.args.get("username")
    logo_url = generate_presigned_url(S3_BUCKET, S3_KEY)
    return render_template("gunner_hello.html", username=username, logo_url=logo_url)

@app.route("/add_gunner", methods=["POST", "GET"])
def AddGunner():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        user_obj = User(username=username, email=email)
        db.session.add(user_obj)
        db.session.commit()
        return redirect(url_for("Gunner_hello", username=username))
    else:
        logo_url = generate_presigned_url(S3_BUCKET, S3_KEY)
        return render_template("add_gunner.html", logo_url=logo_url)

    

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)