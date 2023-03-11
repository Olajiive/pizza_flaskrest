from flask_restx import Namespace, Resource,fields
from ..models.orders import Order
from ..models.users import User
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request
from http import HTTPStatus

order_namespace =Namespace("orders", description= "name space for order")

order_model=order_namespace.model(
    "Order", {
        "id": fields.Integer(description="An ID"),
        "size":fields.String(description="Size of an Order", required=True, 
            enum =["SMALL", "MEDIUM", "LARGE", "EXTRA_LARGE"]
        ),
        "quantity":fields.String(description="Quantity of an Order", required=True),
        "flavour":fields.String(description="flavour of an order", required=True,
            enum=["VANILLA","APPLE","CHOCOLATE"]
        )
        
    }
)
@order_namespace.route("/orders")
class OrderGetCreate(Resource):
    @order_namespace.marshal_with(order_model)

    @jwt_required()
    def get(self):
        """
            get all orders
        """
        orders = Order.query.all()

        return orders, HTTPStatus.OK
    

    @order_namespace.expect(order_model)
    @order_namespace.marshal_with(order_model)
    @jwt_required()
    def post(self):
        """
            place an order
        """

        username= get_jwt_identity()

        current_user = User.query.filter_by(username=username).first()
        data = order_namespace.payload
        
        size= data.get("size")
        quantity=data.get("quantity")
        order_status = data.get("order_status")
        flavour = data.get("flavour")

        new_order=Order(size=size, quantity=quantity, order_status=order_status, flavour=flavour)
        
        new_order.user=current_user

        new_order.save()

        return new_order, HTTPStatus.CREATED
        
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

