import psycopg2
from tabulate import tabulate

#add table values
print("Beginning of create-tables.py")

conn = psycopg2.connect(
    host = "localhost",
    port = "8200",
    database = "cs623progproj",
    user = "raffertyleung",
    password = "postgres"
)

print(conn)

#for isolation: SERIALIZABLE
conn.set_isolation_level(3)

#for atomicity
conn.autocommit = False

#add table values
try:
    curr = conn.cursor()
    insert_product_values = [
        ('p1', 'tape', 2.5),
        ('p2', 'tv', 250),
        ('p3', 'vcr', 80)
    ]

    insert_depot_values = [
        ('d1', 'New York', 9000),
        ('d2', 'Syracuse', 6000),
        ('d4', 'New York', 2000)
    ]

    insert_stock_values = [
        ('p1', 'd1', 1000),
        ('p1', 'd2', -100),
        ('p1', 'd4', 1200),
        ('p3', 'd1', 3000),
        ('p3', 'd4', 2000),
        ('p2', 'd4', 1500),
        ('p2', 'd1', -400),
        ('p2', 'd2', 2000)
    ]

    insert_product_table_query = '''
    INSERT INTO Product (prod, pname, price)
    VALUES (%s, %s, %s);
    '''

    insert_depot_table_query = '''
    INSERT INTO Depot (dep, addr, volume)
    VALUES (%s, %s, %s);
    '''

    insert_stock_table_query = '''
    INSERT INTO Stock (prod, dep, quantity)
    VALUES (%s, %s, %s);
    '''

    curr.executemany(insert_product_table_query, insert_product_values)
    curr.executemany(insert_depot_table_query, insert_depot_values)
    curr.executemany(insert_stock_table_query, insert_stock_values)
except (Exception, psycopg2.DatabaseError) as err:
    print(err)
    print("Transactions incomplete- database rollback")
    conn.rollback()
finally:
    if conn:
        conn.commit()
        print("Table values committed")
        curr.close()
        conn.close()
        print("PSQL connection is now closed")
print("End")