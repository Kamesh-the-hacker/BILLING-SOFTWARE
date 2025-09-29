import sqlite3
con=sqlite3.connect(database='ims.db')
cur=con.cursor()
alter="ALTER TABLE kyc DROP COLUMN transno"
try:
    cur.execute(alter)
    print('sucess')
except sqlite3.OperationalError as e:
    print(f"error{e}")
con.commit()
con.close()