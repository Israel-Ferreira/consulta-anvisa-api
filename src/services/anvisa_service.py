import requests
import logging

from flask import jsonify

from models.medicamento import Medicamento


import json

from redis.commands.json.path import Path


class AnvisaService:

    CONSULTA_ANVISA_URL = "https://consultas.anvisa.gov.br/api/consulta"

    def __init__(self, redis_conn=None):
        self.redis_conn = redis_conn
        self.logging = logging.getLogger(__name__)

    def __anvisa_custom_headers(self):
        return {
            "Authorization": "Guest",
            "Content-Type": "application/json"
        }

    def list_genericos(self, nome_produto, numero_processo, registro, count=25, page=1):
        headers = self.__anvisa_custom_headers()


        url_genericos = f"{self.CONSULTA_ANVISA_URL}/genericos"

        url_genericos = f"{url_genericos}?count={count}&page={page}"

        if nome_produto is not None and nome_produto != "":
            url_genericos += f"&filter[nomeProduto]={nome_produto}"

        if numero_processo is not None and numero_processo != "":
            url_genericos += f"&filter[numeroProcesso]={numero_processo}"

        if registro is not None and registro != "":
            url_genericos  += f"&filter[numeroRegistrbo]={registro}"


        response = requests.get(url_genericos, headers=headers)

        print(response.url)

        if response.status_code >= 400:
            logging.error("Error getting genericos from Anvisa: %s", response.text)
            return {}, response.status_code
        

        json_response =  response.json()["content"]

        medicines =  [Medicamento.convert_anvisa_response_to_object(medicamento).to_dict() for medicamento in json_response]

        return medicines, 200

    def get_generico_by_numero_processo(self, numero_processo):
        headers =  self.__anvisa_custom_headers()

        try:
            logging.info("Acessando o Redis...")
            response = self.redis_conn.get(numero_processo)

            if response is None:
                raise Exception()

            return jsonify(str(response)), 200
        except Exception as e:
            print(e)
            url_genericos = f"{self.CONSULTA_ANVISA_URL}/medicamento/produtos/{numero_processo}"


            r = requests.get(url_genericos, headers=headers) 

            print(r.url)

            if r.status_code == 404:
                logging.error("Error getting genericos from Anvisa: %s", r.text)
                return {}, 404
            

            data = r.json()


            try:
                if self.redis_conn is not None:
                    self.redis_conn.set(numero_processo, str(data))

            except Exception as e:
                print(e)
                logging.error("Erro ao conectar com o redis: %s", e)

            
            return data, 200


