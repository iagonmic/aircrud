import reflex as rx
from aircrud.states.crud_state import CRUDState
from aircrud.components.record_form import record_form


def filter_controls() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.select(
                rx.foreach(
                    CRUDState.table_options,
                    lambda option: rx.el.option(option, value=option),
                ),
                class_name="w-full md:w-auto p-2 border border-pink-300 rounded-lg text-pink-600 focus:ring-2 focus:ring-pink-500 focus:border-transparent",
            ),
            rx.el.select(
                rx.foreach(
                    CRUDState.order_by_options,
                    lambda option: rx.el.option(option, value=option),
                ),
                class_name="w-full md:w-auto p-2 border border-pink-300 rounded-lg text-pink-600 focus:ring-2 focus:ring-pink-500 focus:border-transparent",
            ),
            rx.el.input(
                placeholder="sla",
                on_change=CRUDState.set_search_query1,
                class_name="w-full md:w-auto p-2 border border-pink-300 rounded-lg placeholder-pink-300 focus:ring-2 focus:ring-pink-500 focus:border-transparent",
            ),
            rx.el.input(
                placeholder="sla",
                on_change=CRUDState.set_search_query2,
                class_name="w-full md:w-auto p-2 border border-pink-300 rounded-lg placeholder-pink-300 focus:ring-2 focus:ring-pink-500 focus:border-transparent",
            ),
            class_name="flex flex-wrap gap-4",
        ),
        class_name="mb-8",
    )


def record_row(record: rx.Var[dict]) -> rx.Component:
    return rx.el.div(
        rx.el.p(record["name"], class_name="font-medium text-gray-800"),
        rx.el.div(
            rx.el.button(
                rx.icon("search", class_name="w-5 h-5"),
                class_name="text-gray-500 hover:text-blue-600 transition-colors p-1",
            ),
            rx.el.button(
                rx.icon("pencil", class_name="w-5 h-5"),
                on_click=lambda: CRUDState.open_edit_dialog(record),
                class_name="text-gray-500 hover:text-green-600 transition-colors p-1",
            ),
            rx.el.button(
                rx.icon("trash-2", class_name="w-5 h-5"),
                on_click=lambda: CRUDState.delete_record(record["id"]),
                class_name="text-gray-500 hover:text-red-600 transition-colors p-1",
            ),
            class_name="flex items-center gap-2",
        ),
        class_name="flex items-center justify-between p-4 border border-pink-200 rounded-lg hover:bg-pink-50 transition-colors",
    )


def records_list() -> rx.Component:
    return rx.el.div(
        rx.el.h3("Registros", class_name="text-2xl font-bold text-pink-600 mb-4"),
        rx.el.button(
            "Criar registro",
            rx.icon("circle_plus", class_name="ml-2"),
            on_click=CRUDState.open_create_dialog,
            class_name="flex items-center mb-6 p-2 border border-pink-300 rounded-lg text-pink-600 hover:bg-pink-100 transition-colors",
        ),
        rx.el.div(
            rx.foreach(CRUDState.records, record_row), class_name="flex flex-col gap-3"
        ),
    )


def crud_page() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h1(
                "CRUD", class_name="text-4xl font-bold text-gray-800 mb-8 text-center"
            ),
            rx.el.div(
                filter_controls(),
                records_list(),
                class_name="w-full max-w-4xl p-8 bg-white rounded-2xl shadow-lg border border-gray-100",
            ),
            record_form(),
            class_name="min-h-screen flex flex-col items-center justify-center bg-gray-50 p-4 font-['Inter']",
        )
    )