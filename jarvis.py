import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import pyautogui
import webbrowser
import os


engine=pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice',voices[0].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishme():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning my master, Jarvis at your service")
    elif hour>=12 and hour<18:
        speak("Good Afternoon my master, Jarvis at your service")
    else:
        speak("Good Evening my master, Jarvis at your service")
    speak("How may I help you?")



def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening....")
        r.pause_threshold = 1
        audio = r.listen(source)
        
    try:
        print("Listening.....")
        query = r.recognize_google(audio)
        print(f"You said: {query}\n")
    
    except Exception as e:
        #print(e)
        print("Say that again please....")
        return "None"
    
    return query


if __name__=="__main__":
   
    
    wishme()
    while True:
        query=takecommand().lower()
        if "exit" in query or "quit" in query or "stop" in query:
            speak("Later Master")
            break

        elif "wikipedia" in query:
            print("Seaching Wikipedia.........")
            query = query.replace("wikipedia","")
            results = wikipedia.summary(query,sentences=3)
            print(results)
            speak("According to Wikipedia")
            speak(results)
        
        elif "screenshot" in query:
            speak("Screenshot saved at the designated location")
            myScreenshot = pyautogui.screenshot()
            myScreenshot.save("C:\\Users\\azaan\\Azaan's Code\\JARVIS\\scr.png")
            speak("How else can I help you?")
        
        
        elif "open google" in query:
            webbrowser.open("google.com")
        
       
       
        elif "who are you" in query:
            speak("I'm Jarvis, I go by the name J-Dawg")
            

        
        elif "the time" in query:
            strtime=datetime.datetime.now().strftime("%H:%M:%S")
            lstr= list(strtime)
            print(lstr)
            lstr[2]= "hours"
            lstr[5]="minutes"
            lstr.append('seconds')
            strtime1="".join(lstr)
            if strtime1[0]=="0":
                strtime1 = strtime1[1:]
            speak(f"The time is{strtime1}")


        elif "play song" in query:
            music_dir=""
            songs=os.listdir(music_dir)
            print(songs)
            os.startfile(os.path.join(music_dir,songs[0]))


        elif "watch the office" in query or "play the office" in query or "open the office" in query:
            theoffice_dir="C:\\Movies and TV SHOWS\\The Office\\The.Office.US.SEASON.04.S04.COMPLETE.720p.WEBRip.2CH.x265.HEVC-PSA"
            episodes=os.listdir(theoffice_dir)
            os.startfile(os.path.join(theoffice_dir,episodes[3]))

        elif "drake" in query:
            speak("She say, Do you love me? I tell her, Only partly, I only love my bed and my momma, I'm sorry, Fifty Dub, I even got it tatted on me 81, they'll bring the crashers to the party. And you know me, Turn a O-2 into the O-3, dog, Without 40 Oli', there'd be no me 'Magine if I never met the broskis")
        elif "kendrick" in query:
            speak("I'm willin' to die for this shit, I done cried for this shit, might take a life for this shit, Put the Bible down and go eye for an eye for this shit, D.O.T. my enemy, won't catch a vibe for this shit, ayy, I been stomped out in front of my momma, My daddy commissary made it to commas, Bitch, all my grandmas dead, So ain't nobody prayin' for me, I'm on your head, ayy, Thirty millions later, know the feds watchin', Auntie on my Telegram like, Be cautious!, I be hangin' out at Tam's, I be on Stockton, I don't do it for the 'Gram, I do it for Compton")

        elif "open sublime" in query:
            sublime_path ="C:\\Program Files\\Sublime Text 3\\sublime_text.exe"
            os.startfile(sublime_path)


        
        elif "open youtube" in query:
            webbrowser.open("youtube.com")
        

        
        



























# def favsong(x):

#     if "drake" in x:
#         speak("I think I'm addicted to naked pictures, And sittin' talking 'bout bitches that we almost had, I don't think I'm conscious of making monsters, Outta the women I sponsor 'til it all goes bad, But shit, it's all good, We threw a party, yeah, we threw a party, Bitches came over, yeah, we threw a party")
#     elif "kendrick" in x:
#         speak("I'm willin' to die for this shit, I done cried for this shit, might take a life for this shit, Put the Bible down and go eye for an eye for this shit, D.O.T. my enemy, won't catch a vibe for this shit, ayy, I been stomped out in front of my momma, My daddy commissary made it to commas, Bitch, all my grandmas dead, So ain't nobody prayin' for me, I'm on your head, ayy, Thirty millions later, know the feds watchin', Auntie on my Telegram like, Be cautious!, I be hangin' out at Tam's, I be on Stockton, I don't do it for the 'Gram, I do it for Compton")


# elif "send email to user" in query:
#             try:
#                 print("What's the email?")
#                 speak("What's the email?")
#                 content = takecommand()
#                 to="user-email-address"
#                 sendEmail(to, content)
#                 print("Email has been sent!")
#                 speak("Email has been sent!")
#             except Exception as e:
#                 print(e)
#                 speak("I was unable to send the email. Sincere Apologies")

# def sendEmail(to, content):
#     #smtplib package will be used, less secure apps needs to be allowed in gmail, visit python docs for better understanding of enlo and starttls
    
#     server = smtplib.SMTP("smtp.gmail.com", 587)                #587 port is used for gmail
#     server.ehlo()                                               #identifies yourself to an ESMTP server
#     server.starttls()                                           #Put the SMTP connection in TLS (Transport Layer Security) mode.
#                                                                 #All SMTP commands that follow will be encrypted.
#     server.login('azaansherani88@gmail.com','your-password')
#     server.sendmail('moaz18cs@gmail.com',to, content)
#     server.close()