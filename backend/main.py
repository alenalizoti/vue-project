from flask import Flask , jsonify, request
import mysql.connector
from flask_cors import CORS
import os, base64
from PIL import Image
from io import BytesIO
import random
import string
import imghdr

mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "",
    database = "wsit"
)

app = Flask(__name__)
CORS(app)


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
UPLOAD_FOLDER = '../frontend/public/users_images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
UPLOAD_FOLDER_PRODUCTS = '../frontend/public/products'
app.config['UPLOAD_FOLDER_PRODUCTS'] = UPLOAD_FOLDER_PRODUCTS



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def proveri_username(username):

    cursor = mydb.cursor(prepared=True)
    sql_upit = "select * from korisnici where username = ?"
    parametar = (username,)
    cursor.execute(sql_upit,parametar)
    korisnik = cursor.fetchone()

    return korisnik

def vrati_proizvod(naziv_proizvoda):

    cursor = mydb.cursor(prepared=True)
    sql_upit = "select * from proizvodi where naziv = ?"
    parametar = (naziv_proizvoda,)
    cursor.execute(sql_upit,parametar)
    proizvod = cursor.fetchone()

    return proizvod

def vrati_proizvod_preko_id(id_proizvoda):

    cursor = mydb.cursor(prepared=True,dictionary=True)
    sql_upit = "select * from proizvodi where id = ?"
    parametar = (id_proizvoda,)
    cursor.execute(sql_upit,parametar)
    proizvod = cursor.fetchone()

    return proizvod

def proveri_korisnika(username):

    cursor = mydb.cursor(dictionary=True)
    sql_upit = f"select * from korisnici where username = '{username}'"
    cursor.execute(sql_upit)
    korisnik = cursor.fetchone()

    return korisnik

@app.route('/')
def indeks():
    return "CAO"


@app.route('/register', methods = ["POST"]) 
def register():
    if request.method == 'POST':

        data = request.json
        # print('Primljeni podaci za registraciju:', data)
        username = data.get('username')
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        email = data.get('email')
        godiste = data.get('godiste')
        stanje_novca = data.get('stanje_novca')
        vrsta_korisnika = data.get('vrsta_korisnika')

        korisnik = proveri_username(username)

        
        if korisnik != None:
            response_data = {"success" : False, "message" : "Username vec postoji!"} 
            return jsonify(response_data), 400
        else:
            base64_data = data['putanja_img']
            image_data = base64.b64decode(base64_data)
            image = Image.open(BytesIO(image_data))
            ext = imghdr.what(None, h=image_data)
            if ext and ext.lower() in ALLOWED_EXTENSIONS:

                image_name = f'{username}.{ext}'
                image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_name)
                image.save(image_path)

                cursor = mydb.cursor(prepared=True)
                sql_upit = "INSERT INTO korisnici (username, password, email, godiste, image_path, trenutno_stanje_novca, tip_korisnika) VALUES (?, ?, ?, ?, ?, ?, ?)"
                parametri = (username,password,email,godiste,image_path,stanje_novca,vrsta_korisnika)
                cursor.execute(sql_upit,parametri)
                mydb.commit()


                response_data = {"success": True, "message": "Registracija uspešna"}
                return jsonify(response_data) , 200
           
            

@app.route('/login', methods = ['POST'])
def login():

    if request.method == 'POST':
        data = request.json

        username = data.get('username')
        password = data.get('password')

        korisnik = proveri_korisnika(username)
        
        if korisnik == None:
            response_data = {"success" : False, "message" : "Korisnik sa tim usernameom ne postoji"}
            return jsonify(response_data) , 400
        
        password_iz_baze = korisnik['password']

        if password_iz_baze != password:
            response_data = {"success" : False, "message" : "Netacna lozinka"}
            return jsonify(response_data) , 400
        
       
        
        response_data = {"success" : True, "message" : "Uspesno ulogovan!", "data" : korisnik}
        return jsonify(response_data),200
    
