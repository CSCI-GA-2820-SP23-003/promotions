"""
TestPromotion API Service Test Suite

Test cases can be run with the following:
  nosetests -v --with-spec --spec-color
  coverage report -m
"""
import os
import logging
from unittest import TestCase
#from unittest.mock import MagicMock, patch
from service import app
from service.models import db,init_db,Promotion
from service.common import status  # HTTP Status Codes
from tests.factories import PromotionFactory

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql://postgres:postgres@localhost:5432/testdb"
)
BASE_URL = "/promotion"

######################################################################
#  T E S T   C A S E S
######################################################################
class TestYourResourceServer(TestCase):
    """ REST API Server Tests """

    @classmethod
    def setUpClass(cls):
        """ This runs once before the entire test suite """
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        # Set up the test database
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        init_db(app)
        
        
    @classmethod
    def tearDownClass(cls):
        """ This runs once after the entire test suite """
        db.session.close()


    def setUp(self):
        """ This runs before each test """
        self.client = app.test_client()
        db.session.query(Promotion).delete()  # clean up the last tests
        db.session.commit()


    def tearDown(self):
        """ This runs after each test """
        db.session.remove()

    ######################################################################
    #  P L A C E   T E S T   C A S E S   H E R E
    ######################################################################


    def _create_promotion(self, count):
        """Factory method to create promotions in bulk"""
        promotions = []
        for _ in range(count):
            test_promo = PromotionFactory()
            response = self.client.post(BASE_URL, json=test_promo.serialize())
            self.assertEqual(
                response.status_code, status.HTTP_201_CREATED, "Could not create test Promotion"
            )
            new_pet = response.get_json()
            test_promo.id = new_pet["id"]
            promotions.append(test_promo)
        return promotions





    def test_index(self):
        """ It should call the home page """
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)


    def test_create_promotion(self):
        """It should create a new promotion"""
        test_promo=PromotionFactory()
        logging.debug("Test Promotion: %s", test_promo.serialize())
        response = self.client.post(BASE_URL, json=test_promo.serialize())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        #location = response.headers.get("Location", None)
        #self.assertIsNotNone(location)
        
        new_promotion = response.get_json()
        self.assertEqual(new_promotion["title"], test_promo.title)
        self.assertEqual(new_promotion["promo_type"], test_promo.promo_type)
        self.assertEqual(new_promotion["promo_code"], test_promo.promo_code)
        self.assertEqual(new_promotion["amount"], test_promo.amount)
        self.assertEqual(new_promotion["start_date"], test_promo.start_date)
        self.assertEqual(new_promotion["end_date"], test_promo.end_date)
        self.assertEqual(new_promotion["is_site_wide"], test_promo.is_site_wide)
        self.assertEqual(new_promotion["product_id"], test_promo.product_id)
        
        
        
    ######################################################################
    #  T E S T   S A D   P A T H S
    ######################################################################
    

    def test_create_promotion_no_data(self):
        """It should not Create a promotion with missing data"""
        response = self.client.post(BASE_URL, json={})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_create_promotion_no_content_type(self):
        """It should not Create a promotion with no content type"""
         
        test_promotion=PromotionFactory()
        response = self.client.post(BASE_URL)
        logging.debug(" Test Promotion:%s", test_promotion.serialize())
        self.assertEqual(response.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)


    def test_create_promotion_incorrect_content_type(self):
        """It should not Create a Pet with bad available data"""
        test_promotion = PromotionFactory()
        logging.debug(test_promotion)
        # change available to a string
        test_promotion.available = "true"
        response = self.client.post(BASE_URL, json=test_promotion.serialize())
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)



