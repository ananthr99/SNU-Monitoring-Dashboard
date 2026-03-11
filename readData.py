import pandas as pd
from sqlalchemy import text
from dbConfigReader import get_engine

engine = get_engine()

def getSNUAgingBucketCounts(reference_ts):
    query = text("""
        SELECT *
        FROM cube_battcntrlagingbucketcount
        WHERE recTimeStamp = :ref_date
    """)
    return pd.read_sql(query, engine, params={"ref_date": reference_ts})

def getSNUAgingBucketDetails(reference_ts):
    query = text("""
        SELECT DISTINCT smSiteCode, smSiteName, daysCount, hoursCount, dailyBucket, weeklyBucket, recTimeStamp
        FROM cube_battcntrlagingbucketdetails
        WHERE recTimeStamp = :ref_date
    """)
    return pd.read_sql(query, engine, params={"ref_date": reference_ts})

def getDGCntrlAgingBucketCounts(reference_ts):
    query = text("""
        SELECT *
        FROM cube_dgcntrlagingbucketcount
        WHERE recTimeStamp = :ref_date
    """)
    return pd.read_sql(query, engine, params={"ref_date": reference_ts})

def getDGCntrlAgingBucketDetails(reference_ts):
    query = text("""
        SELECT DISTINCT smSiteCode, smSiteName, daysCount, hoursCount, dailyBucket, weeklyBucket, recTimeStamp
        FROM cube_dgcntrlagingbucketdetails
        WHERE recTimeStamp = :ref_date
    """)
    return pd.read_sql(query, engine, params={"ref_date": reference_ts})

def getBattCntrlAgingBucketCounts(reference_ts):
    query = text("""
        SELECT *
        FROM cube_battcntrlagingbucketcount
        WHERE recTimeStamp = :ref_date
    """)
    return pd.read_sql(query, engine, params={"ref_date": reference_ts})

def getBattCntrlAgingBucketDetails(reference_ts):
    query = text("""
        SELECT DISTINCT smSiteCode, smSiteName, daysCount, hoursCount, dailyBucket, weeklyBucket, recTimeStamp
        FROM cube_battcntrlagingbucketdetails
        WHERE recTimeStamp = :ref_date
    """)
    return pd.read_sql(query, engine, params={"ref_date": reference_ts})

def getRectCntrlAgingBucketCounts(reference_ts):
    query = text("""
        SELECT *
        FROM cube_rectcntrlagingbucketcount
        WHERE recTimeStamp = :ref_date
    """)
    return pd.read_sql(query, engine, params={"ref_date": reference_ts})

def getRectCntrlAgingBucketDetails(reference_ts):
    query = text("""
        SELECT DISTINCT smSiteCode, smSiteName, daysCount, hoursCount, dailyBucket, weeklyBucket, recTimeStamp
        FROM cube_rectcntrlagingbucketdetails
        WHERE recTimeStamp = :ref_date
    """)
    return pd.read_sql(query, engine, params={"ref_date": reference_ts})

def getSolarAgingBucketCounts(reference_ts):
    query = text("""
        SELECT *
        FROM cube_solaragingbucketcount
        WHERE recTimeStamp = :ref_date
    """)
    return pd.read_sql(query, engine, params={"ref_date": reference_ts})

def getSolarAgingBucketDetails(reference_ts):
    query = text("""
        SELECT DISTINCT smSiteCode, smSiteName, daysCount, hoursCount, dailyBucket, weeklyBucket, recTimeStamp
        FROM cube_solaragingbucketdetails
        WHERE recTimeStamp = :ref_date
    """)
    return pd.read_sql(query, engine, params={"ref_date": reference_ts})

def getFuelAgingBucketCounts(reference_ts):
    query = text("""
        SELECT *
        FROM cube_fuelagingbucketcount
        WHERE recTimeStamp = :ref_date
    """)
    return pd.read_sql(query, engine, params={"ref_date": reference_ts})

def getFuelAgingBucketDetails(reference_ts):
    query = text("""
        SELECT DISTINCT smSiteCode, smSiteName, daysCount, hoursCount, dailyBucket, weeklyBucket, recTimeStamp
        FROM cube_fuelagingbucketdetails
        WHERE recTimeStamp = :ref_date
    """)
    return pd.read_sql(query, engine, params={"ref_date": reference_ts})