@app.route('/profil/<username>', methods = ['GET'])
def profil(username):

    cursor = mydb.cursor(prepared=True, dictionary=True)
    sql_upit = "select * from korisnici where username = ?"
    parametar = (username,)
    cursor.execute(sql_upit,parametar)
    korisnik = cursor.fetchone()


    image_path = korisnik.get('image_path')
    _, ext = os.path.splitext(image_path)
    ext = ext.lower()

    if ext[1:] in ALLOWED_EXTENSIONS:
        response_data = {"message" : "dohvatili ste korisnika!", "data" : korisnik, "ext": ext}
    return jsonify(response_data) , 200


@app.route('/profil/update/<username>', methods = ['GET','PUT'])
def update(username):
    user = proveri_korisnika(username)

    if request.method == 'GET':
        cursor = mydb.cursor(prepared=True, dictionary=True)
        sql_upit = "select * from korisnici where username = ?"
        parametar = (username,)
        cursor.execute(sql_upit,parametar)
        korisnik = cursor.fetchone()

        response_data = {"message" : "dohvatili ste korisnika!", "data" : korisnik}
        return jsonify(response_data)
    
    if request.method == 'PUT':

        data = request.json

        username = data.get('username')
        password = data.get('password')
        new_password = data.get('new_password')
        email = data.get('email')
        godiste = data.get('godiste')
        
        username_korisnika = user['username']

        if username == '' or password == '' or new_password == '' or email == '' or godiste == '':
            return jsonify({"message" : "Niste popunili sva polja!"}), 400
        
        if len(username) < 3:
            return jsonify({"message" : "Username mora da ima minimalno 3 karaktera"}), 400
        
        if password != user['password']:
            return jsonify({"message" : "Netacna lozinka!"}), 400
        
        if len(new_password) < 5:
            return jsonify({"message" : "Lozinka mora da ima bar 5 karaktera!"}), 400
        
        if godiste < 1900 or godiste > 2024:
            return jsonify({"message" : "Unos za godsite noje validan!"}), 400
        
        if '@' not in email or '.' not in email:
            return jsonify({"message" : "Email mora da sadrzi @ i ."}), 400
        
        base64_data = data['putanja_img']
        if base64_data != '':
            image_data = base64.b64decode(base64_data)
            image = Image.open(BytesIO(image_data))
            ext = imghdr.what(None, h=image_data)
            if ext and ext.lower() in ALLOWED_EXTENSIONS:
                image_name = f'{username}.{ext}'
                image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_name)
                image.save(image_path)

                cursor = mydb.cursor(prepared=True)
                sql_upit = "update korisnici set username = ?, password = ?, email = ?, godiste = ?, image_path = ? where username = ?"
                parametri = (username,new_password,email,godiste,image_path,username_korisnika)
                cursor.execute(sql_upit,parametri)
                mydb.commit()

                response_data = {"success": True, "message": "Update uspešan"}
                return jsonify(response_data) , 200
        else:
            cursor = mydb.cursor(prepared=True)
            sql_upit = "update korisnici set username = ?, password = ?, email = ?, godiste = ? where username = ?"
            parametri = (username,new_password,email,godiste,username_korisnika)
            cursor.execute(sql_upit,parametri)
            mydb.commit()

            response_data = {"success": True, "message": "Update uspešan"}
            return jsonify(response_data) , 200

@app.route('/products',methods = ['GET'])
def products():
    cursor = mydb.cursor(dictionary=True)
    sql_upit = 'select * from proizvodi'
    cursor.execute(sql_upit)
    proizvodi = cursor.fetchall()

    for proizvod in proizvodi:
        image_path = proizvod.get('image_path')
        if image_path:
            _, ext = os.path.splitext(image_path)
            proizvod['image_extension'] = ext

    response_data = {'message':'uspesno ste dohvatili proizvode', 'data': proizvodi}
    return jsonify(response_data)
    
