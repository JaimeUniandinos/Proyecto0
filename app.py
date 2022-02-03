import re
from flask import Flask
from flask import jsonify,request
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    return app

app = create_app()
CORS(app)

db={}
@app.route('/users', methods=['POST'])
def create_user():
    email=request.json["email"]
    password=request.json["password"]
    db[email]={"email":email, "password":password,"events":[]}

    return jsonify(db)

@app.route('/login', methods=['POST'])
def login_user():
    email=request.json["email"]
    password=request.json["password"]
    loged=False
    if email in db:
        if db[email]["password"]==password:
            loged= True

    return jsonify(loged)

@app.route('/event', methods=['POST'])
def create_event():
    name=request.json["name"]
    hora=request.json["hora"]
    email=request.json["email"]
    db[email]["events"].append({"name":name,"hora":hora})

    return jsonify(db)

@app.route('/delete/event', methods=['POST'])
def delete_event():
    email=request.json["email"]
    name=request.json["name"]
    index=-1
    for idx,event in enumerate(db[email]["events"]):
        if event["name"]==name:
            index=idx
    if index!=-1:
        db[email]["events"].pop(index)


    return jsonify(db)
@app.route('/edit/event', methods=['POST'])
def edit_event():
    name=request.json["name"]
    hora=request.json["hora"]
    email=request.json["email"]
    index=-1
    for idx,event in enumerate(db[email]["events"]):
        if event["name"]==name:
            index=idx
    if index!=-1:
        db[email]["events"][index]["hora"]=hora

    return jsonify(db)

@app.route('/show/event', methods=['POST'])
def show_event():
    name=request.json["name"]
    email=request.json["email"]
    index=-1
    for idx,event in enumerate(db[email]["events"]):
        if event["name"]==name:
            index=idx
    hora=""
    if index!=-1:
        hora=db[email]["events"][index]["hora"]

    return jsonify(hora)

@app.route('/show/events', methods=['POST'])
def show_events():
    
    email=request.json["email"]
    events=db[email]["events"]

    return jsonify(events)

if __name__ == '__main__':
    app.run(port=5000,debug=True)