from flask import Flask,request,render_template,flash,redirect,url_for,session,logging
from flask_mysqldb import MySQL

from wtforms import Form,StringField,TextAreaField,PasswordField,validators
from passlib.hash import sha256_crypt
from functools import wraps
from datetime import date
app=Flask(__name__)
app.config["MYSQL_HOST"]="localhost"
app.config["MYSQL_USER"]="root"
app.config["MYSQL_PASSWORD"]=""
app.config["MYSQL_DB"]="flask"
app.config["MYSQL_CURSORCLASS"]="DictCursor"
mysql=MySQL(app)
@app.route('/',methods=['GET','POST'])
def home():
    session['login']=False
    session['update']=True
    if request.method=='POST':
        username=request.form['username']
        passo=request.form['password']
        cur=mysql.connection.cursor()
        result=cur.execute("select * from userstore  where login=%s",[username])
        
        if result>0:
            data=cur.fetchone()
            if data['password']==passo:
                session['login']=True
                return redirect(url_for('mainpage'))
                
            else:
                error="Invalid username and password"
                return render_template('login.html',error=error)
        else:
            error="Invalid username and password"

            return render_template('login.html',error=error)

            
        
    return render_template('login.html')
class create1(Form):
    name=StringField("Name",[validators.length(min=5,max=25)])
    username=StringField("username",[validators.length(min=1,max=25)])
    email=StringField("email",[validators.length(min=6,max=27)])
    password=PasswordField("password",[
        validators.DataRequired(),
        validators.EqualTo('confirm',message="password donit matched")
    ])
    confirm=PasswordField("confirm password")
