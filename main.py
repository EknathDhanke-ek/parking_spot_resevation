from pyramid.config import Configurator
from pyramid.response import Response
from paste.httpserver import serve
#from sql_wrapper import SqlWrapper
#sqlWrapper = SqlWrapper()
#import psycopg2.extras
import psycopg2
import json


def get_db_connection():
    cur, conn = None, None
    try:
        conn = psycopg2.connect(host="localhost",database="parking", user="postgres", password="postgres321")
        cur = conn.cursor()
        return cur, conn
    except (Exception, psycopg2.Error) as error :
        print ("Error while connecting to PostgreSQL", error)
    finally:
        return cur, conn
 
def available_parking_spots(request):
    print(request) 
    #sqlWrapper = get_db_connection() 
    sqlWrapper, conn = get_db_connection()
    if sqlWrapper is None:
        sqlWrapper, conn, status = get_db_connection()
        
    print(sqlWrapper)
    result = sqlWrapper.execute("select * from parking_spots_tbl where is_available = True")
    print(result)
    result = sqlWrapper.fetchall()
    print(result)
    response_list = []
    for record in result:
         op_dict = {}
         parking_spot_id, lat, lon, is_available, parking_fee = record[0], record[1], record[2], record[3], record[4]

         op_dict['parking_spot_id'], op_dict['latitude'], op_dict['longitute'] = parking_spot_id, str(lat), str(lon)
         op_dict['is_available'], op_dict['parking_fee'] = is_available, parking_fee 
          
         response_list.append(op_dict)                 
   
    print(type(response_list)) 
    print(response_list) 
    
    final_response = {} 
    final_response['data'] = response_list
    print(final_response)
    #final_response = json.loads(final_response) 
    res = json.dumps(final_response) 
 
    return Response(res)
    #return Response(final_response)

def find_nearby_parking_spot(request):
     input_data = request.json_body
     lat = input_data['latitude'] 
     lan = input_data['longitude'] 
     radius = input_data['radius']

     #sqlWrapper = get_db_connection() 
     sqlWrapper, conn = get_db_connection() 
     print(sqlWrapper)

     qry = "select * from parking_spots_tbl where (latitute <= " + str(lat) + " + " + str(radius) + " and latitute >= "+ str(lat) + "-" + str(radius) + " ) and (longitute <="+ str(lan) +" + " + str(radius) + " and longitute >= " + str(lan) + "-" + str(radius) + ")"

     #qry = "select * from parking_spots_tbl where (latitute >= " + in_lat + " + " + radius + " and latitude <= "+ lat " - " + radius + " ) and (longitude >="+ in_lan +" + " + radius + " and longitute <= " + in_lan + "-" + radius + ")"
 
     print('qry is:')
     print(qry) 
     result = sqlWrapper.execute(qry)
     result = sqlWrapper.fetchall()
     response_list = []
     print(result)
     for record in result:
         op_dict = {}
         parking_spot_id, lat, lon, is_available, parking_fee = record[0], record[1], record[2], record[3], record[4]

         op_dict['parking_spot_id'], op_dict['latitude'], op_dict['longitute'] = parking_spot_id, str(lat), str(lon)
         op_dict['is_available'], op_dict['parking_fee'] = is_available, parking_fee 
          
         response_list.append(op_dict)                 
     
     final_response = {} 
     final_response['data'] = response_list
     res = json.dumps(final_response) 
     print(res)
 
     return Response(res)

def reserve_parking_spot(request):
     input_data = request.json_body
     lat = input_data['latitude'] 
     lan = input_data['longitude'] 
     user_id = input_data['user_id']

     sqlWrapper, conn = get_db_connection() 
     qry = "update parking_spots_tbl set is_available = False where latitute = "+ str(lat) +" and longitute = " + str(lan) + " RETURNING parking_spot_id_pk;"
     print(qry)
     result = sqlWrapper.execute(qry)
     result = sqlWrapper.fetchone()
     print(result)
     parkig_spot_id = result[0] 
     print('parkig_spot_id') 
     print(parkig_spot_id) 
     qry = "insert into user_parking_reservation_tbl(user_id_fk, parking_spot_id_fk, is_paid) values("+ str(user_id) +","+ str(parkig_spot_id) +",True) RETURNING user_parking_id_pk;"
     print(qry)
     result = sqlWrapper.execute(qry)
     result = sqlWrapper.fetchone()
     user_parkig_spot_id = result[0] 
     conn.commit()
     print(result)
     if user_parkig_spot_id > 0:
         return Response('success')
     else:
         return Response('failure')
    

def cancel_reservation(request):
     input_data = request.json_body
     lat = input_data['latitude'] 
     lan = input_data['longitude'] 
     user_id = input_data['user_id']
     
     sqlWrapper, conn = get_db_connection() 
     qry = "update parking_spots_tbl set is_available = True where latitute = "+ str(lat) +" and longitute = " + str(lan) + " RETURNING parking_spot_id_pk;"
     print(qry)
     result = sqlWrapper.execute(qry)
     result = sqlWrapper.fetchone()
     print(result)
     parkig_spot_id = result[0] 
     print('parkig_spot_id') 
     print(parkig_spot_id) 
     #qry = "insert into user_parking_reservation_tbl(user_id_fk, parking_spot_id_fk, is_paid) values("+ str(user_id) +","+ str(parkig_spot_id) +",True) RETURNING user_parking_id_pk;"
     qry = "delete from user_parking_reservation_tbl where user_id_fk = "+ str(user_id) + " RETURNING user_parking_id_pk;"
     print(qry)
     result = sqlWrapper.execute(qry)
     result = sqlWrapper.fetchone()
     user_parkig_spot_id = result[0] 
     conn.commit()
     print(result)
     if user_parkig_spot_id > 0:
         return Response('success')
     else:
         return Response('failure')
    

def get_existing_reservation(request):
     input_data = request.json_body
     lat = input_data['latitude'] 
     lan = input_data['longitude'] 
     user_id = input_data['user_id']
     
     sqlWrapper, conn = get_db_connection() 
     qry = "update parking_spots_tbl set is_available = True where latitute = "+ str(lat) +" and longitute = " + str(lan) + " RETURNING parking_spot_id_pk;"
     print(qry)
     result = sqlWrapper.execute(qry)
     result = sqlWrapper.fetchone()
     print(result)
     parkig_spot_id = result[0] 
     print('parkig_spot_id') 
     print(parkig_spot_id) 
     #qry = "insert into user_parking_reservation_tbl(user_id_fk, parking_spot_id_fk, is_paid) values("+ str(user_id) +","+ str(parkig_spot_id) +",True) RETURNING user_parking_id_pk;"
     qry = "delete from user_parking_reservation_tbl where user_id_fk = "+ str(user_id) + " RETURNING user_parking_id_pk;"
     print(qry)
     result = sqlWrapper.execute(qry)
     result = sqlWrapper.fetchone()
     user_parkig_spot_id = result[0] 
     conn.commit()
     print(result)
     if user_parkig_spot_id > 0:
         return Response('success')
     else:
         return Response('failure')
    
if __name__ == '__main__':
    sqlWrapper, conn = get_db_connection() 
    config = Configurator()
    config.add_view(available_parking_spots, name = 'available')
    config.add_view(find_nearby_parking_spot, name = 'nearby')
    config.add_view(reserve_parking_spot, name = 'reserve')
    config.add_view(cancel_reservation, name = 'cancel')
    config.add_view(get_existing_reservation, name = 'existing')
    app = config.make_wsgi_app()
    serve(app, host='0.0.0.0')
