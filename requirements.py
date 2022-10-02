import pandas as pd
from sqlalchemy.sql import text
from colorama import Fore, Back, Style
def get_requirements(db,service_id):
    try:
        requirements = pd.read_csv('data/requirements.csv')
        query="service_id=={service_id}".format(service_id=service_id)
        requirements=requirements.query(query)
        for index, requirement in requirements.iterrows():
            sql_select="""select * from requirements where name ='{name}'  limit 1; """.format(name=requirement['name'])
            db_service = pd.read_sql(sql_select, con=db)
            if len(db_service)==0:
                sql_insert="""
                INSERT INTO requirements ( name, description, route) 
                VALUES ('{name}', '{description}', '{route}');
                    """.format(
                        name=requirement["name"],
                        description=requirement["description"],
                        route=requirement["route"]
                        )
                result=db.execute(sql_insert)
                db_result = pd.read_sql(sql_select, con=db)
                sql="""INSERT IGNORE INTO requirement_service  (service_id, requirement_id) VALUES ({service_id}, {requirement_id});
                 """.format(
                     service_id=service_id,
                     requirement_id=db_result["id"].values[0])
                result=db.execute(sql)
                message ='Create requirement: {name} was create'.format(name=requirement["name"])
                print(Fore.GREEN +message+Style.RESET_ALL)
            else:
                db_result = pd.read_sql(sql_select, con=db)
                sql="""INSERT IGNORE INTO requirement_service  (service_id, requirement_id) VALUES ({service_id}, {requirement_id});
                 """.format(
                     service_id=service_id,
                     requirement_id=db_result["id"].values[0])
                result=db.execute(sql)
                message ='Create requirement: {name} was create'.format(name=requirement["name"])
                print(Fore.GREEN +message+Style.RESET_ALL)
        
    except Exception as e: print(e)