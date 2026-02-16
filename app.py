# flask quickstart for information on flask
from flask import Flask, g
import sqlite3

DATABASE = 'database.db'

# initialise app
app = Flask(__name__)


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


@app.route('/')
def home():
    # home page - just the id, maker, model and image url
    sql = """
                SELECT Phones.PhoneID,Makers.Name,Phones.Model,Phones.ImageURL 
                FROM Phones
                Join Makers ON Makers.MakerID=Phones.MakerID;"""
    results = query_db(sql)
    return str(results)


@app.route("/phone/<int:id>")
def phone(id):
    # one phone based on the id
    sql = """
                SELECT * FROM Phones 
                JOIN Makers ON Makers.MakerID=Phones.MakerID
                Where PhoneID = ?;"""
    result = query_db(sql, (id,), True)
    return str(result)


if __name__ == "__main__":
    app.run(debug=True)
