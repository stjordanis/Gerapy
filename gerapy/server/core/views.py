import json

from django.shortcuts import render
import requests
from .utils import scrapyd_url, log_url
from .models import Client
from django.core.serializers import serialize
from django.http import HttpResponse
from django.forms.models import model_to_dict
from scrapyd_api import ScrapydAPI


def index(request):
    return render(request, 'index.html')


def client_index(request):
    return HttpResponse(serialize('json', Client.objects.order_by('-id')))


def client_show(request, id):
    if request.method == 'GET':
        return HttpResponse(json.dumps(model_to_dict(Client.objects.get(id=id))))


def client_update(request, id):
    if request.method == 'POST':
        client = Client.objects.filter(id=id)
        data = json.loads(request.body)
        client.update(**data)
        return HttpResponse(json.dumps(model_to_dict(Client.objects.get(id=id))))


def list_projects(request, id):
    if request.method == 'GET':
        client = Client.objects.get(id=id)
        scrapyd = ScrapydAPI(scrapyd_url(client.ip, client.port))
        projects = scrapyd.list_projects()
        return HttpResponse(json.dumps(projects))


def list_spiders(request, id, project):
    if request.method == 'GET':
        client = Client.objects.get(id=id)
        scrapyd = ScrapydAPI(scrapyd_url(client.ip, client.port))
        spiders = scrapyd.list_spiders(project)
        spiders = [{'name': spider, 'id': index + 1} for index, spider in enumerate(spiders)]
        return HttpResponse(json.dumps(spiders))


def start_spider(request, id, project, spider):
    if request.method == 'GET':
        client = Client.objects.get(id=id)
        scrapyd = ScrapydAPI(scrapyd_url(client.ip, client.port))
        result = scrapyd.schedule(project, spider)
        return HttpResponse(json.dumps({'job': result}))


def list_jobs(request, id, project):
    if request.method == 'GET':
        client = Client.objects.get(id=id)
        scrapyd = ScrapydAPI(scrapyd_url(client.ip, client.port))
        result = scrapyd.list_jobs(project)
        jobs = []
        statuses = ['pending', 'running', 'finished']
        for status in statuses:
            for job in result.get(status):
                job['status'] = status
                jobs.append(job)
        return HttpResponse(json.dumps(jobs))


def job_log(request, id, project, spider, job):
    if request.method == 'GET':
        client = Client.objects.get(id=id)
        url = log_url(client.ip, client.port, project, spider, job)
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                text = response.text
                return HttpResponse(text[-5000:-1])
            if response.status_code == 404:
                return HttpResponse('日志不存在')
        except requests.ConnectionError:
            return HttpResponse('日志加载失败')
            
def cancel_job(request, id, project, job):
    if request.method == 'GET':
        client = Client.objects.get(id=id)
        scrapyd = ScrapydAPI(scrapyd_url(client.ip, client.port))
        result = scrapyd.cancel(project, job)
        return HttpResponse(json.dumps(result))