import shutil
import os
git_work_path = r"E:/git_work/Beam_Tools"
work_path = r"E:/Beam_Tools"
if os.path.exists(git_work_path):
    print git_work_path
if os.path.exists(work_path):
    print work_path
#shutil.copy2(git_work_path,work_path)