"""
My Service

Describe what your service does here
"""

from flask import Flask, jsonify, request, url_for, make_response, abort
from service.common import status  # HTTP Status Codes
from service.models import Promotion

# Import Flask application
from . import app


######################################################################
# GET INDEX
######################################################################
@app.route("/")
def index():
    """ Root URL response """
    return (
        "Reminder: return some useful information in json format about the service here",
        status.HTTP_200_OK,
    )


######################################################################
#  R E S T   A P I   E N D P O I N T S
######################################################################

######################################################################
# GET ALL PROMOTIONs
######################################################################
@app.route("/promotions", methods=["GET"])
def get_promotions(self):
    """
    get all Promotions

    This endpoint will return a list of Promotions with db
    """
    app.logger.info("Request to list promotions")
    all_promotions = []
    all_promotions = Promotion.all()
    results = [promo.serialize() for promo in all_promotions]
    app.logger.info("Returning %d promotions", len(results))
    return results, status.HTTP_200_OK


######################################################################
# DELETE A PROMOTION
######################################################################
@app.route("/promotions/<int:promotion_id>", methods=["DELETE"])
def delete_promotions(promotion_id):
    """
    Delete a Promotion

    This endpoint will delete a Promotion based the id specified in the path
    """
    app.logger.info("Request to delete promotion with id: %s", promotion_id)
    promotion = Promotion.find(promotion_id)
    if promotion:
        promotion.delete()

    app.logger.info("Promotion with ID [%s] delete complete.", promotion_id)
    return "", status.HTTP_204_NO_CONTENT


