import os
from dotenv import load_dotenv
from pymongo import MongoClient
import atexit

class MongoConnection:

    _instance = None
    _client = None

    def __new__(cls, *args, **kwargs):
        """Implementa o padrão Singleton para garantir uma única instância da classe."""
        if not cls._instance:
            cls._instance = super(MongoConnection, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        """Inicializa a conexão somente uma vez."""
        if MongoConnection._client is None:
            load_dotenv()
            self.host = os.getenv("MONGO_HOST")
            self.port = int(os.getenv("MONGO_PORT"))
            self.database_name = os.getenv("MONGO_DATABASE")
            self.collection_name = os.getenv("MONGO_COLLECTION")
            self._connect()
            atexit.register(self.close_connection)

    def _connect(self):
        """Estabelece a conexão com o MongoDB."""
        try:
            MongoConnection._client = MongoClient(self.host, self.port)
            self._db = MongoConnection._client[self.database_name]
            self._collection = self._db[self.collection_name]
            print("Conectado ao MongoDB com sucesso.")
        except Exception as e:
            print(f"Erro ao conectar ao MongoDB: {e}")
            MongoConnection._client = None

    @property
    def client(self):
        """Retorna o objeto do cliente MongoDB."""
        if MongoConnection._client is None:
            self._connect()
        return MongoConnection._client

    @property
    def db(self):
        """Retorna o objeto do banco de dados."""
        return self._db

    @property
    def collection(self):
        """Retorna o objeto da coleção."""
        return self._collection

    @staticmethod
    def close_connection():
        """Fecha a conexão com o MongoDB."""
        if MongoConnection._client:
            MongoConnection._client.close()
            MongoConnection._client = None
            print("Conexão fechada com sucesso.")