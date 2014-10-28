'''
    Open EEG events files and ET event files per participant. Counts the number of events and compare to find mismatches
'''

import numpy as np
from open_find_write import find_files, write_line
import os
import math


def unique_values(seq):
    seen = set()
    seen_add = seen.add
    return [ x for x in seq if not (x in seen or seen_add(x))]


def count_until(list, last_value):
    count = 0
    for item in list:
        count += 1
        if item == last_value:
            return count
    return -1


def calculate_condition(participant):
    sequence = float(participant[1:]) - (math.floor((float(participant[1:])-1)/4) * 4)
    if sequence <= 2:
        return 0
    else:
        return 1

general_path = 'C:\GC data\Participant_data'
#participants = os.listdir(general_path)
p_without_problems = []
p_with_problem = []

participants = ['P6']
f1 = open('Events_to_delete.txt', 'w')
for participant in participants:
    #try:
        ''' Participant info'''
        print participant
        part_path = general_path + os.sep + participant
        f = open(part_path + os.sep + participant + '_new_eeg_video_events.txt', 'w')


        #Calculate A or B sequence
        cond = calculate_condition(participant)
        if cond:
            print 'Condition B'
        else:
            print 'Condition A'

        ''' Load Files '''
        #EEG events
        eeg_events_path = part_path + os.sep + find_files(part_path, 'CM_', '.txt')[0]
        eeg_all_events = np.loadtxt(eeg_events_path, dtype=np.dtype([('event', (np.str, 20)), ('timestamp', np.int)]))
        eeg_events = []
        eeg_times = []
        for event in eeg_all_events:
            if event['event'].startswith('v'):
                eeg_events.append(event['event'])
                eeg_times.append(event['timestamp'])
        #et events
        et_events_path = part_path + os.sep + find_files(part_path, 'onset_video', 'txt')[0]
        et_events = np.loadtxt(et_events_path, dtype=np.dtype([('video', np.float_), ('timestamp', np.float_)]))

        ''' split events in videos '''
        #Videos order
        video_order = unique_values(et_events['video'])
        #ET events split
        et_events_split = []
        for video in video_order:
            et_events_split.append([x['timestamp'] for x in et_events if x['video'] == video])

        #EEG events split
        final_index = 0
        eeg_events_split = []
        eeg_times_split = []
        for j in range(len(video_order)):
            initial_index = final_index
            eeg_count = count_until(eeg_events[initial_index:], 'vend'  )
            final_index = initial_index + eeg_count
            if video_order[j] == 1:
                eeg_count = count_until(eeg_events[final_index:], 'vend')
                final_index += eeg_count
            eeg_events_split.append(eeg_events[initial_index:final_index])
            eeg_times_split.append(eeg_times[initial_index:final_index])


        ''' find the extra events on eeg recording
            delete them from the events and report the number and time of the extra events per video'''
        eeg_extra_events = [0]*len(video_order)
        eeg_final_events = []
        eeg_final_times = []
        for order, video in enumerate(video_order):
            group_started = 0
            count = 0
            starting_event = -1
            ev = [eeg_events_split[order][0]]
            tm = [eeg_times_split[order][0]]
            for i in range(1, len(eeg_events_split[order])):
                if eeg_times_split[order][i] - eeg_times_split[order][i-1] < 75:
                    if not group_started:
                        time_sec = (eeg_times_split[order][i-1]/float(500)) / 60
                        time_starts = int(time_sec) + ((time_sec - int(time_sec))*0.6)
                        group_started = 1
                        starting_event = i
                        ev.pop(-1)
                        tm.pop(-1)
                    count += 1
                elif group_started:
                    eeg_extra_events[order] = [starting_event, i, count, time_starts]
                    group_started = 0
                    ev.append(eeg_events_split[order][i])
                    tm.append(eeg_times_split[order][i])
                else:
                    ev.append(eeg_events_split[order][i])
                    tm.append(eeg_times_split[order][i])
            eeg_final_events.append(ev)
            eeg_final_times.append(tm)
            #print info about extra events: video, time starts and number of events
            if eeg_extra_events[order]:
                print 'extra events in video', int(video), ':', eeg_extra_events[order][2], 'events starting at', eeg_extra_events[order][0]
                f1.write(str(participant) + '\t' + 'extra events in video' + str(video) + ':' + str(eeg_extra_events[order][2]) + '\t' + 'events starting at' + str(eeg_extra_events[order][0]) + '\n')

        #Save the final eeg events into a txt file
        for i, v in enumerate(video_order):
            for j, event in enumerate(eeg_final_events[i]):
                time_sec = (eeg_final_times[i][j]/float(500)) / 60
                write_line(f, [v, event, int(time_sec) + ((time_sec - int(time_sec))*0.6), eeg_final_times[i][j]/float(500)])
        f.close()
        '''compare lengths and events of et and eeg events and report possible mistakes'''
        problem = 0
        for i in range(0, len(video_order)):
            if len(eeg_final_events[i]) != len(et_events_split[i]):
                print 'Video:', video_order[i], 'Number of events in et -', len(et_events_split[i]), 'Number of events in eeg -', len(eeg_final_events[i])
                problem = 1


        if not problem:
            print 'All the lengths are ok'

        #import pdb; pdb.set_trace()



'''
        #Store only the events related to the videos
        eeg_video_events = []
        eeg_video_events_time = []
        eeg_wrong_index = []
        eeg_final_events = []




        for event in eeg_final_events:
            eeg_video_events.append(event[0])

        print participant
        if eeg_wrong_index:
            print 'eeg events to delete:', len(eeg_wrong_index), 'starting at: ', eeg_wrong_index[0][2]

        else:
            print 'no eeg problems'
        eeg_video_events_time.pop()





        if cond == 0:
            events_number = [('v1A', 33), ('v2A', 30), ('v3A', 27), ('v4A', 17)]
        else:
            events_number = [('v1B', 33), ('v2B', 29), ('v3B', 25), ('v4B', 20)]
        #count number of event in et data,
        #ET:
        eeg_ev_number = 0
        et_ev_number = [(1, len([i for i in et_events['video'] if i == 1])), (2, len([i for i in et_events['video'] if i == 2])),
                        (3, len([i for i in et_events['video'] if i == 3])), (4, len([i for i in et_events['video'] if i == 4]))]




        #EEG video time difference
        #ET Video time difference
        videos_times = []
        for i in range(1, 5):
            times = [j[1] for j in et_events if j[0] == i] #Select the times that correspond to the video
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





        #Report if there is a problem with the subject:
        issue = 0

        for i in range(len(video_order)):
            if eeg_ev_number[i][1] != events_number[i][1]:
                print 'difference in eeg, video', i+1, 'EEG events:', eeg_ev_number[i][1], 'should be:', events_number[i][1]
                issue = 1
            if et_ev_number[i][1] != events_number[i][1]:
                print 'difference in et', i+1, 'et events:', eeg_ev_number[i][1], 'should be:', events_number[i][1]
                issue = 1
        if not issue:
            print 'no problems'
            p_without_problems.append(participant)
    #except:
    #    print 'problem with participant', participant
    #    p_with_problem.append(participant)
    #    continue

'''
'''
print participant
print 'condition', cond[:4]
print 'number of events', events_number

print 'eye tracking events:', et_ev_number
print 'eeg events', eeg_ev_number
'''









