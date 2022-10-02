
import pandas as pd
import pymysql
from sqlalchemy import create_engine
import services_areas
import institutions
import services_responsible
import services
sqlEngine = create_engine('mysql+pymysql://root:@127.0.0.1/prop_gob', pool_recycle=3600)
dbConnection    = sqlEngine.connect()


#print("arreas",services_areas.get_sevices_areas(dbConnection,"Educación","EDUCACIONN"))
#Sprint("institutions: ",institutions.get_institution(dbConnection,"Oficina Gubernamental de Tecnologías de la Información y Comunicación","EDUCACIONN"))
#print("services responsible: ",services_responsible.get_sevice_responsible(dbConnection,1))
print("Services",services.get_sevices(dbConnection))

# df = pd.read_sql('SELECT * FROM services_tmp limit 10', con=mydb)
# print(df['service_old_id'].to_string())
dbConnection.close()