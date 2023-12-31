from .LibraryController import LibraryController
from flask import Flask, render_template, request, make_response, redirect
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

@app.route('/foro')
def foro():
	izena = request.values.get("izena", "")
	page = int(request.values.get("page", 1))
	print(izena)
	gaiak, nb_gaiak = library.search_gaiak(izena=izena, page=page - 1)
	total_pages = (nb_gaiak // 6) + 1
	return render_template('foro.html', gaiak=gaiak, izena=izena, curren_page=page,
						   total_pages=total_pages, max=max, min=min())

@app.route('/book', methods=['GET', 'POST'])
def book():
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

	return render_template('book.html', book=book, msg=msg, botoia_eskuragai=botoia_eskuragai)

@app.route('/history')
def history():
	if 'user' in request.__dict__ and request.user and request.user.token:
		title = request.values.get("title", "")
		author = request.values.get("author", "")
		page = int(request.values.get("page", 1))
		id = request.user.id
		books, nb_books = library.search_history(id=id, title=title, author=author, page=page - 1)
		total_pages = (nb_books // 6) + 1
		return render_template('history.html', books=books, title=title, author=author, current_page=page,
							   total_pages=total_pages, max=max, min=min)
	else:
		return redirect('/login')

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
	path = request.values.get("path", "/")
	resp = redirect(path)
	resp.delete_cookie('token')
	resp.delete_cookie('time')
	if 'user' in dir(request) and request.user and request.user.token:
		request.user.delete_session(request.user.token)
		request.user = None
	return resp
