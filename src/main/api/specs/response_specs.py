from http import HTTPStatus
from requests import Response


class ResponseSpecs:

    @staticmethod
    def has_status_in(expected_status: HTTPStatus):
        def confirm(response: Response):
            assert response.status_code == expected_status, (
                f"Expected status {expected_status}, "
                f"but got {response.status_code}. Response body: {response.text}")
        return confirm

    @staticmethod
    def has_status_any(*expected_statuses: HTTPStatus):
        def confirm(response: Response):
            assert response.status_code in expected_statuses, (
                f"Expected one of statuses "
                f"{[status.value for status in expected_statuses]}, "
                f"but got {response.status_code}. Response body: {response.text}")
        return confirm

    @staticmethod
    def request_ok():
        return ResponseSpecs.has_status_in(HTTPStatus.OK)

    @staticmethod
    def request_create():
        return ResponseSpecs.has_status_in(HTTPStatus.CREATED)

    @staticmethod
    def request_bad():
        return ResponseSpecs.has_status_in(HTTPStatus.BAD_REQUEST)

    @staticmethod
    def request_max_acc():
        return ResponseSpecs.has_status_in(HTTPStatus.CONFLICT)

    @staticmethod
    def request_not_found():
        return ResponseSpecs.has_status_in(HTTPStatus.NOT_FOUND)

    @staticmethod
    def request_422_error():
        return ResponseSpecs.has_status_in(HTTPStatus.UNPROCESSABLE_ENTITY)





    # @staticmethod
    # def request_ok():
    #     def confirm(response: Response):
    #         assert response.status_code == HTTPStatus.OK, response.text
    #     return confirm
    #
    # @staticmethod
    # def request_create():
    #     def confirm(response: Response):
    #         assert response.status_code == HTTPStatus.CREATED, response.text
    #     return confirm
    #
    # @staticmethod
    # def request_bad():
    #     def confirm(response: Response):
    #         assert response.status_code == HTTPStatus.BAD_REQUEST, response.text
    #     return confirm
    #
    # @staticmethod
    # def request_max_acc():
    #     def confirm(response: Response):
    #         assert response.status_code == HTTPStatus.CONFLICT, response.text
    #     return confirm
    #
    # @staticmethod
    # def request_not_found():
    #     def confirm(response: Response):
    #         assert response.status_code == HTTPStatus.NOT_FOUND, response.text
    #     return confirm
