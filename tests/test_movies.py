# tests for movies inside a list, plus the suggestions for the Discover page

GET_OUT = {"title": "Get Out", "year": 2017, "genre": "Horror"}


def add_movie(client, list_id, movie=GET_OUT):
    return client.post(f"/lists/{list_id}/movies", json=movie)


# CREATE
def test_add_movie_to_list(client, horror_list):
    response = add_movie(client, horror_list["id"])

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Get Out"
    assert data["year"] == 2017
    assert data["list_id"] == horror_list["id"]
    assert data["watched"] is False  # default


def test_add_movie_to_missing_list_returns_404(client):
    assert add_movie(client, 999).status_code == 404


# READ ALL
def test_get_movies_in_list(client, horror_list):
    add_movie(client, horror_list["id"])
    add_movie(client, horror_list["id"], {"title": "Hereditary", "year": 2018})

    response = client.get(f"/lists/{horror_list['id']}/movies")

    assert response.status_code == 200
    titles = [m["title"] for m in response.json()]
    assert titles == ["Get Out", "Hereditary"]


# READ ONE
def test_get_one_movie(client, horror_list):
    movie = add_movie(client, horror_list["id"]).json()

    response = client.get(f"/movies/{movie['id']}")

    assert response.status_code == 200
    assert response.json() == movie


# UPDATE
def test_mark_movie_watched_and_rate_it(client, horror_list):
    movie = add_movie(client, horror_list["id"]).json()

    response = client.patch(f"/movies/{movie['id']}", json={"watched": True, "rating": 9})

    assert response.status_code == 200
    data = response.json()
    assert data["watched"] is True
    assert data["rating"] == 9
    assert data["title"] == "Get Out"  # unchanged


def test_rating_over_10_fails(client, horror_list):
    movie = add_movie(client, horror_list["id"]).json()
    response = client.patch(f"/movies/{movie['id']}", json={"rating": 11})
    assert response.status_code == 422


def test_cant_blank_out_title(client, horror_list):
    movie = add_movie(client, horror_list["id"]).json()
    response = client.patch(f"/movies/{movie['id']}", json={"title": None})
    assert response.status_code == 422
    assert client.get(f"/movies/{movie['id']}").json()["title"] == "Get Out"


# DELETE
def test_delete_movie(client, horror_list):
    movie = add_movie(client, horror_list["id"]).json()

    response = client.delete(f"/movies/{movie['id']}")

    assert response.status_code == 204
    assert client.get(f"/movies/{movie['id']}").status_code == 404
    assert client.get(f"/lists/{horror_list['id']}/movies").json() == []


def test_deleting_list_deletes_its_movies(client, horror_list):
    movie = add_movie(client, horror_list["id"]).json()

    client.delete(f"/lists/{horror_list['id']}")

    assert client.get(f"/movies/{movie['id']}").status_code == 404


# SUGGESTIONS
def test_suggestions_skip_movies_already_in_list(client, horror_list):
    url = f"/lists/{horror_list['id']}/suggestions?genre=Horror"
    before = [s["title"] for s in client.get(url).json()]
    assert "Get Out" in before

    add_movie(client, horror_list["id"])

    after = [s["title"] for s in client.get(url).json()]
    assert "Get Out" not in after
    assert len(after) == len(before) - 1


def test_suggestions_genre_filter(client, horror_list):
    response = client.get(f"/lists/{horror_list['id']}/suggestions?genre=comedy")

    assert response.status_code == 200
    genres = {s["genre"] for s in response.json()}
    assert genres == {"Comedy"}
