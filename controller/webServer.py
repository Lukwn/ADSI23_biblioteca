import string

from .LibraryController import LibraryController
from flask import Flask, render_template, request, redirect
from datetime import date, datetime

app = Flask(__name__, static_url_path='', static_folder='../view/static', template_folder='../view/')


library = LibraryController()


@app.before_request
def get_logged_user():
	if '/css' not in request.path and '/js' not in request.path:
		token = request.cookies.get('token')
		time = request.cookies.get('time')
		if token and time:
			request.user = library.get_user_cookies(token, float(time))
			if request.user:
				request.user.token = token


@app.after_request
def add_cookies(response):
	if 'user' in dir(request) and request.user and request.user.token:
		session = request.user.validate_session(request.user.token)
		response.set_cookie('token', session.hash)
		response.set_cookie('time', str(session.time))
	return response


@app.route('/')
def index():
	return render_template('index.html')


@app.route('/catalogue')
def catalogue():
	title = request.values.get("title", "")
	author = request.values.get("author", "")
	page = int(request.values.get("page", 1))
	books, nb_books = library.search_books(title=title, author=author, page=page - 1)
	total_pages = (nb_books // 6) + 1
	return render_template('catalogue.html', books=books, title=title, author=author, current_page=page,
	                       total_pages=total_pages, max=max, min=min)

@app.route('/lagunSarea')
def lagunSarea():
	idUser = request.user.id
	page = int(request.values.get("page", 1))
	lagunak, pictures, nb_lagun = library.search_lagunak(id=idUser, page=page-1)
	total_pages = (nb_lagun // 10) + 1
	return render_template('lagunSarea.html', idUser=idUser, lagunak=lagunak, pictures=pictures, zip=zip, current_page=page,
						   total_pages=total_pages, max=max, min=min)

@app.route('/erabiltzaileak')
def erabiltzaileak():
	username = request.values.get("username", "")
	page = int(request.values.get("page", 1))
	erabiltzaileak, pictures, nb_erabiltzaile = library.search_user(username=username, page=page - 1)
	total_pages = (nb_erabiltzaile // 10) + 1
	return render_template('erabiltzaileak.html', erabiltzaileak=erabiltzaileak, pictures =pictures, zip=zip,
						   current_page=page, total_pages=total_pages, max=max, min=min)

@app.route('/eskaerak')
def eskaerak():
	idUser = request.user.id
	page_bidali = int(request.values.get("page_bidali", 1))
	page_jaso = int(request.values.get("page_jaso", 1))
	bidali, picturesBidali, nb_bidali = library.get_bidalitakoEskaerak(page=page_bidali-1)
	jaso, picturesJaso, nb_jaso = library.get_jasotakoEskaerak(page=page_jaso - 1)
	total_pages_bidali = (nb_bidali // 5) + 1
	total_pages_jaso = (nb_jaso // 5) + 1
	return render_template('eskaerak.html', idUser=idUser,
						   bidali=bidali, jaso=jaso,
						   picturesBidali=picturesBidali, picturesJaso=picturesJaso, zip=zip,
						   current_page_bidali=page_bidali, current_page_jaso=page_jaso,
						   total_pages_bidali=total_pages_bidali, total_pages_jaso=total_pages_jaso,
						   max=max, min=min)

@app.route('/<string>')
def profil(string):

	parts = string.split('-', 1)
	if len(parts) < 2:
		return "Formato incorrecto", 400

	prefix, username = parts

	#Erabiltzile bat balitz user->usr
	if (prefix=='usr'):
		user = library.getUserUsername(username)
		if user is None:
			return "Usuario no encontrado", 404
		picture = library.get_picture(user.picture)
		page_erreseina = int(request.values.get("page_erreseina", 1))
		page_erreserba = int(request.values.get("page_erreserba", 1))
		erreseinak, books_erreseina, count_erreseina = library.get_erreseinaGuztiak(id=user.id, page=page_erreseina - 1)
		erreserbak, books_erreserba, count_erreserba = library.get_erreseinaGuztiak(id=user.id, page=page_erreserba - 1)
		total_pages_erreseina = (count_erreseina // 5) + 1
		total_pages_erreserba = (count_erreserba // 5) + 1
		return render_template('profila.html', user=user, picture=picture,
							   erreseinak=erreseinak, books_erreseina=books_erreseina,
							   erreserbak=erreserbak, books_erreserba= books_erreserba,
							   total_pages_erreseina=total_pages_erreseina, current_page_erreseina=page_erreseina,
							   total_pages_erreserba=total_pages_erreserba, current_page_erreserba=page_erreserba,
							   zip=zip, max=max, min=min)

	#Lagun eskaera bidaltzea balitz gehituLaguna->gl
	elif (prefix=='gl'):
		return gehitu(username)

	#Lagun bat kentzea edo Eskaera bat ukatzea balitz kendu
	elif (prefix=='kl'):
		return kendu(username)

	# Eskaera bat ukatzea balitz ukatuEskaera->ue
	elif (prefix == 'ue'):
		return ukatu(username)

	#Eskaera bat onartzea balitz onartuEskaera->oe
	elif (prefix=='oe'):
		return onartu(username)

	else:
		return "Prefix not found", 404

def gehitu(id):
	resp = redirect('/erabiltzaileak')
	user = library.getUser(id)
	library.gehituLagun(user.id)
	return resp
def kendu(id):
	resp = redirect('/lagunSarea')
	user = library.getUser(id)
	library.kenduUkatu(user.id)
	return resp
def ukatu(id):
	resp = redirect('/eskaerak')
	user = library.getUser(id)
	library.kenduUkatu(user.id)
	return resp
def onartu(id):
	resp = redirect('/eskaerak')
	user = library.getUser(id)
	library.onartuEskaera(user.id)
	return resp

@app.route('/book', methods=['GET', 'POST'])
def book():
	#ERRESERBAK
	id = request.values.get("id", "")
	book = library.get_book(id=id)
	msg = None
	botoia_eskuragai = True
	liburu_erreserbak = library.getLiburuErreserbaAktiboak(book_id=book.id)
	if len(liburu_erreserbak) == 0:
		if request.method == 'POST':
			if "erreserbatu" in request.form:
				if 'user' in request.__dict__ and request.user and request.user.token:
					id = request.user.id
					erab_erreserbak = library.getErabiltzaileErreserba(id=id)
					ahal_du = True
					for erreserba in erab_erreserbak:
						erreserba_data = datetime.strptime(erreserba.bueltatze_data, "%Y-%m-%d").date()
						if erreserba_data < date.today() and erreserba.bueltatu_da == 0:
							msg = "Erreserbatu duzun liburu baten denbora-muga pasatu da eta ez duzu bueltatu, ezin dituzu liburu gehiago erreserbatu."
							ahal_du = False
							botoia_eskuragai = False
							break
					if ahal_du:
						library.erreserbatu(id=id, book_id=book.id)
						botoia_eskuragai = False
						msg = "Liburua erreserbatu duzu."
				else:
					return redirect("/login")
	else:
		msg = "Ez dago liburuaren kopiarik eskuragai."
		botoia_eskuragai = False

	#ERRESEINAK
	book_id = id
	edit= False
	msg_erreseina = None
	if request.method == 'POST':
		user_id = request.user.id
		izarKop = request.form.get("izarKop", 0)
		iruzkina = request.form.get("iruzkina", "")
		# baldintzak
		if izarKop:
			izarKop = int(izarKop)
			if 0 <= izarKop <= 10 and len(iruzkina) <= 1000:
				# edit/add
				editing = request.form.get("editing", "")
				if (editing == 'True'):
					library.edit_erreseina(user_id=user_id, book_id=book_id, izarKop=izarKop, iruzkina=iruzkina)
				else:
					library.add_erreseina(user_id=user_id, book_id=book_id, izarKop=izarKop, iruzkina=iruzkina)
			elif izarKop > 10 or izarKop < 0:
				msg_erreseina = "Izar kopurua 0 eta 10 artean egon behar da"
			else:
				msg_erreseina = "Iruzkina ezin ditu 1000 karaktere baino gehiago izan"

		else:
			msg_erreseina = "Izar kopurua adierazi mesedez"


		# editatzeko botoia sakatzean
		editable = request.form.get("editable", "")
		if (editable == 'True'):
			edit = True


	#erreseinak erakutsi
	if 'user' in dir(request) and request.user and request.user.token:
		user_id = request.user.id
		erreseina_ahal_du = library.erreseinatu_ahal_du(user_id=user_id, book_id=book_id)
	else:
		user_id = 0

	erreseinak, count = library.get_erreseinak(id=id, user_id=user_id)
	user_erreseina = library.get_user_erreseina(id=id, user_id=user_id)
	page = int(request.values.get("page", 1))
	total_pages = (count // 20) + 1
	# konprobatu erreseina existitzen den edo utzik dagoen
	if (len(user_erreseina) > 0):
		# existitzekotan informazioa gorde
		user_erreseina = user_erreseina[0]

	return render_template('book.html', book=book, erreseinak=erreseinak, user_erreseina=user_erreseina, erreseina_ahal_du=erreseina_ahal_du, edit=edit, msg=msg, msg_erreseina=msg_erreseina, botoia_eskuragai=botoia_eskuragai,
							   current_page=page,
							   total_pages=total_pages, max=max, min=min)


@app.route('/history')
def history():
	if 'user' in request.__dict__ and request.user and request.user.token:
		title = request.values.get("title", "")
		author = request.values.get("author", "")
		page = int(request.values.get("page", 1))
		id = request.user.id
		data = date.today()
		books, nb_books = library.search_history(id=id, title=title, author=author, page=page - 1)
		total_pages = (nb_books // 6) + 1
		return render_template('history.html', books=books, title=title, author=author, current_page=page,
							   total_pages=total_pages, max=max, min=min, data=data)
	else:
		return redirect('/login')
@app.route('/bueltatu_erabiltzaile', methods=['GET', 'POST'])
def bueltatu_erabiltzaile():
	if request.method == 'POST':
		id = request.form.get("id", "")
		return redirect(f"/bueltatu_aukeratu?user={id}")
	else:
		resp = render_template('bueltatu_erabiltzaile.html')
	return resp

@app.route('/bueltatu_aukeratu', methods=['GET', 'POST'])
def bueltatu_aukeratu():
	user = request.values.get("user", "")
	if request.method == 'POST':
		liburu_id = request.form.get("liburu_id", "")
		library.liburua_bueltatu(user=user, liburu_id=liburu_id)
	title = request.values.get("title", "")
	author = request.values.get("author", "")
	page = int(request.values.get("page", 1))
	data = date.today()
	print(user)
	books, nb_books = library.search_erreserbatuta(user=user, title=title, author=author, page=page - 1)
	total_pages = (nb_books // 6) + 1
	return render_template('bueltatu_aukeratu.html', books=books, title=title, author=author, current_page=page,
						   total_pages=total_pages, max=max, min=min, data=data)





@app.route('/login', methods=['GET', 'POST'])
def login():
	if 'user' in dir(request) and request.user and request.user.token:
		return redirect('/')
	email = request.values.get("email", "")
	password = request.values.get("password", "")
	user = library.get_user(email, password)
	if user:
		session = user.new_session()
		resp = redirect("/")
		resp.set_cookie('token', session.hash)
		resp.set_cookie('time', str(session.time))
	else:
		if request.method == 'POST':
			return redirect('/login')
		else:
			resp = render_template('login.html')
	return resp


@app.route('/logout')
def logout():
	resp = redirect('/')
	resp.delete_cookie('token')
	resp.delete_cookie('time')
	if 'user' in dir(request) and request.user and request.user.token:
		request.user.delete_session(request.user.token)
		request.user = None
	return resp

@app.route('/foro', methods=['GET', 'POST'])
def foro():
	if request.method == 'POST':
		izena = request.form.get("izena", "")
		if len(izena) <= 50:
			library.add_gaia(izena)
	izena, page, gaiak, nb_gaiak, total_pages = foro_info()
	return render_template('foro.html', gaiak=gaiak, izena=izena, current_page=page,
						   total_pages=total_pages, max=max, min=min)

@app.route('/gaia', methods=['GET', 'POST'])
def gaia():
	user_id = request.user.id
	respondiendo_a = 0
	respondiendo_a_txt = ""
	id = request.values.get("id", "")
	gaia = library.get_gaia(id=id)
	page = int(request.values.get("page", 1))
	if request.method == 'POST':
		if request.form.get("respondiendo") == "true":
			respondiendo_a = request.form.get("respondiendo_a")
			respondiendo_a_txt = request.form.get("respondiendo_a_txt")
		library.add_komentario(id, user_id, request.form.get("txt", ""), respondiendo_a, respondiendo_a_txt)
	komentarioak, count = library.search_komentarioak(id, page=page - 1)
	total_pages = (count // 6) + 1
	return render_template('gaia.html', komentarioak=komentarioak, gaia=gaia, id=id, izena=gaia.izena,
						   respondiendo_a=respondiendo_a, respondiendo_a_txt=respondiendo_a_txt, current_page=page, total_pages=total_pages, max=max, min=min)
@app.route('/add_gaia', methods=['GET', 'POST'])
def add_gaia():
	if request.method == 'POST':
		string.izena = request.form.get("izena", "")
		if len(string.izena) <= 50:
			library.add_gaia(string.izena)
			"""izena, page, gaiak, nb_gaiak, total_pages = foro_info()
			return render_template('foro.html', gaiak=gaiak, izena=izena, current_page=page,
								   total_pages=total_pages, max=max, min=min)"""
	return render_template('add_gaia.html')

def foro_info():
	izena = request.values.get("izena", "")
	page = int(request.values.get("page", 1))
	gaiak, nb_gaiak = library.search_gaiak(izena=izena, page=page - 1)
	total_pages = (nb_gaiak // 6) + 1
	return izena, page, gaiak, nb_gaiak, total_pages