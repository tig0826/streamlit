import pandas as pd
from sqlalchemy import create_engine
import os

def load_psql(sql):
    # 収集したデータを保存
    print('-- load from postgresql ---')
    postgresql_passwd = os.environ.get('postgresql_tig_passwd')
    connection_config = {
            "user": "tig",
            "password": postgresql_passwd,
            "host": "192.168.0.151",
            "port": "5432",
            "dbname": "dqx"}
    engine = create_engine('postgresql://{user}:{password}@{host}:{port}/{dbname}'.format(**connection_config))
    df = pd.read_sql(sql, con=engine)
    return df

