from flask import Flask, flash, redirect, render_template, request, url_for

import psycopg2
app =Flask(__name__)
app.secret_key="123secrete kye"

try:
    # conn = psycopg2.connect("dbname='duka' user='postgres' host='localhost' password='vicciSQL'")
    conn = psycopg2.connect("dbname='db3es5gpr6ngft' user='mrerxiwtdinwip' port='5432' host='ec2-63-35-156-160.eu-west-1.compute.amazonaws.com' password='6639d45c8e3a6b4866c2f29cad5077d35d4b70f7091ada07ee34e593f93aeec8'")
    print ("Successfullly connected to the  Vicci database")
except:
    print ("I am unable to connect to the  Vicci database")
cur=conn.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS products (id serial ,name varchar(55) NOT NULL,bp int,sp int,serial_no varchar(50))')
cur.execute('CREATE TABLE IF NOT EXISTS sales (id serial ,product_id int NOT NULL,quantity int,created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW())')
cur.execute('CREATE TABLE IF NOT EXISTS stock (id serial ,product_name VARCHAR,quantity int,bp int NOT NULL,date time without time zone NOT NULL DEFAULT NOW())')
cur.execute('CREATE TABLE IF NOT EXISTS suppliers (id serial ,name VARCHAR NOT NULL,location VARCHAR NOT NULL,email_address VARCHAR NOT NULL,address VARCHAR NOT NULL)')
conn.commit()

@app.route('/')
def ims():
    return render_template("viccistockims.html")

@app.route('/home')
def home():
    cur=conn.cursor()
    # cur.execute("SELECT count(name)FROM public.products ;")
    cur.execute("SELECT count(pr.id),count(sls.id),count(stk.id) FROM public.products as pr inner join sales as sls on sls.product_id=pr.id inner join stock as stk on stk.id=pr.id;")    
    data=cur.fetchall()
    print(data)
    return render_template("viccistockhome.html", data1=data)

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
        flash('Product Successfully Added','info') 
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
    flash('Purchace Successful','info') 
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
        flash('Product Successfully Edited', 'info') 
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
        flash('Product Successfully Added','info') 
        return redirect(url_for('stock'))
    else:
        flash('Required conditions not met!', 'danger') 

@app.route('/avail', methods=["POST"])
def avail():
    cur=conn.cursor()
    if request.method=="POST":
        quantity=request.form[""]
        request.form[""]
        query=""
        query1=""
        cur.execute(query,query1)
        conn.commit()
        flash('Product Successfully Availed','info')
        return redirect(url_for('stock'))
    else:
        return "Hello" 

@app.route('/sales')
def sales():
    cur=conn.cursor()

    cur.execute("SELECT pr.name,sum((pr.sp-pr.bp)* sl.quantity) as ttlprofit,sum(sl.quantity)as totalprofit FROM public.sales as sl join products as pr on pr.id=sl.product_id group by pr.name  ;")  
    sales= cur.fetchall()
    print(sales)
    return render_template("viccistocksales.html",sale=sales,)

@app.route('/sale/<string:id>')
def sale(id):
    cur=conn.cursor()

    # cur.execute("SELECT pr.name,sum((pr.sp-pr.bp)* sl.quantity) as ttlprofit,sum(sl.quantity)as totalprofit FROM public.sales as sl join products as pr on pr.id=sl.product_id where id=%d group by pr.name ;",[id])
    cur.execute("SELECT pr.name,sum((pr.sp-pr.bp)* sl.quantity) as ttlprofit,sum(sl.quantity)as totalprofit FROM public.sales as sl join products as pr on pr.id=sl.product_id where pr.id=%s group by pr.name ",[id])
    sales= cur.fetchall()
    print(sales)
    return render_template("viccistocksales.html",sale=sales)
    
