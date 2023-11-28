import os
import pathlib

def get_files_in_folder(folder_path, sorted=True) -> list:
    if not os.path.isdir(folder_path):
        return []
    files_in_folder = list(filter(lambda entry: entry.is_file(), pathlib.Path(folder_path).iterdir()))
    files_info = map(lambda file: {"filename": file.name, "size": file.stat().st_size, "ctime": file.stat().st_ctime}, files_in_folder)
    files = list(files_info)
    if sorted:
        files.sort(key=lambda x: x['filename'].casefold())
    return files

def get_files_in_folder_as_choices(folder_path) -> list:
    files_info = get_files_in_folder(folder_path)
    return list(zip((i['filename'] for i in files_info), files_info))

def delete_files(root_directory, files_names: list) -> None:
    for file in files_names:
        file_path = os.path.join(root_directory, file)
        if os.path.isfile(file_path):
            os.remove(file_path)
