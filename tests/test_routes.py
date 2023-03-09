"""
TestPromotion API Service Test Suite

Test cases can be run with the following:
  nosetests -v --with-spec --spec-color
  coverage report -m
"""
import os
import logging
from unittest import TestCase
from service import app
from service.common import status  # HTTP Status Codes
from service.models import Promotion, db, init_db
from tests.factories import PromotionsFactory  # HTTP Status Codes

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql://postgres:postgres@localhost:5432/testdb"
)
BASE_URL = "/promotions"

######################################################################
#  T E S T   C A S E S
######################################################################


class TestPromotionServer(TestCase):
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
        self.app = app.test_client()
        db.session.query(Promotion).delete()  # clean up the last tests
        db.session.commit()

    def tearDown(self):
        """ This runs after each test """
        db.session.remove()

    def _create_promotions(self, count):
        """Factory method to create promotions in bulk"""
        promotions = []
        for _ in range(count):
            test_promotion = PromotionsFactory()
            response = self.app.post(BASE_URL, json=test_promotion.serialize())
            self.assertEqual(
                response.status_code, status.HTTP_201_CREATED, "Could not create test promotion"
            )
            new_promotion = response.get_json()
            test_promotion.id = new_promotion["id"]
            promotions.append(test_promotion)
        return promotions

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_index(self):
        """ It should call the home page """
        resp = self.app.get("/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_create_promotion(self):
        """It should create a new promotion"""
        test_promo = PromotionsFactory()
        logging.debug("Test Promotion: %s", test_promo.serialize())
        response = self.app.post(BASE_URL, json=test_promo.serialize())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        new_promotion = response.get_json()
        self.assertEqual(new_promotion["title"], test_promo.title)
        self.assertEqual(new_promotion["promo_type"], test_promo.promo_type.name)
        self.assertEqual(new_promotion["promo_code"], test_promo.promo_code)
        self.assertEqual(new_promotion["amount"], test_promo.amount)
        self.assertEqual(new_promotion["is_site_wide"], test_promo.is_site_wide)
        self.assertEqual(new_promotion["product_id"], test_promo.product_id)

    def test_get_promotions(self):
        """ It should return all promotions in db """
        # create two promotion
        test_promo0 = self._create_promotions(1)[0]
        test_promo1 = self._create_promotions(1)[0]

        # if it gets 200 status, then pass
        resp = self.app.get(f"{BASE_URL}")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        # check id of test_promos match to the returned JSON
        data = resp.get_json()
        self.assertEqual(data[0]['id'], test_promo0.id)
        self.assertEqual(data[1]['id'], test_promo1.id)

    def test_get_a_promotion(self):
        """ It should return a Promotion if id of a promotion exist in database """
        # get the id of a promotion
        test_promo = self._create_promotions(1)[0]

        # if it gets 200 status, then pass
        resp = self.app.get(f"{BASE_URL}/{test_promo.id}")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        # check id of test_promo match to the returned JSON
        #data = resp.get_json()
        #self.assertEqual(data[0]['id'], test_promo.id)

    def test_delete_promotion(self):
        """It should Delete a Promotion"""
        test_promotion = self._create_promotions(1)[0]
        response = self.app.delete(f"{BASE_URL}/{test_promotion.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(response.data), 0)
        # make sure they are deleted
        response = self.app.get(f"{BASE_URL}/{test_promotion.id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_promotion_happy_path(self):
        """It should update a promotion with provided data if the promotion exists"""
        TEST_PROMOTION_TITLE = "test promotion"
        test_promotion = self._create_promotions(1)[0]

        test_promotion.amount = 9999
        test_promotion.title = TEST_PROMOTION_TITLE
        response = self.app.put(f"{BASE_URL}/{test_promotion.id}", json=test_promotion.serialize())
        updated_promotion = Promotion()
        updated_promotion.deserialize(response.get_json())

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(updated_promotion.amount, test_promotion.amount)
        self.assertEqual(updated_promotion.title, TEST_PROMOTION_TITLE)

    ######################################################################
    #  T E S T   S A D   P A T H S
    ######################################################################

    def test_not_get_a_promotion(self):
        """It should not return a promotion if the promotion does not exist"""
        # get a id of a promotion not exist
        promo_not_exist_id = 77777
        promotion = PromotionsFactory()
        promotion.id = promo_not_exist_id
        response = self.app.get(f"{BASE_URL}/get/{promo_not_exist_id}", json=promotion.serialize())
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_promotion_not_found(self):
        """It should not update a promotion if the promotion does not exist"""
        promotion_id_not_found = 987654321
        promotion = PromotionsFactory()
        promotion.id = promotion_id_not_found
        response = self.app.put(f"{BASE_URL}/{promotion_id_not_found}", json=promotion.serialize())
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_promotion_no_data(self):
        """It should not Create a promotion with missing data"""
        response = self.app.post(BASE_URL, json={})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_promotion_no_content_type(self):
        """It should not Create a promotion with no content type"""
        test_promotion = PromotionsFactory()
        response = self.app.post(BASE_URL)
        logging.debug(" Test Promotion:%s", test_promotion.serialize())
        self.assertEqual(response.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)


    def test_create_promotion_removed_content_type(self):
        """It should not Create a Promotion with removed data of is_site_wide data"""

        test_promotion = PromotionsFactory()
        logging.debug(test_promotion)
        test_promo=test_promotion.serialize()
        del test_promo["is_site_wide"]
        #test_promotion.is_site_wide = "true"
        response = self.app.post(BASE_URL, json=test_promo)
        #self.assertRaises(TypeError)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

