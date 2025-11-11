import psycopg2
from psycopg2 import Error


class Database:
    def __init__(self, host, database, user, password, sslmode="require"):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.sslmode = sslmode
        self.conn = None

    def connect(self):
        try:
            self.conn = psycopg2.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password,
                sslmode=self.sslmode,
            )
            print("✅ Conexão com o banco PostgreSQL estabelecida.")
        except Error as e:
            print(f"❌ Erro ao conectar ao PostgreSQL: {e}")

    def close(self):
        if self.conn:
            self.conn.close()
            print("🔒 Conexão encerrada.")

    def execute_query(self, query, params=None):
        cursor = None
        try:
            cursor = self.conn.cursor()
            cursor.execute(query, params)
            self.conn.commit()
            print("✅ Query executada com sucesso.")
        except Error as e:
            self.conn.rollback()  # Desfaz a transação em caso de erro
            print(f"❌ Erro ao executar a query: {e}")
            raise e  # Re-levanta a exceção para que o controller saiba que algo deu errado
        finally:
            if cursor:
                cursor.close()

    def fetch_all(self, query, params=None):
        cursor = None
        result = []
        try:
            cursor = self.conn.cursor()
            cursor.execute(query, params)
            result = cursor.fetchall()
            return result
        except Error as e:
            print(f"❌ Erro ao buscar dados: {e}")
        finally:
            if cursor:
                cursor.close()

    def fetch_one(self, query, params=None):
        with self.conn.cursor() as cur:
            cur.execute(query, params)
            return cur.fetchone()
