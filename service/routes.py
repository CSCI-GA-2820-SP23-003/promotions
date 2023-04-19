"""
My Service

Describe what your service does here
"""

from flask import jsonify, request, abort, url_for, make_response
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
    return app.send_static_file("index.html")
######################################################################
#  R E S T   A P I   E N D P O I N T S
######################################################################

######################################################################
# GET ALL PROMOTIONs
######################################################################


@app.route("/promotions", methods=["POST"])
def create_promotion():
    """
    Creates a Promotion
    This endpoint will create a Promotion based the data in the body that is posted
    """

    app.logger.info("Request to create a promotion")
    check_content_type("application/json")

    promotion = Promotion()
    promotion.deserialize(request.get_json())
    promotion.create()
    message = promotion.serialize()
    location_url = url_for("get_a_promotion", promotion_id=promotion.id, _external=True)

    app.logger.info("Promotion with ID [%s] created.", promotion.id)
    return jsonify(message), status.HTTP_201_CREATED, {"Location": location_url}


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


@app.route("/promotions", methods=["GET"])
def get_promotions():
    """
    get all Promotions or a list of a promotions of a specified type as passed in the URL under attribute promo_type
    example: http://127.0.0.1:8000/promotions?is_site_wide=true
    This endpoint will return a list of Promotions with db
    """
    app.logger.info("Request to list of promotions")
    all_promotions = []

    title = request.args.get("title")

    if title:
        app.logger.info("Filtering by query for title: %s", title)
        all_promotions = Promotion.find_by_title(title)
    else:
        app.logger.info("All Promotions")
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
    return make_response(jsonify(promotion.serialize()), status.HTTP_200_OK)

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
    return promotion.serialize(), status.HTTP_200_OK

############################################################
# Health Endpoint
############################################################


@app.route("/health")
def health():
    """Performs a health check for Kubernetes"""
    return make_response(jsonify(dict(status="OK")), status.HTTP_200_OK)


@app.route("/promotions/<promotion_id>/valid", methods=["PUT"])
def valid(promotion_id):

    """Activate the Promotion with the promotion_id"""

    app.logger.info(" This endpoint will set the valid attribute to True ")
    promotion = Promotion.find(promotion_id)
    if not promotion:
        abort(status.HTTP_404_NOT_FOUND, f"Promotion {promotion_id} not found.")
    promotion.valid_on()
    app.logger.info("Promotion %s has now valid status True.", promotion_id)

    return promotion.serialize(), status.HTTP_200_OK


@app.route("/promotions/<promotion_id>/invalid", methods=["PUT"])
def invalid(promotion_id):

    """Activate the Promotion with the promotion_id"""

    app.logger.info(" This endpoint will set the valid attribute to False ")
    promotion = Promotion.find(promotion_id)
    if not promotion:
        abort(status.HTTP_404_NOT_FOUND, f"Promotion {promotion_id} not found.")
    promotion.valid_off()
    app.logger.info("Promotion %s has now valid status False.", promotion_id)

    return promotion.serialize(), status.HTTP_200_OK
