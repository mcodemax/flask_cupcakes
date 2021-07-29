"""Flask app for Cupcakes"""


from flask import Flask, request, render_template, redirect, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Cupcake
from flask_cors import CORS
import os



app = Flask(__name__)
CORS(app) #https://flask-cors.readthedocs.io/en/latest/
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql://postgres:myPassword@localhost:5433/cupcakes')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True #prints in ipython the queries being run

app.config["SECRET_KEY"] = os.environ.get('SECRET_KEY', 'idkpassword')
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
# debug = DebugToolbarExtension(app)


connect_db(app)
db.create_all()

@app.route('/')
def home():
    """return html that shows all cupcakes"""
    
    #returns empty page w/ 1.button that lists all cupcakes via js and 2. has a form that uses axios to submit request to add new cupcake
    return render_template('index.html')

@app.route('/api/cupcakes')
def all_cupcakes_info():
    """return jsonified list of all cupcakes"""

    cupcakes = Cupcake.query.all()

    # list comprehension python
    serialized_cupcakes = [cupcake.serialize_cupcake() for cupcake in cupcakes]

    return jsonify(cupcakes=serialized_cupcakes)

@app.route('/api/cupcakes', methods=["POST"])
def add_cupcake_to_db():
    """add a cupcake to db"""

    flavor = request.json["flavor"]
    size = request.json["size"]
    rating = request.json["rating"]
    image = request.json["image"]

    cupcake = Cupcake(flavor=flavor, size=size, rating=rating, image=image)
    db.session.add(cupcake)
    db.session.commit()

    return (jsonify(cupcake=cupcake.serialize_cupcake()), 201)

    #add 201 for successful post request code

@app.route('/api/cupcakes/<int:cupcake_id>')
def cupcake_info(cupcake_id):
    """get info about an indiv cupcake"""
    
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    serialized_cupcake = cupcake.serialize_cupcake()

    return jsonify(cupcake=serialized_cupcake)

@app.route('/api/cupcakes/<int:cupcake_id>', methods=["PATCH"])
def update_cupcake(cupcake_id):
    """Update cupcake info"""
    
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    
    res = request.get_json()
    
    cupcake.flavor = res.get('flavor', cupcake.flavor)
    cupcake.size = res.get('size', cupcake.size)
    cupcake.rating = res.get('rating', cupcake.rating)
    cupcake.image = res.get('image', cupcake.image)

    db.session.commit()
    serialized_cupcake = cupcake.serialize_cupcake()
    
    return jsonify(cupcake=serialized_cupcake)




@app.route('/api/cupcakes/<int:cupcake_id>', methods=["DELETE"])
def delete_cupcake(cupcake_id):
    """Delete a cupcake in database"""
    
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    db.session.delete(cupcake)
    db.session.commit()
    
    return jsonify({'message': 'deleted'}) #single or double quotes?