@app.route('/products/prodavac/<username>',methods = ['GET'])
def products_prodavac(username):

    korisnik = proveri_korisnika(username)
    tip = korisnik['tip_korisnika']
    id_korisnika = korisnik['id']

    cursor = mydb.cursor(prepared=True, dictionary=True)
    sql = 'select * from proizvodi where korisnici_id = ?'
    parametar = (id_korisnika,)
    cursor.execute(sql,parametar)
    proizvodi = cursor.fetchall()
    
    for proizvod in proizvodi:
        image_path = proizvod.get('image_path')
        if image_path:
            _, ext = os.path.splitext(image_path)
            proizvod['image_extension'] = ext


    response_Data = {'message':'uspesno ste dohvatili proizvode',"data": proizvodi}
    return jsonify(response_Data),200

@app.route('/product/<id>',methods = ['GET'])
def product_id(id):

    cursor = mydb.cursor(prepared=True,dictionary=True)
    sql = "select * from proizvodi where id = ?"
    parametar = (id,)
    cursor.execute(sql,parametar)
    proizvod = cursor.fetchone()
    image_path = proizvod.get('image_path')
    if image_path:
        _, ext = os.path.splitext(image_path)
        proizvod['image_extension'] = ext

    response_data = {'message':'uspesno ste dohvatili proizvod', "data":proizvod}
    return jsonify(response_data)


@app.route('/products/add', methods = ['POST'])
def products_add():

    data = request.json
    naziv = data.get('naziv')
    opis = data.get('opis')
    base64_data = data.get('putanja_img')
    cena = data.get('cena')
    kolicina = data.get('kolicina')
    popust = data.get('popust')
    username = data.get('username')

    proizvod = vrati_proizvod(naziv)
    if proizvod != None:
        response_data = {"message": "Proizvod vec postoji!"}
        return jsonify(response_data),400

    if naziv == '' or opis == '' or base64_data == '' or cena == '' or kolicina == '' or popust == '':
        response_data = {"message": "Popunite sva polja"}
        return jsonify(response_data),400
    
    if cena < 0 or kolicina < 0 or popust < 0:
        response_data = {"message": "Cena,kolicina i popust ne smeju biti negativni!"}
        return jsonify(response_data),400
    

    image_data = base64.b64decode(base64_data)
    image = Image.open(BytesIO(image_data))
    ext = imghdr.what(None, h=image_data)
    if ext and ext.lower() in ALLOWED_EXTENSIONS:
        naziv_split = naziv.split(' ')
        naziv_prva = naziv_split[0]
        image_name = f'{naziv_prva}.{ext}'
        image_path = os.path.join(app.config['UPLOAD_FOLDER_PRODUCTS'], image_name)
        print(image_path)
        image.save(image_path)

        cursor = mydb.cursor(prepared=True)
        sq_korisnik = 'select * from korisnici where username = ?'
        cursor.execute(sq_korisnik,(username,))
        korisnik = cursor.fetchone()
        print(korisnik)
        id_korisnika = korisnik[0]
        print(id_korisnika)
        sql_upit = 'insert into proizvodi values (null,?,?,?,?,?,?,?)'
        parametri = (naziv,opis,cena,kolicina,popust,image_path,id_korisnika)
        cursor.execute(sql_upit,parametri)
        mydb.commit()
    
        return jsonify ({'message':'Uspesno ste dodali proizvod!', 'ext':ext})
    

@app.route('/update_product/<id>', methods = ['PUT', 'GET'])
def update_product(id):
    proizvod = vrati_proizvod_preko_id(id)
    if request.method == 'GET':
        respose_data = {'message':'uspesno ste dohvatili proizvod!', 'data' : proizvod} 
        return jsonify(respose_data), 200
    
    if request.method == 'PUT':

        data = request.json
        naziv = data.get('naziv')
        opis = data.get('opis')
        cena = data.get('cena')
        kolicina = data.get('kolicina')
        popust = data.get('popust')

        cena = float(cena)
        kolicina = int(kolicina)
        popust = float(popust)

        print(type(popust))
        if cena < 0 or kolicina < 0 or popust < 0:
            response_data = {"message": "Cena,kolicina i popust ne smeju biti negativni!"}
            return jsonify(response_data),400

        if naziv == '' or opis == '' or cena == '' or kolicina == '' or popust == '':
            respose_data = {'message':'Popunite sva polja!'}
            return jsonify(respose_data), 400
        
       
        
        id_proizvoda = proizvod['id']

        cursor = mydb.cursor(prepared=True)
        sql_upit = 'update proizvodi set naziv = ?, opis = ?, cena = ?, kolicna_na_stanju = ?, opcija_za_snizenje = ? where id = ?'
        parametri = (naziv,opis,cena,kolicina,popust,id_proizvoda)
        cursor.execute(sql_upit,parametri)
        mydb.commit()
    
        response_data = {'message':'uspesno ste izmenili proizvod!', 'data' : data} 
        return jsonify(response_data), 200
    
