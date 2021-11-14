import requests
import json
import csv
import time
import colorama
from requests.models import HTTPError
from colorama import Fore
# create url to send
def cr_url( page, query, client_id, per_page = 100 ) :
  return 'https://api.unsplash.com/search/users?page=' + str(page) + '&per_page=' + str(per_page) + '&query=' + query + '&client_id=' + client_id
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
        csv_ln = ( username + ',' + str( json_dict['instagram_username'] ) + ',' +
                   'https://www.instagram.com/' + str( json_dict['instagram_username'] ) + ',' +
                   str( json_dict['twitter_username'] ) + ',' + str( json_dict['portfolio_url'] ) + '\n' )
        fl.write( csv_ln )
# start search
def st_search( client_id, path ) :
  try :
    colorama.init()
    csv_data = rd_csv( path ) 

    n     = 0 
    pg    = 1
    total = 1
    sec   = time.time()

    print( 'Start of the search...' + Fore.LIGHTMAGENTA_EX )

    while pg < 1000 :
      ch = 'a'
      while ch <= 'z' :
        if n < 50 :
          upd_csv( csv_data, cr_get_request( cr_url( pg, ch, client_id ) ), path )
          print( ( 'The data was recorded to file. Total lines: ' + str( total ) + 
                   ' Page = ' + str( pg ) + ' Query = ' + ch  ) )
          ch    = chr( ord(ch) + 1 )
          total = total + 1
          n     = n + 1
        else :
          sleep_sec = 3600 - time.time() + sec
          print( ( Fore.LIGHTBLUE_EX + 'The limit on sending requests has been exceeded.\n'
                   'Sending will resume after: ' + str( sleep_sec ) + ' sec' ) )
          time.sleep( sleep_sec )
          print( "Resuming sending requests" + Fore.LIGHTMAGENTA_EX )
          n   = 0
          sec = time.time()
      pg = pg + 1

  except HTTPError as http_err :
    print( Fore.RED + f'HTTP error occurred: {http_err}' )
  except Exception as err :
    print( Fore.RED + f'Other error occurred: {err}' )
  else :
    print( Fore.WHITE + 'End of the search' )
# run 
st_search( client_id = 'vm0iCSRKZ2Y16Bwjp5fCkF6LOQbgcGiJui3tbYCEktE', path = 'unsplash_authors.csv' )
input()