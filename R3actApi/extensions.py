from flask.ext.mysqldb import MySQL

# Create MySQL object. We create it here to avoid
# circular dependencies that would occur if we created in
# app.py
mysql = MySQL()