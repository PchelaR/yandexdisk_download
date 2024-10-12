import requests

from django.shortcuts import redirect
from django.urls import reverse

from django.views import View
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from allauth.socialaccount.models import SocialToken
from django.shortcuts import render


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'app/index.html'

    def post(self, request):
        disk_url = request.POST.get('disk_id').strip()

        if disk_url.startswith("https://disk.yandex.ru/d/") or disk_url.startswith("https://disk.yandex.com/d/"):
            disk_id = disk_url.split("/d/")[-1]
        elif len(disk_url) == 20:
            disk_id = disk_url
        else:
            return render(request, 'app/index.html', {
                'error': 'Неверный формат ссылки или ID.'
            })

        return redirect(reverse('file_list', kwargs={'disk_id': disk_id}))


class FileListView(LoginRequiredMixin, View):
    def get(self, request, disk_id):
        try:
            token = SocialToken.objects.get(account__user=request.user, account__provider='yandex').token
        except SocialToken.DoesNotExist:
            return render(request, 'app/file_list.html', {'error': 'Токен доступа не найден.'})

        headers = {
            'Authorization': f'OAuth {token}'
        }

        full_url = f'https://disk.yandex.ru/d/{disk_id}'
        api_url = f'https://cloud-api.yandex.net/v1/disk/public/resources?public_key={full_url}'

        response = requests.get(api_url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            items = data.get('_embedded', {}).get('items', [])
            download_links = []

            for item in items:
                public_key = item['public_key']
                download_url = self.get_download_url(public_key, headers)

                if download_url:
                    download_links.append({
                        'name': item['name'],
                        'download_url': download_url
                    })

            return render(request, 'app/file_list.html', {
                'download_links': download_links
            })
        else:
            return render(request, 'app/file_list.html', {
                'error': f'{response.status_code} - {response.text}'
            })

    @staticmethod
    def get_download_url(public_key, headers):
        download_api_url = 'https://cloud-api.yandex.net/v1/disk/public/resources/download'
        params = {'public_key': public_key}
        response = requests.get(download_api_url, headers=headers, params=params)

        if response.status_code == 200:
            download_data = response.json()
            return download_data.get('href')
        else:
            return None


class LoginView(TemplateView):
    template_name = 'app/login.html'
