from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import OperationalError
from sqlalchemy import text



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:@localhost/flaskdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db=SQLAlchemy(app)

class Users(db.Model):
    __tablename__="users"
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(100))
    email=db.Column(db.String(100))
    password=db.Column(db.String(200))

@app.route('/all')
def hello():
    users=Users.query.all()
    return render_template("users.html",users=users)

@app.route('/listuser')
def alls_user():
    users=Users.query.first()
    return f"Username: {users.username}"

@app.route('/listalluser')
def all_user():
    users=Users.query.all()
    return render_template("users.html",users=users)

@app.route('/delete')
def delete(id):
    pass
# @app.route('/')
# def check_connection():
#     try:
#         db.session.execute(text("SELECT * from users"))
#         return "Connection to MySQL database successful!"
#     except OperationalError as e:
#         return f"Connection failed: {str(e)}"

 
@app.route('/')
def user_register():
    return render_template('register.html')
@app.route('/register', methods=['POST'])
def register_user():
    username=request.form['username']
    email=request.form['email']
    password=request.form['password']

    
    new_user= Users(username=username, email=email, password=password)
    db.session.add(new_user)
    db.session.commit()

    return f"{username} Data inserted."

@app.route('/updateuser/<int:id>')
def updateuser(id):
    user=Users.query.get(id)
    return render_template('updateuser.html',user=user)
    pass

@app.route('/update', methods=["POST"])
def updte(id):
    user=Users.query.get(id)
    user.username=request.form['username']
    user.email=request.form['email']
    user.password=request.form['password']
    db.session.add(user)
    db.session.commit()
    return redirect('listuser')



@app.route('/deleteuser/<int:id>')
def deleteuser(id):
    user=Users.query.get(id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return redirect('/listuser')
    

if __name__ =='__main__':
    app.run(debug=True)