@app.route('/create',methods=['GET','POST'])
def create():
    if request.method=='POST':
        ssn=request.form['id']
        name=str(request.form['name'])
        try:
            age=int(request.form['age'])
            if age>200:
                error="invalid age"
                return render_template('create.html',error=error)


        except:
            error="age should be numerical"
            return render_template('create.html',error=error)

        
        admission=str(request.form['admission'])
        bed=str(request.form.get('bed'))
        adrress=str(request.form['address'])
        state=str(request.form.get('city'))
        city=str(request.form.get('stt'))
        status=str(request.form['status'])
        cur=mysql.connection.cursor()
        cur.execute("insert into patients values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(100000,None,name,age,admission,bed,adrress,state,city,status))
        mysql.connection.commit()
        cur.close()
        msg="sucess"
        
        return render_template('create.html',msg=msg)
        
            

    return render_template('create.html')

class regester(Form):
    name=StringField("Name",[validators.length(min=5,max=25)])
    username=StringField("username",[validators.length(min=1,max=25)])
    email=StringField("email",[validators.length(min=6,max=27)])
    password=PasswordField("password",[
        validators.DataRequired(),
        validators.EqualTo('confirm',message="password donit matched")
    ])
    confirm=PasswordField("confirm password")
@app.route('/mainpage',methods=['GET','POST'])
def mainpage():
    form=regester(request.form)
    return render_template('mainpage.html',form=form)
@app.route('/delete',methods=['GET','POST'])
def delete():
    if request.method=='POST' and request.form['btn']=="Get":
        session['update']=False
        Form=request.form
        id=request.form['id']
        cur=mysql.connection.cursor()
        result=cur.execute("select * from patients where PatientID=%s",[id])
        mysql.connection.commit()
        
       
        if(result>0):
            data=cur.fetchone()
            cur.close()
            
            Form.id=int(data['PatientID'])
            Form.name=data['PatientName']
            Form.age=int(data['Age'])
            Form.admission=str(data['DateofAdmission'])
            Form.bed=str(data['Typeofbed'])
            Form.address=data['Address']
            Form.stt=str(data['State'])
            Form.city=str(data['City'])
            Form.status=str(data['Status'])
            print(data['Address'])
            return render_template('delete.html',form=Form)
        else:
            error="Invalid PatientId"
            return render_template('delete.html',error=error)
    if request.method=='POST' and request.form['btn']=='Delete':
        session['update']=True
        id=request.form['id']
        cur=mysql.connection.cursor()
        
        result=cur.execute("delete from patients where PatientID=%s",[id])
        mysql.connection.commit()
        cur.close()
        if result>0:
            msg="Removed sucessfully"
            return render_template('delete.html',msg=msg)
        else:
            error="Something went wrong try again"
            return render_template('delete.html',error=error)


    return render_template('delete.html')
@app.route('/update',methods=['POST','GET'])
def update():
    if request.method=='POST' and request.form['btn']=='Get':
        session['update']=False
        Form=request.form
        id=request.form['id']
        cur=mysql.connection.cursor()
        result=cur.execute("select * from patients where PatientID=%s",[id])
        mysql.connection.commit()
        
       
        if(result>0):
            data=cur.fetchone()
            cur.close()
            
            Form.id=int(data['PatientID'])
            Form.name=data['PatientName']
            Form.age=data['Age']
            Form.admission=str(data['DateofAdmission'])
            Form.bed=str(data['Typeofbed'])
            
            add=data['Address'].split(' ')
            Form.address=add
            address=data['Address']
            Form.stt=str(data['State'])
            session['state']=data['State']
            Form.city=str(data['City'])
            Form.status=str(data['Status'])
            return render_template('update.html',form=Form)
        else:
            error="Invalid PatientId"
            session['update']=True
            return render_template('update.html',error=error)

        
        
        
        
    if request.method=='POST' and request.form['btn']=='Update':
        session['update']=True
        ssn=request.form['id']
        name=str(request.form['name'])
        age=request.form['age']
        admission=str(request.form['admission'])
        bed=str(request.form.get('bed'))
        address=str(request.form['address'])
        state=str(request.form.get('stt'))
        if state=="":
            state=session['state']
            session.pop('state')
        city=str(request.form.get('city'))
        status=str(request.form['status'])
        cur=mysql.connection.cursor()
        result=cur.execute("update  patients set PatientName=%s,Age=%s,DateofAdmission=%s,Typeofbed=%s,Address=%s,State=%s,City=%s,Status=%s where PatientID=%s",(name,age,admission,bed,address,state,city,status,ssn))
        mysql.connection.commit()
        cur.close()
        if(result>0):
           msg="Updated sucessfully"
           return render_template('update.html',msg=msg)
        else:
            error="Invalid PatientID"
            
            return render_template('update.html',error=error)
        
        

    
        

    

    return render_template('update.html')
@app.route('/view')
def view():
    cur=mysql.connection.cursor()
    result=cur.execute("select * from patients where Status=%s",["Active"])
    data=cur.fetchall()
    mysql.connection.commit()
    cur.close()
    if result>0:
        return render_template('view.html',data=data)
    else:
        msg="msg no patients found"
        return  render_template("view.html",msg=msg)
@app.route('/search',methods=['GET','POST'])
def search():
    if request.method=='POST' and request.form['btn']=='search':
        
        Form=request.form
        id=request.form['id']
        cur=mysql.connection.cursor()
        result=cur.execute("select * from patients where PatientID=%s",[id])
        mysql.connection.commit()
        
       
        if(result>0):
            data=cur.fetchone()
            cur.close()
            
            Form.id=int(data['PatientID'])
            Form.name=data['PatientName'].split(' ')
            Form.age=data['Age']
            Form.admission=str(data['DateofAdmission'])
            Form.bed=str(data['Typeofbed']).split()
            Form.address=data['Address'].split()
            Form.stt=str(data['State']).split()
            Form.city=str(data['City']).split()
            Form.status=str(data['Status'])
            msg="Patient Found Sucessfully"
            
            return render_template('search.html',msg=msg,form=Form)
        else:
            error="Patient Not found"
            return render_template('search.html',error=error)
    return render_template('search.html')
@app.route('/patientmedicine',methods=['GET','POST'])
def patientmedicine():
    data=""
    if request.method=='POST' :
        id=int(request.form['id'])
        cur=mysql.connection.cursor()
        cur1=mysql.connection.cursor()
        result=cur.execute("select * from patients where PatientId=%s",[id])
        cur1.execute("select a.MedicineName,b.QuantityIssued,a.Rateofmedicine from medicine_master  a,tracking_medicines b where a.MedicineID=b.IDofMedicineIssued and b.PatientID=%s",[id])
       
        data=cur.fetchone()
        data1=list(cur1.fetchall())
        
        mysql.connection.commit()
        cur1.close() 
        cur.close()
       
        if result>0:
            session['username']=id
            return render_template('patientmedicine.html',data=data,data1=data1)
        else:
            error="Invalid PatientID"
            return render_template('patientmedicine.html',error=error,data=data)
    return render_template('patientmedicine.html',data=data)

@app.route('/issuemedicine',methods=['GET','POST'])
def issuemedicine():
    
    if request.method=='POST' and request.form['btn']=="search":
        session['iss']=True
        Form=request.form
        name=request.form['name']
        amount=int(request.form['quantity'])
        cur=mysql.connection.cursor()
        result=cur.execute("select MedicineName,QuantityAvailable ,Rateofmedicine from medicine_master where MedicineName=%s",[name])
        data=cur.fetchone()
        mysql.connection.commit()
        cur.close()
        if(result>0):
            if int(data['QuantityAvailable'])>=amount:
                m=dict()
                m['rate']=data['Rateofmedicine']
                m['amnt']=amount*int(data['Rateofmedicine'])
                Form.name=name
                Form.quantity=amount
                return render_template('issuemedicine.html',m=m,form=Form)
                
            else:
                error="Unavailable sorry only Quantity is "+str(data['QuantityAvailable'])+" Available"
                return render_template('issuemedicine.html',error=error)
        else:
            error="MedicineName Invalid"
            return render_template('issuemedicine.html',error=error)
    if request.method=='POST' and request.form['btn']=="issue":
        amant=request.form['quantity']
        name=request.form['name']
        cur=mysql.connection.cursor()
        result=cur.execute("select QuantityAvailable,MedicineID from  medicine_master where MedicineName=%s",[name])
        data=cur.fetchone()
        mysql.connection.commit()
        cur.close()
        if result>0:
            amnt=int(data['QuantityAvailable'])-int(amant)
            cur=mysql.connection.cursor()
            cur.execute("update medicine_master set QuantityAvailable=%s where MedicineName=%s",[amnt,name])
            mysql.connection.commit()
            cur.close()
            cur=mysql.connection.cursor()
            cur.execute("insert into tracking_medicines values(%s,%s,%s)",(session['username'],data['MedicineID'],amant))
            mysql.connection.commit()
            cur.close()
            session['iss']=False
            return render_template("issuemedicine.html")
        else:
            return "hello"
        

    if request.method=='POST' and request.form['btn']=="update":
        if session['iss']!=False:
            amant=request.form['quantity']
            name=request.form['name']
            cur=mysql.connection.cursor()
            result=cur.execute("select QuantityAvailable,MedicineID from  medicine_master where MedicineName=%s",[name])
            data=cur.fetchone()
            mysql.connection.commit()
            cur.close()
            if result>0:
                amnt=int(data['QuantityAvailable'])-int(amant)
                cur=mysql.connection.cursor()
                cur.execute("update medicine_master set QuantityAvailable=%s where MedicineName=%s",[amnt,name])
                mysql.connection.commit()
                cur.close()
                cur=mysql.connection.cursor()
                cur.execute("insert into tracking_medicines values(%s,%s,%s)",(session['username'],data['MedicineID'],amant))
                mysql.connection.commit()
                cur.close()
                session['iss']=False

                msg="medicine issued sucessfully"
                session['username']="somethingelse"
                return render_template('mainpage.html',msg=msg)
        else:
                session['iss']=False
                msg="medicine issued sucessfully"
                session['username']="somethingelse"
                return render_template('mainpage.html',msg=msg)


        
    return render_template('issuemedicine.html')
@app.route('/patientdiagnostic',methods=['GET','POST'])
def patientdiagnostic():
    data=""
    if request.method=='POST' :
        sid=int(request.form['id'])
        session["diagnostic"]=sid
        cur=mysql.connection.cursor()
        cur1=mysql.connection.cursor()
        result=cur.execute("select * from patients where PatientID=%s",[sid])
        cur1.execute("select a.TestName,a.Chargefortest from diagnostics_master a,tracking_diagnostics b where a.TestID=b.TestID and b.PatientID=%s",[sid])       
        data=cur.fetchone()
        data1=list(cur1.fetchall())
        print(data1)
        mysql.connection.commit()
        cur1.close() 
        cur.close()
        print(data1)
        if result>0:
            return render_template('patientdiagnostic.html',data=data,data1=data1)
        else:
            return render_template('patientdiagnostic.html',error="Invalid PatientID, Sorry!",data=data)
    return render_template('patientdiagnostic.html',data=data)
        
@app.route('/diagnostics',methods=["GET","POST"])
def diagnostic():
    data=""
    l=list()
    cur=mysql.connection.cursor()
    cur.execute("select * from diagnostics_master")
    data=cur.fetchall()
    mysql.connection.commit()
    cur.close()
    for i in data:
        l.append(i['TestName'])
    

    if request.method=="POST" and request.form['btn']=="search1":
        
        n=list()
        name=request.form['id']
        cur=mysql.connection.cursor()
        result=cur.execute("select * from diagnostics_master where TestName=%s ",[name])
        data=cur.fetchone()
        mysql.connection.commit()
        cur.close()
        if result>0:
            session['up']=True
            render_template("diagnostics.html",data=data)
        else:
            error="Test Name Invalid !"
            return render_template("diagnostics.html",error=error,data=data,l=l)
    if request.method=="POST" and request.form['btn']=="add":
        testname=str(request.form["id"])

        cur=mysql.connection.cursor()
        result=cur.execute("select * from diagnostics_master where TestName=%s",[testname])
        data=cur.fetchone()
        mysql.connection.commit()
        cur.close()
        if result>0:
            cur=mysql.connection.cursor()
            cur.execute("insert into tracking_diagnostics values(%s,%s)",(session['diagnostic'],data['TestID']))
            mysql.connection.commit()
            cur.close()
            
            session['up']=False
            return render_template('diagnostics.html',data="",l=l)
            
        else:
            error="TestId not found"
            return render_template('diagnostics.html',l=l,data=data,error=error)
    
        
        
    if request.method=='POST' and request.form['btn']=="update":
        if session['up']!=False:
            testname=str(request.form["id"])

            cur=mysql.connection.cursor()
            result=cur.execute("select * from diagnostics_master where TestName=%s",[testname])
            data=cur.fetchone()
            mysql.connection.commit()
            cur.close()
            if result>0:
                cur=mysql.connection.cursor()
                cur.execute("insert into tracking_diagnostics values(%s,%s)",(session['diagnostic'],data['TestID']))
                mysql.connection.commit()
                cur.close()
                session['diagnostic']=False

                msg="diagnostic added sucessfully"
                session['username']="somethingelse"
                session.pop('diagnostic')
                return render_template('mainpage.html',msg=msg)
        else:
                msg="diagnostic added sucessfully"
                session['username']="somethingelse"
                session.pop('diagnostic')
                return render_template('mainpage.html',msg=msg)

        

    return render_template('diagnostics.html',l=l,data=data)
@app.route('/finalbilling',methods=['GET','POST'])
def finalbilling():
    data=""
    sum=0
    sum2=0
    sum1=0
    num=0
   
    d={'General':2000,'Sharing':4000,'Single':8000}
   
    if request.method=='POST' and request.form['btn']=="search":
        id=request.form['id']
        cur=mysql.connection.cursor()
        result=cur.execute("select * from patients where PatientID=%s",[id])
        data=cur.fetchone()
        mysql.connection.commit()
        cur.close()
        
        
        if result>0:
            date2=str(date.today())
            date1=str(data['DateofAdmission'])
            date2=date2.split('-')
            date1=date1.split('-')
            date2=date(int(date2[0]),int(date2[1]),int(date2[2]))
            date1=date(int(date1[0]),int(date1[1]),int(date1[2]))
            var=str(date2-date1)
            var=var.split(' ')
            if len(var)>1:
                var1=int(var[0])
                var2=d[data['Typeofbed']]
                sum=var1*var2
                num=var1

            cur=mysql.connection.cursor()
            cur.execute("select a.MedicineName, b.QuantityIssued ,a.Rateofmedicine from medicine_master a,tracking_medicines b where a.MedicineId=b.IDofMedicineIssued and b.PatientID=%s",[id])
            data1=cur.fetchall()
            mysql.connection.commit()
            cur.close()
            for i in data1:
                sum1+=int(i['QuantityIssued'])*int(i['Rateofmedicine'])
            cur=mysql.connection.cursor()
            cur.execute("select b.TestName,b.Chargefortest from  diagnostics_master b,tracking_diagnostics a where a.TestID=b.TestID and a.PatientID=%s",[id])
            data2=cur.fetchall()
            mysql.connection.commit()
            cur.close()
            for i in data2:
                sum2+=int(i['Chargefortest'])
            return render_template('finalbilling.html',data=data,data1=data1,data2=data2,sum=sum,sum1=sum1,sum2=sum2,date2=date2,num=num)
        else:
            error="Invalid PatientID"
            return render_template('finalbilling.html',error=error,data=data)
    if request.method=="POST" and request.form['btn']=="confirm":
        id=request.form['id']
        cur=mysql.connection.cursor()
        cur.execute("delete from patients where PatientID=%s",[id])
        mysql.connection.commit()
        cur.close()
        msg="Patient Discarged sucessfully"
        return render_template('mainpage.html',msg=msg)


    return render_template('finalbilling.html',data=data)


if __name__=='__main__':
    app.secret_key="secret12345"
    app.run(debug=True)