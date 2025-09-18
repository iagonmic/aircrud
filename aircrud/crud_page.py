import reflex as rx
from aircrud.backend import get_table_by_name, get_table_info, create_record, update_record, delete_record

class CrudState(rx.State):
    data: list[dict] = []
    page: int = 1
    page_size: int = 10

    async def load_data(self, table_name):
        rows = get_table_info(table_name, page=self.page, page_size=self.page_size)
        self.data = [dict(r._mapping) for r in rows]  # converte Row para dict

    async def add_record(self, table_name, data: dict):
        table = get_table_by_name(table_name)
        create_record(table, data)
        await self.load_data()

    async def edit_record(self, table_name, record_id: int, data: dict):
        table = get_table_by_name(table_name)
        update_record(table, record_id, data, pk="HostID")
        await self.load_data()

    async def remove_record(self, table_name, record_id: int):
        table = get_table_by_name(table_name)
        delete_record(table, record_id, pk="HostID")
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

