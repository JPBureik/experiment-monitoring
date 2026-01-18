#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 07 10:00:50 2021

@author: jp

Interactive script to filter past spikes in time-stamped dataseries for
experiment monitoring with influxdb.

Checks the influxdb database for spikes in past data based on a user-defined
spike factor, display time stamps, unix time stamps and values for found spikes
and deletes them on request.
"""

from __future__ import annotations

import datetime
import time
from typing import Any

from influxdb import InfluxDBClient
from tqdm import tqdm


class DbSpikeFilter:
    """Interactive database spike filter for cleaning historical data."""

    database: str
    client: InfluxDBClient
    series_list: list[str]
    selected_series: str
    spike_factor: float
    data: dict[str, list[Any]]
    timestamps: dict[str, list[str]]
    spike_indices: dict[str, list[int]]
    spike_timestamps: dict[str, list[str]]
    spike_utimestamps: dict[str, list[str]]
    total_spikes: dict[str, int]

    def __init__(self) -> None:
        self.database = "helium2"
        self.client = InfluxDBClient(
            host="localhost", port=8086, database=self.database
        )
        self.series_list = []
        self.data = {}
        self.timestamps = {}
        self.spike_indices = {}
        self.spike_timestamps = {}
        self.spike_utimestamps = {}
        self.total_spikes = {}
        self.display_series()
        self.select_series()
        self.set_spike_factor()
        self.find_spikes()
        if self.total_spikes[self.selected_series]:
            self.delete_spikes()

    @staticmethod
    def conv_to_u_time(date_time: datetime.datetime) -> str:
        date_time = date_time + datetime.timedelta(hours=2)
        u_time = time.mktime(date_time.timetuple())
        u_time_str = str(u_time)[:-2] + 9 * "0"
        return u_time_str

    def set_spike_factor(self) -> None:
        spike_factor_in = input(
            "Set spike factor for series {}:\n".format(self.selected_series)
        )
        try:
            self.spike_factor = float(spike_factor_in)
            print("Searching for spikes ...")
        except ValueError:
            print("Try again!")
            self.set_spike_factor()

    def is_spike(self, data_point: float, previous: float, following: float) -> bool:
        if (
            data_point > previous * self.spike_factor
            and data_point > following * self.spike_factor
        ):
            return True
        elif (
            data_point < previous / self.spike_factor
            and data_point < following / self.spike_factor
        ):
            return True
        else:
            return False

    def display_series(self) -> None:
        series_result: Any = self.client.query("SHOW series").raw
        self.series_list = [
            series_result["series"][0]["values"][i][0].split(",")[0]
            for i in range(len(series_result["series"][0]["values"]))
        ]
        print("Measurement series in {}: ".format(self.database))
        for series in self.series_list:
            print("\t", series)

    def select_series(self) -> None:
        user_input = input("Select series to apply spike filter:\n")
        if user_input in self.series_list:
            self.selected_series = user_input
        else:
            print("Try again!")
            self.select_series()

    def find_spikes(self) -> None:
        # Get data:
        data_result: Any = self.client.query(
            'SELECT * FROM "{}"'.format(self.selected_series)
        ).raw
        self.data[self.selected_series] = [
            data_result["series"][0]["values"][i][-1]
            for i in range(len(data_result["series"][0]["values"]))
        ]
        # Get timestaps:
        self.timestamps[self.selected_series] = [
            data_result["series"][0]["values"][i][0]
            for i in range(len(data_result["series"][0]["values"]))
        ]
        # Find spike indices:
        self.spike_indices[self.selected_series] = []
        for i in tqdm(range(1, len(self.data[self.selected_series]) - 1)):
            # Ignore current acquisition (= None):
            if all(self.data[self.selected_series][i - 1 : i + 2]):
                if self.is_spike(
                    self.data[self.selected_series][i],
                    self.data[self.selected_series][i - 1],
                    self.data[self.selected_series][i + 1],
                ):
                    self.spike_indices[self.selected_series].append(i)
        # Get timestamps at spike indices:
        self.spike_timestamps[self.selected_series] = []
        for i in range(len(self.spike_indices[self.selected_series])):
            self.spike_timestamps[self.selected_series].append(
                self.timestamps[self.selected_series][
                    self.spike_indices[self.selected_series][i]
                ]
            )
        # Convert spike timestamp to unix time:
        self.spike_utimestamps[self.selected_series] = []
        for i in range(len(self.spike_timestamps[self.selected_series])):
            spike_timestamp = (
                self.spike_timestamps[self.selected_series][i]
                .strip("Z")
                .replace("T", " ")
            )
            spike_datetimestamp = datetime.datetime.strptime(
                spike_timestamp, "%Y-%m-%d %H:%M:%S"
            ) + datetime.timedelta(hours=2)  # Before summer time +1; after +2h
            spike_utimestamp = time.mktime(spike_datetimestamp.timetuple())
            spike_utimestamp_str = str(spike_utimestamp)[:-2] + 9 * "0"
            self.spike_utimestamps[self.selected_series].append(spike_utimestamp_str)
        # Get total number of spikes:
        self.total_spikes[self.selected_series] = len(
            self.spike_utimestamps[self.selected_series]
        )
        # Print results:
        print(
            "Total spikes detected in {} with spike factor {}: {}".format(
                self.selected_series,
                self.spike_factor,
                self.total_spikes[self.selected_series],
            )
        )
        # If results, show detailed list:
        if self.total_spikes[self.selected_series]:
            show_timestamps = input("Show database entries for spikes? (y/n)" + "\n")
            if show_timestamps == "y":
                for i in range(len(self.spike_utimestamps[self.selected_series])):
                    print(
                        "Time Stamp: {} -- Unix Time Stamp: {} -- Value: {}".format(
                            self.spike_timestamps[self.selected_series][i],
                            self.spike_utimestamps[self.selected_series][i],
                            self.data[self.selected_series][
                                self.spike_indices[self.selected_series][i]
                            ],
                        )
                    )

    def delete_spikes(self) -> None:
        user_delete = input("Delete detected spikes? (y/n)\n")
        if user_delete == "y":
            for spike in self.spike_utimestamps[self.selected_series]:
                self.client.query(
                    'DELETE FROM "{}" WHERE time = {}'.format(
                        self.selected_series, spike
                    )
                )
            print("Spikes deleted!")
        elif user_delete != "y":
            print("No modification made.")


if __name__ == "__main__":
    db_spike_filter = DbSpikeFilter()
