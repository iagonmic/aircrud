import reflex as rx
from aircrud.states.crud_state import CRUDState


def record_form() -> rx.Component:
    return rx.el.dialog(
        rx.el.div(
            rx.el.form(
                rx.el.div(
                    rx.el.h2(
                        rx.cond(CRUDState.is_editing, "Editar Ação", "Nova Ação"),
                        class_name="text-2xl font-bold text-gray-800 mb-6 text-center",
                    ),
                    rx.el.div(
                        rx.el.label(
                            "Campo Textual 1",
                            class_name="text-sm font-medium text-gray-600",
                        ),
                        rx.el.input(
                            name="text_field",
                            default_value=rx.cond(
                                CRUDState.is_editing,
                                CRUDState.current_record["text_field"],
                                "",
                            ),
                            placeholder="Campo textual",
                            class_name="w-full mt-1 p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-pink-500 focus:border-transparent",
                        ),
                        class_name="mb-4",
                    ),
                    rx.el.div(
                        rx.el.label(
                            "Campo Textual 2",
                            class_name="text-sm font-medium text-gray-600",
                        ),
                        rx.el.input(
                            name="name_field_placeholder",
                            placeholder="Campo textual",
                            class_name="w-full mt-1 p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-pink-500 focus:border-transparent",
                        ),
                        class_name="mb-4",
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.el.label(
                                "Seleção 1",
                                class_name="text-sm font-medium text-gray-600",
                            ),
                            rx.el.select(
                                rx.el.option("Option A", value="Option A"),
                                rx.el.option("Option B", value="Option B"),
                                rx.el.option("Option C", value="Option C"),
                                name="selection1",
                                default_value=rx.cond(
                                    CRUDState.is_editing,
                                    CRUDState.current_record["selection1"],
                                    "Option A",
                                ),
                                class_name="w-full mt-1 p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-pink-500 focus:border-transparent",
                            ),
                            class_name="w-full",
                        ),
                        rx.el.div(
                            rx.el.label(
                                "Seleção 2",
                                class_name="text-sm font-medium text-gray-600",
                            ),
                            rx.el.select(
                                rx.el.option("Option X", value="Option X"),
                                rx.el.option("Option Y", value="Option Y"),
                                rx.el.option("Option Z", value="Option Z"),
                                name="selection2",
                                default_value=rx.cond(
                                    CRUDState.is_editing,
                                    CRUDState.current_record["selection2"],
                                    "Option X",
                                ),
                                class_name="w-full mt-1 p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-pink-500 focus:border-transparent",
                            ),
                            class_name="w-full",
                        ),
                        class_name="flex gap-4 mb-6",
                    ),
                    rx.el.div(
                        rx.el.button(
                            "Finalizar",
                            type="submit",
                            class_name="w-full bg-pink-600 text-white py-2 px-4 rounded-lg hover:bg-pink-700 transition-colors",
                        ),
                        rx.el.button(
                            "Cancelar",
                            type="button",
                            on_click=CRUDState.toggle_dialog,
                            class_name="w-full bg-gray-200 text-gray-700 py-2 px-4 rounded-lg hover:bg-gray-300 transition-colors mt-2",
                        ),
                        class_name="flex flex-col items-center",
                    ),
                    class_name="bg-white p-8 rounded-2xl shadow-2xl border border-gray-100 w-[30rem] max-w-[90vw]",
                ),
                on_submit=CRUDState.handle_submit,
                reset_on_submit=True,
            ),
            class_name="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 backdrop-blur-sm z-50",
            on_click=CRUDState.toggle_dialog,
        ),
        open=CRUDState.show_dialog,
    )