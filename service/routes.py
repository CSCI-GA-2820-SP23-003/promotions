"""
My Service

Describe what your service does here
"""

from flask import jsonify, request, abort
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
        jsonify(
            name="Promotion Service",
            version="1.0",
        ),
        status.HTTP_200_OK,
    )


######################################################################
#  R E S T   A P I   E N D P O I N T S
######################################################################

######################################################################
# GET ALL PROMOTIONs
######################################################################
@app.route("/promotions", methods=["GET"])
def get_promotions():
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
# GET A PROMOTION
######################################################################
@app.route("/promotions/<int:promotion_id>", methods=["GET"])
def get_a_promotion(promotion_id):
    """
    get a Promotion by lookup its id.

    This endpoint will return a Promotions in db.
    """
    app.logger.info("Request for promotion with id: %s", promotion_id)
    promotion = Promotion.find(promotion_id)
    if not promotion:
        abort(status.HTTP_404_NOT_FOUND, f"Promotion {promotion_id} not found.")
    return promotion.serialize(), status.HTTP_200_OK

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


######################################################################
# UPDATE A PROMOTION
######################################################################
@app.route("/promotions/<int:promo_id>", methods=["PUT"])
def update_promotion(promo_id):
    """
    Updates a promotion with details provided
    
    This endpoint will update a promotion with provided details
    and return the updated information when successful.
    If the provided promotion id is not found, it will return 404
    """
    app.logger.info("Request to update promotion, id: %s", promo_id)

    promotion = Promotion.find(promo_id)
    if not promotion:
        abort(status.HTTP_404_NOT_FOUND, f"Promotion {promo_id} not found.")

    data = request.get_json()
    promotion.deserialize(data)
    promotion.update()

    app.logger.info("Promotion %s updated.", promotion.id)
    return jsonify(promotion.serialize()), status.HTTP_200_OK
