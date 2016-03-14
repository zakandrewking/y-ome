# -*- coding: utf-8 -*-

def get_or_create(session, query_class, commit=False, **kwargs):
    """Query the query_class, filtering by the given keyword arguments. If no result
    is found, then add a new row to the database. Returns result of the query.

    Arguments
    ---------

    session: The SQLAlchemy session.

    query_class: The class to query.

    commit: If True, then commit. Otherwise flush.

    """
    res = session.query(query_class).filter_by(**kwargs).first()
    if res is not None:
        return res
    res = query_class(**kwargs)
    session.add(res)
    if commit:
        session.commit()
    else:
        session.flush()
    return res
