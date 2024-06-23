import pymysql
from sqlalchemy import create_engine

# MySQL 데이터베이스 연결
def connect_to_database(host, user, password, db_name):
    return pymysql.connect(host=host, user=user, password=password, db=db_name, charset='utf8')

# SQLAlchemy 엔진 생성
def create_sqlalchemy_engine(user, password, host, db_name):
    return create_engine(f"mysql+pymysql://{user}:{password}@{host}/{db_name}")

# 데이터 삽입 함수
def upload_data_to_db(data_dict, engine):
    for symbol in data_dict:
        df = data_dict[symbol]
        table_name = symbol.replace('/', '').replace('USDT', '')

        try:
            df.to_sql(table_name, con=engine, if_exists='append', index=False)
            print(f"Data for {symbol} inserted successfully.")
        except Exception as e:
            print(f"Error inserting data for {symbol}: {e}")

# 데이터베이스에서 테이블 목록 가져오기
def get_table_names(db_connection):
    cursor = db_connection.cursor()
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    return [table[0] for table in tables]
