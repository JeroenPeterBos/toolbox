import pandas as pd
import numpy as np
from pandas import DataFrame
from pathlib import Path


def ingest_clockify(input_path: Path):
    df = pd.read_csv(input_path)
    df = df.rename(columns={
        'Project': 'project',
        'Duration (decimal)': 'hours',
        'Start Date': 'date',
    }, errors='raise')
    df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y')
    return df[['date', 'project', 'hours']]


def process_datapoints(df: DataFrame):
    df = df[~df['project'].isin(['Meetings', 'Other non-WBSO'])]
    df = df.groupby('date').agg(hours=('hours', 'sum'))
    df['hours'] = np.ceil((df['hours'] * .8) * 4) / 4
    return df


def easy_copyable_csv(df: DataFrame):
    all_dates = pd.date_range(start=df.index.min(), end=df.index.max(), freq='D')
    df = df.reindex(all_dates, fill_value=np.NaN).reset_index()

    df['date'] = pd.to_datetime(df['index'])
    df['month'] = df['date'].dt.month
    df['day'] = df['date'].dt.day
    return df.pivot(index='month', columns='day', values='hours')


def process_clockify_to_wbso(in_file: Path, out_file: Path):
    df = ingest_clockify(in_file)
    df = process_datapoints(df)
    df = easy_copyable_csv(df)
    df.to_csv(out_file)

