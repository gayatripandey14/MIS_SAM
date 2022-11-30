from django.db import connections
from collections import OrderedDict
import datetime

def my_custom_sql(query):
    with connections['smpp_db'].cursor() as cursor:
        cursor.execute(query)
        columns = [col[0] for col in cursor.description]
    return [
    dict(zip(columns, row))
    for row in cursor.fetchall()]
    

def fetch_sms_log_table(start_date,end_date):
    sql = f"SELECT table_name FROM information_schema.tables WHERE TABLE_SCHEMA='kannel' AND table_name Like '%sms_cdr%' AND  date_format(create_time,'%Y-%m-%d') >= '{start_date}' AND date_format(create_time,'%Y-%m-%d') <= '{end_date}' "
    sms_cdr_tables = my_custom_sql(sql)  

    return sms_cdr_tables

# def fetch_smslog_data(start_date,end_date,username,page):
#     page_no = int(page)
#     limit = 10 
#     offset = (page_no-1) * limit
#     rtn_data = []
    
#     if start_date!=None and end_date!=None:
        
#         tables = fetch_sms_log_table(start_date,end_date)
#         for data in tables:
            
#             query = f"SELECT * FROM {data['table_name']}  WHERE account= '{username}' LIMIT {offset},{limit} "
#             q = my_custom_sql(query)   
#             rtn_data.extend(q)
#         return rtn_data    
#     else:
#         query = f"SELECT * FROM sms_cdr  LIMIT {offset},{limit} "
#         q = my_custom_sql(query)   
#         return q    
    
def sms_cdr_analytics(start_date,end_date,username):
    
    tables = fetch_sms_log_table(start_date,end_date)
    print(tables)
    rtn_data = []
    for data in tables:
        # query = f"SELECT (SELECT Count(*)  FROM {data['table_name']} WHERE account = '{username}' ) as submission_count,(SELECT COUNT(*)  FROM {data['table_name']} WHERE status = 'UNDELIV' AND account = '{username}') as undelivered_count,(SELECT COUNT(*)  FROM {data['table_name']} WHERE status = 'DELIVRD' AND account = '{username}') as delivered_count "
        cdr_data = f"SELECT COUNT(*) AS submission_count,COUNT(CASE WHEN status = 'UNDELIV' THEN 1 END) AS undelivered_count,COUNT(CASE WHEN status = 'DELIVRD' THEN 1 END) AS delivered_count FROM {data['table_name']} WHERE account = '{username}'"
        cdr_analytics = my_custom_sql(cdr_data)
        
        rtn_data.extend(cdr_analytics)  
    return rtn_data





def fetch_smslog_data(start_date,end_date,username,page):
    page_no = int(page)
    limit = 10 
    offset = (page_no-1) * limit
    rtn_data = []
    
    if start_date!=None and end_date!=None:
        
        tables = fetch_sms_log_table(start_date,end_date)

        query = "select * from ( "

        for i,data in enumerate(tables):
            
            innerQuery = f"SELECT * FROM {data['table_name']}  WHERE account= '{username}'"
            
            if i == len(tables) -1:
                query = query + innerQuery
            else: 
                query = query + innerQuery + " UNION ALL "

        query = f"{query} ) as finaldata order by sql_id LIMIT {offset},{limit} " 
        total_data = my_custom_sql(query)

        return total_data                                   
    else:
        query = f"SELECT * FROM sms_cdr  LIMIT {offset},{limit} "
        q = my_custom_sql(query)   
        return q        