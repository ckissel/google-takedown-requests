"""
Author: Stephanie Northway
Date: 3/8/2015
Utility functions for dealing with large CSVs in Pandas.
"""

import cPickle
from datetime import datetime
from dateutil.parser import parse
from pytz import UTC as utc


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


def make_offset_aware(dt):
    """
    Take a datetime object and make it offset aware so Pandas doesn't cry.
    """
    return utc.localize(dt)


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
