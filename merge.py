from tkinter import *
from tkinter import filedialog
from winsound import *
import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import os

root = Tk()
root.geometry('600x500')
root.title('Translator')

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')

engine.setProperty('voice',voices[0].id)
def speak(audio):
     engine.say(audio)
     engine.runAndWait()

def wishme():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour <12:
        speak("Good morning")
    elif hour>=12 and hour<18:
        speak("Good afternoon")
    else:
        speak("Good Evening!")
    speak("I am your assistant, how may i help you.")   


# menu
def newfile():
    pass


def savefile():
    pass


mainmenu = Menu(root)
m1 = Menu(mainmenu, tearoff=0, bg='gray30', fg='white')
m1.add_command(label='New', command=newfile)
m1.add_separator()
m1.add_command(label='Save', command=savefile)
m1.add_command(label='SaveAs', command=savefile)
root.config(bg='gray20', menu=mainmenu)
mainmenu.add_cascade(label='File', menu=m1)

def runfile():
    pass


m2 = Menu(mainmenu, tearoff=0, bg='gray30', fg='white')
m2.add_command(label='Run', command=runfile)
root.config(menu=mainmenu)
mainmenu.add_cascade(label='Run', menu=m2)


def help_():
    pass


m3 = Menu(mainmenu, tearoff=0, bg='gray30', fg='white')
m3.add_command(label='Help', command=help_)
root.config(menu=mainmenu)
mainmenu.add_cascade(label='Help', menu=m3)

m4 = Menu(mainmenu, tearoff=0, bg='gray30', fg='white')
m4.add_command(label='Quit', command=root.quit)
root.config(menu=mainmenu)
mainmenu.add_cascade(label='Exit', menu=m4)

# frames
frame1 = Frame(root, bg='gray18', relief=SUNKEN, borderwidth=4)
frame1.pack(side='top', anchor='w')

# label
Label(root, text='Enter name of file:', fg='white', padx=7, pady=8, bg='gray20', font=('times', 12)).pack(anchor='w')
# filename
in_put = Entry(root, bg='gray30', width=40)
in_put.pack(padx=7, pady=5, anchor='w')


def save():
    global filename
    filename = in_put.get()


Button(root, text='Enter', padx=4, bg='gray30', command=save).pack(anchor='w', padx=7, pady=5)


scrollbar = Scrollbar(root)
scrollbar.pack(side=RIGHT, fill=Y)
frame2 = Frame(root, bg='gray18', relief=SUNKEN, borderwidth=4)
frame2.pack(anchor='s', fill=X)
scrollbar.config(command=frame2)


def clear():
    output1.delete(1.0, END)


def opendialogue():
    global filepath
    filepath = filedialog.askopenfilename(initialdir="C:\\")
    print('\t\t\t\t', filepath)
    output1.insert(END, f"Selected file path: {filepath}\n")


def play():
    return PlaySound('', SND_FILENAME)


# status bar
statusvar = StringVar()
statusvar.set('No progress')
sbar = Label(root, textvariable=statusvar, relief=SUNKEN, anchor='w')
sbar.pack(side='bottom', fill=X)


