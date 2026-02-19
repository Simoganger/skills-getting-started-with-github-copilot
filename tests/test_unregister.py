from src import app as app_module


def test_unregister_success_removes_participant(client):
    activity_name = "Chess Club"
    email = app_module.activities[activity_name]["participants"][0]

    response = client.delete(f"/activities/{activity_name}/unregister", params={"email": email})

    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {email} from {activity_name}"
    assert email not in app_module.activities[activity_name]["participants"]


def test_unregister_unknown_activity_returns_404(client):
    response = client.delete(
        "/activities/Unknown Club/unregister", params={"email": "student@mergington.edu"}
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_unknown_participant_returns_404(client):
    response = client.delete(
        "/activities/Chess Club/unregister", params={"email": "notfound@mergington.edu"}
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found in this activity"


def test_unregister_missing_email_returns_422(client):
    response = client.delete("/activities/Chess Club/unregister")

    assert response.status_code == 422
