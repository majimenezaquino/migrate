import pandas as pd
from sqlalchemy.sql import text
from colorama import Fore, Back, Style
def get_sevice_responsible(db,institution_id):
    try:
        sql="SELECT * FROM service_responsibles  WHERE institution_id ={institution_id};".format(institution_id=institution_id)
        df = pd.read_sql(sql, con=db)
        if len(df)==0:
            sql_institutions="select  * from institutions where id = {institution_id} limit 1;".format(institution_id=institution_id)
            df = pd.read_sql(sql_institutions, con=db)
            #create responsible
            if len(df)>0:
                user_email=""
                institution_email =df["email"].values[0]
                domail_email =institution_email[institution_email.index('@') + 1 : ]
                if len(domail_email)>0:
                    user_email="responsable.servicios@"+domail_email

                sql_responsible="""INSERT INTO service_responsibles (name, email, phone, institution_id) VALUES ('{name}', '{email}', '{phone}', {institution_id} );""".format(
                    name="Responsable de servicios",
                    email=user_email,
                    phone=df["phone"].values[0],
                    institution_id=institution_id
                    )
                db.execute(sql_responsible)

                df = pd.read_sql(sql, con=db)
                return df["id"].values[0]
        else:
            return df["id"].values[0]
        
    except Exception as e: print(e)