class Medicamento:

    def __init__(self, nome_produto, processo, registro, farmaceutica, cnpj_farma, situacao, data_vencimento, tipo) -> None:
        self.nome_produto = nome_produto
        self.processo = processo
        self.registro = registro
        self.farmaceutica = farmaceutica
        self.cnpj_farma = cnpj_farma
        self.situacao = situacao
        self.data_vencimento = data_vencimento
        self.tipo = tipo


    def to_dict(self):
        return {
            "nome_produto": self.nome_produto,
            "processo": self.processo,
            "registro": self.registro,
            "farmaceutica": self.farmaceutica,
            "cnpj_farma": self.cnpj_farma,
            "situacao": self.situacao,
            "data_vencimento": self.data_vencimento,
            "tipo": self.tipo
        }


    @staticmethod
    def convert_anvisa_response_to_object(anvisa_response):
        return Medicamento(
            anvisa_response["nomeProduto"],
            anvisa_response["processo"],
            anvisa_response["registro"],
            anvisa_response["razaoSocial"],
            anvisa_response["cnpj"],
            anvisa_response["descSituacao"],
            anvisa_response["dataVencimento"],
            anvisa_response["descTipo"]
        )
