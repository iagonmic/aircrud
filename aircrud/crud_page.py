import reflex as rx
from aircrud.backend import get_available_table_names, get_table_by_name, get_table_info, create_record, update_record, delete_record, get_non_pk_fk_columns

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
    insert_data: dict = {}
    show_insert_popup: bool = False
    form_columns: list[str] = []
    is_editing: bool = False
    form_data: dict = {}
    show_form: bool = False
    item_to_delete: dict | None = None
    show_delete_dialog: bool = False

    @rx.event
    def change_table(self, table: str):
        """Change the select table var."""
        self.table = table
        self.filter_column = ""
        self.filter_value = ""
        self.order_column: str = ""
        self.order_direction: str = ""
        self.filter_operator: str = ""
        self.insert_data: dict = {}
        self.show_insert_popup: bool = False
        self.prepare_form()

    @rx.event
    def prepare_form(self):
        """Atualiza as colunas do formulário com base na tabela atual."""
        self.form_columns = get_non_pk_fk_columns(self.table)

    @rx.event
    def toggle_insert_popup(self):
        self.show_insert_popup = not self.show_insert_popup

    @rx.event
    def handle_insert(self, form_data: dict):
        """Recebe dados do form e insere no banco."""
        self.insert_data = form_data
        create_record(get_table_by_name(self.table), form_data)  
        self.load_data()  # recarrega tabela após inserir
        self.show_insert_popup = False

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

    # ações update
    @rx.event
    def open_update_form(self, item: dict):
        self.is_editing = True
        self.form_data = item.copy()
        self.show_form = True
        
    @rx.event
    def close_form(self):
        self.show_form = False
        self.is_editing = False
        self.form_data = {}
    
    @rx.event
    def save_item(self, data: dict):
        if self.is_editing:
            record_id = get_primary_key(self.form_data)
            if record_id:
                update_record(get_table_by_name(self.table), record_id, data)
        else:
            create_record(self.table, data)
        return [CrudState.load_data, CrudState.close_form]
    
    # ações delete
    @rx.event
    def open_delete_dialog(self, item: dict):
        self.item_to_delete = item.copy()
        self.show_delete_dialog = True

    @rx.event
    def close_delete_dialog(self):
        self.show_delete_dialog = False
        self.item_to_delete = None

    @rx.event
    def confirm_delete(self):
        if self.item_to_delete and get_primary_key(self.item_to_delete):
            delete_record(get_table_by_name(self.table), get_primary_key(self.item_to_delete))
        return [CrudState.load_data, CrudState.close_delete_dialog]

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

def insert_form():
    return rx.form(
        rx.vstack(
            rx.foreach(
                CrudState.form_columns,
                lambda col: rx.input(
                    placeholder=col,
                    name=col
                )
            ),
            rx.button("Inserir Dados", type="submit", color_scheme='pink')
        ),
        on_submit=CrudState.handle_insert,
        reset_on_submit=True,
    )

def get_primary_key(d):
    for key in d:
        if "ID" in key:  # verifica se contém "ID"
            return d[key]  # retorna o valor
    return None, None  # caso não tenha nenhuma chave com "ID"

def edit_form():
    return rx.form(
        rx.vstack(
            rx.foreach(
                CrudState.form_columns,
                lambda col: rx.input(
                    placeholder=col,
                    name=col,
                    default_value=CrudState.form_data.get(col, "")
                ),
            ),
            rx.button("💾 Salvar Alterações", type="submit", color_scheme="pink"),
        ),
        on_submit=CrudState.save_item(),
    )
    
def crud_table():
    return rx.table.root(
        # Cabeçalho dinâmico
        rx.table.header(
            rx.table.row(
                rx.foreach(
                    CrudState.columns,
                    lambda col: rx.table.column_header_cell(col)
                ),
                # coluna para as ações de editar e deletar
                rx.table.column_header_cell('Ações')
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
                    ),
                    #ações
                    rx.table.cell(
                        rx.hstack(
                            rx.button(
                                "✏️ Editar",
                                size="1",
                                color_scheme="blue",
                                on_click=lambda: CrudState.open_update_form(row),
                            ),
                            rx.button(
                                "🗑️ Deletar",
                                size="1",
                                color_scheme="red",
                                on_click=lambda: CrudState.open_delete_dialog(row),
                            ),
                            spacing='2'
                        )
                    ),
                )
            )
        ),
        width="100%",
    )

