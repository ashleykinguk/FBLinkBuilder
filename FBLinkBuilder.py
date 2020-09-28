import os 
import json
import argparse
from zipfile import ZipFile 
from datetime import datetime

fname = datetime.now().strftime("FB_Deeplinks%d%m%Y%H%M%S.txt") #default filename

parser = argparse.ArgumentParser() 
parser.add_argument('-i', help='Facebook APK file')
parser.add_argument('-o', help='Output file', nargs='?', default=fname)
parser.add_argument('-e', help='Only show exported. Defaulted to False', nargs='?', default=False)
args = parser.parse_args()

file_name = args.i #apk
output_name = args.o #generated output / provided
exported = args.e #False / provided

with ZipFile(file_name, 'r') as zip: 
    print('Extracting native routes file...') #fyi
    
    data = zip.read('assets/react_native_routes.json') #extract file from zip
    js = json.loads(data.decode("utf-8")) #to read as list

    params = '' #placeholder
    
    i = 0 #deeplink count
    
    text_file = open(output_name, "w") #open output

    print('Manipulating data...') #fyi
    for key in js: #for each block in json
        for key2 in key['paramDefinitions']: #grab the collection of params
            params += key2 + '=' + str(key['paramDefinitions'][key2]['type']).upper() + '&' #append params with type
            
        if exported: #exported only
            if key.get('access','') != 'exported': #check access key
                params = '' #Reset params
                continue #try next block
                
        link = 'fb:/' + key['path'] + '/?' + params #build link
        print(link[:-1]) #fyi
        text_file.write(link[:-1]+ '\n') #write to file
        i += 1 #increase counter
        params = '' #reset params

    text_file.close() #save file
    
    print('File: ' + output_name + ' saved') #fyi
    print(str(i) + ' deep links generated') #fyi
