# tests for the 5 CRRUD operations on lists.
# each one checks the status code AND that the data that comes back is right


# CREATE
def test_create_list(client):
    response = client.post("/lists", json={"name": "Date Night", "description": "cozy"})

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Date Night"
    assert data["description"] == "cozy"
    assert "id" in data


def test_create_list_with_empty_name_fails(client):
    response = client.post("/lists", json={"name": ""})
    assert response.status_code == 422  # rejected by validation


# READ ALL
def test_get_all_lists(client):
    client.post("/lists", json={"name": "List A"})
    client.post("/lists", json={"name": "List B"})

    response = client.get("/lists")

    assert response.status_code == 200
    names = [lst["name"] for lst in response.json()]
    assert names == ["List A", "List B"]


# READ ONE
def test_get_one_list(client, horror_list):
    response = client.get(f"/lists/{horror_list['id']}")

    assert response.status_code == 200
    assert response.json() == horror_list


def test_get_missing_list_returns_404(client):
    response = client.get("/lists/999")
    assert response.status_code == 404


# UPDATE
def test_update_list(client, horror_list):
    response = client.patch(
        f"/lists/{horror_list['id']}", json={"name": "Saturday Horror Night"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Saturday Horror Night"
    # didn't send this, so it shouldn't change
    assert data["description"] == "scary stuff"

    # make sure it actually saved, not just came back in the response
    assert (
        client.get(f"/lists/{horror_list['id']}").json()["name"]
        == "Saturday Horror Night"
    )


# DELETE
def test_delete_list(client, horror_list):
    response = client.delete(f"/lists/{horror_list['id']}")

    assert response.status_code == 204
    assert client.get(f"/lists/{horror_list['id']}").status_code == 404
    assert client.get("/lists").json() == []
