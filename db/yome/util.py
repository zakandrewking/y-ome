# -*- coding: utf-8 -*-

from datetime import timedelta
import pandas as pd

def create(session, query_class, commit=False, **kwargs):
    """Add a new row to the database and return.

    Arguments
    ---------

    session: The SQLAlchemy session.

    query_class: The class to query.

    commit: If True, then commit. Otherwise flush.

    """
    res = query_class(**kwargs)
    session.add(res)
    if commit:
        session.commit()
    else:
        session.flush()
    return res

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
        return res, True
    return create(session, query_class, commit=commit, **kwargs), False

def format_seconds(total_sec):
    """Format a time delta.

    """
    delt = timedelta(seconds=total_sec)
    days = delt.days
    hours, rem = divmod(delt.seconds, 3600)
    minutes, seconds = divmod(rem, 60)
    if seconds == 0:
        return '<1 s'
    s = '%s s' % seconds
    if minutes:
        s = '%d m ' % minutes + s
    if hours:
        s = '%d h ' % hours + s
    if days:
        s = '%d d ' % days + s
    return s

def to_df(res, cols):
    """Convert a SQLAlchemy query result to a DataFrame."""
    data = [{k: v for k, v in zip(cols, x)} for x in res]
    if len(data) == 0:
        return pd.DataFrame()
    return pd.DataFrame(data).loc[:, cols]
