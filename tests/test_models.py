"""
Test cases for Promotion Model

"""
from datetime import datetime
import os
import logging
import unittest
from werkzeug.exceptions import NotFound
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

    def test_find_a_promotion(self):
        """It should find a Promotion"""
        promotion = PromotionsFactory()
        promotion.create()
        promo_id = promotion.id
        self.assertEqual(len(Promotion.all()), 1)
        # find the promotion and make sure it's in the db
        promotion.find(promotion.id)
        search = Promotion.find(promo_id)
        self.assertIsNot(search, None)
        self.assertEqual(search.id, promo_id)

    def test_delete_a_promotion(self):
        """It should Delete a Promotion"""
        promotion = PromotionsFactory()
        promotion.create()
        self.assertEqual(len(Promotion.all()), 1)
        # delete the promotion and make sure it isn't in the database
        promotion.delete()
        self.assertEqual(len(Promotion.all()), 0)

    def test_update_no_id_should_raise_error(self):
        """It should raise an error if no id is there for a Promotion update"""
        promotion = PromotionsFactory()
        promotion.id = None
        self.assertRaises(DataValidationError, promotion.update)

    def test_update_a_promotion_happy_path(self):
        """It should update a Promotion"""
        promotion = PromotionsFactory()
        promotion.create()
        promo_id = promotion.id

        promotion.amount = 9999
        promotion.start_date = datetime(2000, 1, 1)
        promotion.update()

        updated = Promotion.find(promo_id)
        self.assertEqual(updated.amount, promotion.amount)
        self.assertEqual(updated.start_date, promotion.start_date)

    def test_serialize_a_promotion(self):
        """It should serialize a Promotion"""
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
        self.assertEqual(datetime.fromisoformat(data['start_date']), promotion.start_date)
        self.assertIn('end_date', data)
        self.assertEqual(datetime.fromisoformat(data['end_date']), promotion.end_date)
        self.assertIn('is_site_wide', data)
        self.assertEqual(data['is_site_wide'], promotion.is_site_wide)
        self.assertIn('product_id', data)
        self.assertEqual(data['product_id'], promotion.product_id)

    def test_deserialize_a_promotion(self):
        """It should de-serialize a Promotion"""
        data = PromotionsFactory().serialize()
        promotion = Promotion()
        promotion.deserialize(data)
        self.assertNotEqual(promotion, None)
        self.assertEqual(promotion.title, data['title'])
        self.assertEqual(promotion.promo_code, data['promo_code'])
        self.assertEqual(promotion.promo_type, data['promo_type'])
        self.assertEqual(promotion.amount, data['amount'])
        self.assertEqual(promotion.start_date, datetime.fromisoformat(data['start_date']))
        self.assertEqual(promotion.end_date, datetime.fromisoformat(data['end_date']))
        self.assertEqual(promotion.is_site_wide, data['is_site_wide'])
        self.assertEqual(promotion.product_id, data['product_id'])

    def test_deserialize_with_key_error(self):
        """ It should deserialize an Promotion with a KeyError """
        promotion = Promotion()
        self.assertRaises(DataValidationError, promotion.deserialize, {})

    def test_deserialize_bad_data(self):
        """It should not deserialize bad data"""
        data = "this is not a dictionary"
        promotion = Promotion()
        self.assertRaises(DataValidationError, promotion.deserialize, data)

    def test_deserialize_missing_data(self):
        """It should not deserialize a Promotion with missing data"""
        data = {"id": 1, "title": "promo_bogo"}
        promotion = Promotion()
        self.assertRaises(DataValidationError, promotion.deserialize, data)

    def test_find_or_404_found(self):
        """It should Find or return 404 not found"""
        promotions = PromotionsFactory.create_batch(3)
        for promotion in promotions:
            promotion.create()

        promotion = Promotion.find_or_404(promotions[1].id)
        self.assertIsNot(promotion, None)
        self.assertEqual(promotion.id, promotions[1].id)
        self.assertEqual(promotion.title, promotions[1].title)
        self.assertEqual(promotion.promo_code, promotions[1].promo_code)
        self.assertEqual(promotion.promo_type, promotions[1].promo_type)
        self.assertEqual(promotion.amount, promotions[1].amount)
        self.assertEqual(promotion.start_date, promotions[1].start_date)
        self.assertEqual(promotion.end_date, promotions[1].end_date)
        self.assertEqual(promotion.is_site_wide, promotions[1].is_site_wide)
        self.assertEqual(promotion.product_id, promotions[1].product_id)

    def test_find_or_404_not_found(self):
        """It should return 404 not found"""
        self.assertRaises(NotFound, Promotion.find_or_404, 0)

    def test_find_by_is_site_wide(self):
        """It should Find Promotions by is_site_wide"""
        promotions = PromotionsFactory.create_batch(10)
        for promotion in promotions:
            promotion.create()
        test_val = promotions[0].is_site_wide
        count = len([promotion for promotion in promotions if promotion.is_site_wide == test_val])
        found = Promotion.find_by_is_site_wide(test_val)
        self.assertEqual(found.count(), count)
        for promotion in found:
            self.assertEqual(promotion.is_site_wide, test_val)

    def test_find_by_title(self):
        """It should Find a Promotions by Title"""
        promotions = PromotionsFactory.create_batch(5)
        for promotion in promotions:
            promotion.create()
        title = promotions[0].title
        found = Promotion.find_by_title(title)
        self.assertEqual(found.count(), 1)
        self.assertEqual(found[0].title, promotions[0].title)
        self.assertEqual(found[0].promo_code, promotions[0].promo_code)
        self.assertEqual(found[0].promo_type, promotions[0].promo_type)
        self.assertEqual(found[0].amount, promotions[0].amount)
        self.assertEqual(found[0].product_id, promotions[0].product_id)

    def test_find_by_code(self):
        """It should Find a Promotions by promo_code"""
        promotions = PromotionsFactory.create_batch(5)
        for promotion in promotions:
            promotion.create()
        promo_code = promotions[0].promo_code
        found = Promotion.find_by_code(promo_code)
        self.assertEqual(found.count(), 1)
        self.assertEqual(found[0].title, promotions[0].title)
        self.assertEqual(found[0].promo_code, promotions[0].promo_code)
        self.assertEqual(found[0].promo_type, promotions[0].promo_type)
        self.assertEqual(found[0].amount, promotions[0].amount)
        self.assertEqual(found[0].product_id, promotions[0].product_id)
