from PySide6.QtWidgets import QApplication, QMessageBox

from data.entities import Employee
from data.repo import EmployeeRepository
from gui.views.auth import LoginDialog


class AuthService:
    def __init__(self, repo: EmployeeRepository):
        self._repo = repo

    def authorize(self, app: QApplication) -> Employee | None:
        while True:
            dialog = LoginDialog()
            if dialog.exec() != dialog.DialogCode.Accepted:
                return None

            login, password = dialog.get_fields()

            if not login.strip() or not password:
                QMessageBox.warning(None, "Ошибка", "Логин и пароль обязательны")
                continue
            if len(login) > 50:
                QMessageBox.warning(None, "Ошибка", "Слишком длинный логин")
                continue
            if len(password) > 50:
                QMessageBox.warning(None, "Ошибка", "Слишком длинный пароль")
                continue

            employee = self._repo.auth(login, password)

            if employee:
                return employee
            else:
                QMessageBox.critical(None, "Ошибка", "Неверный логин или пароль")
