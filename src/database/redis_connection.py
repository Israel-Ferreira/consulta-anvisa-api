import redis

def connect_in_redis(host="localhost", port=6379) -> redis.Redis | None:
    """
    Cria uma conexão com o redis e retorna a conexão em caso de sucesso.
    Em caso de Falha, retorna None.
    """

    try:
        return redis.Redis(host=host, port=port)
    except Exception as e:
        print(e)
        return None
    
