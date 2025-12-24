import os
import pymysql


def get_connection():
    """
    Create and return a MySQL database connection
    using environment variables (cloud-safe).
    """

    return pymysql.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        database=os.getenv("DB_NAME"),
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True
    )
