import requests
import json
import csv
import time
from requests.models import HTTPError
# create url to send
def cr_url( page, query, client_id ) :
  return 'https://api.unsplash.com/search/users?page=' + str(page) + '&query=' + query + '&client_id=' + client_id
# create GET request
def cr_get_request( url ) :
  return json.loads( requests.get( url ).text )['results']
# read csv
def rd_csv( path ) :
  csv_data = set()
  with open( path, 'r', encoding = 'utf-8' ) as fl :
    csv_reader = csv.reader( fl )
    for row in csv_reader :
      csv_data.add( row[0] )
  return csv_data
# update csv
def upd_csv( csv_data, json_data, path ) :
  with open( path, 'a', encoding = 'utf-8' ) as fl :
    for json_dict in json_data :
      username = 'https://unsplash.com/@' + json_dict['username']
      if not username in csv_data :
        csv_data.add( username )
        csv_ln = ( username + ',' + str(json_dict['instagram_username']) + ',' +
                   'https://www.instagram.com/' + str(json_dict['instagram_username']) + ',' +
                   str(json_dict['twitter_username']) + ',' + str(json_dict['portfolio_url']) + '\n' )
        fl.write( csv_ln )
# start search
def st_search( client_id, path ) :
  try :
    n     = 0 
    pg    = 1
    ch    ='a'
    total = 1
    sec = time.time()
    csv_data = rd_csv( path ) 
    print( 'Start of the search...' )

    while pg < 1000 :
      while ch <= 'z' :
        if n <= 50 :
          upd_csv( csv_data, cr_get_request( cr_url( pg, ch, client_id ) ), path )
          ch = chr( ord(ch) + 1 )
          print( 'The data was recorded to file. Total lines: ' + str( total )  )
          total = total + 1
        else :
          dt = time.time() - sec
          print( ( 'The limit on sending requests has been exceeded.\n'
                   'Sending will resume after: ' + str( dt ) + ' sec' ) )
          time.sleep( 3600 - dt )
          print( "Resuming sending requests" )
          n   = 0
          sec = time.time()
      pg = pg + 1

  except HTTPError as http_err :
    print( f'HTTP error occurred: {http_err}' )
  except Exception as err :
    print( f'Other error occurred: {err}' )
  else :
    print( 'End of the search' )
# run 
st_search( client_id = 'vm0iCSRKZ2Y16Bwjp5fCkF6LOQbgcGiJui3tbYCEktE', path = 'unsplash_authors.csv' )