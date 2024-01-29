import os
from openai import OpenAI
from pydub import AudioSegment
import webvtt
import re
from datetime import datetime, timedelta



current_script_path = os.path.dirname(os.path.abspath(__file__))
#OpenAIClient
client = OpenAI(api_key='##################')

#Split mp3 and call whisper to get vtt
audio_file= open(current_script_path + "/temp.mp3", "rb")
song = AudioSegment.from_mp3(current_script_path + "/temp.mp3")
ten_minutes = 10 * 60 * 1000

total = len(song)
num_segments = total // ten_minutes

f = open(current_script_path + "/temp.vtt", "a")
for i in range(num_segments):
    start_time = i * ten_minutes 
    end_time = (i + 1) * ten_minutes

    # Extract the segment
    segment = song[start_time:end_time]

    # Save the segment to a new file
    output_file = os.path.join(current_script_path, f"temp_segment_{i + 1}.mp3") 

    segment.export(output_file, format="mp3")
    audio_file= open(output_file, "rb")
    transcript = client.audio.transcriptions.create(
              model="whisper-1", 
                file=audio_file,
                response_format="vtt"
                )
    f.write(transcript)

#Process final segment
segment_final = song[num_segments * ten_minutes:]
output_file = os.path.join(current_script_path , f"temp_segment_{num_segments + 1}.mp3") 
segment_final.export(output_file, format="mp3")
audio_file= open(output_file, "rb")
transcript = client.audio.transcriptions.create(
          model="whisper-1", 
            file=audio_file,
            response_format="vtt"
            )
f.write(transcript)

f.close()


#Compose vtt file
segNum = -1

def add_10_minutes_to_range(time_range , segNum):
    print(time_range)
    start_str, end_str = time_range.split(" --> ")
    time_format = "%H:%M:%S.%f"

    start_time = datetime.strptime(start_str, time_format)
    end_time = datetime.strptime(end_str, time_format)

    new_start_time = start_time + timedelta(minutes=(10*segNum))
    new_end_time = end_time + timedelta(minutes=(10*segNum))

    return new_start_time.strftime(time_format)[:-3] + " --> " + new_end_time.strftime(time_format)[:-3]

file_path = current_script_path + '/temp.vtt'  # Replace with the path to your text file

total_time = timedelta()
regex = re.compile("-->")
f = open(current_script_path + "/temp_compose.vtt", "a")
f.write('WEBVTT\n')
with open(file_path, 'r') as file:
    for line in file:
        if line.strip() == 'WEBVTT':
            segNum += 1
            continue

        if  '-->' in line:    
            print(regex.search(line).group())
            processed_line = add_10_minutes_to_range(line.strip() , segNum)
            print(processed_line)
            f.write(processed_line + '\n')
        else:
            f.write(line)

f.close()
