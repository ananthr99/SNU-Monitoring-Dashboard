import os
import configparser
import mysql.connector
from urllib.parse import quote_plus
from sqlalchemy import create_engine



def get_db_config():
    config = configparser.ConfigParser()

    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    config_path = os.path.join(
        base_dir,
        "SNU Monitoring",
        "SNU_Dashboard",
        "dbConfig.ini"
    )

    config.read(config_path)

    return {
        "host": config["mysql"]["host"],
        "port": int(config["mysql"]["port"]),
        "database": config["mysql"]["database"],
        "user": config["mysql"]["user"],
        "password": config["mysql"]["password"],
    }


def get_connection():
    db = get_db_config()

    conn = mysql.connector.connect(
        host=db["host"],
        port=db["port"],
        user=db["user"],
        password=db["password"],
        database=db["database"],
        connection_timeout=120,
        autocommit=True
    )

    return conn


def get_engine():
    db = get_db_config()

    # VERY IMPORTANT: encode password for URL safety
    encoded_password = quote_plus(db["password"])

    conn_str = (
        f"mysql+mysqlconnector://{db['user']}:{encoded_password}"
        f"@{db['host']}:{db['port']}/{db['database']}"
    )

    return create_engine(conn_str, pool_pre_ping=True)