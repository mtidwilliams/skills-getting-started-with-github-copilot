import src.app as app_module


def test_signup_success_adds_participant(signup_request):
    # Arrange
    activity_name = "Chess Club"
    email = "new.student@mergington.edu"
    participants_before = len(app_module.activities[activity_name]["participants"])

    # Act
    response = signup_request(activity_name, email)

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for {activity_name}"}
    assert email in app_module.activities[activity_name]["participants"]
    assert len(app_module.activities[activity_name]["participants"]) == participants_before + 1


def test_signup_rejects_duplicate_participant(signup_request):
    # Arrange
    activity_name = "Chess Club"
    existing_email = app_module.activities[activity_name]["participants"][0]
    participants_before = len(app_module.activities[activity_name]["participants"])

    # Act
    response = signup_request(activity_name, existing_email)

    # Assert
    assert response.status_code == 400
    assert response.json() == {"detail": "Student already signed up for this activity"}
    assert len(app_module.activities[activity_name]["participants"]) == participants_before


def test_signup_unknown_activity_returns_not_found(signup_request):
    # Arrange
    activity_name = "Unknown Activity"
    email = "student@mergington.edu"

    # Act
    response = signup_request(activity_name, email)

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_signup_accepts_url_encoded_email(signup_request):
    # Arrange
    activity_name = "Science Club"
    email = "first.last+robot@mergington.edu"

    # Act
    response = signup_request(activity_name, email)

    # Assert
    assert response.status_code == 200
    assert email in app_module.activities[activity_name]["participants"]
