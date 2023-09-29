import os, sys
import re
import time
import concurrent.futures
import keyboard

class FileTimes:
    def __init__(self, file_name, accessed_time):
        self.file_name = file_name
        self.accessed_time = accessed_time

def main_function():
    folder_path = os.getcwd()
    executable_name = GetFileNameOnly(os.path.basename(sys.argv[0]))
    extension = ".completed"
    #TODO: Below line will be commented in Production
    #folder_path = 'D:\\Pictures\\Trip to Australia'
    folder_iterator = GetFileTimesInFolder(folder_path, executable_name, extension)
    DiaplayFileName = folder_iterator[1]
    files_times = sorted(folder_iterator[0], key=lambda file_time: file_time.accessed_time, reverse=True)
    FileNamePart = FormatFileName(files_times[0].file_name);
    MinutesWatched = StartUserInputThreads("Minutes Watched? ", 0, 2)
    MinutesWatched = MinutesWatched if str(MinutesWatched).isnumeric() else 0
    FormattedTime = format_seconds(int(MinutesWatched))
    rename_file(folder_path, DiaplayFileName, FileNamePart+FormattedTime+extension)

def StartUserInputThreads(msg, defaultValue, sleepTime):
    keyboard.on_press(on_press)
    global UserInputEntered
    UserInputEntered = False
    with concurrent.futures.ThreadPoolExecutor() as executor:
        thread1 = executor.submit(GetUserInput, msg)
        executor.submit(CheckUserInput, sleepTime)
    UserInputResult = thread1.result()
    return defaultValue if not UserInputResult else UserInputResult

def FormatFileName(FileName):
    FileName = FileName.replace('-', '.')
    FileName = FileName.replace(' ', '.')
    string_list = FileName.split('.')
    ReturnName = string_list[0]
    if(len(string_list) > 1):
        ReturnName += string_list[1]
    regex_search = re.search(r"S\d{2}E\d{2}", FileName)
    FileNamePart = ReturnName if (not regex_search) else ReturnName+"-"+(regex_search).group()
    return FileNamePart

def GetFileTimesInFolder(folder_path, executable_name, extension):
    reference_file_name = ''
    my_dict = []
    for file in os.listdir(folder_path):
        IsMyExtension = True if file.endswith(extension) else False
        IsMyExecutable = True if file.startswith(executable_name) else False
        IsDirectory = True if os.path.isdir(os.path.join(folder_path, file)) else False
        if IsMyExtension:
            reference_file_name = file
        elif(not IsMyExecutable and not IsDirectory):
            my_dict.append(FileTimes(os.path.splitext(file)[0], os.path.getatime(os.path.join(folder_path, file))))
    FileName = "FileName"
    if(not my_dict):
        FileName = StartUserInputThreads("File Name to Be? ", FileName, 5)
        my_dict.append(FileTimes(FileName, 0));
    if(not reference_file_name):
        reference_file_name = createfile(folder_path, FileName+extension)
    return my_dict, reference_file_name

def createfile(folder_path, file_name):
    with open(os.path.join(folder_path, file_name), 'w') as f:
        return (os.path.basename(f.name))

def rename_file(folder_path, file, new_name):
    os.rename(os.path.join(folder_path, file), os.path.join(folder_path, new_name));

def GetFileNameOnly(FileName):
    last_dot_index = FileName.rfind(".")
    return FileName[:last_dot_index]

def format_seconds(total_minutes):
    if(total_minutes == 0):
        return "-viewed"
    hours = total_minutes // 60
    minutes = (total_minutes % 60)
    return f"-{hours:02d}h{minutes:02d}m"

def GetUserInput(msg):
    return input(msg)

def CheckUserInput(sleepTime):
    time.sleep(sleepTime)
    global UserInputEntered
    if(not UserInputEntered):
        keyboard.press_and_release('enter')
    UserInputEntered = False

def on_press(event):
    global UserInputEntered
    UserInputEntered = True

if __name__ == '__main__':
  main_function()
