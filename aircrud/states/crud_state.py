import reflex as rx
from typing import TypedDict, Optional


class Record(TypedDict):
    id: int
    name: str
    text_field: str
    selection1: str
    selection2: str


class CRUDState(rx.State):
    records: list[Record] = [
        {
            "id": 1,
            "name": "Registro 1",
            "text_field": "Some text",
            "selection1": "Option A",
            "selection2": "Option X",
        },
        {
            "id": 2,
            "name": "Registro 2",
            "text_field": "Another text",
            "selection1": "Option B",
            "selection2": "Option Y",
        },
        {
            "id": 3,
            "name": "Registro 3",
            "text_field": "More text",
            "selection1": "Option C",
            "selection2": "Option Z",
        },
        {
            "id": 4,
            "name": "Registro 4",
            "text_field": "Example text",
            "selection1": "Option A",
            "selection2": "Option Y",
        },
        {
            "id": 5,
            "name": "Registro 5",
            "text_field": "Sample text",
            "selection1": "Option B",
            "selection2": "Option X",
        },
        {
            "id": 6,
            "name": "Registro 6",
            "text_field": "Test text",
            "selection1": "Option C",
            "selection2": "Option Z",
        },
    ]
    show_dialog: bool = False
    is_editing: bool = False
    current_record: Optional[Record] = None
    table_options: list[str] = ["Tabela 1", "Tabela 2", "Tabela 3"]
    order_by_options: list[str] = ["Name", "Date", "Priority"]
    search_query1: str = ""
    search_query2: str = ""
    next_id: int = 7

    def toggle_dialog(self):
        self.show_dialog = not self.show_dialog
        if not self.show_dialog:
            self.is_editing = False
            self.current_record = None

    def open_create_dialog(self):
        self.is_editing = False
        self.current_record = None
        self.show_dialog = True

    def open_edit_dialog(self, record: Record):
        self.is_editing = True
        self.current_record = record
        self.show_dialog = True

    def handle_submit(self, form_data: dict):
        if self.is_editing and self.current_record:
            record_id_to_update = self.current_record["id"]
            self.records = [
                {**r, **form_data} if r["id"] == record_id_to_update else r
                for r in self.records
            ]
        else:
            new_record: Record = {
                "id": self.next_id,
                "name": f"Registro {self.next_id}",
                "text_field": form_data["text_field"],
                "selection1": form_data["selection1"],
                "selection2": form_data["selection2"],
            }
            self.records.append(new_record)
            self.next_id += 1
        self.toggle_dialog()

    def delete_record(self, record_id: int):
        self.records = [r for r in self.records if r["id"] != record_id]