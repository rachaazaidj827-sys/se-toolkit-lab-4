import httpx


def test_get_interactions_returns_200(client: httpx.Client) -> None:
    response = client.get("/interactions/")
    assert response.status_code == 200


def test_get_interactions_response_is_a_list(client: httpx.Client) -> None:
    response = client.get("/interactions/")
    assert isinstance(response.json(), list)


def test_get_interactions_can_filter_by_item_id(client: httpx.Client) -> None:
    """GET /interactions with item_id returns only matching interactions."""
    response = client.get("/interactions/", params={"item_id": 1})
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert data  # there should be at least one seeded interaction for item 1
    assert {interaction["item_id"] for interaction in data} == {1}


def test_get_interactions_with_unknown_item_id_returns_empty_list(
    client: httpx.Client,
) -> None:
    """GET /interactions with non-existent item_id returns empty list."""
    response = client.get("/interactions/", params={"item_id": 9999})
    assert response.status_code == 200
    assert response.json() == []


def test_post_interaction_creates_new_log(client: httpx.Client) -> None:
    """POST /interactions creates a new interaction log."""
    body = {"learner_id": 1, "item_id": 1, "kind": "attempt"}
    response = client.post("/interactions/", json=body)
    assert response.status_code == 201

    data = response.json()
    assert isinstance(data, dict)
    for key in ("id", "learner_id", "item_id", "kind", "created_at"):
        assert key in data

    assert data["learner_id"] == body["learner_id"]
    assert data["item_id"] == body["item_id"]
    assert data["kind"] == body["kind"]


def test_post_interaction_with_unknown_learner_returns_422(
    client: httpx.Client,
) -> None:
    """POST /interactions with non-existent learner_id returns 422."""
    body = {"learner_id": 9999, "item_id": 1, "kind": "view"}
    response = client.post("/interactions/", json=body)
    assert response.status_code == 422

    payload = response.json()
    assert payload["detail"] == (
        "learner_id or item_id does not reference an existing record"
    )


def test_post_interaction_with_unknown_item_returns_422(
    client: httpx.Client,
) -> None:
    """POST /interactions with non-existent item_id returns 422."""
    body = {"learner_id": 1, "item_id": 9999, "kind": "view"}
    response = client.post("/interactions/", json=body)
    assert response.status_code == 422

    payload = response.json()
    assert payload["detail"] == (
        "learner_id or item_id does not reference an existing record"
    )
def test_get_interactions_response_structure(client: httpx.Client) -> None:
    """Test GET /interactions response has correct fields in each item."""
    response = client.get("/interactions/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if data:  # if there are items
        for item in data:
            # Check required fields exist
            assert "id" in item
            assert "learner_id" in item
            assert "item_id" in item
            assert "kind" in item
            assert "created_at" in item
            # Check field types
            assert isinstance(item["id"], int)
            assert isinstance(item["learner_id"], int)
            assert isinstance(item["item_id"], int)
            assert isinstance(item["kind"], str)
            assert isinstance(item["created_at"], str)
            