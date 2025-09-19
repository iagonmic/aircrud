import reflex as rx
from aircrud.backend import get_available_table_names, get_table_by_name, get_table_info, create_record, update_record, delete_record

class CrudState(rx.State):
    data: list[dict] = []
    page: int = 1
    page_size: int = 10
    table: str = "host"
    filter_column = ""
    filter_value = ""
    filter_operator: str = ""
    order_column: str = ""
    order_direction: str = ""

    @rx.event
    def change_table(self, table: str):
        """Change the select table var."""
        self.table = table
        self.filter_column = ""
        self.filter_value = ""
        self.order_column: str = ""
        self.order_direction: str = ""
        self.filter_operator: str = ""


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

    @rx.event
    def set_filter_column(self, col: str):
        self.filter_column = col

    @rx.event
    def set_filter_value(self, value: str):
        self.filter_value = value

    @rx.event
    def set_filter_operator(self, op: str):
        self.filter_operator = op

    @rx.event
    def set_order_column(self, column: str):
        self.order_column = column

    @rx.event
    def set_order_direction(self, direction: str):
        self.order_direction = direction

    @rx.var
    def columns(self) -> list[str]:
        """Extrai os nomes das colunas do primeiro registro."""
        if self.data:
            return list(self.data[0].keys())
        return []
        

    async def load_data(self):
        filters = {}
        if self.filter_column and self.filter_value:
            filters[self.filter_column] = {
                "op": self.filter_operator,
                "value": self.filter_value,
            }
        
        order_by = None
        if self.order_column:
            order_by = f"{self.order_column} {self.order_direction}"

        rows = get_table_info(
            self.table,
            page=self.page,
            page_size=self.page_size,
            filters=filters,
            order_by=order_by,
        )
        self.data = [dict(r) for r in rows]


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
        rx.hstack(
            rx.text("Número da página:"),
            rx.input(
            title="Número da Página",
            placeholder="Page Number",
            type="number",
            value=CrudState.page,
            on_change=[
                CrudState.set_page_number,
                CrudState.load_data()
            ]
        )
        ),
        # itens por página
        rx.hstack(
            rx.text("Registros por página:"),
            rx.input(
            title="Itens por Página",
            placeholder="Page Size",
            type="number",
            value=CrudState.page_size,
            on_change=[
                CrudState.set_page_size,
                CrudState.load_data()
            ]
        ),
        ),
        # filtro
        rx.hstack(
            rx.text("Filtro:"),
            rx.select(
                CrudState.columns,
                placeholder="Coluna",
                value=CrudState.filter_column,
                on_change=CrudState.set_filter_column,
            ),
            rx.select(
                ["=", "!=", ">", "<", ">=", "<=", "LIKE"],
                value=CrudState.filter_operator,
                on_change=CrudState.set_filter_operator,
            ),
            rx.input(
                placeholder="Digite o valor",
                type="text",
                value=CrudState.filter_value,
                on_change=CrudState.set_filter_value,
                on_blur=CrudState.load_data
            ),
        ),

        # order by
        rx.hstack(
            rx.text("Ordenar por:"),
            rx.select(
                CrudState.columns,
                placeholder="Coluna",
                value=CrudState.order_column,
                on_change=CrudState.set_order_column
            ),
            rx.select(
                ["ASC", "DESC"],
                placeholder="Direção",
                value=CrudState.order_direction,
                on_change=[
                    CrudState.set_order_direction,
                    CrudState.load_data()
                ]
            ),
        ),
        # tabela com dados
        crud_table()
    )

