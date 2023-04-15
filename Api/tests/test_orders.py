import unittest
from .. import create_app
from ..config.config import config_dict
from ..utils import db
from flask_jwt_extended import create_access_token
from ..models.orders import Order

class OrderTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config=config_dict["test"])
        
        self.appctx = self.app.app_context()

        self.appctx.push() 

        self.client = self.app.test_client()
    
    def tearDown(self):
        db.drop_all()

        self.appctx.pop()

        self.app = None

        self.client = None

    def test_get_all_orders(self):
        token = create_access_token(identity="Test User")
        headers = {
            "Authorization": f"Bearer {token}"
        }
        response =self.client.get("/orders/orders", headers=headers)

        assert response.status_code == 200
        assert response.json == []


    def test_create_order(self):
        data = {
            "size":"SMALL",
            "quantity": 1,
            "order_status":"PENDING",
            "flavour":"vanilla"

        }

        token = create_access_token(identity="Test User")
        headers = {
            "Authorization": f"Bearer {token}"
        }

        response = self.client.post("/orders/orders", json=data, headers=headers)
        assert response.status_code == 201

        #orders =Order.query.all()
        #assert len(orders) == []


    