def translate():
    try:
        from ibm_watson import SpeechToTextV1
        from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

        apikey = '_ewufalZkNbx_n7OpZ5yjZTzosvLrvL2s02zL2j3YPZU'
        url = 'https://api.kr-seo.speech-to-text.watson.cloud.ibm.com/instances/a9f9774d-a848-44bb-91e7-5b01c259f741'

        authenticator = IAMAuthenticator(apikey)
        stt = SpeechToTextV1(authenticator=authenticator)
        stt.set_service_url(url)

        import os
        import glob
        import subprocess

        speak("transcription in process, please wait")
        lst = glob.glob(filepath)
        print(lst)
        # mp4 to mp3
        for file in lst:
            # enter the name of file at 'file name'
            os.system(f""""ffmpeg -i {filepath} {filename + '.mp3'}""")

        # mp3 to wav
        for file in lst:
            os.system(f"""ffmpeg -i {filename + '.mp3'} -acodec pcm_u8 -ar 22050 {filename + '.wav'}""")
        # statusvar.set('Done')

        command = f'ffmpeg -i {filename}.wav -vn -ar 44100 -ac 2 -b:a 192k _{filename}.mp3'
        subprocess.call(command, shell=True)
        command = f'ffmpeg -i _{filename}.mp3 -f segment -segment_time 360 -c copy %03d{filename}.mp3'
        subprocess.call(command, shell=True)

        files = []
        for filenames in os.listdir('.'):
            if filenames.endswith(f"0{filename}.mp3") and filenames !=f'_{filename}.mp3':
                files.append(filenames)
        files.sort()
        print("done")
        print(files)

         
        results = []
        for filenames in files:
            with open(filenames, 'rb') as f:
                res = stt.recognize(audio=f, content_type='audio/mp3', model='en-AU_NarrowbandModel', continuous=True, \
                                inactivity_timeout=360).get_result()
                results.append(res)
        text = []
        for file in results:
            for result in file['results']:
                text.append(result['alternatives'][0]['transcript'].rstrip() + '.\n')
        print(text)
        with open(f'{filename}.txt', 'w') as out:
            out.writelines(text)
        

        # import speech_recognition as sr
        # from pydub import AudioSegment
        # c = 0
        # a = 0
        # sound = AudioSegment.from_file(f'{filename}.wav')
        # for i in range(0, len(sound), 10000):
        #     if i == 0:
        #         pass
        #     else:
        #         print(i)
        #         c += 1
        #         part = sound[a:i]
        #         part.export(f'C:/Users/astha/PycharmProjects/miniproject/{filename}{c}.wav', format='wav')

        #         file_name = f'C:/Users/astha/PycharmProjects/miniproject/{filename}{c}.wav'
        #         r = sr.Recognizer()
        #         a = i
        #         with sr.AudioFile(file_name) as source:
        #             # audio = r.record(source, offset=4, duration=3)
        #             audio_data = r.record(source)
        #             text = r.recognize_google(audio_data, language='en-IN')
        #             f = open(f'{filename}.txt', 'a')
        #             f.write(f'{text}\n')
        #             print(text)
                    # output1.insert(END,text)

        def text_to_braille(inp):
            """This function converts text to braille symbols."""
            asciicodes = [' ', '!', '"', '#', '$', '%', '&', '', '(', ')', '*', '+', ',', '-', '.', '/',
                          '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ':', ';', '<', '=', '>', '?', '@',
                          'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q',
                          'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '[', '\\', ']', '^', '_']

            # Braille symbols
            brailles = ['⠀', '⠮', '⠐', '⠼', '⠫', '⠩', '⠯', '⠄', '⠷', '⠾', '⠡', '⠬', '⠠', '⠤', '⠨', '⠌', '⠴', '⠂', '⠆',
                        '⠒',
                        '⠲',
                        '⠢',
                        '⠖', '⠶', '⠦', '⠔', '⠱', '⠰', '⠣', '⠿', '⠜', '⠹', '⠈', '⠁', '⠃', '⠉', '⠙', '⠑', '⠋', '⠛', '⠓',
                        '⠊',
                        '⠚',
                        '⠅',
                        '⠇', '⠍', '⠝', '⠕', '⠏', '⠟', '⠗', '⠎', '⠞', '⠥', '⠧', '⠺', '⠭', '⠽', '⠵', '⠪', '⠳', '⠻', '⠘',
                        '⠸']
            content = ''
            for i in inp():
                for j in range(len(asciicodes)):
                    if i == asciicodes[j]:
                        content += brailles[j]
                        # f= open('braille.txt','a')
                        # f.write(brailles[j])
            return content

        ##############################################################

        # print(text_to_braille.__doc__)
        f = open(f'{filename}.txt', 'r')
        a = text_to_braille(f.read)
        output1.insert(END, a)
        speak("transcription complete")


    except:
         error_ = "\nError Occured: Check internet connection or try different file."
         output1.insert(END, error_)
         speak("an error occured,Check internet connection, or try a different file.")

    finally:
         statusvar.set('Complete..........')



def real_time():
    try:
        def text_to_braille(inp):
            """This function converts text to braille symbols."""
            asciicodes = [' ', '!', '"', '#', '$', '%', '&', '', '(', ')', '*', '+', ',', '-', '.', '/',
                          '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ':', ';', '<', '=', '>', '?', '@',
                          'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q',
                          'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '[', '\\', ']', '^', '_']

            # Braille symbols
            brailles = ['⠀', '⠮', '⠐', '⠼', '⠫', '⠩', '⠯', '⠄', '⠷', '⠾', '⠡', '⠬', '⠠', '⠤', '⠨', '⠌', '⠴', '⠂', '⠆', '⠒',
                        '⠲',
                        '⠢',
                        '⠖', '⠶', '⠦', '⠔', '⠱', '⠰', '⠣', '⠿', '⠜', '⠹', '⠈', '⠁', '⠃', '⠉', '⠙', '⠑', '⠋', '⠛', '⠓', '⠊',
                        '⠚',
                        '⠅',
                        '⠇', '⠍', '⠝', '⠕', '⠏', '⠟', '⠗', '⠎', '⠞', '⠥', '⠧', '⠺', '⠭', '⠽', '⠵', '⠪', '⠳', '⠻', '⠘', '⠸']
            content = ''
            for i in inp:
                for j in range(len(asciicodes)):
                    if i == asciicodes[j]:
                        content += brailles[j]
                        # f= open('braille.txt','a')
                        # f.write(brailles[j])
            return content

        f = open(f'{filename}.txt', "r")
        inpu = f.read()
        val = text_to_braille(inpu)
        print(val)
        output1.insert(END, val)
        speak("Traslation Completed")

    except:
        error_ = "\nError Occured"
        output1.insert(END, error_)
        speak("an error occurred, try again")

    finally:
        statusvar.set('Traslation Completed')


def read():
    
        f = open(f'{filename}.txt', "r")
        # statusvar.set('No progress')
        inpu = f.read()
        speak(inpu)
def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening...')
        r.pause_threshold = 1
        r.energy_threshold=2000
        audio = r.record(source,duration=5)
    try:
        print("Recognising...")
        query = r.recognize_google(audio, language='en-in')
        print(f"user said: {query}\n")

    except Exception as e:
        print(e)

        print("Say that again please...")
        return "None"
    return query
def take_command():
    if 1:
        query=takecommand().lower()

        #task execution
        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia","")
            results = wikipedia.summary(query, sentences=10)
            speak("According to wikipedia")
            print(results)
            speak(results)
        elif "open youtube" in query:
            webbrowser.open("youtube.com")
        elif "open google" in query:
            webbrowser.open("google.com")
        elif "open netflix" in query:
            webbrowser.open("Netflix.com")
        elif "open spotify" in query:
            webbrowser.open("Spotify.com")
        elif "open teams" in query:
            webbrowser.open("https://teams.microsoft.com/_#/school/conversations/General?threadId=19:c13a45186c96469981d16fca432e98ca@thread.tacv2&ctx=channel")
        elif("open notes") in query:
            notes_dir='D:\\'
            notes = os.listdir(notes_dir)
            print(notes)
            os.startfile(os.path.join(notes_dir, notes[0]))
        elif 'the time' in query:
            strtime = datetime.datetime.now().strftime("%H:%H:%S")
            speak(f"Time is {strtime}")
        elif 'open xamp' in query:
            codepath = "C:\\xampp\\xampp-control.exe"
            os.startfile(codepath)
    

######################################


def text_to_braille_real(inp):
    asciicodes = [' ', '!', '"', '#', '$', '%', '&', '', '(', ')', '*', '+', ',', '-', '.', '/',
                  '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ':', ';', '<', '=', '>', '?', '@',
                  'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q',
                  'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '[', '\\', ']', '^', '_']

    # Braille symbols
    brailles = ['⠀', '⠮', '⠐', '⠼', '⠫', '⠩', '⠯', '⠄', '⠷', '⠾', '⠡', '⠬', '⠠', '⠤', '⠨', '⠌', '⠴', '⠂', '⠆', '⠒', '⠲',
                '⠢',
                '⠖', '⠶', '⠦', '⠔', '⠱', '⠰', '⠣', '⠿', '⠜', '⠹', '⠈', '⠁', '⠃', '⠉', '⠙', '⠑', '⠋', '⠛', '⠓', '⠊', '⠚',
                '⠅',
                '⠇', '⠍', '⠝', '⠕', '⠏', '⠟', '⠗', '⠎', '⠞', '⠥', '⠧', '⠺', '⠭', '⠽', '⠵', '⠪', '⠳', '⠻', '⠘', '⠸']
    content = ''
    for i in inp:
        for j in range(len(asciicodes)):
            if i == asciicodes[j]:
                content += brailles[j]
    return content

def listen():
    speak("I'm Listening, please speak")
    import speech_recognition as s
    #statusvar.set('listening......')
    # create a object of recogniser
    sr = s.Recognizer()
    sr.energy_threshold = 1500
    sr.pause_threshold = 5
    print('listening you...................')

    with s.Microphone() as m:
        sr.adjust_for_ambient_noise(m)
        audio = sr.listen(m, timeout=10)

        try:
            query = sr.recognize_google(audio, language='eng-in')
            ip = text_to_braille_real(query)
            output1.insert(END, ip)
            print(query)
        except:
            output1.insert(END, 'Sorry can not recognise')
        statusvar.set('Done')

# button
b1 = Button(frame1, text='Select File', padx=4, pady=6, command=opendialogue, bg='gray30', fg='white', font=('times',10, 'bold'))
b1.pack(side='left')

b2 = Button(frame1, text='Translate', padx=7, pady=6, bg='gray30', fg='white', font=('times', 10, 'bold'), command=translate)
b2.pack(side='left')

b3 = Button(frame1, text='Clear Screen', padx=5, pady=6, bg='gray30', fg='white', font=('times', 10, 'bold'), command=clear)
b3.pack(side='left')

b4 = Button(frame1, text='Translate to text', padx=4, pady=6, bg='gray30', fg='white', font=('times', 10, 'bold'), command=real_time)
b4.pack(side='left')

b5 = Button(frame1, text='Read File', padx=7, pady=6, bg='gray30', fg='white', font=('times', 10, 'bold'), command=read)
b5.pack(side='left')

b6 = Button(frame1, text='Take command', padx=4, pady=6, bg='gray30', fg='white', font=('times', 10, 'bold'), command=take_command)
b6.pack(side='left')

b7 = Button(frame1, text='Listen', padx=12, pady=6, bg='gray30', fg='white', font=('times', 10, 'bold'), command=listen)
b7.pack(side='left')

# Output
output1 = Text(frame2, height=20, bg='gray35', fg='white')
output1.pack(side='bottom', fill=X)

root.mainloop()
a = input()


