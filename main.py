from unicodedata import numeric
from flask import Flask, flash, redirect, render_template, request, url_for
from numpy import integer
import psycopg2
app =Flask(__name__)
app.secret_key="123secrete kye"

try:
    # conn = psycopg2.connect("dbname='duka' user='postgres' host='localhost' password='vicciSQL'")
    conn = psycopg2.connect("dbname='dk28dn22dcnb2' user='lwbdaaftujgejr' port='5432' host='ec2-54-194-147-61.eu-west-1.compute.amazonaws.com' password='cda07fc755061b7a120e7fa2d8f6144dc6268aa98131ef59eeefe2fa3d32da00'")
    print ("Successfullly connected to the  Vicci database")
except:
    print ("I am unable to connect to the  Vicci database")
cur=conn   
cur.cursor()
cur.execute('CREATE TABLE products (id INT NOT NULL PRIMARY KEY,name VARCAHR(55) NOT NULL,bp INT(20),sp INT(20),serial_no VARCHAR)')
cur.execute('CREATE TABLE sales (id INT NOT NULL PRIMARY KEY,product_id FOREIGN KEY(id) REFERENCES products(id) ON UPDATE CASCADE NOT NULL,quantity INT(10),created_at DATE NOT NULL DEFAULT NOW())')
cur.execute('CREATE TABLE stock (id INT NOT NULL PRIMARY KEY,product_name VARCHAR(50) NOT NULL,quantity INT(20) NOT NULL,bp FOREIGN KEY(bp) REFERENCES products(bp) ON UPDATE CASCADE NOT NULL,date DATE NOT NULL DEFAULT NOW())')
cur.execute('CREATE TABLE suppliers (id INT NOT NULL PRIMARY KEY,name VARCHAR(50) NOT NULL,location VARCHAR NOT NULL,email_address VARCHAR NOT NULL,address VARCHAR NOT NULL)')

@app.route('/')
def ims():
    return render_template("viccistockims.html")

@app.route('/home')
def home():
    return render_template("viccistockhome.html")

@app.route('/dashboard')
def dash():
    cur=conn.cursor()
    
    cur.execute("SELECT  extract(year from sl.created_at) || '-' || extract(month from sl.created_at) || '-' || extract(day from sl.created_at)as tarehe,sum((pr.sp-pr.bp)* sl.quantity) as totalprofit,sum(sl.quantity)as totalquantity FROM public.sales as sl join products as pr on pr.id=sl.product_id  group by sl.created_at order by sl.created_at")
    
    mbp=cur.fetchall()
    print(mbp)
    label=[]
    data=[]   
    for i in mbp:
        label.append(i[0])
        data.append(int(i[1]))
    print("abxb",data,"uybce",label)

    return render_template("viccistockdash.html",label=label,data=data)

@app.route('/inventory', methods=["GET","POST"])
def invent():
    cur=conn.cursor()
  
    cur.execute("SELECT * from products")
    
    mbp= cur.fetchall()
    print(mbp)
    # invent=[(1,"Vicci","Omo",500,900,20,"Product"),(2,"Mani","Sunlight",342,723,12,"Product"),(3,"Shameful","Aerial",928,7093,2,"service")]
    return render_template("viccistockinvetry.html",invtory=mbp)

@app.route('/add_item',methods=["POST"])
def adder():
    cur=conn.cursor()
    if request.method == "POST":        
        name= request.form["name"]
        bp= request.form["bp"]
        sp= request.form["sp"]
        serial_no=request.form["serial"] 

        query="INSERT INTO products(name, bp, sp, serial_no) VALUES (%s, %s, %s, %s);"
        row=(name,bp,sp,serial_no)
        cur.execute(query,row)
        conn.commit()
        flash('Product Successfully Added') 
        return redirect(url_for('invent')) 

@app.route('/Make_Sale',methods=["POST"])
def saler():
    cur=conn.cursor()  
    id= request.form["product_id"]  
    quantity= request.form["quantity"]
    created_at="NOW()"
    query="INSERT INTO public.sales (product_id,quantity,created_at) VALUES (%s,%s,%s);"
    row=(id,quantity,created_at)
    cur.execute(query,row)
    conn.commit()
    flash('Purchace Successful') 
    return redirect(url_for('invent')) 

@app.route('/edit',methods=["POST"])
def editor():
    cur=conn.cursor()
    if request.method == "POST":        
        name= request.form["name"]
        bp= request.form["bp"]
        sp= request.form["sp"]
        serial_no=request.form["serial"] 
        id=request.form["id"]        

        query='UPDATE public.products SET name=%s, bp=%s, sp=%s, serial_no=%s WHERE id=%s;'
        row=(name,bp,sp,serial_no,id)
        cur.execute(query,row)
        conn.commit()
        flash('Product Successfully Edited') 
        return redirect(url_for('invent'))

@app.route('/stock')
def stock():    
    cur=conn.cursor()
    cur.execute(" SELECT id, product_name, quantity, bp*quantity as ttlcoast, date FROM public.stock; ")      
    stock=cur.fetchall()
    print(stock)
    return render_template("viccistockstock.html",stock=stock)

@app.route('/add_stock',methods=["POST"])
def stockup():
    cur=conn.cursor()
    if request.method == "POST":        
        name= request.form["product_name"]
        quantity=request.form["quantity"]
        bp= request.form["bp"]         
        created_at="NOW()"
        query="INSERT INTO public.stock (product_name, quantity, bp,date) VALUES (%s,%s,%s,%s);"
        row=(name,quantity,bp,created_at)
        cur.execute(query,row)
        conn.commit()
        flash('Product Successfully Added') 
        return redirect(url_for('stock')) 

@app.route('/sales')
def sale():
    cur=conn.cursor()

    cur.execute("SELECT pr.name,sum((pr.sp-pr.bp)* sl.quantity) as ttlprofit,sum(sl.quantity)as totalprofit FROM public.sales as sl join products as pr on pr.id=sl.product_id group by pr.name  ;")  
    sales= cur.fetchall()
    print(sales)
    return render_template("viccistocksales.html",sale=sales,)

@app.route('/sales')
def sales(id):
    cur=conn.cursor()

    # cur.execute("SELECT pr.name,sum((pr.sp-pr.bp)* sl.quantity) as ttlprofit,sum(sl.quantity)as totalprofit FROM public.sales as sl join products as pr on pr.id=sl.product_id where id=%d group by pr.name ;",[id])
    cur.execute("SELECT pr.name,sum((pr.sp-pr.bp)* sl.quantity) as ttlprofit,sum(sl.quantity)as totalprofit FROM public.sales as sl join products as pr on pr.id=sl.product_id where pr.id=%s group by pr.name ",[id])
    sales= cur.fetchall()
    print(sales)
    return render_template("viccistocksales.html",sale=sales)
    

if __name__ == '__main__':
    app.run(debug=True)