@app.route('/payroll', methods=["GET","POST"] )
def payroll():
    if request.method=="POST":
        sallary=request.form["sallary"]
        bnft1=request.form["bnft1"]
        bnft2=request.form["bnft2"]        
        if sallary !="":
            if bnft1 !="":
                if bnft2 !="":
                    gross_sallary=int(int(sallary)+(int(bnft1)+int(bnft2))) 
                    #Calculating the NHIF    
                    if gross_sallary>300:
                        nhf=150 
                        ans=request.form["ans"]
                        #Calculating the NSSF
                        if ans!="Permanent" or ans!="permanent":
                            nsf=(gross_sallary-nhf)*0 
                            ti=gross_sallary-nhf 

                            if ti<24000:
                                tax=ti*0
                                net=ti
                                print(tax,nhf,nsf,net)
                                return render_template("index.html",callow=bnft2,hallo=bnft1,bsc=sallary,txblI=tax,nhif=nhf,nssf=nsf,n_sal=net,gs=gross_sallary)

                            elif ti>24000 and ti<32333:
                                tax=ti*0.25
                                net=ti*0.75
                                print(tax,nhf,nsf,net)
                                return render_template("index.html",callow=bnft2,hallo=bnft1,bsc=sallary,txblI=tax,nhif=nhf,nssf=nsf,n_sal=net,gs=gross_sallary)
                            
                            else:
                                ti>32333
                                tax=ti*0.3
                                net=ti*0.7  
                                print(tax,nhf,nsf,net)                       
                                return render_template("index.html",callow=bnft2,hallo=bnft1,bsc=sallary,txblI=tax,nhif=nhf,nssf=nsf,n_sal=net,gs=gross_sallary)
                        else:
                            #Calculating the NSSF
                            if gross_sallary<18000 :
                               nsff=(gross_sallary-nhf)*0.06
                               txi=gross_sallary-(nsf+nhf)
                               # Calculating The payee
                               if txi<24000:
                                    tax=txi*0
                                    net=txi
                                    return render_template("index.html",callow=bnft2,hallo=bnft1,bsc=sallary,n_sal=net,txblI=tax,nhif=nhf,nssf=nsff,gs=gross_sallary)
                               elif txi>24000 and ti<32333:
                                    tax=txi*0.25
                                    net=txi*0.75
                                    return render_template("index.html",callow=bnft2,hallo=bnft1,bsc=sallary,n_sal=net,txblI=tax,nhif=nhf,nssf=nsff,gs=gross_sallary)
                               else:
                                    txi>32333
                                    tax=txi*3
                                    net=txi*0.7
                                    return render_template("index.html",callow=bnft2,hallo=bnft1,bsc=sallary,n_sal=net,txblI=tax,nhif=nhf,nssf=nsff,gs=gross_sallary)  
                            else:
                                nsff=(gross_sallary-nhf)*0.1
                                txi=gross_sallary-(nsf+nhf)
                                # Calculating The payee
                                if txi<24000:
                                    tax=txi*0
                                    net=txi
                                    return render_template("index.html",callow=bnft2,hallo=bnft1,bsc=sallary,n_sal=net,txblI=tax,nhif=nhf,nssf=nsff,gs=gross_sallary)
                                elif txi>24000  and ti<32333:
                                    tax=txi*0.25
                                    net=txi*0.75
                                    return render_template("index.html",callow=bnft2,hallo=bnft1,bsc=sallary,n_sal=net,txblI=tax,nhif=nhf,nssf=nsff,gs=gross_sallary)
                                else:
                                    txi>32333
                                    tax=txi*0.3
                                    net=ti*0.7
                                    return render_template("index.html",callow=bnft2,hallo=bnft1,bsc=sallary,n_sal=net,txblI=tax,nhif=nhf,nssf=nsff,gs=gross_sallary)  
                else:
                    flash("Enter commuter benefits:")
            else:
                flash("Enter house benefits:")    
        else:
            flash("Enter The Basic Sallary:")
    return render_template("payroll.html")   

@app.route("/manager",methods=["GET","POST"])   
def manager():

    return render_template("manager.html")

@app.route("/admin",methods=["GET","POST"])   
def admin():

    return render_template("admin.html")

@app.route("/user",methods=["GET","POST"])   
def user():

    return render_template("user.html")

@app.route("/users",methods=["GET","POST"])   
def users():

    return render_template("users.html")

@app.route("/purchase",methods=["GET","POST"])   
def purchase():
    cur=conn.cursor()
  
    cur.execute("SELECT * from products")
    
    mbp= cur.fetchall()
    print(mbp)
    # invent=[(1,"Vicci","Omo",500,900,20,"Product"),(2,"Mani","Sunlight",342,723,12,"Product"),(3,"Shameful","Aerial",928,7093,2,"service")]
    return render_template("purchase.html",invtory=mbp)

if __name__ == '__main__':
    app.run(debug=True)

# cur.execute('CREATE TABLE IF NOT EXISTS products (id serial NOT NULL PRIMARY KEY,name varchar(55) NOT NULL,bp INT(15),sp INT(15),serial_no VARCHAR)')
# cur.execute('CREATE TABLE IF NOT EXISTS sales (id serial NOT NULL PRIMARY KEY,product_id INT NOT NULL,quantity INT (10),created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW())')
# cur.execute('CREATE TABLE IF NOT EXISTS stock (id serial NOT NULL PRIMARY KEY,product_name VARCHAR,quantity INT(20),bp (20) NOT NULL,date WITH TIME ZONE NOT NULL DEFAULT NOW())')
# cur.execute('CREATE TABLE IF NOT EXISTS suppliers (id serial NOT NULL PRIMARY KEY,name VARCHAR NOT NULL,location VARCHAR NOT NULL,email_address VARCHAR NOT NULL,address VARCHAR NOT NULL)')
