% EEGLAB history file generated on the 03-Aug-2014
% ------------------------------------------------
[ALLEEG EEG CURRENTSET ALLCOM] = eeglab;

path  = 'G:\Claire Project\Data\NetStation Files\rawfiles';

files = dir(path);

for i = 1:length(files)
    if length(files(i).name) < 6
        continue
    end
    file_path = [path '\\' files(i).name];
    files(i).name

    EEG = pop_readegi(file_path, [],[],'auto');
    [ALLEEG EEG CURRENTSET] = pop_newset(ALLEEG, EEG, 0,'gui','off'); 

    outputfile = fopen([files(i).name '_EEG_events.txt'], 'w');
    for i = 1:length(EEG.event)
        fprintf(outputfile, [EEG.event(i).type '\t' num2str(EEG.event(i).latency) '\n']) ;
    end
    fclose(outputfile);

end
 eeglab redraw;