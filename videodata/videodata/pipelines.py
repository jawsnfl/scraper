# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os

from scrapy.utils.serialize import ScrapyJSONEncoder

from videodata.items import VideoItem, CategoryItem


class PyVideoJsonWriterPipeline:
    def process_item(self, item, spider):
        if isinstance(item, CategoryItem):
            event_name = spider.slugify(item['title'])
            event_path = os.path.join(spider.settings['OUTPUT_DIR'], event_name)
            os.makedirs(event_path, exist_ok=True)
            category_json_path = os.path.join(event_path, 'category.json')
            with open(category_json_path, 'w') as fp:
                fp.write(ScrapyJSONEncoder().encode(item))

        elif isinstance(item, VideoItem):
            event_name = spider.slugify(item['category'])
            videos_path = os.path.join(spider.settings['OUTPUT_DIR'], event_name, 'videos')
            os.makedirs(videos_path, exist_ok=True)
            video_json_path = os.path.join(videos_path, '{}.json'.format(spider.slugify(item['title'])))
            with open(video_json_path, 'w') as fp:
                fp.write(ScrapyJSONEncoder().encode(item))

        return item
