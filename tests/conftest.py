import pytest
from todo_app import create_app, db
from todo_app.models import Todo   # SQLAlchemy model

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # in-memory DB for testing

    with app.app_context():
        db.create_all()   # create tables before each test
        yield app.test_client()
        db.session.remove()
        db.drop_all()     # clean up tables after test
