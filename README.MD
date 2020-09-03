# PYTTSx3 Server

This simple Flask server interacts with the Windows SAPI to provide Text-To-Speech synthesis over a network using HTTP GET requests.

## Requirements
Requires:
- Python 3 (Tested on 3.8.5)
- Windows 10

For python package requirements, refer to `requirements.txt`.

## Setup
1. Instally Python 3.
2. Use: `pip install -r requirements.txt` to install Flask and PYTTSX3
3. Refer to section at the bottom of this README for enabling additional voices.

## Usage
In the folder with `app.py`, start the server using:
`flask run --port=5122`

To test, use CURL and a GET request similar to the following:
```
curl -G "http://localhost:5122/process?" --data-urlencode "INPUT_TEXT=Welcome to the world of speech synthesis." --data-urlencode "VOICE=1" --data-urlencode "RATE=175" -o test2.wav
```
The _VOICE_ and _RATE_ parameters are optional. 

The number of available voices are dependent on what has been enabled in Windows. By default, only 2 voices are visible to PYTTSX3. Refer to **Unlocking additional SAPI voices** for more infomation.

To test for available voices, use the following CURL GET request:
```
curl -G "http://localhost:5122/voices?"
```
This will return a JSON string consisting of:
```
{
    "availableVoices":
    {
        "0":"Microsoft David Desktop - English (United States)",
        "1":"Microsoft Catherine - English (Australia)",
        "2":"Microsoft Zira Desktop - English (United States)"
    }
}
```

### Unlocking additional SAPI voices
By default, the standard Windows TTS COM object does not expose all of the available voices from SAPI5 due to a Microsoft introduced with their TTS engine.

To make these additional voices visible to PyTTSx3, you'll need to modify the registry.

