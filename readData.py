import pandas as pd
from sqlalchemy import text
from dbConfigReader import get_engine


engine = get_engine()
    

def getAgingBucketCounts(reference_ts):
    query = text("""
        SELECT *
        FROM cube_sitenotupdatingbucketcount
        WHERE refTimeStamp = :ref_date
    """)
    return pd.read_sql(query, engine, params={"ref_date": reference_ts})

def getAgingBucketDetails(reference_ts):
    query = text("""
        SELECT DISTINCT smSiteCode, smSiteName, weeklyBucket, refTimeStamp
        FROM cube_sitenotupdatingbucketdetails
        WHERE refTimeStamp = :ref_date
    """)
    return pd.read_sql(query, engine, params={"ref_date": reference_ts})