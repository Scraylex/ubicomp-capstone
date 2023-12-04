import speech_recognition as sr
import winsound

# Function to emit a beep sound
def beep():
    winsound.Beep(1000, 500)  # Beep at 1000 Hz for 500 milliseconds

# Initialize the recognizer
recognizer = sr.Recognizer()

# Function to listen to voice commands
def listen():
    with sr.Microphone() as source:
        print("Say something...")
        audio = recognizer.listen(source)

        try:
            # Recognize speech using Google Speech Recognition
            command = recognizer.recognize_google(audio)
            print("You said:", command)

            # Emit a beep in response
            beep()

        except sr.UnknownValueError:
            print("Sorry, could not understand the audio.")
        except sr.RequestError:
            print("Could not request results. Check your internet connection.")

# Call the listen function to start listening to voice commands
listen()
