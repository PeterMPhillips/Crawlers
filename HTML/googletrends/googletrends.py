import urllib2
import json
import csv
import sys

try:
    scale = sys.argv[1]
    term = sys.argv[2]
    term = term.replace('-', ' ')
except Exception as e:
    print e
    raise

hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

def get_data(searchterm, timescale):
    if timescale == 'day':
        scale = 'now+1-d'
    if timescale == 'week':
        scale = 'now+7-d'
    if timescale == 'month':
        scale = 'today+1-m'
    if timescale == 'quarter':
        scale = 'today+3-m'
    if timescale == 'year':
        scale = 'today+12-m'

    urlterm = urllib2.quote(searchterm)
    url = 'https://trends.google.com/trends/api/explore?hl=en-US&tz=0&req=%7B%22comparisonItem%22:%5B%7B%22keyword%22:%22' + urlterm + '%22,%22geo%22:%22%22,%22time%22:%22' + scale + '%22%7D%5D,%22category%22:0,%22property%22:%22%22%7D&tz=0'
    req = urllib2.Request(url, headers=hdr)
    response = urllib2.urlopen(req)

    first = True
    for line in response:
        if first:
            first = False
        else:
            j = json.loads(line)
            #print(json.dumps(j, indent=4, separators=(',', ': ')))

    response.close()

    request = json.dumps(j['widgets'][0]['request'])
    token = j['widgets'][0]['token']

    get_csv(searchterm, timescale, request, token)

def get_csv(searchterm, timescale, req, token):
    urlterm = urllib2.quote(searchterm)
    req = urllib2.quote(req)
    tz = "0"

    url = 'https://trends.google.com/trends/api/widgetdata/multiline/csv?req={0}&token={1}&tz={2}'.format(req, token, tz)

    request = urllib2.Request(url, headers=hdr)
    request.add_header('Referer', 'https://trends.google.com/trends/explore?date=now%201-d&q=' + urlterm)
    response = urllib2.urlopen(request)

    trend_csv = csv.reader(response)

    with open('csv/' + searchterm + '.csv', 'w') as fp:
        writer = csv.writer(fp, delimiter=',')

        count = 0
        for row in trend_csv:
            count += 1
            if count == 3:
                row[0] = 'Date'
                row[1] = searchterm.title() + ' Trends'
                writer.writerow(row)
                print row

            if count > 3:
                writer.writerow(row)
                print row

    response.close()



get_data(term, scale)
