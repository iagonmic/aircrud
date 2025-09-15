import reflex as rx

config = rx.Config(
    app_name="aircrud",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ]
)