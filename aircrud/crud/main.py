from dotenv import load_dotenv
import os
from sqlalchemy import create_engine, MetaData, Table, func, select

load_dotenv()
engine = create_engine("mysql+pymysql://root:" + os.getenv("password") + "@127.0.0.1/aircrud")
metadata = MetaData()

host = Table("host", metadata, autoload_with=engine)

def query_builder(table, filters=None, order_by=None, group_by=None,
                  page: int = 1, page_size: int = 10, aggregates=None):
    stmt = select(table)

    # Filtros dinâmicos
    if filters:
        for col, val in filters.items():
            if hasattr(table.c, col):
                stmt = stmt.where(getattr(table.c, col) == val)

    # Agregações + group by
    if aggregates:
        stmt = select(
            *[getattr(table.c, col) for col in group_by or []],
            *[func.__getattr__(agg)(getattr(table.c, col)).label(f"{agg}_{col}")
              for col, agg in aggregates.items()]
        )
        if group_by:
            stmt = stmt.group_by(*[getattr(table.c, col) for col in group_by])

    # Ordenação
    if order_by:
        if isinstance(order_by, list):
            stmt = stmt.order_by(*[getattr(table.c, col) for col in order_by])
        else:
            stmt = stmt.order_by(getattr(table.c, order_by))

    # Paginação
    stmt = stmt.offset((page - 1) * page_size).limit(page_size)

    with engine.connect() as conn:
        return conn.execute(stmt).fetchall()