@app.route('/product/delete/<id>', methods = ['DELETE'])
def product_delete(id):

    proizvod = vrati_proizvod_preko_id(id)
    cursor = mydb.cursor(prepared=True)
    sql_upit = 'delete from proizvodi where id = ?'
    parametar = (id,)
    cursor.execute(sql_upit,parametar)
    mydb.commit()

    response_data = {'message':'uspesno ste obrisali proizvod!'}
    return jsonify(response_data)

@app.route('/products/<product_id>/comment',methods = ['POST'])
def product_coment(product_id):
    
    data = request.json
    komentar = data.get('komentar')
    korisnik_id = data.get('id_korisnika')

    if komentar == '':
        response_data = {'message':'Popunite polje za komentar!'}
        return jsonify(response_data), 400
    
    cursor = mydb.cursor(prepared=True)
    sql = 'insert into komentari values (null,?,now(),?,?)'
    parametri = (komentar,product_id,korisnik_id)
    cursor.execute(sql,parametri)
    mydb.commit()

    return jsonify({"message":'uspesno','data': data})

@app.route('/products/comments/<id>',methods = ['GET'])
def products_comments(id):

    cursor = mydb.cursor(dictionary=True,prepared=True)
    sql = '''select komentari.*, korisnici.username
    from komentari
    JOIN korisnici ON komentari.Korisnici_id = korisnici.id
    where komentari.Proizvodi_id = ?'''
    parametar = (id,)
    cursor.execute(sql,parametar)
    komentari = cursor.fetchall()

    response_data = {'message':'dohvatili ste korisnike','data':komentari}
    return jsonify(response_data), 200

@app.route('/products/<product_id>/comment/delete/<comment_id>', methods = ['DELETE'])
def delete_comment(product_id,comment_id):

    cursor = mydb.cursor(prepared=True)
    sql = 'delete from komentari where id = ? and Proizvodi_id = ?'
    parametar = (comment_id,product_id)
    cursor.execute(sql,parametar)
    mydb.commit()

    if cursor.rowcount > 0:
        return jsonify({'message': 'Uspešno ste obrisali komentar!'}), 200
    else:
        return jsonify({'error': 'Komentar sa datim ID-om ne postoji!'}), 404

@app.route('/cart/add/<product_id>',methods = ['POST'])
def cart_add(product_id):
    
    data = request.json
    kolicina = data.get('kolicina')
    korisnik_id = data.get('korisnik_id')

    proizvod = vrati_proizvod_preko_id(product_id)
    kolicina_na_stanju = proizvod['kolicna_na_stanju']

    cursor = mydb.cursor(prepared=True)
    sql = 'insert into korpa_proizvodi values (null,?,?,?)'
    parametri = (korisnik_id,product_id,kolicina)
    cursor.execute(sql,parametri)
    mydb.commit()

    if kolicina > kolicina_na_stanju:
        return jsonify({'message':'Nema dovoljno proizvoda na stanju!'}), 400
    
    return jsonify({'data':data,'kolicina':kolicina_na_stanju})

@app.route('/cart/<korisnik_id>', methods = ['GET'])
def cart(korisnik_id):
    
    cursor = mydb.cursor(prepared=True,dictionary=True)

    sql_proizvodi = 'SELECT proizvodi.*, korpa_proizvodi.kolicina FROM proizvodi INNER JOIN korpa_proizvodi ON proizvodi.id = korpa_proizvodi.proizvod_id WHERE korpa_proizvodi.korisnik_id = ?'
    cursor.execute(sql_proizvodi, (korisnik_id,))
    proizvodi = cursor.fetchall()

    response_data = {
        'proizvodi' : proizvodi
    }

    return jsonify({'message':'uspesno ste dohvatili','data':response_data}), 200

