import reflex as rx
from aircrud.backend import get_available_table_names, get_table_by_name, get_table_info, create_record, update_record, delete_record

class CrudState(rx.State):
    data: list[dict] = []
    page: int = 1
    page_size: int = 10
    table: str = "host"

    @rx.event
    def change_table(self, table: str):
        """Change the select table var."""
        self.table = table

    @rx.event
    def set_page_number(self, page: str):
        """Change the select page_size var."""
        if page.isdigit():
            self.page = int(page)

    @rx.event
    def set_page_size(self, page_size: str):
        """Change the select page_size var."""
        if page_size.isdigit():
            self.page_size = int(page_size)

    @rx.var
    def columns(self) -> list[str]:
        """Extrai os nomes das colunas do primeiro registro."""
        if self.data:
            return list(self.data[0].keys())
        return []
        

    async def load_data(self):
        rows = get_table_info(self.table, page=self.page, page_size=self.page_size)
        self.data = [dict(r) for r in rows]  # converte Row para dict

    async def add_record(self, data: dict):
        table = get_table_by_name(self.table)
        create_record(table, data)
        await self.load_data()

    async def edit_record(self, record_id: int, data: dict):
        table = get_table_by_name(self.table)
        update_record(table, record_id, data)
        await self.load_data()

    async def remove_record(self, record_id: int):
        table = get_table_by_name(self.table)
        delete_record(table, record_id)
        await self.load_data()
    
def crud_table():
    return rx.table.root(
        # Cabeçalho dinâmico
        rx.table.header(
            rx.table.row(
                rx.foreach(
                    CrudState.columns,
                    lambda col: rx.table.column_header_cell(col)
                )
            )
        ),
        # Corpo da tabela
        rx.table.body(
            rx.foreach(
                CrudState.data,
                lambda row: rx.table.row(
                    rx.foreach(
                        CrudState.columns,
                        lambda col: rx.table.cell(row[col])
                    )
                )
            )
        ),
        width="100%",
    )

def crud_page():
    return rx.vstack(
        rx.heading("CRUD Dinâmico"),

        # seletor de tabela
        rx.select(
            [table_name for table_name in get_available_table_names()],
            value=CrudState.table,
            on_change=[
                CrudState.change_table,
                CrudState.load_data()
            ]
        ),
        # tamanho da página
        rx.input(
            placeholder="Page Number",
            type="number",
            value=CrudState.page,
            on_change=[
                CrudState.set_page_number,
                CrudState.load_data()
            ]
        ),
        rx.input(
            placeholder="Page Size",
            type="number",
            value=CrudState.page_size,
            on_change=[
                CrudState.set_page_size,
                CrudState.load_data()
            ]
        ),
        crud_table()
    )

