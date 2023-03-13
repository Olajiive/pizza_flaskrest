from flask_restx import Namespace, Resource,fields
from ..models.orders import Order
from ..models.users import User
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request
from ..utils import db
from http import HTTPStatus

order_namespace =Namespace("orders", description= "name space for order")

order_model=order_namespace.model(
    "Order", {
        "id": fields.Integer(description="An ID"),
        "size":fields.String(description="Size of an Order", required=True, 
            enum =["SMALL", "MEDIUM", "LARGE", "EXTRA_LARGE"]
        ),
        "order_status":fields.String(description="Status of an Order", required=True,
            enum=["PENDING", "IN_TRANSIT", "DELIVERED"]),
        "quantity":fields.String(description="Quantity of an Order", required=True),
        "flavour":fields.String(description="flavour of an order", required=True,
            enum=["VANILLA","APPLE","CHOCOLATE"]
        )
        
    }
)

order_status_model=order_namespace.model(
    "OrderStatus", {
         "order_status":fields.String(description="Status of an Order", required=True,
            enum=["PENDING", "IN_TRANSIT", "DELIVERED"])
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

    @order_namespace.marshal_with(order_model)
    @jwt_required()
    def get(self, order_id):
        """
           Retrieving an order by id
        """
        order = Order.get_by_id(order_id)
        return order, HTTPStatus.OK
    
    @order_namespace.expect(order_model)
    @order_namespace.marshal_with(order_model)
    @jwt_required()
    def put(self, order_id):
        """
           Update an order by id
        """
        order_to_update = Order.get_by_id(order_id)
        data=order_namespace.payload

        order_to_update.size= data.get("size")
        order_to_update.quantity=data.get("quantity")
        order_to_update.flavour = data.get("flavour")

        db.session.commit()

        return order_to_update, HTTPStatus.OK

    @jwt_required()
    def delete(self, order_id):
        """
           Delete an order by id
        """
        order = Order.get_by_id(order_id)

        db.session.delete(order)
        db.session.commit()

        return {"message": "Order has been succesfully deleted"}

@order_namespace.route('/user/<int:user_id>/order/<int:order_id>')
class GetSpecificOrderbyUser(Resource):
    @order_namespace.marshal_with(order_model)
    @jwt_required()
    def get(self, user_id,order_id):
        """
           Get a user specific order
        """
        user = User.get_by_id(user_id)

        order= Order.query.filter_by(id=order_id).filter_by(user=user).first()

        return order, HTTPStatus.OK

@order_namespace.route('/user/<int:user_id>/orders')
class GetSpecificOrderbyUser(Resource):
    @order_namespace.marshal_list_with(order_model)
    @jwt_required()
    def get(self, user_id):
        """
           Get all user orders
        """
        user=User.get_by_id(user_id)

        orders=user.orders

        return orders, HTTPStatus.OK



@order_namespace.route('/order/status/<int:order_id>')
class GetSpecificOrderbyUser(Resource):
    @order_namespace.expect(order_status_model)
    @order_namespace.marshal_with(order_model)
    @jwt_required()
    def patch(self, order_id):
        """
           Update an order status
        """
        order_to_update = Order.get_by_id(order_id)
        
        data=order_namespace.payload
        order_to_update.order_status=data.get("order_status")

        db.session.commit()

        return order_to_update, HTTPStatus.OK

