import pandas as pd
from sqlalchemy import text
from dbConfigReader import get_engine


engine = get_engine()   # create once
    

def get_daily_counts(selected_date):
    query = text("""
        SELECT *
        FROM vwmon_snusitecountsdaily
        WHERE ref_date = :ref_date
    """)
    return pd.read_sql(query, engine, params={"ref_date": selected_date})


def get_weekly_counts(selected_date):
    query = text("""
        SELECT *
        FROM vwmon_snusitecountsweekly
        WHERE ref_date = :ref_date
    """)
    return pd.read_sql(query, engine, params={"ref_date": selected_date})


def get_daily_details(selected_date):
    query = text("""
        SELECT *
        FROM vwmon_snusitedetailsdaily
        WHERE ref_date = :ref_date
    """)
    return pd.read_sql(query, engine, params={"ref_date": selected_date})


def get_weekly_details(selected_date):
    query = text("""
        SELECT *
        FROM vwmon_snusitedetailsweekly
        WHERE ref_date = :ref_date
    """)
    return pd.read_sql(query, engine, params={"ref_date": selected_date})