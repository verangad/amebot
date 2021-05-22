import discord
from discord.ext.commands import Bot
from discord.ext import commands
from discord import Game
import nacl
import random

import youtube_dl

from queue import Queue

from youtubesearchpython.__future__ import VideosSearch



import os



PREFIX = '*'
YTLINK = "youtube.com"


songQueue = Queue(maxsize = 0)

isPlaying = False



ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}   


bot = commands.Bot(command_prefix='*')

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))



    
    


@bot.command()
async def play(ameBot, url):

  global curr_voice
  global isPlaying
  global songQueue


  voice_state = ameBot.author.voice

  if(url is None):
    return await ameBot.send('No url was given')

    
  if(voice_state is None):
        
    return await ameBot.send('You need to be in a voice channel to use this command')

  elif(not is_connected(ameBot)):
    curr_voice = await voice_state.channel.connect()
 

  guild = ameBot.message.guild

  with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    file = ydl.extract_info(url, download=True)
    path = str(file['title']) + "-" + str(file['id'] + ".mp3")

    if(not isPlaying):

      curr_voice.play(discord.FFmpegPCMAudio(path), after=lambda x: endSong(guild, path,curr_voice))
      curr_voice.source = discord.PCMVolumeTransformer(curr_voice.source, 1)
      isPlaying = True
      

    else:
      songQueue.put(path)

  await ameBot.send(f'**Music: **{url}')

@bot.command()
async def pause(ameBot):
  curr_voice.pause()
  await ameBot.send("Song Paused")

@bot.command()
async def resume(ameBot):
  curr_voice.resume()
  await ameBot.send("Song Resumed")


@bot.command()
async def stop(ameBot):
  
  curr_voice.stop()

  await ameBot.send("Song stopped")


@bot.command()
async def skip(ameBot):
  curr_voice.stop()

  await ameBot.send("Song skipped")


def endSong(guild, path, voice_client):

  global isPlaying
  global songQueue

  if(songQueue.qsize() > 0):
    curr_voice.play(discord.FFmpegPCMAudio(songQueue.get()), after=lambda x: endSong(guild, path,curr_voice))
    curr_voice.source = discord.PCMVolumeTransformer(curr_voice.source, 1)

  else:
    isPlaying = False
    
  os.remove(path)  
 

@bot.command()
async def leave(ameBot):
  
  await curr_voice.disconnect()

  await ameBot.send("Bot left the voice channel")


def is_connected(ameBot):
  voice_client = discord.utils.get(ameBot.bot.voice_clients, guild=ameBot.guild)
  return voice_client and voice_client.is_connected()



@bot.command()
async def test(ameBot, arg):

  test_service = build('books', 'v1', developerKey=os.getenv('YTAPI'))

    
  await ameBot.send("HELLO")




  

bot.run(os.getenv('TOKEN'))