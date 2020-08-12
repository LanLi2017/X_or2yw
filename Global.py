from pymongo import MongoClient
from JSON2DB.argo import demo_init
import psycopg2

__author__ = 'Gary'

from Settings import PSQL_USER

# INIT PSQL Argo Connection
argo_db = demo_init.get_db()
print("connected to argo...")
# INIT PSQL Direct Connection
psql_db = psycopg2.connect(
    f"dbname=argo user={PSQL_USER} password='123456'"
)

# INIT PSQL JSONB Direct Connection
# pjson_db = psycopg2.connect(
#     'dbname=pjson user={0} password=coin0nioc'.format(PSQL_USER)
# )
