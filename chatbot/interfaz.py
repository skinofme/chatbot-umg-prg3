import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QLabel, QScrollArea, QFrame, QMenu
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap

from main import procesar_input


class ChatUI(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("CHATBOT")
        self.setGeometry(100, 100, 400, 550)

        self.modo = None
        self.last_input = ""

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)

        # 🖼️ FONDO
        self.fondo = QLabel(self)
        self.fondo.setGeometry(0, 0, 400, 550)

        pixmap_fondo = QPixmap("assets/fondo.jpg")
        self.fondo.setPixmap(pixmap_fondo)
        self.fondo.setScaledContents(True)
        self.fondo.lower()

        header = QFrame()
        header.setStyleSheet("background-color: #2d3e50; padding: 10px;")
        header_layout = QHBoxLayout()

        logo_label = QLabel()
        logo_pixmap = QPixmap("assets/logo.jpg")
        logo_pixmap = logo_pixmap.scaled(50, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        logo_label.setPixmap(logo_pixmap)
        logo_label.setFixedSize(80, 80)
        logo_label.setStyleSheet("border-radius: 25px;")
        logo_label.setScaledContents(True)

        title = QLabel("CHATBOT")
        title.setStyleSheet("color: white; font-size: 20px; font-weight: bold; margin-left: 10px;")

        config_btn = QPushButton("⋮")
        config_btn.setStyleSheet("""
            color: white;
            font-size: 45px;
            background: transparent;
        """)
        config_btn.setFixedWidth(30)
        config_btn.clicked.connect(self.mostrar_menu)

        header_layout.addWidget(logo_label)
        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(config_btn)

        header.setLayout(header_layout)
        main_layout.addWidget(header)

        # 🧾 CHAT
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setStyleSheet("border: none; background: transparent;")

        self.chat_container = QWidget()
        self.chat_layout = QVBoxLayout()
        self.chat_layout.setAlignment(Qt.AlignTop)

        self.chat_container.setLayout(self.chat_layout)
        self.scroll.setWidget(self.chat_container)

        main_layout.addWidget(self.scroll)

        # ✏️ INPUT
        bottom_layout = QHBoxLayout()

        self.input = QLineEdit()
        self.input.setPlaceholderText("Enter Message")
        self.input.setStyleSheet("""
            padding: 20px;
            border-radius: 20px;
            background-color: rgba(255,255,255,0.8);
        """)
        self.input.returnPressed.connect(self.send_message)

        send_button = QPushButton("➤")
        send_button.setStyleSheet("""
            background-color: #4a90e2;
            color: white;
            border-radius: 20px;
            padding: 20px;
        """)
        send_button.clicked.connect(self.send_message)

        bottom_layout.addWidget(self.input)
        bottom_layout.addWidget(send_button)

        main_layout.addLayout(bottom_layout)
        self.setLayout(main_layout)

        self.add_bot_message("Hola gracias por preferirnos, como puedo ayudarte? escribe alguna de estas palabras clave para que pueda ayudarte con tu consulta: producto, pedido, comprar o salir")

    def mostrar_menu(self):
        menu = QMenu()
        menu.addAction("Cuenta")
        menu.addAction("Configuración")
        salir = menu.addAction("Salir")

        action = menu.exec_(self.mapToGlobal(self.rect().topRight()))

        if action == salir:
            self.close()

    def add_bot_message(self, message):
        layout = QHBoxLayout()

        avatar = QLabel()
        pixmap = QPixmap("assets/robot.jpg")
        pixmap = pixmap.scaled(40, 40, Qt.KeepAspectRatioByExpanding)

        avatar.setPixmap(pixmap)
        avatar.setFixedSize(40, 40)
        avatar.setStyleSheet("border-radius: 20px;")

        bubble = QLabel(message)
        bubble.setWordWrap(True)
        bubble.setStyleSheet("""
            background-color: rgba(229,229,229,0.9);
            padding: 10px;
            border-radius: 10px;
        """)
        bubble.setMaximumWidth(220)

        layout.addWidget(avatar)
        layout.addWidget(bubble)
        layout.addStretch()

        frame = QFrame()
        frame.setLayout(layout)

        self.chat_layout.addWidget(frame)

        return bubble

    def add_user_message(self, message):
        layout = QHBoxLayout()

        bubble = QLabel(message)
        bubble.setWordWrap(True)
        bubble.setStyleSheet("""
            background-color: #4a90e2;
            color: white;
            padding: 10px;
            border-radius: 10px;
        """)
        bubble.setMaximumWidth(220)

        layout.addStretch()
        layout.addWidget(bubble)

        frame = QFrame()
        frame.setLayout(layout)

        self.chat_layout.addWidget(frame)

    def send_message(self):
        text = self.input.text()
        if not text:
            return

        self.add_user_message(text)

        if self.modo == "producto":
            text = f"producto:{text}"
        elif self.modo == "pedido":
            text = f"pedido:{text}"

        self.last_input = text

        self.typing_label = self.add_bot_message("Escribiendo.")

        self.dots = 1
        self.timer = QTimer()
        self.timer.timeout.connect(self.animar_escribiendo)
        self.timer.start(500)

        QTimer.singleShot(1000, self.respuesta_bot)

        self.input.clear()

    def animar_escribiendo(self):
        self.dots += 1
        if self.dots > 3:
            self.dots = 1

        texto = "Escribiendo" + "." * self.dots
        self.typing_label.setText(texto)

    def respuesta_bot(self):
        self.timer.stop()

        respuesta = procesar_input(self.last_input)

        if respuesta == "__PEDIR_NOMBRE_PRODUCTO__":
            self.typing_label.setText("Ingresa el nombre del producto que buscas: ")
            self.modo = "producto"

        elif respuesta == "__PEDIR_ID_PEDIDO__":
            self.typing_label.setText("Escribe el ID del pedido que quieres consultar: ")
            self.modo = "pedido"

        else:
            self.typing_label.setText(respuesta)
            self.modo = None


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ChatUI()
    window.show()
    sys.exit(app.exec_())