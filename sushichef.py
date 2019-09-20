#!/usr/bin/env python
import os
import sys
sys.path.append(os.getcwd()) # Handle relative imports
import requests
from le_utils.constants import licenses
import logging
from ricecooker.chefs import SushiChef
from ricecooker.classes.nodes import TopicNode
import index
from foundry import foundry
import foundry as F

F.bits.BAD_TYPES = ["text/plain"]
LOGGER = logging.getLogger()

foundry.copyright_holder="Global African Storybooks Project"

def storybook_xpath(xpath):
    drop_list = [
            "//header[@class='navbar']",
            "//a[text()='Back to stories list']",
            "//select",
            "//div[text()='Download PDF']",
            "//div[@id='colophon']/div[2]"
            ]

    icon_list = {
            "arrow-down": "V",
            "volume-up": ">)))",
            }

    for drop in drop_list:
        try:
            bads = xpath.xpath(drop)
        except:
            print (drop)
            raise
        for bad in bads:
            bad.getparent().remove(bad)

    for icon, replacement in icon_list.items():
        tags = xpath.xpath(f"//i[@class='icon-{icon}']")
        for tag in tags:
            tag.name="span"
            print (dir(tag))
            tag.attrib['class'] = ""
            tag.text=replacement
    return xpath

class MathplanetChef(SushiChef):
    channel_info = {
        'CHANNEL_SOURCE_DOMAIN': 'global-asp.github.io', # who is providing the content (e.g. learningequality.org)
        'CHANNEL_SOURCE_ID': 'storybooks-minnesota',         # channel's unique id
        'CHANNEL_TITLE': 'Storybooks Minnesota',
        'CHANNEL_LANGUAGE': 'en',                          # Use language codes from le_utils
        'CHANNEL_THUMBNAIL': 'sbmn_logo.jpg',
        'CHANNEL_DESCRIPTION': 'Set of the 40 most popular African Storybooks translated into various languages, leveled to specific literacy levels, with read-aloud audio. An initiative of the open-source Storybooks Minnesota project.'
    }

    def construct_channel(self, **kwargs):
        channel = self.get_channel(**kwargs)
        for lang_code, lang_name in index.languages.items():
            lang_node = TopicNode(lang_code, lang_name)
            lang_node.language = lang_code
            channel.add_child(lang_node)
            for level in range(1,5+1):
                level_node = TopicNode(lang_code+str(level), "Level "+str(level))
                lang_node.add_child(level_node)
                urls = index.get_lang_level(lang_code, level)
                for url in urls:
                    f = foundry.Foundry(url, storybook_xpath, owndomain=False)
                    node = f.node()
                    node.language = lang_code
                    level_node.add_child(node)
                    return channel
        return channel


if __name__ == '__main__':
    """
    Set the environment var `CONTENT_CURATION_TOKEN` (or `KOLIBRI_STUDIO_TOKEN`)
    to your Kolibri Studio token, then call this script using:
        python souschef.py  -v --reset
    """
    mychef = MathplanetChef()
    if 'KOLIBRI_STUDIO_TOKEN' in os.environ:
        os.environ['CONTENT_CURATION_TOKEN'] = os.environ['KOLIBRI_STUDIO_TOKEN']
    mychef.main()
