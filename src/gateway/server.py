import os, gridfs, pika, json
from re import L
from flask import Flask, request
from flask_pymongo import PyMongo
from auth_svc import access
from storage import util


server = Flask(__name__)

server.config['MONGO_URI'] = 'mongo://host.minikube.internal:27017/videos'

# pymongo is a wrapper that abstracts the db access logic for accessing mongodb
mongo = PyMongo(server)

# gridfs is used in mongodb when we need to store documents that are larger than 16mb. gridfs uses sharding to split the file into chunks
# and stores them in 2 collections; one for the chunks and one for metadata that is used to reassemble the file
fs = gridfs.GridFS(mongo.db)

pika = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq"))
channel = pika.channel()

@server.route('/login', methods=['POST'])
def login():
    
    token, err = access.login(request)

    if not err:
        return token
    else:
        return err
    

@server.route('/upload', methods=['POST'])
def upload():
    
    data, err = access.validate_token(request) 
    
    data = json.loads(data)
    
    if data["admin"]:
        #make sure there is a file being uploaded. if there is a file, len of request.files dict will be greater than 0
        
        #make sure there is exactly one file
        if len(request.files) > 1 or len(request.files) < 1:
            return "please upload exactly 1 file", 400
        
        for _, f in request.files.items():
            err =  util.upload(f, fs, channel, data)
            
            if err:
                return err
        
        return "success", 200
    else:
        return "not authorized", 401
    

@server.route("/download", methods=["POST"])
def download():
    pass


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=8080)

            
