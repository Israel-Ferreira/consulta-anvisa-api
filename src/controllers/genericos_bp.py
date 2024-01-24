from flask import Blueprint, request, jsonify

from services.anvisa_service import AnvisaService

import database


generico_bp =  Blueprint('consulta_genericos', __name__, url_prefix="/api/consulta-genericos")

redis_conn = database.connect_in_redis()

anvisa_service = AnvisaService(redis_conn)


@generico_bp.get("/")
def list_all_medicines():
    product_name = request.args.get('nome_produto')
    process_number = request.args.get('numero_processo')

    register = request.args.get("numero_registro")
    
    if product_name is None and process_number is None and register is None:
        bad_request_error = {
            "error_msg": "A requisição deve ter pelo menos um filtro passado na url"
        }

        return jsonify(bad_request_error), 400
    

    return anvisa_service.list_genericos(product_name, process_number, register)


@generico_bp.get("/<protocol_number>")
def get_medicine_by_protocol_number(protocol_number):
    result = anvisa_service.get_generico_by_numero_processo(protocol_number)
    return result

