from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django_filters.views import FilterView

from django.contrib import messages # メッセージフレームワーク

from .filters import ItemFilter
from .forms import ItemForm
from .models import Item


# Create your views here.
# 検索一覧画面
class ItemFilterView(FilterView):
    model = Item

    # デフォルトの並び順を新しい順とする
    queryset = Item.objects.all().order_by('-created_at')

    # django-filter用設定
    filterset_class = ItemFilter
    strict = False

    # 1ページあたりの表示件数
    paginate_by = 10

    # 検索条件をセッションに保存する
    def get(self, request, **kwargs):
        if request.GET:
            request.session['query'] = request.GET
        else:
            request.GET = request.GET.copy()
            if 'query' in request.session.keys():
                for key in request.session['query'].keys():
                    request.GET[key] = request.session['query'][key]

        return super().get(request, **kwargs)


# 詳細画面
class ItemDetailView(DetailView):
    model = Item


# 登録画面
class ItemCreateView(CreateView):
    model = Item
    form_class = ItemForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):

        messages.success(self.request, '登録しました。')
        return super().form_valid(form)


# 更新画面
class ItemUpdateView(UpdateView):
    model = Item
    form_class = ItemForm
    success_url = reverse_lazy('index')

    # 以下メッセージングを実装したメソッド
    def form_valid(self, form):

        messages.success(self.request, '変更内容を保存しました。')
        return super().form_valid(form)


# 削除画面
class ItemDeleteView(DeleteView):
    model = Item
    success_url = reverse_lazy('index')


    # 以下削除メッセージ表示メソッド（メッセージングFW）
    def delete(self, request, *args, **kwargs):

        result = super().delete(request, *args, **kwargs)

        messages.success(self.request, '削除しました。')
        return result
