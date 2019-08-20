import os

ffmpeg = "Q:\\Info5Film\\Heritage\\Z_Tools\\Scripts\\AviToJpg\\ffmpeg.exe"
fToConv_Path = "C:\\Users\\mboulogne\\Desktop\\the-angry-birds-movie-character-animation.mp4"
fToConv_Path = "C:\\Users\\tvanbastelaere\\Desktop\New\\ToJpg\\"


for i in os.listdir(fToConv_Path):
    print i
    
    # fToConv_Name = os.path.basename(i)
    fToConv_Name_woExt = os.path.splitext(i)
    convExt = "%04d.jpg"
    fConvert_Name = [fToConv_Name_woExt [0], convExt]
    fConvert_Name_NEW = '_'.join(fConvert_Name)
    
    fConv_Path = os.path.dirname(fToConv_Path)
    fConv_Path_New = os.path.join(fConv_Path, fToConv_Name_woExt [0])
    fConv_Path_Last = os.path.join(fConv_Path_New, fConvert_Name_NEW)
    
    fToConv_Path_NEW = os.path.join(fToConv_Path, i)
    
    if not os.path.exists(os.path.dirname(fConv_Path_Last)):
        try:
            os.makedirs(os.path.dirname(fConv_Path_Last))
        
        # Guard against race condition
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise
                
    os.system("C:\\Windows\\System32\\cmd.exe /c" + ffmpeg+' -i '+fToConv_Path_NEW+' -an '+fConv_Path_Last)