import reflex as rx
from aircrud.backend import query_builder, create_record, update_record, delete_record, host

class CrudState(rx.State):
    data: list[dict] = []
    page: int = 1
    page_size: int = 10

    async def load_data(self):
        rows = query_builder(host, page=self.page, page_size=self.page_size)
        self.data = [dict(r._mapping) for r in rows]  # converte Row para dict

    async def add_record(self, data: dict):
        create_record(host, data)
        await self.load_data()

    async def edit_record(self, record_id: int, data: dict):
        update_record(host, record_id, data, pk="HostID")
        await self.load_data()

    async def remove_record(self, record_id: int):
        delete_record(host, record_id, pk="HostID")
        await self.load_data()

def crud_page():
    return rx.vstack(
        rx.heading("CRUD Dinâmico"),
        rx.button("Carregar dados", on_click=CrudState.load_data),
        rx.data_list.root(
            rx.foreach(
                rx.data_list.item(
                    rx.data_list.label(rx.text(f))
                )
            )
        )
    )

