import psycopg2
from tabulate import tabulate

#create tables
print("Beginning of create-tables.py")

conn = psycopg2.connect(
    host = "localhost",
    #port = "8200",
    database = "cs623progproj",
    user = "postgres",
    password = "postgres"
)

print(conn)

#for isolation: SERIALIZABLE
conn.set_isolation_level(3)

#for atomicity
conn.autocommit = False

#create tables
try:
    curr = conn.cursor()
    create_product_table = '''
    CREATE TABLE Product (
      prod VARCHAR(3),
      pname VARCHAR(30),
      price DECIMAL
    );
    '''
    create_depot_table = '''
    CREATE TABLE Depot (
      dep VARCHAR(3),
      addr VARCHAR(255),
      volume INTEGER
    );
    '''
    create_stock_table = '''
    CREATE TABLE Stock(
      prod VARCHAR(3),
      dep CHAR(2),
      quantity INTEGER
    );
    '''

    curr.execute(create_depot_table)
    curr.execute(create_product_table)
    curr.execute(create_stock_table)
except (Exception, psycopg2.DatabaseError) as err:
    print(err)
    print("Transactions incomplete- database rollback")
    conn.rollback()
finally:
    if conn:
        conn.commit()
        curr.close()
        conn.close()
        print("PSQL connection is now closed")
print("End")
