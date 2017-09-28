import requests
import datetime
import traceback
import csv


def get_session():
    s = requests.Session()
    s.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:48.0) Gecko/20100101 Firefox/48.0'
    return s

def url_list_generator():
    years = ['2012', '2013', '2014', '2015', '2016', '2017']
    months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
    days = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31']
    base_url = 'http://content.caiso.com/green/renewrpt/{0}{1}{2}_DailyRenewablesWatch.txt'
    

    url_list = []
    for i in years:
        for j in months:
            for k in days:
                try:
                    url_list.append((datetime.date(int(i), int(j), int(k)), base_url.format(i, j, k)))
                except:
                    pass
                
    return url_list

def main():
    
    data = {}
    urls = url_list_generator()
    
    for i in urls:
        s = get_session()
        r = s.get(i[1], stream=True)
        if r.status_code == 200:
            print(i[0])
            headers = []
            for line in r.iter_lines():
                
                if line: 
                    formatted_line= str(line).replace("b'", '').split('\\t')
                    formatted_line = [j.replace("'",'') for j in formatted_line if (len(j) > 0 and j != "'")]
                    
                    print(formatted_line)
                    try:
                        if formatted_line[0] == 'Hour':
                            headers = formatted_line[1:]
                            print(headers)
                    except:
                        print('error', formatted_line)

                    if len(headers) >0:
                        try: 
                            hour = int(formatted_line[0])
                            
                            zipped_line = zip(formatted_line[1:], headers)
                            print(zipped_line)
                            for z in zipped_line:
                                print(z)
                                data[(i[0], hour, z[1])] = z[0]
                            
                        except:
                            #not a data line
                            pass
                            #traceback.print_exc()
                            
    
        
    with open('caiso_data.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(('date', 'hour', 'type', 'data'))
        for i in data.keys():
            writer.writerow((i[0], i[1], i[2], data[i]))
                    
                    
                    
                    
                    
            
main()