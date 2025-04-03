import mysql.connector
from mysql.connector import Error

class BaseRepository:
    def __init__(self):
        self.dataBaseHostName = "localhost"
        self.dataBasePort = "3306"
        self.dataBaseName = "stock"
        self.dataBaseUser = "root"
        self.dataBasePassWord = ""

    def connect(self):
        """Estabelece conexão segura com o banco de dados."""
        try:
            return mysql.connector.connect(
                host=self.dataBaseHostName,
                port=self.dataBasePort,
                user=self.dataBaseUser,
                password=self.dataBasePassWord,
                database=self.dataBaseName
            )
        except Error as e:
            print(f"Erro ao conectar ao banco: {e}")
            return None

    def execute(self, command: str, values: tuple = None):
        """Executa um comando SQL sem retorno (INSERT, UPDATE, DELETE)."""
        connection = self.connect()
        if connection:
            try:
                with connection.cursor() as cursor:
                    cursor.execute(command, values)
                    connection.commit()
            except Error as e:
                print(f"Erro ao executar comando SQL: {e}")
            finally:
                connection.close()

    def executeQuery(self, query: str, values: tuple = None):
        """Executa um comando SQL com retorno (SELECT)."""
        connection = self.connect()
        if connection:
            try:
                with connection.cursor(dictionary=True) as cursor:
                    cursor.execute(query, values)
                    result = cursor.fetchall()
                    return result
            except Error as e:
                print(f"Erro ao executar consulta SQL: {e}")
                return None
            finally:
                connection.close()
