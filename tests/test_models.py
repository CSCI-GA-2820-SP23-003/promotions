"""
Test cases for Promotion Model

"""
from datetime import date
import os
import logging
import unittest
from datetime import date
from service.models import Promotion, DataValidationError, db
from service import app
from tests.factories import PromotionsFactory

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql://postgres:postgres@localhost:5432/testdb"
)


######################################################################
#  P R O M O T I O N   M O D E L   T E S T   C A S E S
######################################################################
class TestPromotion(unittest.TestCase):
    """ Test Cases for Promotion Model """

    @classmethod
    def setUpClass(cls):
        """ This runs once before the entire test suite """
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        Promotion.init_db(app)

    @classmethod
    def tearDownClass(cls):
        """ This runs once after the entire test suite """
        db.session.close()

    def setUp(self):
        """ This runs before each test """
        db.session.query(Promotion).delete()  # clean up the last tests
        db.session.commit()

    def tearDown(self):
        """ This runs after each test """
        db.session.remove()

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_delete_a_promotion(self):
        """It should Delete a Promotion"""
        promotion = PromotionsFactory()
        promotion.create()
        self.assertEqual(len(Promotion.all()), 1)
        # delete the promotion and make sure it isn't in the database
        promotion.delete()
        self.assertEqual(len(Promotion.all()), 0)

    def test_update_no_id_should_raise_error(self):
        promotion = PromotionsFactory()
        promo.id = None
        self.assertRaises(DataValidationError, promo.update)

    def test_update_a_promotion_happy_path(self):
        promo = PromotionsFactory()
        promo.create()
        promo_id = promo.id

        promo.amount = 9999
        promo.start_date = date(2000, 1, 1)
        promo.update()

        updated = Promotion.find(promo_id)
        self.assertEqual(updated.amount, promo.amount)
        self.assertEqual(updated.start_date, promo.start_date)

    def test_serialize_an_order(self):
        """It should serialize an Order"""
        promotion = PromotionsFactory()
        data = promotion.serialize()
        self.assertNotEqual(data, None)
        self.assertIn('id', data)
        self.assertEqual(data['title'], promotion.title)
        self.assertIn('promo_code', data)
        self.assertEqual(data['promo_code'], promotion.promo_code)
        self.assertIn('promo_type', data)
        self.assertEqual(data['promo_type'], promotion.promo_type.name)
        self.assertIn('amount', data)
        self.assertEqual(data['amount'], promotion.amount)
        self.assertIn('start_date', data)
        self.assertEqual(date.fromisoformat(data['start_date']), promotion.start_date)
        self.assertIn('end_date', data)
        self.assertEqual(date.fromisoformat(data['end_date']), promotion.end_date)
        self.assertIn('is_site_wide', data)
        self.assertEqual(data['is_site_wide'], promotion.is_site_wide)
        self.assertIn('product_id', data)
        self.assertEqual(data['product_id'], promotion.product_id)

    def test_deserialize_an_order(self):
        """It should de-serialize an Order"""
        data = PromotionsFactory().serialize()
        promotion = Promotion()
        promotion.deserialize(data)
        self.assertNotEqual(promotion, None)
        self.assertEqual(promotion.title, data['title'])
        self.assertEqual(promotion.promo_code, data['promo_code'])
        self.assertEqual(promotion.promo_type, data['promo_type'])
        self.assertEqual(promotion.amount, data['amount'])
        self.assertEqual(promotion.start_date, date.fromisoformat(data['start_date']))
        self.assertEqual(promotion.end_date, date.fromisoformat(data['end_date']))
        self.assertEqual(promotion.is_site_wide, data['is_site_wide'])
        self.assertEqual(promotion.product_id, data['product_id'])
