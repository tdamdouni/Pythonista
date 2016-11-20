#!/usr/bin/env python
 
"""
Socrata Open Data datasets can be selected, cached locally, and printed out.
Datasets published by City of Chicago @ http://data.cityofchicago.org
 
Read in description data on all datasets (currently 294)
loop: Allow the user to select one
    Write a json version of the dataset to a local file
    From the dataset metadata, create a namedtuple for the column names
    Dump all dataset rows as namedtuples
    Go to loop
 
Notes:
    Not all datasets have json representations --> script fails
    Avoid monstrous datasets such as All Crimes from 2001 to Present (5m records)
"""
 
import bs4, collections, contextlib, datetime, json, os.path, sys, time, urllib2
 
fmt_dict = { 'city_name': 'cityofchicago',
             'data_format' : 'json',
             'data_set'    : None }
 
base_url_fmt  = 'https://data.{city_name}.org'
base_url      = base_url_fmt.format(**fmt_dict)
browse_datasets_url = base_url + '/browse?limitTo=datasets&utf8=%E2%9C%93&view_type=rich'
file_name_fmt = '{data_set}.{data_format}'
url_fmt       = 'https://data.{city_name}.org/api/views/{data_set}/rows.{data_format}'
headerFmt     = '{attribution} ({category}) - {id}: {name}'
 
dataset_info = collections.namedtuple('dataset_info',
                'url short_descrition long_description')
 
def get_user_int(prompt, in_min=-1000000, in_max=100000):
    (in_min, in_max) = (min(int(in_min), int(in_max)), # make sure both are ints
                        max(int(in_min), int(in_max))) # and in_min <= in_max
    try:
        user_int = int(raw_input(prompt))
        if in_min <= user_int <= in_max:
            return user_int
    except ValueError:
        pass
    return get_user_int(prompt, in_min, in_max)
 
def get_webpage_source(in_url):
    print('Downloading webpage...')
    print(in_url)
    with contextlib.closing(urllib2.urlopen(in_url)) as in_file:
        return in_file.read()
 
def get_soup_from_url(in_url):
    the_html = get_webpage_source(in_url)
    return bs4.BeautifulSoup(the_html) if the_html else None
 
def hours_ago(in_hours_ago = 24):
    delta_t = datetime.timedelta(hours=in_hours_ago)
    return time.time() - delta_t.total_seconds()
 
def file_must_be_refreshed(in_file_name):
    if (os.path.isfile(in_file_name)
    and os.path.getmtime(in_file_name) > hours_ago(24)):
        return False # file exists and modified in past 24hrs
    return True
 
def get_data_dict(in_file_name):
    with open(in_file_name) as in_file:
        return json.loads(in_file.read())
 
def data_row_named_tuple(in_data_dict):
    data_columns = []
    for columns_dict in in_data_dict['meta']['view']['columns']:
        if 'cachedContents' in columns_dict:
            data_columns.append(columns_dict['fieldName'])
    return collections.namedtuple('data_row', data_columns)
 
def get_dataset_info_from_soup(in_soup):
    dataset_list = [] # empty list
    for result in in_soup.find('div', {'class' : 'results' }):
        if isinstance(result, bs4.Tag):
            for table_row in result.tbody.find_all('td', {'class' : 'richSection'}):
                dataset_url = table_row.find('a')['href']
                short_desc = table_row.find('span').text
                long_desc = table_row.find('div',
                                        {'class' : 'description collapsed'}).text
                dataset_list.append(
                    dataset_info(dataset_url, short_desc, long_desc))
    return dataset_list
 
def gather_dataset_info(in_url = browse_datasets_url):
    dataset_list = [] # empty list
    the_soup = get_soup_from_url(in_url)
    last_page = int(the_soup.find('a', {'title' : 'Last Page'})['href'].rpartition('=')[2])
    curr_page = 1 # the_soup already contains the html of page 1
    ds_count = int(the_soup.find('div', {'class' : 'resultCount'}).text.split()[-1])
    print('Gathering info on {} datasets from {} webpages...'.format(ds_count, last_page))
    while the_soup:
        dataset_list += get_dataset_info_from_soup(the_soup)
        print('Information gathered on {} datasets...'.format(len(dataset_list)))
        curr_page += 1
        if curr_page > last_page:
            the_soup = None
        else:
            next_url = '{}&page={}'.format(in_url, curr_page)
            the_soup = get_soup_from_url(next_url)
    return dataset_list
 
def process_dataset(in_dataset_id = '28km-gtjn'):
    fmt_dict['data_set'] = in_dataset_id
    file_name = file_name_fmt.format(**fmt_dict)
    print(file_name + '=' * 80)
    if file_must_be_refreshed(file_name):
        the_url = url_fmt.format(**fmt_dict)
        print('Writing {} --> {}'.format(the_url, file_name))
        with open(file_name, 'w') as out_file:
            out_file.write(get_webpage_source(the_url))
    data_dict = get_data_dict(file_name)
    data_row = data_row_named_tuple(data_dict)
    dict_view = data_dict['meta']['view']
    print(headerFmt.format(**dict_view))
    print('> {description}'.format(**dict_view))
    for the_item in data_dict['data']:
        print(data_row(*the_item[8:]))

def main(argv):
    dataset_list = gather_dataset_info()
    s = raw_input('Press <Return> to continue...')
    for i, dsi in enumerate(dataset_list):
        dataset_id = dsi.url.rpartition('/')[2]
        print('{:>3} {} {}\n'.format(i+1, dataset_id ,dsi))
    prompt_fmt = 'To view a dataset, enter a number between 1 and {}.\nOr to quit enter 0 (zero): '
    i = ds_count = len(dataset_list)
    while i:
        i = get_user_int(prompt_fmt.format(ds_count), 0, ds_count)
        if i:
            dataset_info = dataset_list[i-1]
            print('Going for {}...'.format(dataset_info))
            process_dataset(dataset_info.url.rpartition('/')[2])
 
if __name__ == '__main__':
    sys.exit(main(sys.argv))
