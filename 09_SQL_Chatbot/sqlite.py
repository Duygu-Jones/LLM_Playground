import sqlite3

# Connect to SQLite database
connection = sqlite3.connect("student.db")

# Create cursor object for database operations
cursor = connection.cursor()

# Drop table if exists and create new one
cursor.execute("DROP TABLE IF EXISTS STUDENT")

# Create student table with schema
table_info = """
CREATE TABLE STUDENT(
    NAME VARCHAR(25),
    CLASS VARCHAR(25),
    SECTION VARCHAR(25),
    MARKS INT
)
"""

cursor.execute(table_info)

# Insert sample student records
cursor.execute('''Insert Into STUDENT values('Jones','Data Science','A',90)''')
cursor.execute('''Insert Into STUDENT values('Duygu','Data Science','B',100)''')
cursor.execute('''Insert Into STUDENT values('Smiths','Data Science','A',86)''')
cursor.execute('''Insert Into STUDENT values('Jacob','DEVOPS','A',50)''')
cursor.execute('''Insert Into STUDENT values('Chris','DEVOPS','A',35)''')

# Display all inserted records
print("The inserted records are:")
data = cursor.execute('''Select * from STUDENT''')
for row in data:
    print(row)

# Commit changes and close connection
connection.commit()
connection.close()



# ### Code Flow:
# 1. Connect to SQLite database
# 2. Create cursor for database operations 
# 3. Create student table with name, class, section and marks columns
# 4. Insert sample student records
# 5. Display all records
# 6. Commit changes and close database connection

# To run:
# 1. Make sure sqlite3 is installed
# 2. Run the script: python create_db.py
# 3. This will create student.db file in your current directory
# 4. Verify the database is created with sample records