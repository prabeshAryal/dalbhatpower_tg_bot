import subprocess
import string,random
import json, os

def extract_media_info(media_file_path, media_type):
    command = [
        'ffprobe', '-v', 'error', '-show_entries', f'stream=duration,width,height{",album" if media_type=="audio" else ""}', '-of', 'json', media_file_path
    ]
    try:
        ffprobe_output = subprocess.check_output(command).decode('utf-8')
        media_info = json.loads(ffprobe_output)['streams'][0]
        duration = media_info.get('duration')  # Get the 'duration' value or None
        
        dimensions = {}
        if 'width' in media_info and 'height' in media_info:
            dimensions['width'] = int(media_info['width'])
            dimensions['height'] = int(media_info['height'])
    except (subprocess.CalledProcessError, KeyError, IndexError):
        duration = None
        dimensions = {}
    
    # Cast 'duration' to integer if it's not None, otherwise set a default value of 0
    duration = int(float(duration)) if duration is not None else 0
    
    thumbnail_path = None
    if media_type == 'video':
        thumbnail_path = extract_video_thumbnail(media_file_path)
    
    return duration, dimensions, thumbnail_path



def extract_video_thumbnail(video_url):
# Use ffmpeg to extract video thumbnail
    thumbnail_filename = generate_random_string() + '.jpg'
    THUMBNAIL_DIR = os.path.join(os.getcwd(),'downloads')
    thumbnail_path = os.path.join(THUMBNAIL_DIR, thumbnail_filename)
    command = ['ffmpeg', '-i', video_url, '-ss', '00:00:01', '-vframes', '1', thumbnail_path, '-y']
    subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return thumbnail_path

def generate_random_string(length=10):
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for _ in range(length))