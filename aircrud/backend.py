from dotenv import load_dotenv
import os
from sqlalchemy import create_engine, MetaData, Table, func, select, insert, update, delete

load_dotenv()
engine = create_engine("mysql+pymysql://root:" + os.getenv("password") + "@127.0.0.1/aircrud")
metadata = MetaData()
metadata.reflect(bind=engine)

def get_available_tables():
    for table in metadata.tables:
        yield table

def create_record(table, data: dict):
    stmt = insert(table).values(**data)
    with engine.begin() as conn:  # begin = abre transação automática
        result = conn.execute(stmt)
        return result.inserted_primary_key


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
        result = conn.execute(stmt)
        return [dict(row) for row in result.mappings().all()]
    
def update_record(table, record_id, data: dict, pk="id"):
    stmt = (
        update(table)
        .where(getattr(table.c, pk) == record_id)
        .values(**data)
    )
    with engine.begin() as conn:
        result = conn.execute(stmt)
        return result.rowcount  # número de linhas afetadas
    
def delete_record(table, record_id, pk="id"):
    stmt = delete(table).where(getattr(table.c, pk) == record_id)
    with engine.begin() as conn:
        result = conn.execute(stmt)
        return result.rowcount

def get_table_by_name(name):
    return Table(name, metadata, autoload_with=engine)

def query_table(name, **kwargs):
    table = get_table_by_name(name)
    return query_builder(table, **kwargs)
