import os
import psycopg2
from psycopg2 import Error
import uuid
import random

class PostgreeDatabase:

    def __init__(self):
        self.connection = None
        self.cursor = None
    
    def __enter__(self):
        try:
            self.connection = psycopg2.connect(
                user=os.environ.get("POSTGRES_USER"),
                password=os.environ.get("POSTGRES_PASSWORD"),
                host=os.environ.get("POSTGRES_HOST"),
                port="5432",
                database=os.environ.get("POSTGRES_DATABASE")
            )

            self.cursor = self.connection.cursor()

            return self
        except (Exception, Error) as error:
            raise Exception("Cannot connect with the database, error: ", error)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.connection:
            self.cursor.close()
            self.connection.close()

    def insert(self, word: str) -> str:
        the_uuid = str(uuid.uuid4())
        self.cursor.execute(
            "INSERT INTO word_uuid (uuid, word) VALUES (%s, %s)", (the_uuid, word)
        )

        self.connection.commit()

        return the_uuid

    def find_all(self) -> list:
        self.cursor.execute("SELECT * FROM word_uuid")
        rows = self.cursor.fetchall()
        words = []
        for row in rows:
            word = {
                "uuid": row[0],
                "word": row[1]
            }

            words.append(word)

        return words
    
    def find_by_id(self, id_) -> dict:
        id_ = str(id_)
        self.cursor.execute(
            "SELECT * FROM word_uuid WHERE uuid = %s", (id_,)
        )
        row = self.cursor.fetchone()
        if row:
            word = {
                "uuid": row[0],
                "word": row[1]
            }
            return word
        else:
            return {}
        
    def find_random(self) -> dict:
        self.cursor.execute(
            "SELECT * FROM word_uuid"
        )
        rows = self.cursor.fetchall()
        if rows:
            randow_row = random.choice(rows)
            word = {
                "uuid": randow_row[0],
                "word": randow_row[1]
            }

            return word
        else:
            return {}

    def get_word_of_the_day(self):
        try:
            self.cursor.execute(
                "SELECT word_uuid FROM date_uuid WHERE date = CURRENT_DATE"
            )
            word_uuid = self.cursor.fetchone()

            if word_uuid:
                return self.find_by_id(word_uuid[0])
            else:
                self.cursor.execute(
                    "INSERT INTO date_uuid (date, word_uuid) SELECT CURRENT_DATE, uuid FROM word_uuid OFFSET floor(random() * (SELECT COUNT(*) FROM word_uuid)) LIMIT 1 RETURNING word_uuid"
                )
                self.connection.commit()
                word_uuid = self.cursor.fetchone()

                return self.find_by_id(word_uuid[0]) if word_uuid else {}
        except Exception as exception:
            return {}