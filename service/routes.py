"""
My Service

Describe what your service does here
"""

#from flask import Flask,  request, url_for, make_response, abort
from flask import request, abort
from flask import jsonify
from service.common import status  # HTTP Status Codes
from service.models import Promotion

# Import Flask application
from . import app


######################################################################
# GET INDEX
######################################################################
@app.route("/")
def index():
    """ Promotion's Home URL response """
    app.logger.info("Request for Promotion's Home Root URL")
    return (
        jsonify(
            name="Promotion Rest API Service!!",
            version="1.0"
        ),
        status.HTTP_200_OK
    )
    

######################################################################
#  R E S T   A P I   E N D P O I N T S
######################################################################

# Place your REST API code here ...




######################################################################
# ADD A NEW Promotion
######################################################################
@app.route("/promotions", methods=["POST"])
def create_promotion():
    """
    Creates a Promotion
    This endpoint will create a Promotion based the data in the body that is posted
    """
    
    app.logger.info("Request to create a promotion")
    check_content_type("application/json")
    
    promo = Promotion()
    promo.deserialize(request.get_json())
    promo.create()
    message = promo.serialize()
    

    app.logger.info("Promotion with ID [%s] created.", promo.id)
    return jsonify(message), status.HTTP_201_CREATED


def check_content_type(content_type):
    """Checks that the media type is correct"""
    if "Content-Type" not in request.headers:
        app.logger.error("No Content-Type specified.")
        abort(
            status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            f"Content-Type must be {content_type}",
        )

    if request.headers["Content-Type"] == content_type:
        return

    app.logger.error("Invalid Content-Type: %s", request.headers["Content-Type"])
    abort(
        status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        f"Content-Type must be {content_type}",
    )
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


