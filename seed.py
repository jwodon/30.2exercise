from flask import Flask
from models import db, Cupcake

app = Flask(__name__)

# Configure your app as needed (database URI, etc.)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the SQLAlchemy instance with the app
db.init_app(app)


def seed_data():
    with app.app_context():
        # Drop and recreate the tables
        db.drop_all()
        db.create_all()

        # Seed data
        c1 = Cupcake(
            flavor="cherry",
            size="large",
            rating=5,
        )

        c2 = Cupcake(
            flavor="chocolate",
            size="small",
            rating=9,
            image="https://www.bakedbyrachel.com/wp-content/uploads/2018/01/chocolatecupcakesccfrosting1_bakedbyrachel.jpg"
        )

        db.session.add_all([c1, c2])
        db.session.commit()

if __name__ == '__main__':
    seed_data()
