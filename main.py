import cv2
import mediapipe as mp
import time
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
import pyttsx3

# ------------------ TTS ------------------
engine = pyttsx3.init()

def speak_sentence():
    global sentence
    if sentence:
        engine.say(" ".join(sentence))
        engine.runAndWait()
        # Clear sentence after speaking
        sentence = []
        sentence_label.config(text="Sentence: ")

# ------------------ ORIGINAL VARIABLES ------------------
sentence=[]
last_word="None"
last_checked_word = None
count = 0
threshold = 8
current_word = ""

# ------------------ MEDIAPIPE ------------------
mpHands= mp.solutions.hands
hands= mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

# ------------------ FUNCTIONS (UNCHANGED) ------------------
def landmarks_identify(handLms,img):
    landmarks =[]
    for id,lm in enumerate(handLms.landmark):
        h, w, c = img.shape
        x = int(lm.x * w)
        y = int(lm.y * h)
        landmarks.append([id, x, y])
    return landmarks

def fingers(points,img):
    landmarks=landmarks_identify(points,img)
    fingers=[]
    fingers.append(1 if landmarks[8][2]<landmarks[6][2] else 0)
    fingers.append(1 if landmarks[12][2]<landmarks[10][2] else 0)
    fingers.append(1 if landmarks[16][2]<landmarks[14][2] else 0)
    fingers.append(1 if landmarks[20][2]<landmarks[18][2] else 0)
    fingers.append(1 if landmarks[4][1]<landmarks[2][1] else 0)
    return tuple(fingers)

def gestures(points,img):
    global last_word, last_checked_word, count, sentence,current_word
    gesture_list = fingers(points,img)
    gesture_dict = {
        (0,1,1,1,0): "Good",
        (0,0,0,0,0): "No",
        (1,1,1,1,1): "Hi",
        (1,0,0,0,0): "Wait",
        (1,1,0,0,0): "What's Up",
        (0,0,0,0,1): "Thumbs Up",
        (1,1,1,1,0): "Four",
        (1,0,0,1,0): "Rock It"
    }
    if gesture_list in gesture_dict:
        current_word = gesture_dict[gesture_list]

    if current_word == last_checked_word:
        count += 1
    else:
        last_checked_word = current_word
        count = 1

    if count >= threshold and current_word != last_word:
        sentence.append(current_word)
        last_word = current_word

# ------------------ TKINTER GUI ------------------
root = Tk()
root.title("Hand Gesture Recognition")
root.geometry("500x300")
root.configure(bg="#1e1e2f")
root.resizable(False, False)

video_label = Label(root, bg="#1e1e2f")
sentence_label = Label(root, fg="white", bg="#1e1e2f",
                       font=("Arial",14,"bold"))

cap = None
running = False

# ------------------ START CAMERA / VIDEO ------------------
def start_camera():
    start_processing(cv2.VideoCapture(0))

def upload_video():
    path = filedialog.askopenfilename(
        filetypes=[("Video Files","*.mp4 *.avi *.mov")]
    )
    if path:
        start_processing(cv2.VideoCapture(path))

def start_processing(capture):
    global cap, running, sentence, last_word, last_checked_word, count, current_word
    cap = capture
    running = True

    # Reset variables for fresh run
    sentence = []
    last_word = "None"
    last_checked_word = None
    count = 0
    current_word = ""

    root.geometry("1000x750")
    root.resizable(True, True)

    start_frame.pack_forget()
    video_label.pack(pady=10)
    sentence_label.pack(pady=5)
    control_frame.pack(pady=10)

    # ================= DIRECT WHILE TRUE LOOP =================
    while True:
        root.update()   # keep tkinter alive

        if not running:
            break

        success, img = cap.read()
        if not success:
            stop()
            break

        img = cv2.flip(img,1)

        # For MediaPipe processing
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(imgRGB)

        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:
                mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)
                gestures(handLms, img)

        sentence_label.config(text="Sentence: " + " ".join(sentence))

        # ===== BLUE SCREEN FIX: Convert BGR to RGB =====
        imgRGB2 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        imgTk = ImageTk.PhotoImage(Image.fromarray(imgRGB2))
        video_label.imgtk = imgTk
        video_label.config(image=imgTk)

# ------------------ STOP FUNCTION + RESET VARIABLES ------------------
def stop():
    global running, sentence, last_word, last_checked_word, count, current_word
    running = False
    if cap:
        cap.release()

    # Reset variables for next run
    sentence = []
    last_word = "None"
    last_checked_word = None
    count = 0
    current_word = ""

    root.geometry("500x300")
    root.resizable(False, False)
    video_label.pack_forget()
    sentence_label.pack_forget()
    control_frame.pack_forget()
    start_frame.pack(expand=True)

# ------------------ START SCREEN ------------------
start_frame = Frame(root, bg="#1e1e2f")
start_frame.pack(expand=True)

Label(start_frame, text="Select Input Source",
      font=("Arial",16,"bold"),
      fg="white", bg="#1e1e2f").pack(pady=20)

Button(start_frame, text="📷 Start Camera",
       font=("Arial",12,"bold"),
       bg="#00b894", fg="white",
       width=18, command=start_camera).pack(pady=10)

Button(start_frame, text="🎞 Upload Video",
       font=("Arial",12,"bold"),
       bg="#0984e3", fg="white",
       width=18, command=upload_video).pack(pady=10)

# ------------------ CONTROL BUTTONS ------------------
control_frame = Frame(root, bg="#1e1e2f")

Button(control_frame, text="🔊 Speak Sentence",
       font=("Arial",11,"bold"),
       bg="#6c5ce7", fg="white",
       command=speak_sentence).grid(row=0,column=0,padx=10)

Button(control_frame, text="⏹ Stop",
       font=("Arial",11,"bold"),
       bg="#d63031", fg="white",
       command=stop).grid(row=0,column=1,padx=10)

root.mainloop()
