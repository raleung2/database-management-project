import psycopg2
from tabulate import tabulate

#Group 3/9 - The product p1 changes its name to pp1 in Product and Stock
print("Beginning of pk-fk.py")

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

#add change p1 to pp1
try:
  curr = conn.cursor()

  #update product name in product table
  curr.execute("UPDATE Product SET prod = 'pp1' WHERE prod = 'p1';")

  #update product name in stock table
  curr.execute("UPDATE Stock SET prod = 'pp1' WHERE prod = 'p1';") 
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