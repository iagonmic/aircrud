import reflex as rx
from rxconfig import config
from aircrud.crud_page import crud_page, CrudState

class MapContainer(rx.NoSSRComponent):
    library = "react-leaflet"
    tag = "MapContainer"
    center: rx.Var[list]
    zoom: rx.Var[int]
    scroll_wheel_zoom: rx.Var[bool]

    def add_imports(self):
        return {"": ["leaflet/dist/leaflet.css"]}


class TileLayer(rx.NoSSRComponent):
    library = "react-leaflet"
    tag = "TileLayer"
    url: rx.Var[str]


map_container = MapContainer.create
tile_layer = TileLayer.create


def index() -> rx.Component:
    return rx.el.div(
        map_container(
            tile_layer(
                url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
            ),
            center=[51.505, -0.09],
            zoom=5,
            scroll_wheel_zoom=False,
            width="100%",
            height="100%",
            style={"position": "absolute", "top": 0, "left": 0, "zIndex": 0},
        ),
        rx.el.div(
            rx.el.h2(
                "Bem-vindo ao AirCRUD!", class_name="text-4xl text-white font-bold"
            ),
            rx.el.button(
                "Clique aqui para iniciar",
                on_click=rx.redirect("/crud"),
                class_name="mt-4 py-4 px-8 bg-[#F76B15] text-white rounded-lg hover:bg-[#D35D14] focus:outline-none focus:shadow-none",
            ),
            class_name="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 bg-black/80 p-8 rounded-2xl shadow-lg text-center z-[1001]",
        ),
        rx.el.div(
            class_name="absolute top-0 left-0 right-0 h-[120px] pointer-events-none bg-gradient-to-b from-black/40 to-transparent z-[1000]"
        ),
        rx.el.div(
            class_name="absolute bottom-0 left-0 right-0 h-[120px] pointer-events-none bg-gradient-to-t from-black/40 to-transparent z-[1000]"
        ),
        rx.el.div(
            class_name="absolute top-0 bottom-0 left-0 w-[120px] pointer-events-none bg-gradient-to-r from-black/40 to-transparent z-[1000]"
        ),
        rx.el.div(
            class_name="absolute top-0 bottom-0 right-0 w-[120px] pointer-events-none bg-gradient-to-l from-black/40 to-transparent z-[1000]"
        ),
        class_name="h-screen w-screen relative font-['Inter']",
    )


app = rx.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", crossorigin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700;800&display=swap",
            rel="stylesheet",
        ),
    ],
)
app.add_page(index, route="/")
app.add_page(crud_page, route="/crud", on_load=CrudState.load_data())