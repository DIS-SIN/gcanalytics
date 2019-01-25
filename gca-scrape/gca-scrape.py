# gca-scrape is the json generator for gcanalytics dashboard
# the goal here is to build 'live' data from the existing page
# without having to wait for access to the raw data because
# nothing is worse waiting while an idea runs away
# eventually this tool is eventually not needed once a real
# reporter is generated from the raw data source. baby steps!
print ('-- gca-scrape: webpage scrape tool --')

import requests
import json
import locale
import calendar
import copy
import datetime

from dateutil import parser
from bs4 import BeautifulSoup

# setup locale for timestamping
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

# the source data url, we will scrape this for content
# note: working directly with the data is obviously better
# but we're about disrupting with purpose. Before we engage
# the other teams with requests and emails and the meat of the ask
# we want to make sure it's worth it for everyone. This scrape is
# currently tightly coupled to the page structure (not ideal), but
# its enough to build us the files we need. As a plus when were done
# and we end up asking, we have some real specs we can work with
url = 'https://www.canada.ca/en/analytics.html'
output_folder = "../static/data/can-live/"
# grab the html
print(f"* url: {url}")
page = requests.get(url)
print(f"* HTTP-return: {page.status_code}")

if page.status_code == requests.codes.ok:
    page_text = page.text
else:
    page_text = ""

# were using bs4 here to chew through the tags and give us workable data
soup = BeautifulSoup(page_text, 'lxml')
datapoints = soup.find_all('div', class_='mwsanalytics')

# our reports for the new dashboard
reports = [\
    "snapshot","pageviews","mobileusers",\
    "visits",\
    "departments-en","departments-fr",\
    "downloads-en","downloads-fr",\
    "news-en","news-fr",\
    "pages-en","pages-fr",\
    "sections-en","sections-fr",\
    "videos-en","videos-fr",\
    "visitor-location-city","visitor-location-region","visitor-location-country"\
    ]

# our json templates for reporr types. these are the generics we will fill up
report_templates = [\
    "template-visits",\
    "template-metric",\
    "template-metric-percent",\
    "template-page-href-view",\
    "template-page-view",\
    "template-place-percent"\
    ]

# hints we will use to intuit the type of report
# warn: this segment is tightly coupled to the structure and content of the source page
# likely if anything will need updating its this
report_to_chart_map_json = '{\
   " Visits": {"t":"visits","r":"template-visits"},\
   "Most visited sections (Visits to English content)": {"t":"sections-en","r":"template-page-view"},\
   "Most visited sections(Visits to French content)":  {"t":"sections-fr","r":"template-page-view"},\
   "Most visited departments (Visits to English content)":  {"t":"departments-en","r":"template-page-view"},\
   "Most visited departments(Visits to French content)":  {"t":"departments-fr","r":"template-page-view"},\
   "Most viewed English pages": {"t":"pages-en","r":"template-page-href-view"},\
   "Most viewed  French pages": {"t":"pages-fr","r":"template-page-href-view"},\
   "Most viewed  English news": {"t":"news-en","r":"template-page-href-view"},\
   "Most viewed  French news": {"t":"news-fr","r":"template-page-href-view"},\
   "English pages with the most downloads": {"t":"downloads-en","r":"template-page-href-view"},\
   "French pages with the most downloads": {"t":"downloads-fr","r":"template-page-href-view"},\
   "Most played English videos": {"t":"videos-en","r":"template-page-href-view"},\
   "Most played French videos": {"t":"videos-fr","r":"template-page-href-view"},\
   "By city ": {"t":"visitor-location-city","r":"template-place-percent"},\
   "By region ": {"t":"visitor-location-region","r":"template-place-percent"},\
   "By country ": {"t":"visitor-location-country","r":"template-place-percent"},\
   "Mobile users": {"t":"mobileusers","r":"template-metric"},\
   "Visits-metric": {"t":"snapshot","r":"template-metric"},\
   "Page views": {"t":"pageviews","r":"template-metric"}\
    }'

# json up the hint map so we can use it in our checks
report_to_chart_map = json.loads(report_to_chart_map_json)

# pull in the json file and load it for use
def get_report_template_json(template):
    with open("templates/"+template+'.json') as f:
        data = json.load(f)
        return data

