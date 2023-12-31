import os
import yt_dlp


class FilenameCollectorPP(yt_dlp.postprocessor.common.PostProcessor):
    def __init__(self, outtmpl):
        super(FilenameCollectorPP, self).__init__(None)
        self.filenames = []
        if str(os.path.split(outtmpl)[1]).startswith("%(creator)s - "):
            self.filename_starts_w_creator = True
        else:
            self.filename_starts_w_creator = False

    def run(self, information):
        filepath = information['filepath']
        filepath_splitted = os.path.split(filepath)
        filedir = filepath_splitted[0]
        filename = filepath_splitted[1]
        if self.filename_starts_w_creator and filename.startswith("NA - "): # Pokud filename ma zacinat umelcem, ale v metadatech neni
            filename = filename[5:]                                         # odstrani se prvnich 5 znaku('NA - ') a filename bude jen nazev videa
        filename = filename.replace("#", "") # Hash('#') v nazvu zpusobuje chybu, potom to nejde stahnout pres web, proto se musi odstranit
        os.rename(filepath, os.path.join(filedir, filename))
        self.filenames.append(filename)
        return [], information
    