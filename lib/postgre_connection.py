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
        
    def _get_existing_word_of_the_day(self):
        self.cursor.execute(
            "SELECT word_uuid FROM date_uuid WHERE date = CURRENT_DATE"
        )
        return self.cursor.fetchone()
    
    def _select_random_word_uuid(self):
        self.cursor.execute(
            "SELECT uuid FROM word_uuid WHERE uuid NOT IN (SELECT word_uuid FROM date_uuid) ORDER BY random() LIMIT 1"
        )
        return self.cursor.fetchone()
    
    def _insert_word_of_the_day(self, word_uuid):
        self.cursor.execute(
            "INSERT INTO date_uuid (date, word_uuid) VALUES (CURRENT_DATE, %s)", (word_uuid[0],)
        )
        self.connection.commit()

    def get_word_of_the_day(self):
        try:
            word_uuid = self._get_existing_word_of_the_day()
            if word_uuid:
                return self.find_by_id(word_uuid[0])
            else:
                word_uuid = self._select_random_word_uuid()
                if word_uuid:
                    self._insert_word_of_the_day(word_uuid[0])
                    return self.find_by_id(word_uuid[0])
                else:
                    raise Exception("There no more unique words to set a new date.")
        except psycopg2.Error as psycopg_error:
            raise Exception("Database raised a exception") from psycopg_error
        except Exception as exception:
            raise Exception("Exception on word_of_the_day") from exception
