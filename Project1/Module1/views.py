import os
from urllib.parse import urlencode

from django.urls import reverse

from Module1.utils.fileutils import get_files_in_folder, get_files_in_folder_as_choices, delete_files
from Module1.forms.fileForm import FileForm
from Module1.models.download_format import DownloadFormat
from Module1.forms.downloaderForm import DownloaderForm
from Module1.models.download_request import DownloadRequest, MAX_URL_LENGTH
from Module1.forms.loginForm import LoginForm
from Module1.tasks import download_items
from Project1.settings import MEDIA_ROOT
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.template import loader
from django.views.static import serve
from django.contrib.auth.forms import PasswordChangeForm
from django_celery_results.models import TaskResult

#def is_superuser(user):
#    return user.is_superuser
#@login_required(login_url='login_page')
#@user_passes_test(is_superuser)
#def controler(req):

MY_REQUESTS_PAGE_SIZE = 5

@login_required(login_url='login_page')
def downloader(request):
    if request.method == "POST":
        form = DownloaderForm(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
            stripped_urls = map(lambda x: x.strip(), form_data.get("content", "").split("\n"))
            unique_urls = dict.fromkeys(stripped_urls).keys()
            playlist = form_data.get("playlist", False)
            selected_format = DownloadFormat.get_format_from_cache(format_id = form_data.get("format")) 
            output_dir = os.path.join(MEDIA_ROOT, request.user.username)
            added_to_queue_count = 0
            for url in unique_urls:
                if len(url) == 0:
                    continue
                elif len(url) > MAX_URL_LENGTH: 
                    messages.error(request, f"{url} bude přeskočena, protože je příliš dlouhá ...")
                else:
                    added_to_queue_count += 1
                    new_dl_req = DownloadRequest.objects.create(url=url, format=selected_format, user=request.user)
                    task = download_items.delay(url=url, ydl_opts=selected_format.yt_dl_opts, playlist=playlist, output_dir=output_dir, dl_req_id=new_dl_req.id)
                    new_dl_req.task = TaskResult.objects.get(task_id = task.id)
                    new_dl_req.save()
            messages.info(request, f"{added_to_queue_count} stahování zařazeno do fronty. ")
            return redirect("my_requests")
    else:
        form = DownloaderForm()
    template = loader.get_template('downloader.html')
    content = {
        "title": "Nové stahování",
        "form": form,
    }
    return HttpResponse(template.render(content, request))

@login_required(login_url='login_page')
def file_manager(request):
    if request.user.is_superuser and request.GET.get('username') is not None:
        username = request.GET.get('username')
        #messages.info(request, f"Prohlížíte si stažené soubory uživatele {username}.")
        title = f"Soubory uživatele {username}"
    else:
        username = request.user.username
        title = f"Soubory"
    folder = os.path.join(MEDIA_ROOT, username)

    if request.method == "POST":
        files = get_files_in_folder_as_choices(folder)
        form = FileForm(files, request.POST)
        if form.is_valid():
            form_files = form.cleaned_data["files"]
            if form_files:
                delete_files(folder, form_files)
                messages.info(request, f"Úspěšně jsem odstranil {len(form_files)} souborů. ")
            else: 
                messages.warning(request, "Nebyl vybrán žádný soubor k odtranění. ")
        else:
            for _, errors in form.errors.items():
                messages.error(request, errors)
        base_url = reverse('file_manager')
        query_string =  f"?{urlencode({'username': username})}" if request.user.is_superuser else ""
        return redirect(f"{base_url}{query_string}")
    else:
        files = get_files_in_folder_as_choices(folder)
        form = FileForm(file_list=files)
        template = loader.get_template('file_manager.html')
        content = {
            "title": title,
            "username": username,
            "form": form,
            "action_url": "file_manager",
            "submit_button_text" : "Odstranit vybrané soubory",
        }
        return HttpResponse(template.render(content, request))


@login_required(login_url='login_page')
def my_requests(request):
    template = loader.get_template('my_requests.html')
    page_number = request.GET.get('page', 1) 
    dl_requests = DownloadRequest.objects.filter(user=request.user, task__isnull=False).order_by("-task__date_created").select_related("task", "format").prefetch_related("downloadedfile_set")
    paginator_dl_requests = Paginator(dl_requests, MY_REQUESTS_PAGE_SIZE)
    page = paginator_dl_requests.get_page(page_number)
    content = {
        "title": "Moje požadavky",
        "dl_requests": page,
    }
    return HttpResponse(template.render(content, request))

@csrf_protect
def login_page(request):
    if request.user.is_authenticated:
        return redirect('downloader')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_url = request.GET.get('next', 'downloader') 
        else:
            messages.error(request, 'Uživatelské jméno nebo heslo není správné!')
            next_url = 'login_page'
        return redirect(next_url)
    template = loader.get_template('login_page.html')
    form = LoginForm()
    content = {
        "title": "Přihlášení",
        "form": form,
        "action_url": "login_page",
        "submit_button_text" : "Přihlásit se",
        "upper_text": "Zapomněli jste heslo ? "
    }
    return HttpResponse(template.render(content, request))


@login_required(login_url='login_page')
def logout_page(request):
    logout(request)
    messages.warning(request, 'Byl jste odhášen.')
    return redirect('login_page')


@login_required(login_url='login_page')
def protected_serve(request, path):
    if request.user.is_superuser and request.GET.get('username') is not None:
        username = request.GET.get('username')
    else:
        username = request.user.username
    filename = os.path.split(path)[1]
    document_root = os.path.join(MEDIA_ROOT,username) 
    return serve(request, filename, document_root)

@login_required(login_url='login_page')
def password_change(request):
    if request.method == "POST":
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, "Změna hesla proběhla úspěšně. ")
            redirect("downloader")
    else:
        form = PasswordChangeForm(user=request.user)
    template = loader.get_template('simple_form.html')
    content = {
        "title": "Změna hesla",
        "form": form,
        "action_url": "password_change",
        "submit_button_text" : "Změnit heslo",
    }
    return HttpResponse(template.render(content, request))

@login_required
def api_files(request):
    username = request.GET.get('username') if request.user.is_superuser and request.GET.get('username') is not None else request.user.username
    folder = os.path.join(MEDIA_ROOT, username)
    files = get_files_in_folder(folder, sorted=False)
    return JsonResponse({"files": files})

@login_required
def api_my_requests(request):
    page_number = request.GET.get('page', 1) 
    dl_requests = DownloadRequest.objects.filter(user=request.user, task__isnull=False).order_by("-task__date_created").select_related("task", "format").prefetch_related("downloadedfile_set")
    paginator_dl_requests = Paginator(dl_requests, MY_REQUESTS_PAGE_SIZE)
    page = paginator_dl_requests.get_page(page_number)
    serializable_page = []
    for obj in page:
        temp_dict = obj.as_dict()
        temp_dict.update({"downloaded_files": [file.filename for file in obj.downloadedfile_set.all()]})
        serializable_page.append(temp_dict)
    return JsonResponse({"my_requests": serializable_page})