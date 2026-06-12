import sqlite3
con = sqlite3.connect("restaurant.db")
c = con.cursor()
c.execute("""
                CREATE TABLE IF NOT EXISTS user(
                username TEXT PRIMARY KEY,
                password TEXT  NOT NULL,
                user_type TEXT DEFAULT 'user' 
                );
                """)
c.execute("""
                CREATE TABLE IF NOT EXISTS signature_items(
                item_name TEXT PRIMARY KEY,
                price INT NOT NULL,
                quantity INT,
                is_available INTEGER DEFAULT 1,
                added_by TEXT NOT NULL,
                FOREIGN KEY(added_by)
                 REFERENCES user(username)
                 );
                """)
#c.execute("ALTER TABLE user ADD COLUMN user_type TEXT DEFAULT 'user'")
con.commit()
def userreg():
    u = input("Enter username:")
    p = input("Enter password:")
    c.execute("SELECT * FROM user WHERE username = ?",(u,))
    if c.fetchone():
        print("user already registered,try another.")
    else:
        c.execute("INSERT INTO user (username,password,user_type) VALUES (?,?,?)",(u,p,"user"))
    con.commit()
    print("user registered successfully")
def staffreg():
    s = input("Enter username:")
    p = input("Enter password:")
    c.execute("SELECT * FROM user WHERE username = ?",(s,))
    if c.fetchone():
        print("user already registered,try another.")
    c.execute("INSERT INTO user(username,password,user_type) VALUES(?,?,?)",(s,p ,"staff"))
    con.commit()
    print("staff registered successfully")
def loginfn():
    username = input("Enter username:")
    password = input("Enter password:")
    c.execute("SELECT username,password,user_type  FROM user WHERE username=? AND password=?",(username,password))
    data = c.fetchone()
    if data:
        print("login successful",username)
        user_type = data[2]
        return username,user_type
    else:
        print("login failed!invalid username or password")
        return None,None
def add_item(logged_in_user):
    name = input("Enter item name:")
    price = float(input("Enter price:"))
    quantity = int(input("Enter quantity:"))
    c.execute("SELECT * FROM signature_items WHERE item_name =?",(name,))
    if c .fetchone():
        print("item already exists!")
    else:
        c.execute("""INSERT INTO signature_items(item_name,price,quantity,is_available,added_by)
        VALUES(?,?,?,?,?)""",(name,price,quantity,1,logged_in_user))
        con.commit()
        print(f"{name}item added successfully!")
def view_items():
    c.execute("SELECT item_name,price,quantity FROM signature_items WHERE is_available+1")
    items = c.fetchall()
    print("\n---All items ---")
    if items:
        for item in items:
            print("Item Name :",item[0])
            print("price :",item[1])
            print("quantity :",item[2])
    else:
        print("NO items found.Add items first")
def todays_special():
    c.execute("SELECT item_name,price FROM signature_items WHERE is_available = 1")
    item = c.fetchone()
    if item:
        print("Today's specail")
        print("item name:",item[0])
        print("price:",item[1])
    else:
        print("NO special today!add item first.")
while True:
            print("\n---main Menu---")
            print("1 = Register user")
            print("2 = Register staff")
            print("3 =login to staff menu")
            print("4 = View All items")
            print("5 = Today's special")
            print("6 = Exit")
            try:
                x=int(input("enter your choice:"))
            except ValueError:
                print("please enter  a valid choice")
                continue
            if x== 1:
                userreg()
            elif x == 2:
                staffreg()
            elif x ==3:
                username,user_type = loginfn()
                if username and user_type == "staff":
                    while True:
                        print("\n---staffmenu---")
                        print("1 = Add item")
                        print("2 = view all items")
                        print("3 = Today's special")
                        print("4 = back to main menu")
                        ch=int(input("enter your choice:"))
                        if ch ==1:
                            add_item(username)
                        elif ch == 2:
                             view_items()
                        elif ch == 3:
                            todays_special()
                        elif ch == 4:
                            break
                elif username:
                        print("only staff can access staff menu")
            elif x ==4:
                view_items()
            elif x == 5:
                todays_special()
            elif x == 6:
                print("exit")
                break
            else:
                print("invalid choice")
con.close()


