import reflex as rx
from rxconfig import config

class State(rx.State):
    pass

def index():
    return rx.center(
        rx.vstack(
            rx.heading("Bem-vindo ao AirCRUD!"),
            rx.button(
            "Clique aqui para iniciar",
            color_scheme="pink",
            margin_top="1em",
            size="4",
            variant="surface",
            ),
        align="center",
        size="5"
        ),
    align="center",
    justify="center",
    height="100vh",
    )

app = rx.App()
app.add_page(index)