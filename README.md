Here’s a well-structured **README.md** file for your **Podcast Transcriber** project. This README includes clear instructions, explanations, and formatting for easy readability.

---

# 🎙️ Podcast Transcriber  

**Podcast Transcriber** is a Python-based tool that extracts and transcribes audio from YouTube videos. It supports multiple workflows:  
1. **Uses YouTube transcripts if available.**  
2. **Downloads audio and transcribes it using Whisper if no transcript is found.**  

## 🚀 Features  
✔️ **Automatic Transcript Extraction** – Fetches official or auto-generated YouTube subtitles.  
✔️ **Language Translation** – Translates auto-generated transcripts if needed.  
✔️ **Audio Download & Transcription** – Downloads and transcribes audio using OpenAI's Whisper.  
✔️ **Custom Output Files** – Saves the transcript in a user-defined text file.  

---

## 🛠️ Installation  

### **1️⃣ Clone the Repository**  
```sh
git clone https://github.com/cyberbotsaber/podcast-transcriber.git
cd podcast-transcriber
```

### **2️⃣ Set Up a Virtual Environment (Recommended)**
```sh
python -m venv .venv
source .venv/bin/activate  # On macOS/Linux
# or
.venv\Scripts\activate     # On Windows
```

### **3️⃣ Install Dependencies**  
```sh
pip install -r requirements.txt
```

### **4️⃣ Install FFmpeg (For Audio Processing)**  
Ensure **FFmpeg** is installed and accessible:  

- **Windows:** [Download FFmpeg](https://ffmpeg.org/download.html), extract, and add its `bin` directory to your system PATH.  
- **Mac:**  
  ```sh
  brew install ffmpeg
  ```
- **Linux:**  
  ```sh
  sudo apt update && sudo apt install ffmpeg
  ```

---

## 🎯 Usage  

### **1️⃣ Run the Script**
```sh
python complete_transcribe.py
```
It will prompt for a **YouTube video URL**, check for transcripts, and process accordingly.

### **2️⃣ Select an Output Filename**  
After transcription, you can save the text with a custom name.

---

## 🔧 How It Works  

### **Step 1: Fetching YouTube Transcripts**  
- If **English subtitles** exist, they are retrieved.  
- If **auto-generated subtitles** exist in another language, they are translated to English.  
- If **no subtitles** exist, the script proceeds to download audio.

### **Step 2: Downloading & Transcribing Audio**  
- The script downloads the **best-quality audio** using `yt-dlp`.  
- The downloaded audio is **transcribed using OpenAI's Whisper model**.  

---

## 🏗️ Project Structure  

```
podcast-transcriber/
│── complete_transcribe.py   # Main script  
│── download_audio.py        # Handles YouTube audio downloads  
│── transcribe.py            # Uses Whisper to transcribe audio  
│── requirements.txt         # Dependencies  
│── README.md                # Documentation  
```

---

## 📌 Dependencies  
The script relies on:  
- `youtube-transcript-api` – Fetching YouTube transcripts  
- `yt-dlp` – Downloading YouTube audio  
- `openai-whisper` – Transcribing audio  
- `ffmpeg` – Audio processing  

Install them using:  
```sh
pip install -r requirements.txt
```

---

## ❓ Troubleshooting  

### **1. No Transcript Found?**  
If no transcript is available, the script downloads the audio and transcribes it using Whisper.  

### **2. `OSError: Invalid Argument` When Saving Transcripts?**  
Ensure the filename does not contain special characters (`?`, `/`, `\`, `:`).  

### **3. `yt-dlp` or `FFmpeg` Not Found?**  
Ensure `yt-dlp` and `ffmpeg` are installed correctly and added to the system `PATH`.  

---

## 💡 Future Improvements  
- 🔹 Add GUI support for easier use  
- 🔹 Improve language detection and translation accuracy  
- 🔹 Integrate OpenAI’s GPT for better summaries  

---

## 🎉 Contributing  
Pull requests are welcome! Feel free to fork the repo and submit changes.  

---

## 📜 License  
This project is open-source and available under the **MIT License**.  

---
