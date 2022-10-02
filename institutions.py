import pandas as pd
from sqlalchemy.sql import text
from colorama import Fore, Back, Style
import services_responsible
def get_institution(db,name,acronym):
    try:
        sql="SELECT * FROM institutions where name='{name}' or acronym='{acronym}' limit 1;".format(name=name,acronym=acronym)
        df = pd.read_sql(sql, con=db)
        if len(df)==0:
            query="name=='{name}' or acronym=='{acronym}'".format(name=name,acronym=acronym)
            df_institutions = pd.read_csv('data/institutions.csv')
            institutions=df_institutions.query(query)
       
            if len(institutions)>0:
                query="""
                  INSERT IGNORE INTO institutions
                    ( name, rnc, email, acronym, token, website, slug, phone, picture,  address_id, is_exported)
                    VALUES ( '{name}', '{rnc}', '{email}', '{acronym}', '{token}', '{website}',
                            '{slug}', '{phone}', '{picture}',  1, true);
                """.format(
                    name=institutions["name"].values[0],
                    rnc=institutions["rnc"].values[0],
                    email=institutions["email"].values[0],
                    acronym=institutions["acronym"].values[0],
                    token=institutions["token"].values[0],
                    website=institutions["website"].values[0],
                    slug=institutions["slug"].values[0],
                    phone=institutions["phone"].values[0],
                    picture=institutions["picture"].values[0])
                result=db.execute(query)
                df = pd.read_sql(sql, con=db)
                message ='Service area: {name} was create'.format(name=df["id"].values[0])
                print(Fore.GREEN +message+Style.RESET_ALL)
                institution_id = df["id"].values[0]
                #create service reponsible

                responsable_id =services_responsible.get_sevice_responsible(db,institution_id)
                return {
                    "institution_id":institution_id,
                    "responsable_id":responsable_id,
                }
                
                #cursor.commit()
            else:
                print(Fore.RED + 'Error the service area no exist in data/insittution.csv'+Style.RESET_ALL)
        else:
            institution_id = df["id"].values[0]
            responsable_id = services_responsible.get_sevice_responsible(db,institution_id)
            return {
                    "institution_id":institution_id,
                    "responsable_id":responsable_id,
                }
        
    except Exception as e: print(e)