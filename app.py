from flask import Flask, request, redirect, render_template, jsonify
from models import db, connect_db, Cupcake

from flask_debugtoolbar import DebugToolbarExtension


app = Flask(__name__)

app.config['SECRET_KEY'] = "123456"

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

connect_db(app)

app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)

@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = 'http://127.0.0.1:5000'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, PATCH, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response

@app.route("/")
def root():
    """Render homepage."""

    cupcakes = Cupcake.query.all()
    return render_template("index.html", cupcakes=cupcakes)

@app.route("/api/cupcakes")
def list_all_cupcakes():
    """{cupcakes: [{id, flavor, size, rating, image},...]}"""

    cupcakes = Cupcake.query.all()
    cupcake_dict = [Cupcake.to_dict(c) for c in cupcakes]

    return jsonify(cupcakes=cupcake_dict)

@app.route("/api/cupcakes/<cupcake_id>")
def list_single_cupcake(cupcake_id):
    """{cupcakes: [{id, flavor, size, rating, image},...]}"""

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    cupcake_dict = Cupcake.to_dict(cupcake)

    return jsonify(cupcake=cupcake_dict)

@app.route("/api/cupcakes", methods=["POST"])
def create_cupcake():
    """Create cupcake from form data & return it.

    Returns JSON {cupcake: {id, flavor, size, rating, image}}
    """

    flavor = request.json["flavor"]
    size = request.json["size"]
    rating = request.json["rating"]
    image = request.json["image"] or None

    new_cupcake = Cupcake(flavor=flavor, size=size, rating=rating, image=image)

    db.session.add(new_cupcake)
    db.session.commit()

    cupcake_dict = Cupcake.to_dict(new_cupcake)

    # Return w/status code 201 --- return tuple (json, status)
    return ( jsonify(cupcake=cupcake_dict), 201 )


@app.route('/api/cupcakes/<int:cupcake_id>', methods=["PATCH"])
def update_cupcake(cupcake_id):
    """Updates a particular cupcake and responds w/ JSON of that updated cupcake {cupcake:{id,flavor,size,rating,image}}"""
    cupcake = Cupcake.query.get_or_404(cupcake_id)

    cupcake.flavor = request.json.get('flavor',  cupcake.flavor)
    cupcake.size = request.json.get('size',  cupcake.size)
    cupcake.rating = request.json.get('rating',  cupcake.rating)
    cupcake.image = request.json.get('image',  cupcake.image)

    db.session.add(cupcake)
    db.session.commit()

    return jsonify(cupcake=cupcake.to_dict())


@app.route('/api/cupcakes/<int:cupcake_id>', methods=["DELETE"])
def delete_todo(cupcake_id):
    """Deletes a particular cupcake"""
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    db.session.delete(cupcake)
    db.session.commit()
    return jsonify(message="Deleted")