# determine what kind of chart/report this block of soup is
# this relies on the structure of our sourced url html
# warn: another brittle point, but such is the nature of 
# kind of this function. ideally this whole py script is just
# a shim to make this work until we get our various teams and orgs
# standardized on one tracking and metrics system and we get the data
# from a single source
def intuit_report_details(dp):
    print(f"* intuiting report type")
    contains_thead = dp.find('thead')
    if contains_thead is not None:
        # items with a thead are usually our basic charts
        chart_label = dp.find('h2')
        if chart_label is not None:
            report_name = report_to_chart_map[chart_label.text]['t']
            print(f"* think its {report_name} based on {chart_label.text}")
            report_template = get_report_template_json( report_to_chart_map[chart_label.text]['r'] )
            report_template['name'] = report_name
            report_template['meta']['name'] = chart_label.text
            report_template['meta']['description'] = "Chart that displays " + chart_label.text + " measured from tracker data"
            # location charts have slighty altered dat labels
            if report_name == 'visitor-location-city':
                report_template['query']['dimensions'] = "rt:city"
            if report_name == 'visitor-location-region':
                report_template['query']['dimensions'] = "rt:region"
            if report_name == 'visitor-location-country':
                report_template['query']['dimensions'] = "rt:country"
            return report_template
    print(f"* hmm, might be a metric... checking")
    contains_h4 = dp.find('span', class_='h4')
    if contains_h4 is not None:
        # our metrics usually have an h4
        metric_label = contains_h4.text.strip()
        if metric_label == "Visits":
            metric_label = "Visits-metric"
        report_name = report_to_chart_map[metric_label]['t']
        print(f"* think its {report_name} based on {metric_label}")
        report_template = get_report_template_json( report_to_chart_map[metric_label]['r'] )
        report_template['name'] = report_name
        report_template['meta']['name'] = metric_label
        report_template['meta']['description'] = "Metric that displays " + metric_label + " measured from tracker data"
        return report_template        
    print(f"* failed, using default, found {dp}")
    return get_report_template_json('template-page-view')    

# the meat of the parsing happens here
# ok lets grab the data
for dp in datapoints:
    report_template = intuit_report_details(dp)
    rec_body = dp.find_all('tr')

    #dt = datetime.datetime
    report_template['taken_at'] = str(datetime.datetime.utcnow())

    rec_body_data = []

    if report_template['name'] in ['mobileusers','snapshot','pageviews']:
        # metric
        print(f"* metric data detected")
        rec_body = dp.find_all('span',class_='h1')
        index_offset = 0
        if report_template['name'] == 'snapshot':
            print(f"* snaphot metric: custom case, extract pageviews metric now")
            # this metric has two in the chunk we need
            index_offset = 1
            # we will quickly create and add this metric so its not lost
            report_template_pageviews = copy.deepcopy(report_template)
            report_template_pageviews['name'] = 'pageviews'
            report_template_pageviews['data'] = [{'active_visitors': locale.atoi( rec_body[index_offset].text.strip('%,') )}]
            serialized = json.dumps(report_template_pageviews, sort_keys=True, indent=3)
            with open(output_folder+report_template_pageviews['name']+".json", "w") as text_file:
                print(f"* JSON written to {text_file}")
                print(f"{serialized}", file=text_file)
        index_offset = 0 # reset offset
        item = {}
        # depending on the data its either an int or percent as float
        # but d3 wants no commas or %s yet, so lets get rid of them now
        if report_template['name'] == 'mobileusers': 
            item['active_visitors'] = rec_body[index_offset].text.strip('%,')
        else:
            item['active_visitors'] = locale.atoi( rec_body[index_offset].text.strip('%,') )
        rec_body_data.append(item)
    else:
        #chart
        parseflag_skip_first_record = True #column headers appear, skip this
        parseflag_start_date_parsed = False #visits chart get first rec date for config
        for rp in rec_body:
            if parseflag_skip_first_record:
                parseflag_skip_first_record = False
                continue
            item = {} # the shell of a datapoint we will breathe life into
            str_list = rp.text.splitlines()
            # so some data has 2 fields (normal), some has 3 and some 4... 
            # but the extras are duplicate data, so we can just edge case these to progress
            # warn: this is another brittle point
            bundled_dps = list(filter(None, str_list))
            index_offset = 0
            if len(bundled_dps) > 2:
                index_offset = 1
            if report_template['name'] in ['visitor-location-city','visitor-location-region','visitor-location-country']:
                index_offset = 0

            dlabel = bundled_dps[0+index_offset]
            
            #try for date, just use the label otherwise 
            try:
                dlabel = parser.parse(dlabel).strftime('%Y-%m-%d')
            except ValueError:
                dlabel = dlabel
            
            # setup report specific config as needed    
            if report_template['name'] == 'visits':
                item['hour'] ="00"
                item['date'] = dlabel;
                if parseflag_start_date_parsed is False:
                    report_template['query']['start-date'] = dlabel
                    parseflag_start_date_parsed = True
                report_template['query']['end-date'] = dlabel
            elif report_template['name'] == 'visitor-location-city':
                item['city'] = dlabel
            elif report_template['name'] == 'visitor-location-region':
                item['region'] = dlabel
            elif report_template['name'] == 'visitor-location-country':
                item['country'] = dlabel
            else:
                item['page_title'] = dlabel
            
            # values    
            try:
                vlabel = int(locale.atof(bundled_dps[1+index_offset].strip(',')))
            except:
                vlabel = bundled_dps[1+index_offset].strip('%,')

            if report_template['name'] == 'visits':
                item['visits'] = vlabel
            else:
                item['active_visitors'] = vlabel

            # hrefs
            hyperlink_payload = rp.a
            if hyperlink_payload is None:
                pass
            else:
                item['page'] = str(rp.a.get('href'))
            # push the data into its home. 
            rec_body_data.append(item)
    # report json ready, attach the data to the filled template
    report_template['data'] = rec_body_data
    # write it out
    serialized = json.dumps(report_template, sort_keys=True, indent=3)
    with open(output_folder+report_template['name']+".json", "w") as text_file:
        print(f"* JSON written to {text_file}")
        print(f"{serialized}", file=text_file)
print("-- gca-scrape complete --")
