import csv
import numpy as np
import os
import math


def open_csv(path, delim = '\t', skip = 1):
    output = []
    with open(path, 'rb') as csv_file:
        f = csv.reader(csv_file, delimiter = delim)
        line_number = 1
        for row in f:
            if line_number > skip: #skip headers
                output.append(map(float,row))
            line_number += 1

    return np.asarray(output)

def write_line(file,line):
    for item in line:
        file.write(str(item) + "\t")
    file.write('\n')
    return


def as_string(list):
    return [str(i) for i in list]


def save_txt(name, data, header=0):
    f = open(name+'.txt', 'w')
    if header:
        write_line(f, header)
    for line in data:
        write_line(f, as_string(line))
    f.close()


def modify_times(path):
    ovf = open_csv(path)

    #Delete two first rows of each video as they are repeated:
    next = 0
    onset_video_file = np.zeros(shape=(1, 2))

    for line in ovf:
        if line[0] and not next:
            onset_video_file = np.vstack((onset_video_file, line))
        else:
            if next:
                next = 0
            else:
                next = 1

    output = np.delete(onset_video_file, 0, 0) #Delete first rows with zeros
    return output
#Load video coding: 4 videos A and B versions
video_codes = open_csv('event_delays_1_to_4_A_and_B.csv', ';', 0)
general_path = 'G:\\Claire Project\\Data\\Participants\\'
participants = os.listdir(general_path)

for participant in participants:
    participant_number = str(participant)
    print 'Participant: ' + participant_number[1:]
    participant_path = participant_number + '\\'
    #Open onset video files
    for file in os.listdir(general_path + participant_path):
        if file.startswith('onset_video_file'):
            onset_video_file_path = general_path + participant_path + file

    onset_video_file = modify_times(onset_video_file_path)
    #Save new file
    save_txt(general_path + participant_path + 'onset_video_' + participant_number, onset_video_file)

    #Calculate A or B sequence
    sequence = float(participant_number[1:]) - (math.floor((float(participant_number[1:])-1)/4) * 4)
    if sequence <= 2: cond = 0
    else: cond = 4

    videos_times = []
    for i in range(1, 5):
        times = [j[1] for j in onset_video_file if j[0] == i] #Select the times that correspond to the video
        video = []
        for j in range(1, len(times)):
            video.append(times[j] - times[j-1]) #time difference (time between events)
        videos_times.append(video) #List containing 4 list, one per video
    for i, video_times_exp in enumerate(videos_times):
        video_times_or = video_codes[:len(video_times_exp), i+cond]

        errors = [x for x, j in enumerate(video_times_exp) if abs(video_times_exp[x]-video_times_or[x]) > 0.1]
        if errors:
            print 'video:'+str(i+1)
            print errors






