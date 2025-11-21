#using MySQL, Python with Flask web framework to create a web app that interacts with a database of suppliers, parts, and shipments.

from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

# database connection 
def connect_db():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="andy", #REPLACE WITH YOUR MYSQL ROOT PASSWORD
    )
        #create database if not exists and use it, easier for testing
        cursor = connection.cursor()
        cursor.execute("create database if not exists suppliers_and_parts")
        cursor.execute("use suppliers_and_parts")

        #create tables if not exists
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Supplier (
            Sno VARCHAR(5) PRIMARY KEY,
            Sname VARCHAR(20),
            Status INT,
            City VARCHAR(20)
        )
    """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Part (
                Pno VARCHAR(5) PRIMARY KEY,
                Pname VARCHAR(20),
                Color VARCHAR(20),
                Weight INT,
                City VARCHAR(20)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Shipment (
                Sno VARCHAR(5),
                Pno VARCHAR(5),
                Qty INT,
                Price DECIMAL(10,4),
                PRIMARY KEY (Sno, Pno),
                FOREIGN KEY (Sno) REFERENCES Supplier(Sno),
                FOREIGN KEY (Pno) REFERENCES Part(Pno)
            )
        """)

        connection.commit()
        cursor.close()

        print("database connection successful")
        return connection

    except mysql.connector.Error as error:
        print(f"database connection failed: {error}")
        raise

#insert into the shipment table and give success or error msg
    # https://www.geeksforgeeks.org/python/python-sqlite-cursor-object/
    # https://dev.mysql.com/doc/connector-python/en/connector-python-api-mysqlcursor-constructor.html
def insert_shipment(sno, pno, qty, price):
    print("inserting shipment:", sno, pno, qty, price)
    connection = connect_db()
    cursor = connection.cursor()
    #try block to catch errors
    try:
        cursor.execute("insert into shipment (sno, pno, qty, price) values (%s, %s, %s, %s)", (sno, pno, qty, price))
        connection.commit()
        print("Shipment information successfully entered!")
        return True, f"Shipment information successfully entered!"
    
    except mysql.connector.Error as error:
        print(f"Error when entering shipment information: {error}")
        return False, f"Error when entering shipment information: {error}"
        # https://www.geeksforgeeks.org/python/try-except-else-and-finally-in-python/
    finally:
        cursor.close()
        connection.close()

#increase supplier status by 10% and give success or error msg 
def increase_status():
    connection = connect_db()
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute("update supplier set status = status * 1.1") # increase status by 10%
        connection.commit()
        print("Supplier status successfully updated!")
        return True, f"Supplier status successfully updated!"
    except mysql.connector.Error as error:
        print(f"Error when updating supplier status: {error}")
        return False, f"Error when updating supplier status: {error}"
    finally:
        cursor.close()
        connection.close()

#display info of all suppliers
def display_info():
    connection = connect_db()
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute("select * from supplier")
        suppliers = cursor.fetchall()
        print("suppliers fetched:", suppliers)
        print("DEBUG supplier row keys:", suppliers[0].keys())

        return suppliers
    except mysql.connector.Error as error:
        print(f"Error getting supplier information: {error}")
        return []
    finally:
        cursor.close()
        connection.close()

#part number that displays all suppliers who shipped that part w no vulnerability
def suppliers_by_part(part):
    #testing
    # part = input("Enter part number: ").strip()
    # https://realpython.com/prevent-python-sql-injection/#crafting-safe-query-parameters
    connection = connect_db()
    cursor = connection.cursor(dictionary=True)
    try:
        query = "select supplier.sno, sname, status, city, shipment.qty, shipment.price from supplier join shipment on supplier.sno = shipment.sno where shipment.pno = %s"
        cursor.execute(query, (part,))

        suppliers = cursor.fetchall()
        if suppliers:
            print("DEBUG keys:", suppliers[0].keys())
        #in case there are no suppliers for entered part
        if not suppliers:
            print(f"No suppliers found for part {part}")
            return []
        return suppliers
    except mysql.connector.Error as error:
        print(f"Error getting suppliers for part {part}: {error}")
        return []
    finally:
        cursor.close()
        connection.close()

#made this to test but seems like its useful
def reset():
    connection = connect_db()
    cursor = connection.cursor()

    #clear old data
    try:
        cursor.execute("delete from shipment")
        cursor.execute("delete from part")
        cursor.execute("delete from supplier")

        #reseed with initial data from db hw 
        # supplier table
        cursor.execute("""
            INSERT INTO SUPPLIER VALUES
            ('s1','Smith',20,'London'),
            ('s2','Jones',10,'Paris'),
            ('s3','Blake',30,'Paris'),
            ('s4','Clark',20,'London'),
            ('s5','Adams',30,NULL)
        """)
        
        # part table
        cursor.execute("""
            INSERT INTO PART VALUES
            ('p1','Nut','Red',12,'London'),
            ('p2','Bolt','Green',17,'Paris'),
            ('p3','Screw',NULL,17,'Rome'),
            ('p4','Screw','Red',14,'London'),
            ('p5','Cam','Blue',12,'Paris'),
            ('p6','Cog','Red',19,'London')
        """)

        # shipment table
        cursor.execute("""
            INSERT INTO SHIPMENT VALUES
            ('s1','p1',300,0.005),
            ('s1','p2',200,0.009),
            ('s1','p3',400,0.004),
            ('s1','p4',200,0.009),
            ('s1','p5',100,0.01),
            ('s1','p6',100,0.01),
            ('s2','p1',300,0.006),
            ('s2','p2',400,0.004),
            ('s3','p2',200,0.009),
            ('s3','p3',200,NULL),
            ('s4','p2',200,0.008),
            ('s4','p3',NULL,NULL),
            ('s4','p4',300,0.006),
            ('s4','p5',400,0.003)
        """)

        connection.commit()
        print("Database reseeded successfully.")
        return True, "Database reseeded successfully."


    except mysql.connector.Error as error:
        print(f"Error when reseeding db: {error}")
        return False, f"Error when reseeding db: {error}"

    finally:
        cursor.close()
        connection.close()

