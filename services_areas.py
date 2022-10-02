import pandas as pd
from sqlalchemy.sql import text
from colorama import Fore, Back, Style
def get_sevices_areas(db,name,slug):
    try:
        sql="SELECT * FROM area_services where name='{name}' or slug='{slug}' limit 1;".format(name=name,slug=slug)
        df = pd.read_sql(sql, con=db)
        if len(df)==0:
            query="name=='{name}' or slug=='{slug}'".format(name=name,slug=slug)
            df_service_area = pd.read_csv('data/service_area.csv')
            service_area=df_service_area.query(query)

            if len(service_area)>0:
                query="INSERT INTO area_services (name, slug) VALUES ('{name}', '{slug}');".format(name=name,slug=slug)
                result=db.execute(query)
                df = pd.read_sql(sql, con=db)
                message ='Service area: {name} was create'.format(name=df["id"].values[0])
                print(Fore.GREEN +message+Style.RESET_ALL)
                return df["id"].values[0]
                
                #cursor.commit()
            else:
                print(Fore.RED + 'Error the service area no exist in data/service_area.csv'+Style.RESET_ALL)
        else:
            return df["id"].values[0]
        
    except Exception as e: print(e)