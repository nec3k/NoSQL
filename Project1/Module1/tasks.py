# Create your tasks here


import os
import yt_dlp
import logging
import datetime
from celery import shared_task
from Module1.utils.ytdutils import FilenameCollectorPP
from Module1.models.download_request import DownloadRequest
from Module1.models.downloaded_file import DownloadedFile


@shared_task
def download_items(url: str, ydl_opts: dict, playlist: bool, output_dir: str, dl_req_id: int) -> None:
    ydl_opts["quiet"] = True
    ydl_opts["noprogress"] = True
    ydl_opts["nowarnings"] = True
    ydl_opts["noplaylist"] = not playlist
    ydl_opts["outtmpl"] = os.path.join(output_dir, ydl_opts["outtmpl"])
    for idx, pp in enumerate(ydl_opts.get("postprocessors", [])):
        if pp.get("key") == "MetadataParser" and pp.get("when") == "pre_process":
            ydl_opts["postprocessors"][idx]["actions"].append((yt_dlp.postprocessor.MetadataParserPP.Actions.INTERPRET, 'artist', r'(?P<creator>[^,]+)'))
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.cache.remove()
        filename_collector = FilenameCollectorPP()
        ydl.add_post_processor(filename_collector)
        ydl.download([url])
        DownloadedFile.objects.bulk_create([DownloadedFile(filename=filename, request=DownloadRequest.objects.get(pk=dl_req_id)) for filename in filename_collector.filenames])


