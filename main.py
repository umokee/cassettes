import sys

from PySide6.QtWidgets import QApplication

from app.dependency import Container


def main():
    app = QApplication(sys.argv)

    container = Container()
    auth_service = container.auth_service

    employee = auth_service.authorize(app)
    if not employee:
        return

    main_window = container.main_window(employee)
    main_window.show()

    exit_code = app.exec()
    container.close()
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
