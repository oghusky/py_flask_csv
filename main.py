import csv
import subprocess
import sys

try:
    from flask import Flask, jsonify, request
except ImportError:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'flask'])
finally:
    from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route('/people', methods=['GET'])
def get_all_people():
    with open('db.csv', 'r') as people_file:
        file = csv.reader(people_file)
        next(people_file)
        people = []
        for item in file:
            try:
                people.append({
                    "id": int(item[0].strip()),
                    "name": item[1].strip(),
                    "age": int(item[2].strip()),
                    "email": item[3].strip(),
                })
            except:
                pass
        return jsonify({'people': people, 'msg': "Found all people", "status": 200})


@app.route('/people/<age>', methods=['GET'])
def get_over_age_twoone(age):
    with open('db.csv', 'r') as people_file:
        file = csv.reader(people_file)
        next(people_file)
        people = []
        for item in file:
            if int(item[2]) > int(age):
                people.append({
                    "id": int(item[0].strip()),
                    "name": item[1].strip(),
                    "age": int(item[2].strip()),
                    "email": item[3].strip(),
                })
        return jsonify({'people': people})


@app.route('/people', methods=['POST'])
def post_add_person():
    id = request.form['id']
    name = request.form['name']
    age = request.form['age']
    email = request.form['email']
    if id != '' and name != '' and age != '' and email != '':
        var_list = [id, name, age, email]
        with open('db.csv', 'a', newline='') as people_file:
            writer_object = csv.writer(people_file)
            writer_object.writerow(var_list)
            # add comma at the end of return statement to get correct status code in postman
            return jsonify({"msg": "New Person Added", "status": 201}), 201
    else:
        return jsonify({"msg": "All fields required", "status": 500})


if __name__ == '__main__':
    app.run(debug=True)
