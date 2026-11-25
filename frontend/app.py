from flask import Flask, abort, flash, redirect, render_template, request, url_for

from frontend import api

app = Flask(__name__)
# flash() needs this. fine for a class project, not for a real site
app.secret_key = "dev"


# HTML forms can only send GET or POST. so the form POSTs to flask,
# and flask turns it into the right PATCH or DELETE call to the API.


def clean_form(form, fields):
    """Pull fields out of a form. Blank inputs become None so the API leaves them empty."""
    data = {}
    for field in fields:
        value = form.get(field, "").strip()
        data[field] = value or None
    return data


def movie_form_data(form):
    data = clean_form(form, ["title", "year", "genre", "overview", "rating"])
    # numbers come in from forms as text
    for field in ["year", "rating"]:
        if data[field] is not None:
            data[field] = int(data[field]) if data[field].isdigit() else data[field]
    data["watched"] = "watched" in form  # checkboxes are only sent when checked
    return data


def check_found(response):
    if response.status_code == 404:
        abort(404)
    return response.json()


# ---------- Lists ----------


@app.route("/")
def index():
    lists = api.get("/lists").json()
    return render_template("index.html", lists=lists)


@app.route("/lists/new", methods=["GET", "POST"])
def new_list():
    if request.method == "POST":
        data = clean_form(request.form, ["name", "description"])
        response = api.post("/lists", data)
        if response.status_code == 201:
            flash(f'Made "{data["name"]}"')
            return redirect(url_for("list_detail", list_id=response.json()["id"]))
        for msg in api.error_messages(response):
            flash(msg, "error")
        return render_template("list_form.html", movie_list=data)
    return render_template("list_form.html", movie_list=None)


@app.route("/lists/<int:list_id>")
def list_detail(list_id):
    movie_list = check_found(api.get(f"/lists/{list_id}"))
    movies = api.get(f"/lists/{list_id}/movies").json()
    return render_template("list_detail.html", movie_list=movie_list, movies=movies)


@app.route("/lists/<int:list_id>/edit", methods=["GET", "POST"])
def edit_list(list_id):
    if request.method == "POST":
        data = clean_form(request.form, ["name", "description"])
        response = api.patch(f"/lists/{list_id}", data)
        if response.status_code == 200:
            flash("List updated")
            return redirect(url_for("list_detail", list_id=list_id))
        for msg in api.error_messages(response):
            flash(msg, "error")
        return render_template("list_form.html", movie_list={"id": list_id, **data})
    # GET: grab the current list so the form shows up pre-filled
    movie_list = check_found(api.get(f"/lists/{list_id}"))
    return render_template("list_form.html", movie_list=movie_list)


@app.route("/lists/<int:list_id>/delete", methods=["POST"])
def delete_list(list_id):
    api.delete(f"/lists/{list_id}")
    flash("List deleted")
    return redirect(url_for("index"))


# ---------- Movies ----------


@app.route("/lists/<int:list_id>/movies/new", methods=["GET", "POST"])
def new_movie(list_id):
    movie_list = check_found(api.get(f"/lists/{list_id}"))
    if request.method == "POST":
        data = movie_form_data(request.form)
        response = api.post(f"/lists/{list_id}/movies", data)
        if response.status_code == 201:
            flash(f'Added "{data["title"]}"')
            return redirect(url_for("list_detail", list_id=list_id))
        for msg in api.error_messages(response):
            flash(msg, "error")
        return render_template("movie_form.html", movie_list=movie_list, movie=data)
    return render_template("movie_form.html", movie_list=movie_list, movie=None)


@app.route("/movies/<int:movie_id>")
def movie_detail(movie_id):
    movie = check_found(api.get(f"/movies/{movie_id}"))
    movie_list = api.get(f"/lists/{movie['list_id']}").json()
    return render_template("movie_detail.html", movie=movie, movie_list=movie_list)


@app.route("/movies/<int:movie_id>/edit", methods=["GET", "POST"])
def edit_movie(movie_id):
    movie = check_found(api.get(f"/movies/{movie_id}"))
    movie_list = api.get(f"/lists/{movie['list_id']}").json()
    if request.method == "POST":
        data = movie_form_data(request.form)
        response = api.patch(f"/movies/{movie_id}", data)
        if response.status_code == 200:
            flash("Movie updated")
            return redirect(url_for("movie_detail", movie_id=movie_id))
        for msg in api.error_messages(response):
            flash(msg, "error")
        movie = {**movie, **data}
    return render_template("movie_form.html", movie_list=movie_list, movie=movie)


# quick button on the list page so you don't have to open the edit form
@app.route("/movies/<int:movie_id>/toggle-watched", methods=["POST"])
def toggle_watched(movie_id):
    movie = check_found(api.get(f"/movies/{movie_id}"))
    api.patch(f"/movies/{movie_id}", {"watched": not movie["watched"]})
    return redirect(url_for("list_detail", list_id=movie["list_id"]))


@app.route("/movies/<int:movie_id>/delete", methods=["POST"])
def delete_movie(movie_id):
    movie = check_found(api.get(f"/movies/{movie_id}"))
    api.delete(f"/movies/{movie_id}")
    flash(f'Removed "{movie["title"]}"')
    return redirect(url_for("list_detail", list_id=movie["list_id"]))


# ---------- Discover ----------


# shows one suggestion at a time. skip is how many you've passed on
@app.route("/lists/<int:list_id>/discover")
def discover(list_id):
    movie_list = check_found(api.get(f"/lists/{list_id}"))
    genre = request.args.get("genre", "")
    skip = request.args.get("skip", 0, type=int)
    suggestions = api.get(f"/lists/{list_id}/suggestions", genre=genre or None).json()
    genres = api.get("/genres").json()
    movie = suggestions[skip] if skip < len(suggestions) else None
    return render_template(
        "discover.html",
        movie_list=movie_list,
        movie=movie,
        genres=genres,
        genre=genre,
        skip=skip,
    )


# skip stays the same after adding because the added movie drops out of the suggestions
@app.route("/lists/<int:list_id>/discover/add", methods=["POST"])
def discover_add(list_id):
    data = clean_form(request.form, ["title", "year", "genre", "overview"])
    data["year"] = int(data["year"])
    api.post(f"/lists/{list_id}/movies", data)
    flash(f'Added "{data["title"]}"')
    return redirect(
        url_for(
            "discover",
            list_id=list_id,
            genre=request.form.get("filter"),
            skip=request.form.get("skip"),
        )
    )


@app.errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404
