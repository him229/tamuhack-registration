from resources import person, parser
from flask import Flask, render_template, request, redirect
from flask_pymongo import PyMongo
from pymongo import MongoClient

"""
note: in mongo, a document is a an object or a row, and a collection is a table
a column represents a key in the databse and values are analgous

note: in flask-pymongo, the name of this file must be the same name as the databse at hand, in this case, test.
"""

# creating a person instance
# note: we need to discuss how the person object will be utilized, right now its not being used
app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'hackdb'
app.config['MONGO_URI'] = 'mongodb://tamuhack17:Tamuhackdb17@ds147979.mlab.com:47979/hackdb'
mongo = PyMongo(app)


@app.route('/')
def home_page():
    # we can get info from a mongo document
    print str(mongo.db.people.find_one({}))
    count = mongo.db.people.count({})
    return render_template('home.html', count=count)


# route that handles buttons on the home page
@app.route("/modify", methods=['GET', 'POST'])
def modify():
    if request.method == 'POST':
        if request.form['action'] == 'add':
            fname = request.form['fname_add']
            lname = request.form['lname_add']
            email = request.form['email_add']
            mongo.db.people.insert({"first_name": fname, "last_name": lname, "email": email})
            print str(mongo.db.people.find_one({}))
            count = mongo.db.people.count({})
            return render_template('add_delete.html', count=count)
        elif request.form['action'] == 'delete':
            b = request.form['fname_delete']
            mongo.db.people.delete_one({"first_name": b})
            count = mongo.db.people.count({})
            return render_template('add_delete.html', count=count)
    elif request.method == 'GET':
        count = mongo.db.people.count({})
        return render_template('add_delete.html', count=count)

@app.route('/participants')
def participants():
    count = mongo.db.people.count({})
    entries = list(mongo.db.people.find({}))
    query = request.args.get('q', '')
    if query:
        entries = mongo.db.people.find({'$or': [{"first_name": {'$regex': '.*' + query + '.*'}},
                                                {"last_name": {'$regex': '.*' + query + '.*'}},
                                                {"email": {'$regex': '.*' + query + '.*'}}
                                                ]})

    return render_template('results.html', count=count, entries=entries, query=query)

@app.route("/upload", methods=['GET', 'POST'])
def upload():
    if request.method == 'GET':
        count = mongo.db.people.count({})
        return render_template('upload.html', count=count)
    if request.method == 'POST':
        #when we receive a post reqeust, we need to take the text, convert them to python objects and add these as mm_document
        #note: if there happens to be a repeat, we must consider this and simply overwrite the new information, not a add new
        count = mongo.db.people.count({})
        pars = parser.Parser(request.form['schema'])
        print request.form['csv'].splitlines()
        return render_template('upload.html', count=count)


if __name__ == "__main__":
    app.run()