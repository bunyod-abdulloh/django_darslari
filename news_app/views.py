from django.http import Http404, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView

from .models import Category, News
from .forms import ContactForm


def news_List(request):
    news = News.published.all()
    context = {
        'news_list': news,
    }

    return render(request, 'news/news_list.html', context)


def news_detail(request, id):
    news = get_object_or_404(klass=News, pk=id, status=News.Status.Published)
    context = {
        'news': news,
    }
    return render(request, 'news/news_detail.html', context)


def homePageView(request):
    news_list = News.published.all().order_by('-publish_time')
    categories = Category.objects.all()
    context = {
        'news_list': news_list,
        'categories': categories,
    }
    return render(request, 'news/index.html', context)


class HomePageView(TemplateView):
    template_name = 'news/index.html'

    def get(self, request, *args, **kwargs):
        news_list = News.published.all().order_by('-publish_time')[:15]
        categories = Category.objects.all()
        context = {
            'news_list': news_list,
            'categories': categories,
        }
        return self.render_to_response(context)


class ContactPageView(TemplateView):
    template_name = 'news/contact.html'

    def get(self, request, *args, **kwargs):
        form = ContactForm()
        context = {'form': form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        if request.method == 'POST' and form.is_valid():
            form.save()
            return HttpResponse(
                "<h2>Bizga habar yuborganingiz uchun tashakkur! Tez orada javob qaytarishga harakat qilamiz!</h2>")
        context = {
            'form': form,
        }
        return render(request, self.template_name, context)
