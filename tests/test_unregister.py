def test_unregister_removes_existing_participant(client):
    existing_email = "michael@mergington.edu"

    response = client.delete(
        "/activities/Chess%20Club/participants",
        params={"email": existing_email},
    )

    assert response.status_code == 200
    assert response.json()["message"] == f"Removed {existing_email} from Chess Club"

    activities_response = client.get("/activities")
    participants = activities_response.json()["Chess Club"]["participants"]
    assert existing_email not in participants


def test_unregister_returns_404_for_unknown_activity(client):
    response = client.delete(
        "/activities/Unknown%20Club/participants",
        params={"email": "student@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_returns_404_for_non_registered_participant(client):
    response = client.delete(
        "/activities/Chess%20Club/participants",
        params={"email": "not-registered@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Student is not signed up for this activity"


def test_signup_then_unregister_roundtrip(client):
    email = "roundtrip@mergington.edu"

    signup_response = client.post("/activities/Gym%20Class/signup", params={"email": email})
    assert signup_response.status_code == 200

    unregister_response = client.delete(
        "/activities/Gym%20Class/participants",
        params={"email": email},
    )
    assert unregister_response.status_code == 200

    activities_response = client.get("/activities")
    participants = activities_response.json()["Gym Class"]["participants"]
    assert email not in participants
