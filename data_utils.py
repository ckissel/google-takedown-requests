"""
Author: Stephanie Northway
Date: 3/8/2015
Utility functions for dealing with large CSVs in Pandas.
"""

import pandas as pd
import cPickle
from datetime import datetime
from dateutil.parser import parse
from pytz import UTC as utc


CSV_PATH = '/media/Seagate Backup Plus Drive/Olin Classes/Software Design/google-websearch-copyright-removals'


def pickle_dataframe(df, filename):
    """
    Save a dataframe in a pickle file.
    df: dataframe to be saved
    filename: name of file to save to
    """
    with open(filename, 'wb') as f:
        cPickle.dump(df, f)


def unpickle_dataframe(filename):
    """
    Load a dataframe from a pickle file.
    filename: name of file to load from
    """
    return cPickle.load(open(filename, 'rb'))


def better_column_names(df):
    """
    Make lowercase, and replace spaces with underscores in column names
    so you don't have to type brackets and quotes.
    df: dataframe to modify
    """
    df.columns = map(lambda s: s.lower().replace(' ', '_'), df.columns)
    return df


def datestring_to_datetime(datestring):
    """
    Converts a date string (like the ones in the Google takedown request data)
    into a datetime object.
    """
    return parse(datestring)


def datetime_to_datestring(dt):
    """
    Takes a datetime object and returns a string formatted in the way that Google's
    takedown request data was formatted.
    """
    pass


def make_offset_aware(dt):
    """
    Take a datetime object and make it offset aware so Pandas doesn't cry.
    """
    return utc.localize(dt)


def get_latest():
    """
    A one-off function to get only the domains rows from after 2013 for a more workable dataset.
    The csv won't push to git because it's too big, so you'll have to trust me.
    """
    domains_iterator = pd.read_csv(CSV_PATH + '/domains.csv', iterator=True, chunksize=100000)
    # start_date = make_offset_aware(datetime(2013, 1, 1, 0, 0))
    request_ids = unpickle_dataframe('requests_after_2013.p')['Request ID'].values
    domains_df = None
    for df in domains_iterator:
        df = df[df['Request ID'].isin(request_ids)]
        if domains_df is not None:
            domains_df = domains_df.append(df)
        else:
            domains_df = df

    # pickle_dataframe(domains_df, 'domains_after_2013.p')
    return domains_df


def get_abusers():
    """
    Return the subset of domains.csv for which 'From Abuser' is True.
    """
    domains_iterator = pd.read_csv(CSV_PATH + '/domains.csv', iterator=True, chunksize=100000)
    domains_df = None
    for df in domains_iterator:
        df = df[df['From Abuser'] == True]
        if domains_df is not None:
            domains_df = domains_df.append(df)
        else:
            domains_df = df

    return domains_df


def filter_large_df(df_iter, fn):
    """
    Takes a dataframe iterator and function to filter the domains dataframe by.
    """
    return_df = None
    for df in df_iter:
        df = df[fn(df)]
        if return_df is not None:
            return_df = return_df.append(df)
        else:
            return_df = df

    return return_df


def filter_df(df, fn):
    new_df = df[fn(df)]
    return new_df


def generate_main_df():
    """
    Generate the dataframe that will FINALLY be the source of data for our bokeh visualization.
    """

    requests = unpickle_dataframe('requests_abusers.p')
    domains = unpickle_dataframe('domains_abusers.p')

    return requests, domains  # eh


def generate_entities():
    """
    Make a DisplayEntity for Caleb to use.
    """
    foxr = better_column_names(pd.read_pickle('requests_fox.p'))
    foxr.date = foxr.date.apply(lambda x: (datestring_to_datetime(x).year, datestring_to_datetime(x).month))
    # foxr.date = foxr.date.apply(lambda x: (x.year, x.month))
    foxd = better_column_names(pd.read_pickle('domains_fox.p'))
    first_hundred = foxd[:100]
    # top = foxd.sort(['urls_removed'], ascending=False)[:num]

    # domains = top.domain.values
    # sizes = [float(s)/max(top.urls_removed.values) for s in top.urls_removed.values]
    # DE = DisplayEntity(Entity('Fox', 'requester', 20), [Entity(domains[i], 'target', sizes[i]) for i in range(len(domains))])
    # return DE

    max_sum = 154807  # experimentally determined
    outer = []
    # alldates = sorted(list(set(foxr.date.values)))
    # month_maxes = [max(foxd[foxd.request_id in foxr[foxr.date==d].request_id.values].urls_removed.sum()) for d in alldates]
    # month_maxes = []
    # for d in alldates:
    #     rr = foxr[foxr.date == d].request_id.values
    #     rd = foxd[foxd.request_id in rr]
    for s in set(first_hundred.domain.values):
        name = s
        category = 'target'
        size = [0, 0, 0]  # [#urls removed, no action, pending]
        relevant_domains = foxd[foxd.domain == s]
        size[0] = relevant_domains.urls_removed.sum()  # urls removed
        size[1] = relevant_domains.urls_for_which_we_took_no_action.sum()  # urls not removed
        size[2] = relevant_domains.urls_pending_review.sum()  # urls pending review
        # request_ids = relevant_domains.request_id.values  # get the request ids associated with this domain
        # relevant_requests = foxr[foxr.request_id.isin(request_ids)].sort('date')  # get the relevant rows from foxr
        # date_sizes = []
        # date_sizes = [foxd[foxd.request_id in relevant_requests[relevant_requests.date == d]].urls_removed.sum() for d in sorted(list(set(relevant_requests.date)))]
        # for d in alldates:
        #     requests_in_month = relevant_requests[relevant_requests.date == d].request_id.values
        #     date_sizes.append(foxd[foxd.request_id.isin(requests_in_month)].urls_removed.sum())
        outer.append(Entity(name, category, size))
    center = Entity('Fox', 'requester', 20)
    # pickle_dataframe(return_de, 'fox_display_entity.p')
    return DisplayEntity(center, outer)
    # return outer



class Entity:
    """
    Represents a requester or domain.

    name: copyright owner name or domain name
    category: requester or target
    size: how large the circle should be
    """
    def __init__(self, name, category, size):
        self.name = name
        self.category = category
        self.size = size
        self.x = None
        self.y = None
        self.width = 1
        self.alpha = 1


class DisplayEntity:
    """
    View class. (Or viewmodel I guess?)
    center: center Entity
    outer: list of Entity objects connected to center
    """
    def __init__(self, center, outer):
        self.center = center
        self.outer = outer


if __name__ == '__main__':
    # domains_iterator = pd.read_csv(CSV_PATH + '/domains.csv', iterator=True, chunksize=500000)
    # # fox_requests = unpickle_dataframe('requests_startswith_fox.p')
    # fox_requests = filter_large_df(pd.read_csv(CSV_PATH + '/requests.csv', iterator=True, chunksize=100000), lambda df: df['Copyright owner name'].str.match('^Fox$').fillna(False))
    # pickle_dataframe(fox_requests, 'requests_fox.p')
    # df = filter_large_df(domains_iterator, lambda x: x['Request ID'].isin(fox_requests['Request ID'].values))
    # pickle_dataframe(df, 'domains_fox.p')
    DE = generate_entities()
    pd.to_pickle(DE, 'first_hundred.p')