@app.route('/cart/delete/<product_id>', methods = ['DELETE'])
def cart_delete(product_id):

    cursor = mydb.cursor(prepared=True)
    sql = 'delete from korpa_proizvodi where proizvod_id = ?'
    cursor.execute(sql,(product_id,))
    mydb.commit()

    return jsonify({'message':'uspesno ste uklonili iz korpe'}), 200

@app.route('/cart/update/<product_id>', methods = ['PUT'])
def cart_update(product_id):

    data = request.json
    kolicina = data.get('kolicina')
    cursor = mydb.cursor(prepared=True)
    sql = 'update korpa_proizvodi set kolicina = ? where proizvod_id = ?'
    cursor.execute(sql,(kolicina,product_id))
    mydb.commit()

    return jsonify({'message':'uspesno ste azurirali kolicinu!'}), 200

@app.route('/checkout', methods = ['POST'])
def checkout():

    data = request.json
    # print(data)
    cena_za_placanje = data.get('cena')
    id_korisnika = data.get('korisnik_id')
    proizvodi = data.get('proizvodi')

    for proizvod in proizvodi:
        prodavac_id = proizvod['korisnici_id']
        kolicina = proizvod['kolicna_na_stanju']
        id_proizvoda = proizvod['id']

        cursor = mydb.cursor(prepared=True,dictionary=True)
        sql_kupac = 'select * from korisnici where id = ?'
        cursor.execute(sql_kupac,(id_korisnika,))
        korisnik = cursor.fetchone()

        stanje_novca_kupca = korisnik['trenutno_stanje_novca']
        kolicina_proizvoda = proizvod['kolicna_na_stanju']
        # print(stanje_novca_kupca)

        if cena_za_placanje > stanje_novca_kupca:
            # print(stanje_novca_kupca)
            return jsonify({'message':'Nemate dovoljno novca!'}), 400
    
        novo_stanje = stanje_novca_kupca - cena_za_placanje

        cursor.execute('UPDATE korisnici SET trenutno_stanje_novca = ? WHERE id = ?',(novo_stanje,id_korisnika) )

        sql_prodavac = 'SELECT * FROM korisnici WHERE id = ?'
        cursor.execute(sql_prodavac, (prodavac_id,))
        prodavac = cursor.fetchone()

        stanje_novca_prodavca = prodavac['trenutno_stanje_novca']
        novo_stanje_prodavca = stanje_novca_prodavca + cena_za_placanje

        cursor.execute('UPDATE korisnici SET trenutno_stanje_novca = ? WHERE id = ?', (novo_stanje_prodavca, prodavac_id))
        sql_kolicina = '''select korpa_proizvodi.kolicina,proizvodi.kolicna_na_stanju 
        from proizvodi 
        join korpa_proizvodi on proizvodi.id = korpa_proizvodi.proizvod_id
        where korpa_proizvodi.proizvod_id = ?'''
        cursor.execute(sql_kolicina,(id_proizvoda,))
        kolicina_porudzbina = cursor.fetchone()
        kolicina_iz_korpe = kolicina_porudzbina['kolicina']
        kolicina_iz_baze = kolicina_porudzbina['kolicna_na_stanju']
        print(kolicina_iz_korpe,kolicina_iz_baze)
        nova_kolicina = kolicina_iz_baze - kolicina_iz_korpe
        if nova_kolicina < 0:
            return jsonify({"message":'Proizvod nije na stanju!'})
        

        sql_prodavac_stanje = 'update proizvodi set kolicna_na_stanju = ? where id = ?'
        cursor.execute(sql_prodavac_stanje,(nova_kolicina,id_proizvoda))

        sql_kupovina = 'insert into kupovina values (null, now(),?,?)'
        cursor.execute(sql_kupovina,(id_korisnika,id_proizvoda))
       
        cursor.execute('DELETE FROM korpa_proizvodi WHERE korisnik_id = ?', (id_korisnika,))
        mydb.commit()


    return jsonify({'message':'uspesno izvrsena kupovina!'})

