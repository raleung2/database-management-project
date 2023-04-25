import psycopg2
from tabulate import tabulate

#add primary keys and foreign keys
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

#add pk and fk constraints
try:
  curr = conn.cursor()

  #add pk to product table
  curr.execute('ALTER TABLE Product ADD CONSTRAINT pk_product_prod PRIMARY KEY (prod);')

  #add pk to depot table
  curr.execute('ALTER TABLE Depot ADD CONSTRAINT pk_depot_dep PRIMARY KEY (dep);')

  #add keys to stock table
  curr.execute('ALTER TABLE Stock ADD CONSTRAINT pk_stock_dep_prod PRIMARY KEY (dep, prod);')

  #add fks
  curr.execute('ALTER TABLE Stock ADD CONSTRAINT fk_prod FOREIGN KEY (prod) REFERENCES Product (prod) ON DELETE CASCADE ON UPDATE CASCADE;')
  curr.execute('ALTER TABLE Stock ADD CONSTRAINT fk_dep FOREIGN KEY (dep) REFERENCES Depot (dep);')


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

