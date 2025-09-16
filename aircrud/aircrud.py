import reflex as rx
from rxconfig import config

class State(rx.State):
    pass

class MapContainer(rx.NoSSRComponent):

    library = "react-leaflet"

    tag = "MapContainer"

    center: rx.Var[list]

    zoom: rx.Var[int]

    scroll_wheel_zoom: rx.Var[bool]

    # Can also pass a url like: https://unpkg.com/leaflet/dist/leaflet.css
    def add_imports(self):
        return {"": ["leaflet/dist/leaflet.css"]}


class TileLayer(rx.NoSSRComponent):

    library = "react-leaflet"

    tag = "TileLayer"

    url: rx.Var[str]


map_container = MapContainer.create
tile_layer = TileLayer.create

def index() -> rx.Component:
    return rx.el.div(map_container(
        tile_layer(
            url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
        ),
        center=[51.505, -0.09],
        zoom=5,
        # scroll_wheel_zoom=True
        width="100%",
        height="100vh",
        ),
    rx.el.div(
        rx.text("Bem-vindo ao AirCRUD!", font_size="2em", color="white"),
        rx.button("Clique aqui para iniciar", on_click=rx.redirect("/quiz"), 
                  bg="#FF5A60",
                  color='white',
                  border_color="#FF5A60",
                  _hover={"bg": "#CC484C"}, 
                  padding="1em 2em",
                  margin_top="1em", 
                  size="4", 
                  variant="surface"),
        position="absolute",
        top="50%",
        left="50%",
        transform="translate(-50%, -50%)",
        bg="rgba(0, 0, 0, 0.6)",
        padding="2em",
        border_radius="1em",
        box_shadow="lg",
        z_index=1000,
        text_align="center",
        ),
        style={"height": "100vh", "width": "100vw", "position": "relative"},
    )
    
app = rx.App()
app.add_page(index)