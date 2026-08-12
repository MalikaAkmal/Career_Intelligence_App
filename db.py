# import mysql.connector as mycon
# from dotenv import load_dotenv
# import os
# load_dotenv()

# def sql_connection():
#     return mycon.connect(
#         host=os.getenv("MYSQL_HOST", "localhost"),
#         user=os.getenv("MYSQL_USER", "root"),
#         password=os.getenv("MYSQL_PASSWORD", ""),
#         database=os.getenv("MYSQL_DATABASE", "career_intelligence_db")
#     )
# def init_database():
#     my_db=mycon.connect(
#         host=os.getenv("MYSQL_HOST", "localhost"),
#         user=os.getenv("MYSQL_USER", "root"),
#         password=os.getenv("MYSQL_PASSWORD", "")
#     )
#     db_cursor=my_db.cursor()
#     db_cursor.execute("CREATE DATABASE IF NOT EXISTS career_intelligence_db")
#     my_db.close()

#     #Connect directly to DB and create raw_jobs table
#     db_conn=sql_connection()
#     db1_cursor=db_conn.cursor()
#     db1_cursor.execute("""
#     create table if not exists jobs(
#     job_no int auto_increment primary key,
#     job_role varchar(100) ,
#     description text ,
#     company_name varchar(100),
#     search_role varchar(100) not null
#     )
#     """)
#     db_conn.commit()
#     db_conn.close()
# def save_job(job_list,job_role):
#     if not job_list:
#         return 
#     db_conn=sql_connection()
#     cursor=db_conn.cursor()
#     insert_query=("""
# insert into jobs(job_role,company_name,description,search_role)
# values(%s,%s,%s,%s)
#     """)
# #we initialize as a list because we donot know the size of data api bought during insertion it will change to tuple format 
#     record_insert=[]
#     for job in job_list:
#         record_insert.append((
#             job.get("job_role", "N/A"),
#             job.get("company_name", "N/A"),
#             job.get("description", ""),
#             job.get("search_role",job_role)
#         ))
#     cursor.executemany(insert_query,record_insert)
#     db_conn.commit()
#     cursor.close()
#     db_conn.close()

# if __name__ == "__main__":
#     init_database()
#     print("MySQL database initialized successfully!")
import os
from dotenv import load_dotenv
import mysql.connector as mycon

load_dotenv()

def sql_connection():
    return mycon.connect(
        host=os.getenv("MYSQL_HOST", "localhost"),
        user=os.getenv("MYSQL_USER", "root"),
        password=os.getenv("MYSQL_PASSWORD", ""),
        database=os.getenv("MYSQL_DATABASE", "career_intelligence_db")
    )

def init_database():
    # 1. Connect without specifying database to create database schema
    my_db = mycon.connect(
        host=os.getenv("MYSQL_HOST", "localhost"),
        user=os.getenv("MYSQL_USER", "root"),
        password=os.getenv("MYSQL_PASSWORD", "")
    )
    db_cursor = my_db.cursor()
    db_name = os.getenv("MYSQL_DATABASE", "career_intelligence_db")
    db_cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
    my_db.close()

    # 2. Connect directly to database to create raw_jobs table
    db_conn = sql_connection()
    db1_cursor = db_conn.cursor()
    db1_cursor.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            job_no INT AUTO_INCREMENT PRIMARY KEY,
            job_role VARCHAR(100),
            description TEXT,
            company_name VARCHAR(100),
            search_role VARCHAR(100) NOT NULL
        )
    """)
    db_conn.commit()
    db_conn.close()

def save_job(job_list, job_role):
    if not job_list:
        return

    db_conn = sql_connection() # Fixed: Added ()
    cursor = db_conn.cursor()

    insert_query = """
        INSERT INTO jobs (job_role, company_name, description, search_role)
        VALUES (%s, %s, %s, %s)
    """

    record_insert = []
    for job in job_list: # Fixed: Removed () from job_list
        record_insert.append((
            job.get("job_role", "N/A"),
            job.get("company_name", "N/A"),
            job.get("description", ""),
            job.get("search_role", job_role) # Map job_role parameter
        ))

    cursor.executemany(insert_query, record_insert)
    db_conn.commit()
    cursor.close()
    db_conn.close()

if __name__ == "__main__":
    init_database()
    print("MySQL database initialized successfully!")
