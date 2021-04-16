from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from marshmallow import Schema, fields, validate
from utils import make_parameter, make_request_body, make_response

specification = APISpec(
    title="Orders API",
    version="1.0.0",
    openapi_version="3.0.3",
    plugins=[MarshmallowPlugin()],
    **{
        "info": {"description": "API that allows you to manage orders for CoffeeMesh"},
        "servers": [
            {"url": "https://coffeemesh.com", "description": "main production server"},
            {
                "url": "https://coffeemesh-staging.com",
                "description": "staging server for testing purposes only",
            },
        ],
    }
)


class OrderItem(Schema):
    product = fields.String(required=True)
    size = fields.String(
        required=True, validate=validate.OneOf(["small", "medium", "big"])
    )
    quantity = fields.Integer(default=1, validate=validate.Range(1, min_inclusive=True))


class CreateOrder(Schema):
    order = fields.List(fields.Nested(OrderItem), required=True)


class GetOrder(Schema):
    id_ = fields.UUID(data_key="id", required=True)
    created = fields.Integer(required=True)
    status = fields.String(
        required=True, validate=validate.OneOf(["active", "cancelled", "completed"])
    )
    order = fields.List(fields.Nested(OrderItem), required=True)


specification.components.schema("GetOrder", schema=GetOrder)
specification.components.schema("CreateOrder", schema=CreateOrder)

specification.path(
    path="/orders",
    operations={
        "get": {
            "description": "A list of orders made by the customer sorted by date. Allows to filter orders by range of dates.",
            "responses": make_response(
                {
                    "type": "object",
                    "properties": {
                        "data": {
                            "type": "array",
                            "items": {"$ref": "#/components/schemas/GetOrder"},
                        }
                    },
                },
                description="A JSON array of orders",
            ),
        },
        "post": {
            "summary": "Creates an Order",
            "requestBody": make_request_body("CreateOrder"),
            "responses": make_response(
                "GetOrder",
                status_code="201",
                description="A JSON representation of the created order",
            ),
        },
    },
)

specification.path(
    path="/orders/{order_id}",
    parameters=[make_parameter(in_="path", name="order_id", schema={"type": "string"})],
    operations={
        "get": {
            "summary": "Returns the details of a specific order",
            "responses": make_response(
                "GetOrder", description="A JSON representation of an order"
            ),
        },
        "put": {
            "description": "Replaces an existing order",
            "requestBody": make_request_body("CreateOrder"),
            "responses": make_response(
                "GetOrder", description="A JSON representation of an order"
            ),
        },
        "delete": {
            "description": "Deletes an existing order",
            "responses": {
                "204": {"description": "The resource was deleted successfully"}
            },
        },
    },
)

print(specification.to_yaml())
