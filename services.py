import pandas as pd

from sqlalchemy import null
from sqlalchemy.sql import text
from colorama import Fore, Back, Style
import institutions as inst
import services_areas as area

def get_sevices(db):
    sql_insert =""
    try:
        df = pd.read_csv('data/services.csv')
        df = df.reset_index()  # make sure indexes pair with number of rows
        
        df['process_id'] = df['process_id'].fillna("")
        df['document_exit'] = df['document_exit'].fillna("")
        df['sirit_code'] = df['sirit_code'].fillna("")
        df['config_service'] = df['config_service'].fillna("")
        df['expertform_id'] = df['expertform_id'].fillna("")
        df['flow_id'] = df['flow_id'].fillna("")
        df['process_flow'] = df['process_flow'].fillna(0)

        for index, service in df.iterrows():
            sql="""
            select * from services where name ='{name}' or slug='{slug}' limit 1
            """.format(name=service['name'],slug=service['slug'])
            db_service = pd.read_sql(sql, con=db)
            if len(db_service)==0:
              
                get_institution = inst.get_institution(db,service['institution_name'],service['institution_acronym'])
                get_area = area.get_sevices_areas(db,service['area_name'],service['area_slug'])
                print("Get area",service['name'])

              
             
                try:
                    sql_insert="""
                    INSERT IGNORE INTO services ( name, service_code, process_id, send, send_expertcode, app_movil, multiple_document, 
                    responsible_id, area_service_id, institution_id, service_status_id, service_type_id, service_provider_id, flow_id,  process_flow, rating,
                    description,  slug, criticidad, link_access, helper_link, visited, is_always_available, sirit_code,
                    ispublished)
                    VALUES ('{name}', '{service_code}', '{process_id}', '{send}', '{send_expertcode}', {app_movil}, {multiple_document}, 
                    '{responsible_id}', '{area_service_id}', '{institution_id}', '{service_status_id}', '{service_type_id}','{service_provider_id}',
                    '{flow_id}', '{process_flow}', {rating}, '{description}', '{slug}', '{criticidad}', '{link_access}', '{helper_link}', '{visited}',
                    '{is_always_available}', '{sirit_code}', '{ispublished}');

                    """.format(
                        name=str(service['name']),
                        service_code=str(service['code_serv']),
                        process_id=service["process_id"],
                        send=1,
                        send_expertcode=str(service['send_expertcode']),
                        app_movil=service['app_movil'],
                        multiple_document=bool(service['multiple_document']),
                        responsible_id=get_institution['responsable_id'],
                        area_service_id=get_area,
                        institution_id=get_institution['institution_id'],
                        service_status_id=2,
                        service_type_id=1,
                        service_provider_id=2,
                        flow_id=service["flow_id"],
                        process_flow=str(service["process_flow"]),
                        rating=service["rating"],
                        description=str(service["description"]),
                        slug=str(service["slug"]),
                        criticidad=service["criticidad"],
                        link_access=str(service["link_access"]),
                        helper_link=str(service["helper_link"]),
                        visited=service["visited"],
                        is_always_available=service["is_always_available"],
                        sirit_code=service["sirit_code"],
                        ispublished=1

                    )
                    
                    result=db.execute(sql_insert)
                    message ='Service created: {name} was create'.format(name=service['name'])
                    print(Fore.GREEN +message+Style.RESET_ALL)
                except Exception as e:
                    print(Fore.RED+"Error"+ e+sql_insert,Style.RESET_ALL)
                    continue

            else:
                continue
    except Exception as e:
         print("Error",e)
         print(sql_insert)