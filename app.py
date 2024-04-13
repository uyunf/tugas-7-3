import os
from os.path import join, dirname
from dotenv import load_dotenv
from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
from datetime import datetime 

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MONGODB_URI = os.environ.get("MONGODB_URI")
DB_NAME =  os.environ.get("DB_NAME")

client = MongoClient(MONGODB_URI)

db = client[DB_NAME]
# connection_string = 'mongodb+srv://test:sparta@cluster0.zfjim4j.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'
# client = MongoClient(connection_string)
# db = client.dbsparta

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/diary', methods=['get'])
def show_diary():
    # sample_receive = request.args.get('sample_give')
    # print(sample_receive)
    articles = list(db.diary.find({}, {'_id': False})) # membaca semua list yang ada di mongodb
    return jsonify({'articles': articles})

@app.route('/diary', methods=["post"])
def save_diary():
    # sample_receive = request.form.get('sample_give')
    # print(sample_receive)
    title_receive = request.form.get('title_give')
    content_receive = request.form.get('content_give')

    today = datetime.now()
    mytime = today.strftime('%y-%m-%d-%H-%M-%S')

    file = request.files['file_give']
    file_extension = file.filename.split('.')[-1]
    # save_to = 'static/myimage.jpg'
    filename = f'static/post-{mytime}.{file_extension}'
    file.save(filename)

    profile = request.files['profile_give']
    profile_extension = profile.filename.split('.')[-1]
    profilename = f'static/profile-{mytime}.{profile_extension}'
    profile.save(profilename)

    time = today.strftime('%y.%m.%d')

    doc = {
        'file': filename,
        'profile': profilename,
        'title': title_receive,
        'content': content_receive,
        'time': time,
    }
    db.diary.insert_one(doc)
    return jsonify({'message': 'data was saved'})

if __name__ =="__main__":
    app.run('0.0.0.0', port=5000, debug=True)
