import tkinter as tk
from tkinter import ttk
from tkinter import *
from PIL import Image, ImageTk
import speech_recognition as sr
import pyttsx3
import nltk
import pandas as pd
import numpy as np
from nltk.sentiment import SentimentIntensityAnalyzer
from transformers import AutoTokenizer
from transformers import AutoModelForSequenceClassification
from scipy.special import softmax
import threading
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg



class SpeechToTextGUI:
    def __init__(self):

        #______Preloader____________

        self.preloader = tk.Tk()
        self.preloader.title("Mentel Well Bot")
        self.preloader.resizable(False, False)

        # Load the logo image
        self.logo_image = Image.open("mental-health.png")
        self.logo_photo = ImageTk.PhotoImage(self.logo_image)

        # Create a label with the logo
        self.logo_label = ttk.Label(self.preloader, image=self.logo_photo)
        self.logo_label.pack(padx=20, pady=20)

        # Center the preloader window on the screen
        self.preloader.update_idletasks()
        self.screen_width = self.preloader.winfo_screenwidth()
        self.screen_height = self.preloader.winfo_screenheight()
        self.window_width = self.preloader.winfo_width()
        self.window_height = self.preloader.winfo_height()
        self.x = (self.screen_width - self.window_width) // 2
        self.y = (self.screen_height - self.window_height) // 2
        self.preloader.geometry(f"+{self.x}+{self.y}")

        # Update the preloader window
        self.preloader.update()

        # Wait for 2 seconds
        self.preloader.after(2000)

        # Close the preloader window
        self.preloader.destroy()



        #__________________________



        self.root = tk.Tk()
        self.root.title("Mental Well Bot")
        #self.root.geometry("400x400")
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"{self.screen_width}x{self.screen_height}")

        self.small_icon = tk.PhotoImage(file="mental-health.png")
        self.large_icon = tk.PhotoImage(file="mental-health.png")
        self.root.iconphoto(False, self.large_icon, self.small_icon)

        self.canvas = tk.Canvas(self.root)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = ttk.Scrollbar(self.root, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.scrollbar = ttk.Scrollbar(self.root, orient=tk.HORIZONTAL, command=self.canvas.xview)
        self.scrollbar.pack(side=tk.BOTTOM, fill=tk.X)


        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.canvas.configure(xscrollcommand=self.scrollbar.set)
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))


        self.frame = ttk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.frame, anchor="nw")
        #_________________________________________________Bg Logo_______________________________________
        #self.logo_image = Image.open("mental-health.png")
        #self.logo_photo = ImageTk.PhotoImage(self.logo_image)
        #self.image_label = tk.Label(self.canvas, image=self.logo_photo)
        #self.image_label.photo = self.logo_photo  
        #self.image_label.place(relx=0.5, rely=0, anchor="n") 
        #self.text_label = tk.Label(self.canvas, text="Mental Well Bot", font=("Helvetica", 16, "bold"))
        #self.text_label.place(relx=0.5, rely=0.1, anchor="n")
        #_________________________________________________________________________________________________
        # Create a label to display the recognized text
        self.label = tk.Label(self.frame, text="")
        self.label.pack()

        # Create a button to start the speech recognition
        #self.button = tk.Button(self.root, text="Start", command=self.start_speech_recognition)
        #self.button.pack()
        self.thread = threading.Thread(target=self.start_speech_recognition)
        self.thread.start()

    def start_speech_recognition(self):
        
        #initialize speech recognition engine and text to speech engine
        r=sr.Recognizer()
        engine=pyttsx3.init()

        responses = []
        #responses1 = []
        total = []

        #___________________________________________________________________________________________________________
        #___________________________________BOT STARTS HERE_________________________________________________________
        #___________________________________________________________________________________________________________
        #set the properties for the text to spech engine
        voices=engine.getProperty('voices')
        engine.setProperty('voice',voices[0].id)
        engine.setProperty('rate',150)


        def content2Ui(content):
            self.label = tk.Label(self.frame, text=content)
            self.label.pack()
        def speech_to_text():
            recognizer = sr.Recognizer()
            with sr.Microphone() as source:
                print("Speak now:") #Replace this with GUI code..
                #
                self.labelspeak = tk.Label(self.frame, text="Speak now:")
                self.labelspeak.configure(bg="white", fg="blue", font=("Arial", 16, "bold"))
                self.labelspeak.pack()
                #
                audio = recognizer.listen(source)

            try:
                text = recognizer.recognize_google(audio)
                return text
            except sr.UnknownValueError:
                print("Sorry, I couldn't understand what you said.")
                return ""
            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))
                return ""

        def speak(text):
            engine.say(text)
            engine.runAndWait()
        speak("Hello,I'm your personnel A I.")

        #questions = [     "Do you get panic attacks on hearing about covid19 news?",
        #                "How often have you felt nervous or anxious?"]

        
        questions = [   "Do you get panic attacks on hearing about covid19 news?",
                        "How often have you felt nervous or anxious?",
                        "Have you ever felt lonely during the covid time?",
                        "Did you lose anyone you loved during the covid19?",
                        "Have any of your personal plans been changed after the pandemic?",
                        "Have you felt hopeless about your future?",
                        "When was the last time you felt good about yourself?",
                        "Are you able to enjoy the things you used to before like meeting family members or going for a walk?",
                        "Have you experienced mood swings?",
                        "Do you feel unable to cope up with daily problems?",
                        "Do you feel mentally weak when interacting with others?",
                        "Have you or someone you know ever struggled with mental illness? What was that experience like for them?",
                        "Have you felt frustrations during the quarantine?",
                        "Have you lost interest in your field of working?",
                        "What are the thoughts,feelings or behaviour that have been troubling you?"
        ]
        



        for question in questions:
            print(question)  #Display this on UI
            #
            self.labelques = tk.Label(self.frame, text=question)
            self.labelques.configure(bg="white", fg="orange", font=("Arial", 16, "bold"))
            self.labelques.pack()
            #
            speak(question)
            response = speech_to_text()
            responses.append(response)
            print(response)  #Display this on UI
            #
            self.labelresponse = tk.Label(self.frame, text=response)
            self.labelresponse.configure(bg="white", fg="yellow", font=("Arial", 16, "bold"))
            self.labelresponse.pack()
            # 

        speak("Thank you for your responses. Here are your answers:")
        for i in range(len(questions)):
            print(f"{questions[i]} {responses[i]}") #Display this on UI
            #
            self.label = tk.Label(self.frame, text=f"{questions[i]} {responses[i]}")
            self.label.pack()
            # #

        #___________________________________________________________________________________________________________
        #___________________________________BOT IS WORKING PROPERLY_________________________________________________
        #___________________________________________________________________________________________________________


        #_______________________________________SENTIMENT ANALYSIS__________________________________________________

        def find_largest(neg, neu, pos):
            if neg >= neu and neg >= pos:
                return {'negative' : neg}
            elif neu >= neg and neu >= pos:
                return {'neutral' : neu}
            else:
                return {'positive' : pos}



        #_________VADER_________
        model1 = SentimentIntensityAnalyzer()
        responses_string = " ".join(responses)
        vader_scores = model1.polarity_scores(responses_string)
        print(vader_scores)

        vader_largest = find_largest(vader_scores['neg'],vader_scores['neu'],vader_scores['pos'])
        print(vader_largest)

        #For Pie-chart...
        vader_size = [vader_scores['neg']*100,vader_scores['neu']*100,vader_scores['pos']*100]
        vader_labels = ["Negetive","Neutral","Positive"]


        #_______Vader End________



        #_________RoBERTa_________

        Model = f"cardiffnlp/twitter-roberta-base-sentiment"
        tokenizer = AutoTokenizer.from_pretrained(Model)
        model = AutoModelForSequenceClassification.from_pretrained(Model)

        text_data = tokenizer(responses_string,return_tensors='pt')

        result = model(**text_data)
        score = result[0][0].detach().numpy()
        score = softmax(score)

        label = {
            'neg' : score[0],
            'neu' : score[1],
            'pos' : score[2]
        }

        print(label)
        roberta_largest = find_largest(label['neg'],label['neu'],label['pos'])
        print(roberta_largest)

        #For Pie-chart...abs
        roberta_sizes = [label['pos']*100,label['neg']*100,label['neu']*100]
        roberta_labels = ["Positive","Negative","Neutral"]
        #print(roberta_sizes)
        #print(roberta_labels)


        #_______RoBERTa End________

        total.append(list(vader_largest)[0])
        total.append(list(roberta_largest)[0])

        print("Total scores : \n vader = {0}\n roberta = {1} \n {2}".format(vader_largest,roberta_largest,total))

        #___________________________Predictions from both with results______________________________

        neutral1 = ['neutral','neutral']
        negative1 = [
            ['neutral','negative'],
            ['negative','neutral'],
            ['negative','negative']
        ]
        positive1 = [
            ['positive','positive'],
            ['neutral','positive'],
            ['positive','neutral']
        ]

        if total in negative1:
                print("Based on your responses, it seems like you might be suffering from a mental illness. We recommend seeking professional help.")
                #Display this on UI with some emotes..
                self.label = tk.Label(self.frame, text="Based on your responses, it seems like you might be suffering from a mental illness. We recommend seeking professional help.")
                self.label.configure(bg="red", fg="white", font=("Arial", 16, "bold"))
                self.label.pack()
                speak("Based on your responses, it seems like you might be suffering from a mental illness.\n We recommend seeking professional help.")
                
                #
        else:
                print("Based on your responses, it seems like you are not currently suffering from a mental illness. However, if you ever feel overwhelmed, don't hesitate to reach out for support.")
                #Display this on UI with some emotes..
                self.label = tk.Label(self.frame, text="Based on your responses, it seems like you are not currently suffering from a mental illness.\n However, if you ever feel overwhelmed, don't hesitate to reach out for support.")
                self.label.configure(bg="green", fg="white", font=("Arial", 16, "bold"))
                self.label.pack()
                speak("Based on your responses, it seems like you are not currently suffering from a mental illness. However, if you ever feel overwhelmed, don't hesitate to reach out for support.")
                
                #

        fig = Figure(figsize=(3, 2), dpi=100)
        ax = fig.add_subplot(111)
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
        ax.pie(vader_size, labels=vader_labels, autopct='%1.1f%%', startangle=90)
        ax.set_title('Vader')

        fig2 = Figure(figsize=(3, 2), dpi=100)
        bx = fig2.add_subplot(111)
        bx.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
        bx.pie(roberta_sizes, labels=roberta_labels, autopct='%1.1f%%', startangle=90)
        bx.set_title('Roberta')

        canvas = FigureCanvasTkAgg(fig, master=self.frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.LEFT, anchor=tk.CENTER, expand=True)
        canvas2 = FigureCanvasTkAgg(fig2, master=self.frame)
        canvas2.draw()
        canvas2.get_tk_widget().pack(side=tk.RIGHT, anchor=tk.CENTER, expand=True)

        #________________________________________________________________________________________

    

if __name__ == "__main__":
    gui = SpeechToTextGUI()
    gui.root.mainloop()
