import pytest

from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.login_user_request import LoginUserRequest
from sqlalchemy.orm import Session
from src.main.api.db.crud.user_crud import UserCrudDb as User
from src.main.api.generators.creation_rule import UserRole


@pytest.mark.api
class TestUserLogin:
    def test_admin_login(self, db_session: Session, api_manager: ApiManager):
        login_user_request = LoginUserRequest(username="admin", password="123456")
        response = api_manager.admin_steps.login_user(login_user_request)

        assert login_user_request.username == response.user.username
        assert response.user.role == UserRole.ADMIN

        user_from_db = User.get_user_by_username(db_session, login_user_request.username)
        assert user_from_db.username == response.user.username

    def test_user_login(self, db_session: Session, api_manager: ApiManager, create_user_request: CreateUserRequest):
        response = api_manager.admin_steps.login_user(create_user_request)
        assert create_user_request.username == response.user.username
        assert response.user.role == UserRole.USER

        user_from_db = User.get_user_by_username(db_session, response.user.username)
        assert user_from_db.username == response.user.username
