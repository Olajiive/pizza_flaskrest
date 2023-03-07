from flask_restx import Namespace, Resource

order_namespace =Namespace("orders", description= "name space for order")

@order_namespace.route("/orders")
class OrderGetCreate(Resource):
    def get(self):
        """
            get all orders
        """
        pass

    def post(self):
        """
            place an order
        """
        pass
        
@order_namespace.route("/order/<int:order_id>")
class GetUpdateDelete(Resource):
    def get(self, order_id):
        """
           Retrieving an order by id
        """
        pass

    def put(self, order_id):
        """
           Update an order by id
        """
        pass

    def delete(self, order_id):
        """
           Delete an order by id
        """
        pass

@order_namespace.route('/user/<int:user_id>/order/<int:order_id>')
class GetSpecificOrderbyUser(Resource):
    def get(self, user_id,order_id):
        """
           Get a user specific order
        """
        pass

@order_namespace.route('/user/<int:user_id>/orders')
class GetSpecificOrderbyUser(Resource):
    def get(self):
        """
           Get all user orders
        """
        pass

@order_namespace.route('/Order/status/<int:order_id>')
class GetSpecificOrderbyUser(Resource):
    def patch(self, order_id):
        """
           Update an order status
        """

