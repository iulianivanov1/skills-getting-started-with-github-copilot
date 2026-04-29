def test_get_activities_returns_dictionary(client):
    response = client.get("/activities")

    assert response.status_code == 200
    payload = response.json()
    assert isinstance(payload, dict)


def test_get_activities_includes_required_fields(client):
    response = client.get("/activities")
    activities = response.json()

    assert "Chess Club" in activities

    required_fields = {"description", "schedule", "max_participants", "participants"}

    for details in activities.values():
        assert required_fields.issubset(details.keys())
        assert isinstance(details["participants"], list)
