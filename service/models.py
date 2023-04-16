"""
Models for Promotions

All of the models are stored in this module

Models
------
Promotion - A representation of a special promotion/sale that is running against product

Attributes:
-----------
id (int) = id of the promotion
title (String)= title of the promotion
promo_code (String) = code of promotion (6 characters)
promo_type (Enum(PromoType))= type of the promotion
amount (int) = amount of discount
start_date (timestamp)= start date of promotion
end_date (timestamp)= end date of promotion
is_site_wide (bool)= status whether promotion is site-wide
product_id (int) = id of the product
"""

import logging
from enum import Enum
from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


logger = logging.getLogger("flask.app")

# Create the SQLAlchemy object to be initialized later in init_db()
db = SQLAlchemy()


# Function to initialize the database
def init_db(app):
    """ Initializes the SQLAlchemy app """
    Promotion.init_db(app)


class DataValidationError(Exception):
    """ Used for an data validation errors when deserializing """


class PromoType(Enum):
    """ Enumeration of valid promotion types"""
    BOGO = 1		    # buy X get 1 free
    DISCOUNT = 2	    # X% off
    FIXED = 3		    # $X off


class Promotion(db.Model):
    """
    Class that represents a Promotion
    """
    # pylint: disable=too-many-instance-attributes

    app = None

    # Table Schema
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(63), nullable=False)
    promo_code = db.Column(db.String(63), nullable=True)
    promo_type = db.Column(db.Enum(PromoType), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    start_date = db.Column(db.DateTime(), nullable=False)
    end_date = db.Column(db.DateTime(), nullable=False)
    is_site_wide = db.Column(db.Boolean(), nullable=False, default=False)
    product_id = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<Promotion {self.title} id=[{self.id}]>"

    def create(self):
        """
        Creates a Promotion to the database
        """
        logger.info("Creating promotion %s", self.title)
        self.id = None  # pylint: disable=invalid-name
        db.session.add(self)
        db.session.commit()

    def update(self):
        """
        Updates a Promotion to the database
        """
        if not self.id:
            raise DataValidationError("Promo id not provided.")
        logger.info("Saving %s", self.title)
        db.session.commit()

    def delete(self):
        """ Removes a Promotion from the data store """
        logger.info("Deleting promotion %s", self.title)
        db.session.delete(self)
        db.session.commit()

    def serialize(self):
        """ Serializes a Promotion into a dictionary """

        return {
            "id": self.id,
            "title": self.title,
            "promo_code": self.promo_code,
            "promo_type": self.promo_type.name,
            "amount": self.amount,
            "start_date": self.start_date.isoformat(),
            "end_date": self.end_date.isoformat(),
            "is_site_wide": self.is_site_wide,
            "product_id": self.product_id
            }

    def deserialize(self, data):
        """
        Deserializes a Promotion from a dictionary

        Args:
            data (dict): A dictionary containing the resource data
        """
        try:
            self.title = data["title"]
            self.promo_code = data["promo_code"]
            self.promo_type = data["promo_type"]
            self.amount = data["amount"]
            self.start_date = datetime.fromisoformat(data["start_date"])
            self.end_date = datetime.fromisoformat(data["end_date"])
            self.is_site_wide = data["is_site_wide"]
            self.product_id = data["product_id"]
            self.amount = data["amount"]
        except KeyError as error:
            raise DataValidationError(
                "Invalid Promotion: missing " + error.args[0]
            ) from error
        except TypeError as error:
            raise DataValidationError(
                "Invalid Promotion: body of request contained bad or no data - "
                "Error message: " + str(error)
            ) from error
        return self

    @classmethod
    def init_db(cls, app: Flask):
        """ Initializes the database session """
        logger.info("Initializing database")
        cls.app = app
        # This is where we initialize SQLAlchemy from the Flask app
        db.init_app(app)
        app.app_context().push()
        db.create_all()  # make our sqlalchemy tables

    @classmethod
    def all(cls):
        """ Returns all of the Promotions in the database """
        logger.info("Processing all Promotions")
        return cls.query.all()

    @classmethod
    def find(cls, promotion_id: int):
        """ Finds a Promotion by it's ID

        Args:
            promotion_id (int): the id of the Promotions

        """
        logger.info("Processing lookup for promotion id %s ...", promotion_id)
        return cls.query.get(promotion_id)

    @classmethod
    def find_or_404(cls, promotion_id: int):
        """Find a Promotion by it's id

        Args:
            promotion_id (int): the id of the Promotions
        """
        logger.info("Processing title query for %s ...", promotion_id)
        return cls.query.get_or_404(promotion_id)

    @classmethod
    def find_by_is_site_wide(cls, value: bool):
        """Returns a list of all promotions of the given promo_type

        Args:
            promo_type: (Enum(PromoType))= type of the promotion

        """
        logger.info("Processing lookup query to return a list of all promotions of the type %s...", value)
        return cls.query.filter(cls.is_site_wide == value)

    def valid_on(self):
        "Turn Valid value to True"
        logger.info("Set Valid status to True")
        self.is_site_wide = True
        db.session.commit()

    def valid_off(self):
        "Turn Valid value to False"
        logger.info("Set Valid status to False")
        self.is_site_wide = False
        db.session.commit()
