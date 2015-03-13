"""
Steph Northway
March 10 2015
For internal use only. Processing the Google Takedown Request data. Various attempts to make the data usable.
"""
import pandas as pd

from entities import Entity, DisplayEntity
from data_utils import unpickle_dataframe, better_column_names, datestring_to_datetime

# Path to giant csvs in my hard drive
CSV_PATH = '/media/Seagate Backup Plus Drive/Olin Classes/Software Design/google-websearch-copyright-removals'


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


def generate_entities(requests_file, domains_file, center_name, num_entries=100):
    """
    Makes a DisplayEntity object for the Bokeh code. Only makes one where the center object is a requester.

    requests_file: a .p file containing requests data
    domains_file: a .p file containing domains data
    center_name: the name of the center object
    num_domains: number of entries to use from the start of the domains file
    returns: a DisplayEntity to be used by the bokeh applet
    """
    requests_df = better_column_names(pd.read_pickle(requests_file))
    requests_df.date = requests_df.date.apply(lambda x: (datestring_to_datetime(x).year, datestring_to_datetime(x).month))
    domains_df = better_column_names(pd.read_pickle(domains_file))
    entries = domains_df[:num_entries]

    outer = []
    for s in set(entries.domain.values):
        name = s
        category = 'target'
        size = [0, 0, 0]  # [#urls removed, no action, pending]
        relevant_domains = domains_df[domains_df.domain == s]
        size[0] = relevant_domains.urls_removed.sum()  # urls removed
        size[1] = relevant_domains.urls_for_which_we_took_no_action.sum()  # urls not removed
        size[2] = relevant_domains.urls_pending_review.sum()  # urls pending review
        outer.append(Entity(name, category, size))
    center = Entity(center_name, 'requester', 20)
    # pickle_dataframe(return_de, 'fox_display_entity.p')
    return DisplayEntity(center, outer)


if __name__ == '__main__':
    DE = generate_entities('requests_fox.p', 'domains_fox.p', 'Fox')
    pd.to_pickle(DE, 'first_hundred.p')
