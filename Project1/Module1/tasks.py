# Create your tasks here


import os
import yt_dlp
import logging
import datetime
from celery import shared_task
from Module1.utils.ytdutils import FilenameCollectorPP
from Module1.models.download_request import DownloadRequest
from Module1.models.downloaded_file import DownloadedFile
import Module1.apps


@shared_task
def download_items(url: str, ydl_opts: dict, playlist: bool, output_dir: str, dl_req_id: int) -> None:
    ydl_opts["quiet"] = True
    ydl_opts["noprogress"] = True
    ydl_opts["noplaylist"] = not playlist
    outtmpl_path = os.path.join(output_dir, ydl_opts["outtmpl"])
    ydl_opts["outtmpl"] = outtmpl_path
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.cache.remove()
        filename_collector = FilenameCollectorPP(outtmpl_path)
        ydl.add_post_processor(filename_collector)
        ydl.download([url])
        DownloadedFile.objects.bulk_create([DownloadedFile(filename=filename, request=DownloadRequest.objects.get(pk=dl_req_id)) for filename in filename_collector.filenames])


