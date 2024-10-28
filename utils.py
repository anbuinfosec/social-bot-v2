# coding=utf-8
#!/bin/python3
#############################$##############
# PYTHON SOCIAL MEDIA VIDEO DOWNLOADER BOT #
#          BOT VERSION: 1.0.2              #
#  AUTHOR : MOHAMMAD ALAMIN (anbuinfosec)  #
#  GET APIKEY : https://anbuinfosec.xyz    #
#           COPYRIGHT : anbuinfosec        #
############################################
import os
import aiohttp
import re
import asyncio
import uuid
import aiofiles
from func import convert_bytes
import mimetypes
import requests
from urllib.parse import quote
from dotenv import load_dotenv

load_dotenv()

def get_extension_from_mime_type(mime_type):
    '''
    Check content ext from type
    '''
    extension = mimetypes.guess_extension(mime_type)
    return extension or "Unknown"


async def check_tmp():
    '''
    A dunction for check tmp folder exist or not
    If tmp folder not exist auto create a tmp folder
    '''
    tmp_folder = await asyncio.to_thread(os.path.join, os.getcwd(), 'tmp')
    if not os.path.exists(tmp_folder):
        await asyncio.to_thread(os.makedirs, tmp_folder)


def random_name(content_type):
    '''
    Generate random name for save the video
    '''
    random_id = str(uuid.uuid4())
    return f'{random_id}{content_type}'


def check_downloader(url):
    '''
    A function for checking a valid url.
    '''
    facebook_regex = r'(https?://)?(www\.)?(facebook\.com|fb\.watch|fb\.com|m\.facebook\.com|web\.facebook\.com)/.+$'
    youtube_regex = r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/.+$'
    terabox_regex = r'https?://(www\.)?(teraboxapp\.com|terabox\.com|4funbox\.com)/s/.+$'
    instagram_regex = r'(https?://)?(www\.)?instagram\.com/(p|reel|tv)/.+'
    twitter_regex = r'https?:\/\/(x|twitter)\.com\/.*'
    tiktok_regex = r'https?:\/\/tiktok\.com\/.*'

    if re.match(facebook_regex, url):
        return "facebook"
    elif re.match(youtube_regex, url):
        return "youtube"
    elif re.match(terabox_regex, url):
        return "terabox"
    elif re.match(instagram_regex, url):
        return "instagram"
    elif re.match(twitter_regex, url):
        return "twitter"
    elif re.match(tiktok_regex, url):
        return "tiktok"
    else:
        return False


async def downloadFromUrl(url, destination_folder='tmp'):
    '''
    Download file from url on tmp folder
    '''
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                c_type = str(response.headers.get('Content-Type'))
                content_type = get_extension_from_mime_type(c_type)
                size = (convert_bytes(int(response.headers.get('Content-Length'))))
                await check_tmp()
                
                if c_type and c_type.startswith('image'):
                    file_type = 'photo'
                elif c_type and c_type.startswith('video'):
                    file_type = 'video'
                else:
                    file_type = 'doc'
                
                FileName = random_name(content_type)
                file_path = os.path.join(destination_folder, FileName)
                async with aiofiles.open(file_path, "wb") as f:
                    await f.write(await response.read())
                    return  file_path, size, file_type
            else:
                return url


async def get_video_download_info(video_url, downloader, apikey):
    f'''
    Geting the download url from user provided url.
    For apikey create account on : {HOST}
    '''
    HOST = os.getenv("HOST")
    if HOST == "":
        sys.exit ("[-] Host url not found.")
    base_url = f'{HOST}/api/downloader/{downloader}'
    query_params = {'apikey': apikey, 'url': video_url, 'pwd': ''}
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(base_url, params=query_params) as response:
                response.raise_for_status()
                result = await response.json()
                return result
    except aiohttp.ClientResponseError as e:
        return {"status": False, "message": f"Error: {e}"}
    
def urlShort (url):
    req = requests.get(f'https://tinyurl.com/api-create.php?url={quote(url)}')
    if req.status_code == 200:
        return req.text
    else:
        False