def crud_page():
    return rx.center(
        rx.vstack(
            rx.heading("AirCRUD 🏨", size='6', margin_bottom='20px'),
            rx.box(
                rx.hstack(                
                # seletor de tabela
                rx.hstack(
                    rx.text('Tabela:',weight='bold'),
                    rx.select(
                        [table_name for table_name in get_available_table_names()],
                        value=CrudState.table,
                        on_change=[
                            CrudState.change_table,
                            CrudState.load_data()
                        ],
                        width='200px'
                    ),
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
                        ],
                        width='100px'
                    ),
                    spacing='4'
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
                        ],
                        width='100px'
                    ),
                    spacing='4'
                )
            ),
            padding="10px",
            border="1px solid #202020",
            border_radius="8px",
            shadow="sm",
            width="100%",
            ),
            
            # filtro
            rx.box(
                rx.hstack(
                    rx.text("Filtro:", weight='bold'),
                    rx.select(
                        CrudState.columns,
                        placeholder="Coluna",
                        value=CrudState.filter_column,
                        on_change=CrudState.set_filter_column,
                        width='150px',
                    ),
                    rx.select(
                        ["=", "!=", ">", "<", ">=", "<=", "LIKE"],
                        value=CrudState.filter_operator,
                        on_change=CrudState.set_filter_operator,
                        width='100px'
                    ),
                    rx.input(
                        placeholder="Digite o valor",
                        type="text",
                        value=CrudState.filter_value,
                        on_change=CrudState.set_filter_value,
                        on_blur=CrudState.load_data,
                        width='200px'
                    ),
                    spacing='4'
                ),
                padding="10px",
                border="1px solid #202020",
                border_radius="8px",
                shadow="sm",
                width="100%",
            ),
            # order by
            rx.box(
                rx.hstack(
                rx.text("Ordenar por:", weight='bold'),
                rx.select(
                    CrudState.columns,
                    placeholder="Coluna",
                    value=CrudState.order_column,
                    on_change=CrudState.set_order_column,
                    width='150px'
                ),
                rx.select(
                    ["ASC", "DESC"],
                    placeholder="Direção",
                    value=CrudState.order_direction,
                    on_change=[
                        CrudState.set_order_direction,
                        CrudState.load_data()
                    ],
                    width='100px'
                ),
                spacing='4'
            ),
            padding="10px",
            border="1px solid #202020",
            border_radius="8px",
            shadow="sm",
            width="100%"
            ),
            # inserir dados
            rx.button(
                "✙ Inserir Registro",
                on_click=CrudState.toggle_insert_popup,
                margin_top='15px',
                color_scheme='pink'
            ),
            # tabela com dados
            rx.box(
                crud_table(),
                margin_top='20px',
                padding="15px",
                border="1px solid #202020",
                border_radius="10px",
                shadow="sm",
                width="100%",
            ),
            # popups
            #insert
            rx.dialog.root(
                rx.dialog.trigger(rx.text("")),
                rx.dialog.content(
                    rx.dialog.title("Inserir Novo Registro"),
                    insert_form(),
                    rx.dialog.close(rx.button("Fechar", color_scheme='red', margin_top='10px')),
                ),
                open=CrudState.show_insert_popup,
                on_open_change=CrudState.toggle_insert_popup,
            ),
            # update
            rx.dialog.root(
                rx.dialog.trigger(rx.text("")), 
                rx.dialog.content(
                    rx.dialog.title("Editar Registro"),
                    edit_form(),
                    rx.dialog.close(
                        rx.button("Cancelar", color_scheme="red", margin_top="10px")
                    ),
                ),
                open=CrudState.show_form,
                on_open_change=CrudState.close_form,
            ),
            # delete
            rx.dialog.root(
                rx.dialog.trigger(rx.text("")),
                rx.dialog.content(
                    rx.dialog.title("Confirmar Exclusão"),
                    rx.text("Tem certeza que deseja excluir este registro?"),
                    rx.hstack(
                        rx.dialog.close(
                            rx.button("Cancelar", color_scheme="gray"),
                        ),
                        rx.button(
                            "🗑️ Excluir",
                            color_scheme="red",
                            on_click=CrudState.confirm_delete,
                        ),
                        spacing="3",
                        margin_top="10px",
                    ),
                ),
                open=CrudState.show_delete_dialog,
                on_open_change=CrudState.close_delete_dialog,
            ),
            spacing="5",
            width="80%",
            max_width="900px",
        ),
        padding="30px",
        bg="#121212",
        min_height="100vh",
)
