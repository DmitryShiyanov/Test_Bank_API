import pytest
from sqlalchemy.orm import Session
from src.main.api.classes.api_manager import ApiManager
from src.main.api.generators.creation_rule import UserRole
from src.main.api.db.crud.user_crud import UserCrudDb as User


@pytest.mark.api
class TestAdminRole:
    def test_get_all_users(self, db_session: Session, api_manager: ApiManager):
        response = api_manager.admin_steps.get_all_users()
        all_users = next((user for user in response
                          if user.username == "admin" and
                          user.role == UserRole.ADMIN), None)
        assert all_users is not None

        admin_from_db = User.get_user_by_username(db_session, response[0].username)
        assert admin_from_db is not None
        assert admin_from_db.username == response[0].username
