import os
import yt_dlp



class FilenameCollectorPP(yt_dlp.postprocessor.common.PostProcessor):
    def __init__(self):
        super(FilenameCollectorPP, self).__init__(None)
        self.filenames = []

    def run(self, information):
        filepath = information['filepath']
        filepath_splitted = os.path.split(filepath)
        filedir = filepath_splitted[0]
        filename = filepath_splitted[1]
        if filename.startswith("NA - "):
            filename = filename[5:]
            os.rename(filepath, os.path.join(filedir, filename))
        self.filenames.append(filename)
        return [], information
    