import MySQLdb


def allowGoingIn(plateNumber):
    db = MySQLdb.connect(host="192.168.43.28", user="mehdi", passwd="mehdi", db="crs")
    cur = db.cursor()

    # Execute the SQL query to check if the plate number exists
    cur.execute("select * from plate where licence_number ='" + plateNumber + "';")

    # Fetch one row from the result
    row = cur.fetchone()

    db.commit()
    db.close()

    # Return True if the plate number is found, False otherwise
    return row is not None
