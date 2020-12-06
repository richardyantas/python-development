import psycopg2

# Connect to an existing database

conn = psycopg2.connect(dbname='insights')

cur = conn.cursor()
cur.execute("SELECT * FROM clients;")
version = cur.fetchone()
print(version)

# with conn:
#     cur = conn.cursor()
#     cur.execute("SELECT * FROM clients")
    
#     row = cur.fetchone()
#     print(row)
#     #print(f"{row[0]} {row[1]} {row[2]}")
    
#     #rows = cur.fetchall()
#     #for row in rows:
#     #    print(f"{row[0]} {row[1]} {row[2]}")


# x = cur.fetchone()[0]
# print (x, type(x), repr(x))