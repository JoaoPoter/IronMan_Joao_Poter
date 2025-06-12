
import cx_Freeze
executaveis = [ 
               cx_Freeze.Executable(script="main.py", icon="assets/icone.png") ]
cx_Freeze.setup(
    name = "Iron Man",
    options={
        "build_exe":{
            "packages":["pygame", "speech_recognition", "rapidfuzz", "random", "os", "json", "datetime", "cv2", "sys", "PIL", "aifc", "chunk", "audioop", "pyttsx3.drivers.sapi5"],
            "include_files":["assets"]
        }
    }, executables = executaveis
)
