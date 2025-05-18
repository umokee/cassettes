from PySide6.QtWidgets import QDialog, QFormLayout, QLineEdit, QPushButton, QVBoxLayout


class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SBC")
        self.resize(300, 150)
        self._build_ui()

    def _build_ui(self):
        self.login_input = QLineEdit()
        self.pass_input = QLineEdit()
        self.pass_input.setEchoMode(QLineEdit.EchoMode.Password)

        form = QFormLayout()
        form.addRow("Логин:", self.login_input)
        form.addRow("Пароль:", self.pass_input)

        self.ok_btn = QPushButton("Войти")
        self.ok_btn.clicked.connect(self.accept)

        layout = QVBoxLayout(self)
        layout.addLayout(form)
        layout.addWidget(self.ok_btn)

    def get_fields(self) -> tuple:
        return self.login_input.text(), self.pass_input.text()
