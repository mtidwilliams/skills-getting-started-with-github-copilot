import src.app as app_module


def test_remove_success_deletes_participant(remove_request):
    # Arrange
    activity_name = "Basketball Team"
    email = "james@mergington.edu"
    participants_before = len(app_module.activities[activity_name]["participants"])

    # Act
    response = remove_request(activity_name, email)

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Removed {email} from {activity_name}"}
    assert email not in app_module.activities[activity_name]["participants"]
    assert len(app_module.activities[activity_name]["participants"]) == participants_before - 1


def test_remove_rejects_non_registered_participant(remove_request):
    # Arrange
    activity_name = "Art Studio"
    email = "not.registered@mergington.edu"
    participants_before = len(app_module.activities[activity_name]["participants"])

    # Act
    response = remove_request(activity_name, email)

    # Assert
    assert response.status_code == 400
    assert response.json() == {"detail": "Student is not registered for this activity"}
    assert len(app_module.activities[activity_name]["participants"]) == participants_before


def test_remove_unknown_activity_returns_not_found(remove_request):
    # Arrange
    activity_name = "Unknown Activity"
    email = "student@mergington.edu"

    # Act
    response = remove_request(activity_name, email)

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_signup_then_remove_same_participant(signup_request, remove_request):
    # Arrange
    activity_name = "Music Band"
    email = "temporary.user@mergington.edu"

    # Act
    signup_response = signup_request(activity_name, email)
    remove_response = remove_request(activity_name, email)

    # Assert
    assert signup_response.status_code == 200
    assert remove_response.status_code == 200
    assert email not in app_module.activities[activity_name]["participants"]
