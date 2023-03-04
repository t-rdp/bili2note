#!/usr/bin/python3
# -*- coding: utf-8 -*-
from utils.feed_parser import FeedParaser
from utils.feed2note import Feed2Toot
from utils.get_config import GetConfig
import os

config = GetConfig()

if __name__ == '__main__':
  if config['PROXY']['ProxyOn'] == 'true':
    os.environ['HTTP_PROXY'] = config['PROXY']['HttpProxy']
    os.environ['HTTPS_PROXY'] = config['PROXY']['HttpsProxy']

  RSS_dict = FeedParaser(config['BILI']['BiliRss'])
  Feed2Toot(RSS_dict)
