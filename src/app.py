from flask import Flask,render_template,redirect,url_for,session,request,send_from_directory
from werkzeug.utils import secure_filename
import pyrebase
import os
config = {
  "apiKey": "AIzaSyC7SNbTSUQlm3iJJ18ix5EoHNAVnCP53_k",
  "authDomain": "befrsher-34882.firebaseapp.com",
  "databaseURL": "https://befrsher-34882-default-rtdb.firebaseio.com/",
  "projectId": "befrsher-34882",
  "storageBucket": "befrsher-34882.appspot.com",
  "messagingSenderId": "959663258260",
  "appId": "1:959663258260:web:cdcca535c355ef88811281",
  "measurementId": "G-N9DHD5Q49G"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()
app = Flask(__name__)
app.secret_key = 'saraswat'
storage = firebase.storage()


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        name = request.form['name']
        try:
            user=auth.create_user_with_email_and_password(email,password)
            auth.update_profile(user['idToken'],display_name=name)
            return redirect('/login')
        except:
            return 'Error creating account'
    else:
        return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            user=auth.sign_in_with_email_and_password(email, password)
            session['user']={
                'name':user['displayName'],
                'email':user['email'],
                'uid':user['localId']
            }
            return redirect('/dashboard')
        except:
            return 'Invalid email or password'
    else:
        return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')

@app.route('/dashboard')
def dashboard():
    if 'user' in session:
        user=session['user']
        print(user)
        db.child('users').child(user['uid']).set({"email":user['email'],'name':user['name']})
        return render_template('dashboard.html',user=user)
    else:
        return redirect('/login')

@app.route('/addData',methods=['GET','POST'])
def AddData():
    if request.method == 'POST':
        file = request.files['file']
        front = request.files['front']
        back = request.files['back']
        shopName = request.form['name']
        landmark = request.form['landmark']
        ownerName = request.form['owner']
        park = str(request.form.get('park'))
        estyear=str(request.form.get('estyear'))
        phone = request.form['phone']
        apparels = str(request.form.get('apparels'))
        marketplace=str(request.form.get('Marketplace'))
        price = str(request.form.get('Price'))
        inventorymng=str(request.form.get('InventoryManagment'))
        challenge = str(request.form.get('challenge'))
        hiring=str(request.form.get('hiring'))
        platforms = str(request.form.get('platforms'))
        transaction=str(request.form.get('transaction'))
        spending = str(request.form.get('spending'))
        mindset=str(request.form.get('mindset'))
        size = str(request.form.get('size'))
        infrastructure=str(request.form.get('infrastructure'))
        filename = secure_filename(file.filename)
        print(file,front,back)
        print(apparels,
        marketplace,
        price,
        inventorymng,
        challenge,
        hiring,
        platforms,
        transaction,
        spending,
        mindset,
        size,
        infrastructure)
        frontfilename = secure_filename(front.filename)
        backfilename = secure_filename(back.filename)
        print(filename,frontfilename,backfilename)
        basedir = os.path.abspath(os.path.dirname(__file__))
        file.save(os.path.join(basedir,filename))
        front.save(os.path.join(basedir,frontfilename))
        back.save(os.path.join(basedir,backfilename))
        storage.child('befrsher-'+filename).put(filename)
        storage.child('befrsher-'+frontfilename).put(frontfilename)
        storage.child('befrsher-'+backfilename).put(backfilename)
        os.remove(os.path.join(basedir,filename))
        os.remove(os.path.join(basedir,frontfilename))
        os.remove(os.path.join(basedir,backfilename))
        db.child('data').child(shopName).set({
            'shopname':shopName,
            'owner':ownerName,
            'landmark':landmark,
            'parking':park,
            'EstYear':estyear,
            'Whatsappnumber':phone,
            'categories':apparels,
            'marketplace':marketplace,
            'price':price,
            'spending':spending,
            'inventory':inventorymng,
            'challenge':challenge,
            'hiring':hiring,
            'platforms':platforms,
            'transaction':transaction,
            'mindset':mindset,
            'size':size,
            'infrasrtucture':infrastructure})
        return render_template('dashboard.html')


    
if __name__=='__main__':
    app.run(debug=True)
