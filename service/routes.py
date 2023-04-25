"""
My Service

Describe what your service does here
"""

from flask import jsonify, abort
from flask_restx import Resource, fields, reqparse, inputs
from service.common import status  # HTTP Status Codes
from service.models import Promotion, PromoType

# Import Flask application
from . import app, api


######################################################################
# Configure the Root route bofre OpenAPI setup
######################################################################
@app.route("/")
def index():
    """ Root URL response """
    return app.send_static_file("index.html")

# Define the model so that the docs reflect what can be sent


create_model = api.model('Promotion', {
    'name': fields.String(required=True, description='The name of the Promotion'),
    'code': fields.String(required=True, description='The code of the Promotion'),
    'promo_type': fields.String(enum=[promo.name for promo in PromoType], description='The type of the Promotion'),
    'description': fields.String(required=True, description='The description of the Promotion'),
    # 'created_date': fields.DateTime(required=True,
    #                         description='The created date of the Promotion'),
    # 'updated_date': fields.DateTime(required=True,
    #                         description='The updated date of the Promotion'),
    'is_site_wide': fields.Boolean(required=True, description='The active status of the Promotion'),
    'start_date': fields.DateTime(required=True, description='The start date of the Promotion'),
    'end_date': fields.DateTime(required=True, description='The end date of the Promotion'),
    'product_id': fields.Integer(required=True, description='The product id of the Promotion'),
    'amount': fields.Integer(required=True, description='The amount of the Promotion')
})

promotion_model = api.inherit(
    'Promotion', create_model,
    {
        'id': fields.Integer(readOnly=True,
                             description='The unique id assigned internally by service')
        # 'created_date': fields.DateTime(readOnly=True,
        #                      description='The date and time when the Promotion was created'),
        # 'updated_date': fields.DateTime(readOnly=True,
        #                      description='The date and time when the Promotion was updated')
    })

# query string arguments
promotion_args = reqparse.RequestParser()
promotion_args.add_argument('name', type=str, location='args', required=False, help='List Promotions by name')
promotion_args.add_argument('code', type=str, location='args', required=False, help='List Promotions by code')
promotion_args.add_argument('promo_type', type=str, location='args', required=False, help='List Promotions by type')
promotion_args.add_argument('description', type=str, location='args', required=False, help='List Promotions by description')
promotion_args.add_argument('is_site_wide', type=inputs.boolean, location='args', required=False,
                            help='List Promotions by site wide status')
promotion_args.add_argument('start_date', type=str, location='args', required=False, help='List Promotions by start date')
promotion_args.add_argument('end_date', type=str, location='args', required=False, help='List Promotions by end date')
promotion_args.add_argument('product_id', type=int, location='args', required=False, help='List Promotions by product id')
promotion_args.add_argument('amount', type=int, location='args', required=False, help='List Promotions by amount')


######################################################################
#  PATH: /promotions/{id}
######################################################################
@api.route('/promotions/<int:id>')
@api.param('id', 'The Promotion identifier')
class PromotionResource(Resource):
    """
    PromotionResource class

    Allows the manipulation of a single Promotion
    GET /Promotion{id} - Returns a Promotion with the id
    PUT /Promotion{id} - Update a Promotion with the id
    DELETE /Promotion{id} -  Deletes a Promotion with the id
    """

    # ------------------------------------------------------------------
    # RETRIEVE A PROMOTION
    # ------------------------------------------------------------------
    @api.doc('get_promotions')
    @api.response(404, 'Promotion not found')
    @api.marshal_with(promotion_model)
    def get(self, promo_id):
        """
        Retrieve a single Promotion

        This endpoint will return a Promotion based on it's id
        """
        app.logger.info("Request to Retrieve a promotion with id [%s]", promo_id)
        promotion = Promotion.find(promo_id)
        if not promotion:
            api.abort(status.HTTP_404_NOT_FOUND,
                      f"Promotion with id '{promo_id}' was not found."
                      )
        return promotion.serialize(), status.HTTP_200_OK

    # ------------------------------------------------------------------
    # UPDATE AN EXISTING PROMOTION
    # ------------------------------------------------------------------
    @api.doc('update_promotions')
    @api.response(404, 'Promotion not found')
    @api.response(400, 'The posted Promotion data was not valid')
    @api.expect(promotion_model)
    @api.marshal_with(promotion_model)
    def put(self, promo_id):
        """
        Update a Promotion

        This endpoint will update a Promotion based the body that is posted
        """
        app.logger.info("Request to Update a promotion with id [%s]", promo_id)
        promotion = Promotion.find(promo_id)
        if not promotion:
            api.abort(status.HTTP_404_NOT_FOUND,
                      f"Promotion with id '{promo_id}' was not found."
                      )
        app.logger.debug('Payload = %s', api.payload)
        data = api.payload
        promotion.deserialize(data)
        promotion.id = promo_id
        promotion.update()
        return promotion.serialize(), status.HTTP_200_OK

    # ------------------------------------------------------------------
    # DELETE A PROMOTION
    # ------------------------------------------------------------------
    @api.doc('delete_promotions')
    @api.response(204, 'Promotion deleted')
    def delete(self, promo_id):
        """
        Delete a Promotion

        This endpoint will delete a Promotion based the id specified in the path
        """
        app.logger.info("Request to Delete a promotion with id [%s]", promo_id)
        promotion = Promotion.find(promo_id)
        if promotion:
            promotion.delete()
        return '', status.HTTP_204_NO_CONTENT


