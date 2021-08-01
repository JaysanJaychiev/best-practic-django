# render для возврата response html
#get_object_or_404 возвратить или показать баг
from django.shortcuts import render, get_object_or_404
#встроенный пагинтор
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail #импорт для отправки имейлов
from django.views.generic import ListView

from .models import Post, Comment #импортируем модели пост и комметы
from .forms import EmailPostForm, CommentForm #импортиеруем формы емайла и комента



class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = "blog/post/list.html"



def post_share(request, post_id):
    #Получение статьи по идентификатору
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False
    if request.method == 'POST':
        #Форма была отправлена  на сохранение.
        form = EmailPostForm(request.POST)
        if form.is_valid():
            #Все поля формы прошли валидацию.
            cd = form.cleaned_data
            # ... Отправка электронной почты.
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} ({cd['email']}) recommends you reading '{post.title}'"
            message = f"Read '{post.title}' at {post_url}\n\n{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'gurin@gmail.com', [cd['to']])
            sent = True
            return render(request, 'blog/post/share.html', {'post':post, 'form': form, 'sent': sent})
    else:
        form = EmailPostForm()
        return render(request, 'blog/post/share.html', {'post':post, 'form': form, 'sent': sent})


def post_list(request):
    object_list = Post.published.all()
    paginator = Paginator(object_list, 3) #По 3 статьи на каждой странице.
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        #Если страница не является целым числом, возвращаем первую страницу.
        posts = paginator.page(1)
    except EmptyPage:
        #Если номер страницы больше, чем общее количество страниц, возвращаем последнюю.
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/post/list.html', {'page': page, 'posts': posts})




def post_detail(request, year, month, day, post): #эта функция для отображения статьи
    post = get_object_or_404(Post, slug=post, status='published', publish__year=year, publish__month=month, publish__day=day)

    
    comments = post.comments.filter(active=True)#Для получения всех активных коментриев QuerySet
    new_comment = None #для сохранения созданного коментария пока что None
    if request.method == 'POST':
        # Пользователь отправил комантарий.
        comment_form = CommentForm(data=request.POST)#ComentForm Для инициализации формы при GET-запросе, если получаем POST запрос то заполняем форму данными и валидируем с помошью is_valid() если форма заполнена не корректно отображаем html шаблон
        if comment_form.is_valid():
            #если все поля успешно прошли валидацию создаем new-comment
            #создаем коментайрий, но пока не сохраняем в базе данных
            new_comment = comment_form.save(commit=False)#commit=False обьект создан но не сохранен в Базе Данных
            #привязываем комантарий к текущей статье.
            new_comment.post = post
            
            #Сохраняем комаентарий в базе данных.
            new_comment.save()
        else:
            comment_form = CommentForm()
        return render(request, 'blog/post/detail.html', {'post': post,
                                                        'comments': comments,
                                                        'new_comment': new_comment,
                                                        'comment-form': comment_form})

