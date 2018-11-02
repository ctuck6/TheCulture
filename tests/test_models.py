def test_review_model(session):
    tempUser = User("John", "Doe", "johnnyfootball", "john.doe@gmail.com", "Password1", "default_1.jpg")
    session.add(tempUser)
    session.commit()
    review = Review("Test Review", "This is a test!", tempUser)
    session.add(review)
    session.commit()

    assert review.id > 0
