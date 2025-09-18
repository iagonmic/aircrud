from dotenv import load_dotenv
import os
from sqlalchemy import create_engine, MetaData, Table, func, select, insert, update, delete

load_dotenv()
engine = create_engine("mysql+pymysql://root:" + os.getenv("password") + "@127.0.0.1/aircrud")
metadata = MetaData()
metadata.reflect(bind=engine)

def get_available_table_names():
    for table in metadata.sorted_tables:
        yield table.fullname

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

    # exemplo: host_results = query_table("host", order_by=['RoomsRent'])

    # Paginação
    stmt = stmt.offset((page - 1) * page_size).limit(page_size)

    with engine.connect() as conn:
        result = conn.execute(stmt)
        return [dict(row) for row in result.mappings().all()]
    
def update_record(table, record_id, data: dict):
    pk = get_pk_column_name(table)
    stmt = (
        update(table)
        .where(getattr(table.c, pk) == record_id)
        .values(**data)
    )
    with engine.begin() as conn:
        result = conn.execute(stmt)
        return result.rowcount  # número de linhas afetadas
    
def delete_record(table, record_id):
    pk = get_pk_column_name(table)
    stmt = delete(table).where(getattr(table.c, pk) == record_id)
    with engine.begin() as conn:
        result = conn.execute(stmt)
        return result.rowcount
    
def get_table_info(table_name, **kwargs):
    table = get_table_by_name(table_name)
    if table:
        return query_builder(table, **kwargs)
    print("Tabela não encontrada")

def get_table_by_name(table_name):
    for table in metadata.sorted_tables:
        if table.fullname == table_name:
            return table
    return None

def get_pk_column_name(table):
    return table.primary_key.columns.keys()[0]
    