#view entire database
@app.route('/view_database', methods=['POST'])
def view_database():
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)

    # Fetch Supplier
    cursor.execute("SELECT * FROM supplier")
    suppliers = cursor.fetchall()

    # Fetch Parts
    cursor.execute("SELECT * FROM part")
    parts = cursor.fetchall()

    # Fetch Shipments
    cursor.execute("SELECT * FROM shipment")
    shipments = cursor.fetchall()

    cursor.close()
    conn.close()

    # Build HTML
    html = "<h3>SUPPLIER</h3>"
    html += "<table class='table table-bordered'><tr><th>Sno</th><th>Sname</th><th>Status</th><th>City</th></tr>"
    for s in suppliers:
        html += f"<tr><td>{s['Sno']}</td><td>{s['Sname']}</td><td>{s['Status']}</td><td>{s['City']}</td></tr>"
    html += "</table>"

    html += "<h3>PART</h3>"
    html += "<table class='table table-bordered'><tr><th>Pno</th><th>Pname</th><th>Color</th><th>Weight</th><th>City</th></tr>"
    for p in parts:
        html += f"<tr><td>{p['Pno']}</td><td>{p['Pname']}</td><td>{p['Color']}</td><td>{p['Weight']}</td><td>{p['City']}</td></tr>"
    html += "</table>"

    html += "<h3>SHIPMENT</h3>"
    html += "<table class='table table-bordered'><tr><th>Sno</th><th>Pno</th><th>Qty</th><th>Price</th></tr>"
    for sh in shipments:
        html += f"<tr><td>{sh['Sno']}</td><td>{sh['Pno']}</td><td>{sh['Qty']}</td><td>{sh['Price']}</td></tr>"
    html += "</table>"

    return render_template("index.html", popup_message=html)


#routes

#homepage
@app.route('/')
def index():
    return render_template('index.html')

#increase status route
@app.route('/increase_status', methods=['POST'])
def increase_status_route():
    success, message = increase_status()
    return render_template('index.html', popup_message=message)

#display all suppliers route
@app.route('/suppliers', methods=['POST'])
def suppliers_route():
    suppliers = display_info()
    # https://getbootstrap.com/docs/4.1/components/modal/
    table_html = '<table class="table table-bordered"><tr><th>SNO</th><th>Name</th><th>Status</th><th>City</th></tr>'
    for s in suppliers:
        table_html += f"<tr><td>{s['Sno']}</td><td>{s['Sname']}</td><td>{s['Status']}</td><td>{s['City']}</td></tr>" #capitalize first letter to match db name
    table_html += "</table>"

    return render_template("index.html", popup_message=table_html)

#suppliers by part route
@app.route('/suppliers_by_part', methods=['GET', 'POST'])
def suppliers_by_part_route():
    #testing
    print('request.form =', request.form)
    part = request.form.get('part')
    print('part =', part)

    if not part:
        return render_template('index.html', popup_message="Please enter a part number.")
    
    part = part.strip() #strip after potential of none
    suppliers = suppliers_by_part(part)

    if not suppliers:
        return render_template('index.html', popup_message=f"No suppliers found for part {part}.")
    
    table_html = f"<h5>Suppliers shipping part: {part}</h5>"
    table_html += '<table class="table table-bordered table-striped"><tr><th>SNO</th><th>Name</th><th>Status</th><th>City</th><th>Qty</th><th>Price</th></tr>'

    for s in suppliers:
        table_html += (
            f"<tr>"
            f"<td>{s['sno'] if 'sno' in s else s['Sno']}</td>"
            f"<td>{s['sname'] if 'sname' in s else s['Sname']}</td>"
            f"<td>{s['status'] if 'status' in s else s['Status']}</td>"
            f"<td>{s['city'] if 'city' in s else s['City']}</td>"
            f"<td>{s['qty'] if 'qty' in s else s['Qty']}</td>"
            f"<td>{s['price'] if 'price' in s else s['Price']}</td>"
            f"</tr>"
        )

    table_html += "</table>"
    
    print('result =', suppliers)
    return render_template('index.html', popup_message=table_html)

#insert shipment route
# @app.route('/insert_shipment', methods=['POST'])
# def insert_shipment_route():
#     success1, message1 = insert_shipment('s2', 'p3', 200, 0.006)
#     success2, message2 = insert_shipment('s4', 'p2', 100, 0.005)
#     return render_template("index.html", message1=message1, message2=message2)

#second attempt - separate them 
#shipment 1 route
@app.route('/insert_shipment1', methods=['POST'])
def insert_shipment1_route():
    success, message = insert_shipment('s2', 'p3', 200, 0.006)
    return render_template("index.html", popup_message=message)

#insert shipment 2 route
@app.route('/insert_shipment2', methods=['POST'])
def insert_shipment2_route():
    success, message = insert_shipment('s4', 'p2', 100, 0.005)
    return render_template("index.html", popup_message=message)

#reset database route
@app.route('/reset_database', methods=['POST'])
def reset_database():
    success, message = reset()
    return render_template("index.html", popup_message=message)


if __name__ == "__main__":
    app.run(debug=True)
