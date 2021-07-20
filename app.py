"""Flask app for Cupcakes"""

# from forms import AddPetForm, EditPetForm
from flask import Flask, request, render_template, redirect, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Cupcake



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:myPassword@localhost:5433/cupcakes' #@ people looking at this code; you may need to change on your own computer for code to work
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True #prints in ipython the queries being run

app.config["SECRET_KEY"] = "maxcode1"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)


connect_db(app)
db.create_all()


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

