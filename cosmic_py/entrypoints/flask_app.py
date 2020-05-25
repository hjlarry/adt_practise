from datetime import datetime
from flask import Flask, jsonify, request

import config
from service_layer import services, unit_of_work
from adapters import repository, orm
from domain import models

orm.start_mappers()
app = Flask(__name__)


@app.route("/allocate", methods=["POST"])
def allocate_endpoint():
    uow = unit_of_work.SqlAlchemyUnitOfWork()
    try:
        batchref = services.allocate(
            request.json["orderid"], request.json["sku"], request.json["qty"], uow
        )
    except services.InvalidSku as e:
        return jsonify({"message": str(e)}), 400

    return jsonify({"batchref": batchref}), 201


@app.route("/add_batch", methods=["POST"])
def add_batch():
    uow = unit_of_work.SqlAlchemyUnitOfWork()
    eta = request.json["eta"]
    if eta is not None:
        eta = datetime.fromisoformat(eta).date()
    services.add_batch(
        request.json["ref"], request.json["sku"], request.json["qty"], eta, uow
    )
    return "OK", 201
