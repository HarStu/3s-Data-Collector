"""
Entry point for 3s Data Collector

TODO:
    tasks in replayscraper.py and replayfetcher.py
"""
import sys
import json
import os
import subprocess

import replayfetcher
import replayscraper


challenge_id = None

def main():
    # fetcher = replayfetcher.Replayfetcher("../data/output.json")
    # games = fetcher.get_username_replays("TheLetterH")
    # fetcher.save_games_to_test_json(games)

    scraper = replayscraper.Replayscraper("../data/test.json")
    scraper.scrape_replay("1649265467782-9148")
    
main()