######################################################################
#  PATH: /promotions
######################################################################
@api.route('/promotions', strict_slashes=False)
class PromotionCollection(Resource):
    """ Handles all interactions with collections of Promotions """
    # ------------------------------------------------------------------
    # LIST ALL Promotions
    # ------------------------------------------------------------------
    @api.doc('list_promotions')
    @api.expect(promotion_args, validate=True)
    @api.marshal_list_with(promotion_model)
    def get(self):
        """ Returns all of the Promotions """
        app.logger.info("Request to list of promotions")
        all_promotions = []
        args = promotion_args.parse_args()

        if args['title']:
            app.logger.info("Filtering by query for title: %s", args['title'])
            all_promotions = Promotion.find_by_title(args['title'])
        elif args['code']:
            app.logger.info("Filtering by query for promotion code: %s", args['code'])
            all_promotions = Promotion.find_by_code(args['code'])
        elif args['promo_type'] is not None:
            app.logger.info("Filtering by query for promotion type: %s", args['promo_type'])
            all_promotions = Promotion.find_by_type(args['promo_type'])
        else:
            app.logger.info("All Promotions")
            all_promotions = Promotion.all()

        app.logger.info("Returning %d promotions", len(all_promotions))
        results = [promo.serialize() for promo in all_promotions]
        return results, status.HTTP_200_OK

    # ------------------------------------------------------------------
    # ADD A NEW PROMOTION
    # ------------------------------------------------------------------
    @api.doc('create_promotions')
    @api.response(400, 'The posted data was not valid')
    @api.expect(promotion_model)
    @api.marshal_with(promotion_model, code=201)
    def post(self):
        """
        Creates a Promotion

        This endpoint will create a Promotion based the data in the body that is posted
        """
        app.logger.info('Request to Create a promotion')
        promotion = Promotion()
        app.logger.debug('Payload = %s', api.payload)
        promotion.deserialize(api.payload)
        promotion.create()
        app.logger.info('Promotion with new id [%s] saved!', promotion.id)
        location_url = api.url_for(PromotionResource, id=promotion.id, _external=True)
        return promotion.serialize(), status.HTTP_201_CREATED, {'Location': location_url}


############################################################
# Health Endpoint
############################################################
@app.route("/health")
def health():
    """Performs a health check for Kubernetes"""
    return jsonify({"status": "OK"}), status.HTTP_200_OK


######################################################################
#  PATH: /promotions/{id}/active
######################################################################
@app.route("/promotions/<promotion_id>/active", methods=["PUT"])
def activate(promotion_id):
    """Activate the Promotion with the promotion_id"""

    app.logger.info(" This endpoint will set the active attribute to True ")
    promotion = Promotion.find(promotion_id)
    if not promotion:
        abort(status.HTTP_404_NOT_FOUND, f"Promotion {promotion_id} not found.")
    promotion.activate()
    app.logger.info("Promotion %s has now active status True.", promotion_id)

    return promotion.serialize(), status.HTTP_200_OK


######################################################################
#  PATH: /promotions/{id}/deactive
######################################################################
@app.route("/promotions/<promotion_id>/deactive", methods=["PUT"])
def deactivate(promotion_id):

    """Deactivate the Promotion with the promotion_id"""

    app.logger.info(" This endpoint will set the active attribute to False ")
    promotion = Promotion.find(promotion_id)
    if not promotion:
        abort(status.HTTP_404_NOT_FOUND, f"Promotion {promotion_id} not found.")
    promotion.deactivate()
    app.logger.info("Promotion %s has now active status False.", promotion_id)

    return promotion.serialize(), status.HTTP_200_OK


# @app.route("/promotions/<promotion_id>/valid", methods=["PUT"])
# def valid(promotion_id):

#     """Activate the Promotion with the promotion_id"""

#     app.logger.info(" This endpoint will set the valid attribute to True ")
#     promotion = Promotion.find(promotion_id)
#     if not promotion:
#         abort(status.HTTP_404_NOT_FOUND, f"Promotion {promotion_id} not found.")
#     promotion.valid_on()
#     app.logger.info("Promotion %s has now valid status True.", promotion_id)

#     return promotion.serialize(), status.HTTP_200_OK


# @app.route("/promotions/<promotion_id>/invalid", methods=["PUT"])
# def invalid(promotion_id):

#     """Deactivate the Promotion with the promotion_id"""

#     app.logger.info(" This endpoint will set the valid attribute to False ")
#     promotion = Promotion.find(promotion_id)
#     if not promotion:
#         abort(status.HTTP_404_NOT_FOUND, f"Promotion {promotion_id} not found.")
#     promotion.valid_off()
#     app.logger.info("Promotion %s has now valid status False.", promotion_id)

#     return promotion.serialize(), status.HTTP_200_OK
