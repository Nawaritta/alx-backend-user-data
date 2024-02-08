#!/usr/bin/env python3
"""This module contains filter_datum function"""
from typing import List
import re
import logging
from typing import Tuple
import os


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    FORMAT_FIELDS = ('name', 'levelname', 'asctime', 'message')
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """constractor"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Format the log record."""
        message = super().format(record)
        return self.filter_message(message)


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """returns the log message obfuscated"""
    return re.sub(
        f'({"|".join(fields)})=[^\\{separator}]+',
        f'\\1={redaction}',
        message
    )


def get_logger() -> logging.Logger:
    """returns a logging.Logger object."""
    logger = logging.getLogger("user_data")
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.setLevel(logging.INFO)
    logger.propagate = False
    logger.addHandler(stream_handler)
    return logger


def get_db():
    """returns a connector to the database"""
    username = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    password = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    database = os.getenv("PERSONAL_DATA_DB_NAME", "")

    return mysql.connector.connect(
        user=username,
        password=password,
        host=host,
        database=database
    )


RedactingFormatter = __import__('filtered_logger').RedactingFormatter
get_db = __import__('filtered_logger').get_db


def main():
    """obtain a database connection using get_db and retrieve all rows
    in the users table and display each row under a filtered format"""
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")

    formatter = RedactingFormatter(fields=("name", "email",
                                           "phone", "ssn", "password"))
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    for row in cursor:
        logger.info(row)

    cursor.close()
    db.close()


if __name__ == '__main__':
    main()
