from flask import Flask
from flask_restful import Api

import config


def create_app(config_name):
    '''Function to create a flask app depending on the configuration passed'''

    app = Flask(__name__)
    api = Api(app)

    app.config.from_object('config')
    app.url_map.strict_slashes = False

    from app.resources.orders import Order
    from app.resources.orders import Orders
    from app.resources.user import Signup
    from app.resources.user import Login

    api.add_resource(Order, '/api/v1/orders/<int:order_id>')
    api.add_resource(Orders, '/api/v1/orders')
    api.add_resource(Signup, '/api/v1/auth/signup')
    api.add_resource(Login, '/api/v1/auth/login')

    return app