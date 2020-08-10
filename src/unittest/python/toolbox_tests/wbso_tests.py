from test_base import ToolboxTest
import pandas as pd
import numpy as np

from toolbox.wbso import ingest_clockify, process_datapoints, easy_copyable_csv


class IngestClockifyTest(ToolboxTest):
    def test_ingest(self):
        df = ingest_clockify(self.test_data_dir / 'wbso' / 'demo.csv')

        self.assertTrue(set(df.columns) == {'date', 'project', 'hours'})
        self.assertGreater(df.shape[0], 1)


class ProcessDatapointsTest(ToolboxTest):
    def test_filter_meetings(self):
        df = pd.DataFrame(data={
            'date': pd.to_datetime(['2019-01-01', '2019-01-02', '2019-01-03']),
            'project': ['Load Forecasting', 'Meetings', 'Other non-WBSO'],
            'hours': [1.0, 2.3, 5.3]
        })
        df = process_datapoints(df)
        expected = pd.DataFrame(data={
            'date': pd.to_datetime(['2019-01-01']),
            'hours': [np.ceil(1.0 * 0.8 * 4) / 4]
        }).set_index('date')

        pd.testing.assert_frame_equal(df, expected)

    def test_aggregate_days(self):
        df = pd.DataFrame(data={
            'date': pd.to_datetime(['2019-01-01', '2019-01-02', '2019-01-02']),
            'project': ['Load Forecasting', 'Baselines', 'Baselines'],
            'hours': [1.0, 2.3, 5.3]
        })
        df = process_datapoints(df)

        expected = pd.DataFrame(data={
            'date': pd.to_datetime(['2019-01-01', '2019-01-02']),
            'hours': np.ceil(np.array([1.0, 7.6]) * 0.8 * 4) / 4
        }).set_index('date')

        pd.testing.assert_frame_equal(df, expected)

    def test_round_upper_90_percent(self):
        df = pd.DataFrame(data={
            'date': pd.to_datetime(['2019-01-01', '2019-01-02', '2019-01-03']),
            'project': ['baselines', 'baselines', 'baselines'],
            'hours': [0.25, 0.26 / .8, .49 / .8]
        })
        df = process_datapoints(df)

        expected = pd.DataFrame(data={
            'date': pd.to_datetime(['2019-01-01', '2019-01-02', '2019-01-03']),
            'hours': [.25, .50, .50]
        }).set_index('date')

        pd.testing.assert_frame_equal(df, expected)


class EasyCopyableTest(ToolboxTest):
    def test_easy_copyable(self):
        df = pd.DataFrame(data={
            'date': pd.to_datetime(['2019-01-01', '2019-02-02', '2019-03-01']),
            'hours': [0.25, .5, .5]
        }).set_index('date')
        df = easy_copyable_csv(df)

        self.assertEqual(set(range(1, 4)), set(df.index.tolist()))
        self.assertEqual(set(range(1, 32)), set(df.columns))

