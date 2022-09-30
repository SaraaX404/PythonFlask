from flask import Flask, Response, request
import pymongo
import json
from bson.objectid import ObjectId

app = Flask('__name__')


try:
    mongo = pymongo.MongoClient(
        "mongodb+srv://machine:DmSBqJXsSTYfDRbY@cluster0.mthll.mongodb.net/flask_app?retryWrites=true&w=majority"
    )
    db = mongo.flask_app
    mongo.server_info()
except Exception as ex:
    print("************")
    print(ex)


@app.route('/users', methods=['POST'])
def create_user():
    try:
        user = {"name": request.form['name'],
                "lastName": request.form['lastName']}

        adResponse = db.users.insert_one(user)
        print(adResponse.inserted_id)
        return Response(
            response=json.dumps({"message": "user created",
                                 "id": f"{adResponse.inserted_id}"}),
            status=200,
            mimetype="application/json"
        )
    except Exception as ex:
        print(ex)


@app.route('/users', methods=['GET'])
def get_users():
    try:
        data = list(db.users.find())
        for user in data:
            user['_id'] = str(user["_id"])
        print(data)
        return Response(
            response=json.dumps(data),
            status=500,
            mimetype="application/json"
        )

    except Exception as ex:
        print(ex)
        return Response(
            response=json.dumps({"message": "user cannot be get"}),
            status=500,
            mimetype="application/json"
        )


@app.route('/users/<id>', methods=['PATCH'])
def updateUser(id):
    print(request.form['name'])
    try:
        dbResponse = db.users.update_one(
            {"_id": ObjectId(id)},
            {"$set": {"name": request.form["name"]}}
        )
        if dbResponse.modified_count == 1:
            return Response(
                response=json.dumps({"message": "user updated",
                                     "data": f"{dbResponse._UpdateResult__raw_result}"}),
                status=200,
                mimetype="application/json"
            )
        else:
            return Response(
                response=json.dumps({"message": "Nothing to be updated",
                                     "data": f"{dbResponse._UpdateResult__raw_result}"}),
                status=200,
                mimetype="application/json"
            )

    except Exception as ex:
        print("************")
        print(ex)
        print("************")
        return Response(
            response=json.dumps({"message": "user cannot be updated"}),
            status=500,
            mimetype="application/json"
        )


@app.route('/users/<id>', methods=['DELETE'])
def deleteUser(id):
    try:
        if ObjectId(id):
            dbResponse = db.users.delete_one({"_id": ObjectId(id)})
            if dbResponse.deleted_count == 1:
                return Response(
                    response=json.dumps(
                        {"message": "User Deleted", "id": f"{id}"}),
                    status=200,
                    mimetype="application/json"
                )
            else:
                return Response(
                    response=json.dumps(
                        {"message": "No user allocated with ID", "id": f"{id}"}),
                    status=200,
                    mimetype="application/json"
                )

        else:
            return Response(
                response=json.dumps(
                    {"message": "This ID is not valid object ID", "id": f"{id}"}),
                status=200,
                mimetype="application/json"
            )

    except Exception as ex:
        print("************")
        print(ex)
        print("************")
        return Response(
            response=json.dumps({"message": "user cannot be Deleted"}),
            status=500,
            mimetype="application/json"
        )


if __name__ == "__main__":
    app.run(port=4500, debug=True)
