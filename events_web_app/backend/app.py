from flask import Flask, jsonify, send_from_directory
from json import JSONDecodeError
import json
import os
from pathlib import Path
import boto3


WEB_APP_DIR = os.environ.get('WEB_APP_DIR', Path(__file__).parent.parent) 
app = Flask(__name__, static_folder=os.path.join(WEB_APP_DIR, "frontend/build"))


def get_jsonl_from_s3(bucket_name, city, date):
    session = boto3.Session(
        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'),
    )

    s3 = session.resource('s3')
    # List the objects within the specified folder
    bucket = s3.Bucket(bucket_name)
    objects = bucket.objects.all()
    

    data_list = []

    for s3_object in [obj for obj in objects if (city in obj.key) and (date in obj.key)]:
        obj = s3.Object(bucket_name, s3_object.key)
        response = obj.get()
        file_content = response['Body'].read().decode('utf-8')
        try:
            # Split the content by lines and load each line as a JSON
            for line in file_content.strip().split('\n'):
                data = json.loads(line)
                
                # exclude all the wochenmarkt 
                if 'wochenmarkt' in data.get('title','').lower():
                    continue

                data_list.append(data)
        except JSONDecodeError:
            print(f'The s3 object {s3_object.key} seems to be empty.')


    return data_list


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')


@app.route('/events/<city>/<date>', methods=['GET'])
def get_events(city, date):

    combined_events = get_jsonl_from_s3('chirashi-events', city, date)
    return jsonify(combined_events)
    

if __name__ == "__main__":
    app.run(debug=True)
