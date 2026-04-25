import pytest
from sqlalchemy.orm import Session
from src.main.api.classes.api_manager import ApiManager
from src.main.api.fixtures.user_fixture import create_user_request
from src.main.api.generators.model_generator import RandomModelGenerator
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.db.crud.user_crud import UserCrudDb as User
from src.main.api.generators.creation_rule import UserRole



@pytest.mark.api
class TestUserCreate:
    @pytest.mark.parametrize("create_user_request", [
        RandomModelGenerator.generate(CreateUserRequest)
    ])
    def test_user_create_success(self, api_manager: ApiManager, create_user_request: CreateUserRequest, db_session: Session):
        response = api_manager.admin_steps.create_user(create_user_request)

        assert create_user_request.username == response.username
        assert create_user_request.role == response.role

        user_from_db = User.get_user_by_username(db_session, create_user_request.username)
        assert user_from_db.username == create_user_request.username, "Созданного пользователя нет в БД"


    @pytest.mark.parametrize(
        'username,password',
        [
            ("абв","Pas!sw0rd"),
            ("ab","Pas!sw0rd"),
            ("abv!","Pas!sw0rd"),
            ("Dim221","Pas!sw0rд"),
            ("Dim222","Pas!swwrd"),
            ("Dim223","pas!sw0rd"),
            ("Dim224","Pas!sw0"),
            ("Dim225","PASSWORD"),
            ("Dddimnfhsjdjdrty","Pas!sw0rd")
        ]
    )
    def test_create_user_invalid_credentials(self, api_manager: ApiManager, db_session: Session, username: str, password: str):
        create_user_request = CreateUserRequest(username=username, password=password, role=UserRole.USER)
        api_manager.admin_steps.create_invalid_user(create_user_request)

        user_from_db = User.get_user_by_username(db_session, create_user_request.username)

        assert user_from_db is None, 'Пользователь создан, ошибка'