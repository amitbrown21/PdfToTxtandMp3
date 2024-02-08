import os
from tkinter.filedialog import *

import PyPDF2
import customtkinter
import pyttsx3

pdf_path = ""
txt_file_path = ""
mode = 1
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")


class TTS:
    engine: pyttsx3.Engine

    def __init__(self, voice, rate: int, volume: float):
        self.engine = pyttsx3.init()
        if voice:
            self.engine.setProperty('voice', voice)
        self.engine.setProperty('rate', rate)
        self.engine.setProperty('volume', volume)


def switch_event():
    global mode
    if mode:
        customtkinter.set_appearance_mode("light")
        mode = 0
    else:
        customtkinter.set_appearance_mode("dark")
        mode = 1


# Converts pdf to txt file
def PdfToText():
    global pdf_path
    global txt_file_path
    if pdf_path != "":
        start_button.configure(state='disabled')
        reader = PyPDF2.PdfReader(pdf_path)
        pages = len(reader.pages)
        txt_file_path = os.path.splitext(pdf_path)[0] + ".txt"
        with open(txt_file_path, 'w', encoding='utf-8') as txt_file:
            for page_num in range(pages):
                prog_bar.set((page_num + 1) / pages)
                page = reader.pages[page_num]
                text = page.extract_text()
                txt_file.write(text + "\n")

        print_box.configure(state='normal')
        print_box.insert("1.0", "Text file has been created successfully!\n")
        TxttoMp3(print_box)
        print_box.configure(state='disabled')
    else:
        print_box.configure(state='normal')
        print_box.insert("1.0", "Please enter a pdf path\n")
        print_box.configure(state='disabled')


def PdfPath():
    global pdf_path
    print_box.configure(state='normal')
    path_entry.configure(state="normal")
    start_button.configure(state="normal")
    pdf_path = askopenfilename()
    if not pdf_path.lower().endswith('.pdf'):
        print_box.insert("1.0", "Error: Selected file is not a PDF.\n")
        print_box.configure(state='disabled')
        return
    else:
        path_entry.configure(placeholder_text=pdf_path)
        path_entry.configure(state="disabled")


# prints available voices in pyttsx3
def setup_gui():
    tts = TTS(None, 200, 1.0)
    voices = tts.list_voices()
    print("Available Voices:")
    for voice in voices:
        print(voice)


# Converts txt file to mp3 file and saves it in the same path
def TxttoMp3(print_box):
    global pdf_path
    global txt_file_path
    if pdf_path and txt_file_path:
        # Initialize TTS engine
        tts_engine = pyttsx3.init()
        # Read the content from the text file
        with open(txt_file_path, 'r', encoding='utf-8') as txt_file:
            text_content = txt_file.read()
        # Save the content as an MP3 file
        mp3_output_path = os.path.splitext(pdf_path)[0] + ".mp3"
        tts_engine.save_to_file(text_content, mp3_output_path)
        # Wait for the conversion to finish
        tts_engine.runAndWait()
        print_box.insert("1.0", f"Text has been converted to MP3 and saved to: {mp3_output_path}\n")
    else:
        print_box.insert("1.0", "Please enter a valid PDF and text file path\n")


# Gui for the app
root = customtkinter.CTk()
frame = customtkinter.CTkFrame(master=root)
root.title("PDF to TXT and MP3 convertor")
root.geometry("800x600")
frame.pack(pady=10, padx=10, fill="both", expand=True)
label = customtkinter.CTkLabel(master=frame, text="PDF-to-MP3", font=("Helvetica", 48))
label.pack(pady=20, padx=10)
path_entry = customtkinter.CTkEntry(master=frame, font=("Helvetica", 24), placeholder_text="Browse pdf")
path_entry.pack(pady=15, padx=10, ipadx=500, ipady=0)
browse_button = customtkinter.CTkButton(master=frame, text="Browse", font=("Helvetica", 24), command=PdfPath)
browse_button.pack(pady=15, padx=10)
start_button = customtkinter.CTkButton(master=frame, text="Start", font=("Helvetica", 24), command=PdfToText)
start_button.pack(pady=15, padx=10)
prog_bar = customtkinter.CTkProgressBar(master=frame, orientation="horizontal", width=500)
prog_bar.pack(pady=15, padx=10)
prog_bar.set(0)
print_box = customtkinter.CTkTextbox(master=frame, width=500, height=100, state='disabled')
print_box.pack(pady=15, padx=10)
switch_var = customtkinter.StringVar(value="on")
switch = customtkinter.CTkSwitch(master=frame, text="Dark Mode", command=switch_event,
                                 variable=switch_var, onvalue="on", offvalue="off")
switch.pack(pady=15, padx=10)

root.mainloop()