[This link shows the process required to expose the additional voices.](https://www.ghacks.net/2018/08/11/unlock-all-windows-10-tts-voices-system-wide-to-get-more-of-them/)

 Otherwise, the following steps outline this process:

**Warning: You need administrator privileges.**

1. Open `regedit`.
2. In `regedit`, browse to `Computer\HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech_OneCore\Voices\Token`. This lists all of the available MS SAPI voices installed on the machine.
3. Right click on a folder for one of the voices, IE: `MSTTS_V110_enAU_CatherineM`, and select Export. Choose a location on the Desktop or in your Documents.
4. Enter a name for the new registry file, IE: 'catherinem'
5. Open the newly export registry file using your favourite text editor.
6. Copy all of the information in the file **except** for the `Windows Registry Editor Version 5.00` line and paste the contents **below** the existing text. (We need the registry file to point to two different locations)
7. Replace the **location** in the first data set with:
`HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens`. Retain the voice name!
8. Replace the **location** in the second data set with:
`HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\Microsoft\SPEECH\Voices\Tokens`. Retain the voice name!
9. Your registry file should now look similar to this:
```
Windows Registry Editor Version 5.00

[HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\MSTTS_V110_enAU_CatherineM]
@="Microsoft Catherine - English (Australia)"
"C09"="Microsoft Catherine - English (Australia)"
"CLSID"="{179F3D56-1B0B-42B2-A962-59B7EF59FE1B}"
"LangDataPath"=hex(2):25,00,77,00,69,00,6e,00,64,00,69,00,72,00,25,00,5c,00,53,\
  00,70,00,65,00,65,00,63,00,68,00,5f,00,4f,00,6e,00,65,00,43,00,6f,00,72,00,\
  65,00,5c,00,45,00,6e,00,67,00,69,00,6e,00,65,00,73,00,5c,00,54,00,54,00,53,\
  00,5c,00,65,00,6e,00,2d,00,41,00,55,00,5c,00,4d,00,53,00,54,00,54,00,53,00,\
  4c,00,6f,00,63,00,65,00,6e,00,41,00,55,00,2e,00,64,00,61,00,74,00,00,00
"VoicePath"=hex(2):25,00,77,00,69,00,6e,00,64,00,69,00,72,00,25,00,5c,00,53,00,\
  70,00,65,00,65,00,63,00,68,00,5f,00,4f,00,6e,00,65,00,43,00,6f,00,72,00,65,\
  00,5c,00,45,00,6e,00,67,00,69,00,6e,00,65,00,73,00,5c,00,54,00,54,00,53,00,\
  5c,00,65,00,6e,00,2d,00,41,00,55,00,5c,00,4d,00,33,00,30,00,38,00,31,00,43,\
  00,61,00,74,00,68,00,65,00,72,00,69,00,6e,00,65,00,00,00

[HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\MSTTS_V110_enAU_CatherineM\Attributes]
"Age"="Adult"
"DataVersion"="11.0.2015.0909"
"Gender"="Female"
"Language"="C09"
"Name"="Microsoft Catherine"
"SayAsSupport"="spell=NativeSupported; cardinal=NativeSupported; ordinal=NativeSupported; date=NativeSupported; time=NativeSupported; telephone=NativeSupported; computer=NativeSupported; address=NativeSupported; currency=NativeSupported; message=NativeSupported; media=NativeSupported; url=NativeSupported; alphanumeric=NativeSupported"
"SharedPronunciation"=""
"Vendor"="Microsoft"
"Version"="11.0"

[HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\Microsoft\SPEECH\Voices\Tokens\MSTTS_V110_enAU_CatherineM]
@="Microsoft Catherine - English (Australia)"
"C09"="Microsoft Catherine - English (Australia)"
"CLSID"="{179F3D56-1B0B-42B2-A962-59B7EF59FE1B}"
"LangDataPath"=hex(2):25,00,77,00,69,00,6e,00,64,00,69,00,72,00,25,00,5c,00,53,\
  00,70,00,65,00,65,00,63,00,68,00,5f,00,4f,00,6e,00,65,00,43,00,6f,00,72,00,\
  65,00,5c,00,45,00,6e,00,67,00,69,00,6e,00,65,00,73,00,5c,00,54,00,54,00,53,\
  00,5c,00,65,00,6e,00,2d,00,41,00,55,00,5c,00,4d,00,53,00,54,00,54,00,53,00,\
  4c,00,6f,00,63,00,65,00,6e,00,41,00,55,00,2e,00,64,00,61,00,74,00,00,00
"VoicePath"=hex(2):25,00,77,00,69,00,6e,00,64,00,69,00,72,00,25,00,5c,00,53,00,\
  70,00,65,00,65,00,63,00,68,00,5f,00,4f,00,6e,00,65,00,43,00,6f,00,72,00,65,\
  00,5c,00,45,00,6e,00,67,00,69,00,6e,00,65,00,73,00,5c,00,54,00,54,00,53,00,\
  5c,00,65,00,6e,00,2d,00,41,00,55,00,5c,00,4d,00,33,00,30,00,38,00,31,00,43,\
  00,61,00,74,00,68,00,65,00,72,00,69,00,6e,00,65,00,00,00

[HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\Microsoft\SPEECH\Voices\Tokens\MSTTS_V110_enAU_CatherineM\Attributes]
"Age"="Adult"
"DataVersion"="11.0.2015.0909"
"Gender"="Female"
"Language"="C09"
"Name"="Microsoft Catherine"
"SayAsSupport"="spell=NativeSupported; cardinal=NativeSupported; ordinal=NativeSupported; date=NativeSupported; time=NativeSupported; telephone=NativeSupported; computer=NativeSupported; address=NativeSupported; currency=NativeSupported; message=NativeSupported; media=NativeSupported; url=NativeSupported; alphanumeric=NativeSupported"
"SharedPronunciation"=""
"Vendor"="Microsoft"
"Version"="11.0"
```
10. To install, save the registry file, exit the editor and double click on the file. Accept the warning prompt and the voice will now be available, no need to restart.