@app.route('/admin/users',methods = ['GET'])
def admin_users():
    cursor = mydb.cursor(prepared=True,dictionary=True)
    sql = 'select * from korisnici'
    cursor.execute(sql)
    korisnici = cursor.fetchall()

    return jsonify({'data':korisnici}), 200

@app.route('/admin/users/delete/<id>', methods = ['DELETE'])
def admin_users_delete(id):

    cursor = mydb.cursor(prepared=True)
    sql = 'delete from korisnici where id = ?'
    cursor.execute(sql,(id,))
    mydb.commit()

    return jsonify({'message':'uspesno ste obrisali korisnika!'})

@app.route('/admin/users/update/<username>', methods = ['GET','PUT'])
def admin_update(username):

    if request.method == 'GET':
        cursor = mydb.cursor(prepared=True,dictionary=True)
        sql = 'select * from korisnici where username = ?'
        cursor.execute(sql,(username,))
        korisnik = cursor.fetchone()

        return jsonify({'data': korisnik})
    
    if request.method == 'PUT':
        data = request.json
        password = data.get('password')
        email = data.get('email')
        godiste = data.get('godiste')
        stanje_novca = data.get('stanje_novca')
        tip_korisnika = data.get('tip_korisnika')
        stanje_novca = int(stanje_novca)
        
        if password == '' or email == '' or godiste == ''  or stanje_novca =='' or tip_korisnika == '':
            response_data = {'message':'Popunite sva polja!'}
            return jsonify(response_data), 400
        
        if '@' not in email or '.' not in email:
            response_data = {'message':'Email mora da sadrzi @ i .'}
            return jsonify(response_data), 400
        
        if godiste < 1900 or godiste > 2024:
            response_data = {'message':'Unos za godinu rodjenja nije validan!!'}
            return jsonify(response_data), 400
        
        if stanje_novca < 0:
            response_data = {'message':'Novac na racunu ne sme biti negativan!!'}
            return jsonify(response_data), 400
    

        base64_data = data['putanja_img']
        if base64_data != '':
            image_data = base64.b64decode(base64_data)
            image = Image.open(BytesIO(image_data))
            ext = imghdr.what(None, h=image_data)
            if ext and ext.lower() in ALLOWED_EXTENSIONS:
                image_name = f'{username}.{ext}'
                image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_name)
                image.save(image_path)

                cursor = mydb.cursor(prepared=True)
                sql_upit = 'update korisnici set password = ?, email = ?, godiste = ?, image_path = ?, trenutno_stanje_novca = ?, tip_korisnika = ? where username = ?'
                parametri = (password,email,godiste,image_path,stanje_novca,tip_korisnika, username)
                cursor.execute(sql_upit,parametri)
                mydb.commit()

                response_data = {"success": True, "message": "Update uspešan"}
                return jsonify(response_data) , 200
        else:
            cursor = mydb.cursor(prepared=True)
            sql_upit = sql = 'update korisnici set password = ?, email = ?, godiste = ?, trenutno_stanje_novca = ?, tip_korisnika = ? where username = ?'
            parametri = (password,email,godiste,stanje_novca,tip_korisnika, username)
            cursor.execute(sql_upit,parametri)
            mydb.commit()

            response_data = {"success": True, "message": "Update uspešan"}
            return jsonify(response_data) , 200
        
@app.route('/istorija/kupovina/<id>', methods = ['GET'])
def istorija_kupovina(id):

    cursor = mydb.cursor(prepared=True, dictionary=True)
    sql = '''select kupovina.*, proizvodi.cena, proizvodi.naziv 
    from kupovina 
    join proizvodi on proizvodi.id = kupovina.proizvod_id
    where kupovina.Korisnici_id = ?'''
    cursor.execute(sql,(id,))
    kupovina = cursor.fetchall()

    

    return jsonify ({'data2': kupovina})

app.run(debug=True)