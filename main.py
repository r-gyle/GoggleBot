import discord
import os
import requests
#import bs4
import urllib
#import pandas as pd
#from requests_html import HTML
from requests_html import HTMLSession

client = discord.Client()

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if message.content.startswith('g-'):
    text = message.content
    text = text.replace('g-','')
    links = search(text)
    await message.channel.send(links[0])

def get_source(url):
    try:
        session = HTMLSession()
        response = session.get(url)
        return response

    except requests.exceptions.RequestException as e:
        print(e)

def search(input):

    input = urllib.parse.quote_plus(input)
    response = get_source("https://www.google.com/search?q=" + input)
    links = list(response.html.absolute_links)
    google_domains = ("https://www.google.", 
                      "https://google.", 
                      "https://webcache.googleusercontent.", 
                      "http://webcache.googleusercontent.", 
                      "https://policies.google.",
                      "https://support.google.",
                      "https://maps.google.")
    for url in links[:]:
        if url.startswith(google_domains):
            links.remove(url)
    return links

client.run(os.environ['TOKEN'])