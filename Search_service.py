from flask import Flask, Response, jsonify, request
import db

app = Flask(__name__)

# Methods executed via HTTP requests
@app.route('/person',
           methods=['PUT',
                    'POST',
                    'DELETE']
           )  # CRUD actions
def person_actions():
    person_name = request.args.get('name')  # passed parameter through HTTP request
    try:
        str(person_name)
    except Exception:
        return Response(
            "Bad request",
            status=400, )

    if request.method == 'POST' or request.method == 'PUT':

        coord_long = (request.args.get('longitude'))  # passed parameter through HTTP request
        coord_lat = (request.args.get('latitude'))  # passed parameter through HTTP request
        try:
            coord_lat = float(coord_lat)
            coord_long = float(coord_long)
        except Exception:
            return Response(
                "Bad request",
                status=400, )
        if request.method == 'POST':  # insert table (possibly create table, if doesn't exist)
            person = db.insert_pers(person_name, coord_long, coord_lat)
            return jsonify(person)

        elif request.method == 'PUT':  # update coordinates
            new_position = db.update_coords(person_name, coord_long, coord_lat)
            return jsonify(new_position)

    elif request.method == 'DELETE':
        one = db.del_one_pers(person_name)  # delete certain person in a table
        return jsonify(one)


@app.route('/persons', methods=['GET', 'DELETE'])  # read
def show_data():
    if request.method == 'GET':
        return jsonify(db.select_all())  # select all persons in the table

    elif request.method == 'DELETE':  # delete whole table
        return jsonify(db.del_all_pers())


@app.route('/persons_near',
           methods=['GET'])  # search nearest persons
def search_near():
    name = (request.args.get('name'))
    distance = (request.args.get('distance'))
    try:
        name = str(name)
        distance = int(distance)
        distance = float(distance)
    except Exception:
        return Response(
            "Bad request",
            status=400, )
    res = db.neighbours(name, distance)
    return jsonify(res)


if __name__ == '__main__':
    app.run(debug=True)
