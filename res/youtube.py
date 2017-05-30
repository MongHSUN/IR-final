#!/usr/bin/python
import webbrowser
import os
import sys
from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser

# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of
#   https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.

DEVELOPER_KEY = "AIzaSyAAWsdajiwk9v84_ZctzmFbqnmXADVTBxM"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

result_path='../data/result'
keyword_path='../data/query'

def time_search(keyword_path, videoid, song_path):
  keyword_list=[]
  key_count=0
  with open(keyword_path,'r', encoding='utf8') as keyword_f:
    for word in keyword_f:
      word=word.rstrip('\n')
      keyword_list.append(word)
      key_count = key_count+1
  #print ("%s" % keyword_list)
  with open(song_path,'r', encoding='big5') as song_f:
    find_word=0
    for line in song_f:
      #print("%s" % line)
      i=0
      while i < key_count:
        if keyword_list[i] in line:
          j=0
          for j in range(len(line)):
            if line.find("[", j) == -1:
              break
          sec=int(line[j+3:j+5])
          final_url=videoid+"&feature=youtu.be&t="+line[j+1]+"m"+str(sec)+"s"
          print ("%s" % final_url);
          webbrowser.open(final_url)
          find_word=1
          break
        i=i+1

      if find_word==1:
        break

  return

def check_title(title, query_list):
  if query_list[0] in title and query_list[1] in title:
    return 1
  else:
    song_count=0
    name_count=0
    #song name
    for word in query_list[1]:
      #singer name is english
      #if (word >= u'\u0041' and word <= u'\u005a')or(word >= u'\u0061' and word <= u'\u007a'):
      if word in title:
        song_count=song_count+1
   # print ("%d %d" % (song_count, len(query_list[1])))
    title_len=len(title)
    if 'music' in title:
      title_len=title_len-5
    elif 'mv' in title:
      title_len=title_len-2
    elif 'video' in title:
      title_len=title_len-5
    elif 'mp3' in title:
      title_len=title_len-3
    elif 'audio' in title:
      title_len=title_len-5
    if song_count/title_len<0.3:
      return 0
    #singer name
    for word in query_list[0]:
      if word in title:
        name_count=name_count+1
    #print ("%d %d" % (name_count, len(query_list[0])))
    if name_count/len(query_list[0])<0.5:
      return 0
  return 1

def youtube_search(options):
  youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)

  # Call the search.list method to retrieve results matching the specified
  # query term.
  search_response = youtube.search().list(
    q=options.q,
    part="id,snippet",
    maxResults=options.max_results
  ).execute()

  videos = []

  # Add each result to the appropriate list, and then display the lists of
  # matching videos, channels, and playlists.
  novideo='not found'
  for search_result in search_response.get("items", []):
    if search_result["id"]["kind"] == "youtube#video":
      if check_title(search_result["snippet"]["title"].lower(), options.q)==1:
        return search_result["id"]["videoId"]
      else:
        continue
      
  return novideo  

if __name__ == "__main__":
  #this is for PJ
  keyword_list=[]
  key_count=0
  with open(keyword_path,'r', encoding='utf8') as keyword_f:
    for word in keyword_f:
      word=word.rstrip('\n')
      keyword_list.append(word)
      key_count = key_count+1
  if ("National Taiwan" in keyword_list):
      webbrowser.open("https://youtu.be/Ev4pwFMaZQc?t=35s")
      sys.exit(0)
  #pj end
  statinfo = os.stat(result_path)
  if statinfo.st_size==0:
    webbrowser.open("https://www.youtube.com/watch?v=7g58WySGo7E")
  else:
    f = open(result_path,'r',encoding='utf8')

    #set argparse
    argparser.add_argument("--q", help="Search term", default='')
    argparser.add_argument("--max-results", help="Max results", default=25)
    argparser.add_argument("-t", action="store_true")

    args = argparser.parse_args()
    timeSearch = args.t
    #while loop until proper video is found
    find_song=0
    count=0
    while find_song==0 and count<10:
      search_var=f.readline()
      song_path=search_var.rstrip('\n')
      #get singer and song name
      #search_var is a list, search[0]=singer, search_var[1]=song name
      search_var=search_var.rstrip('.lrc\n')
      search_var=search_var.split('/')
      if len(search_var) > 2:
        length=len(search_var)
        search_var=search_var[length-2:length]

      #search by keyword
      args.q=search_var
      try:
        videoid=youtube_search(args)
        #check if video is found
        if videoid != "not found":
          videoid='https://www.youtube.com/watch?v='+videoid 
          find_song=1
          break

      except HttpError as e:
        print ("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))
 
    #get lrc time and combine url with time
    if find_song==1:
  
      #modify path for windows    
      #song_path=song_path.replace('/', '\\')
      if timeSearch:
        time_search(keyword_path, videoid, "../data/lrcc"+song_path)
      else:
        webbrowser.open(videoid)
    else:
      print("not found")
