fixing_onset_times
==================
There was a bug on the Matlab script during the learning phase (videos). If the pause or attention grabber button was pressed during this phase, whenever the video was resumed the ET events were completely substitute with the wrong times and more triggers than necessary were sent to NetStation.
The problem was solved offline in the files that had this problem in the following way:
•	report_videos_with_problems.py detected the videos that had the issue described with the ET onset video file.
o	This script generated a new video onset file to match the GSA format which removed the extra markers due to the beginning and end of the video. The new onset video files are called onset_video_PX.txt
o	participant_video_info.txt was created as a summary of the videos with some timing problem
•	save_EEG_events.m saved the EEG events from .raw files in a txt file containing the event name and time
•	check_number_events_eeg_et.py detected in the corrupted files the extra EEG events and a mismatch in the number of events between EEG and eye tracking (due to this problem)
With this information, each ET file was corrected manually using excel and the EEG onset times.
All the extra EEG events were marked but could not be removed because NetStation files didn’t allow to edit the event data. The events can be removed manually as invalid trials after data segmentation.
•	Fixing_sumary_def.xlsx contains the summary of all the changes made in every file, EEG and ET onset times. This info is useful to remove the extra EEG events during analysis and to keep track of the changes made.
