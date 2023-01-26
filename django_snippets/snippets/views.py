from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.views.generic import ListView, CreateView
from django_snippets import settings
from django.views.generic import RedirectView
from snippets.models import Snippet, Language
from snippets.forms import SnippetForm
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User 

class LoginFormView(LoginView):
    template_name = 'login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(settings.LOGIN_REDIRECT_URL)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Iniciar sesión'
        return context


class LogoutView(RedirectView):
    pattern_name = 'login'

    def dispatch(self, request, *args, **kwargs):
        logout(request)
        return super().dispatch(request, *args, **kwargs)

class IndexView(ListView):
    model = Snippet
    template_name = 'index.html'
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class SnippetListView(ListView):
    model = Snippet
    template_name = 'snippets/snippet_list.html'
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Snippets'
        return context



class Snippet_Add(CreateView):
    model = Snippet
    form_class = SnippetForm
    template_name = 'snippets/snippet_add.html'
    success_url = reverse_lazy('index')

    def post(self, request, *args, **kwargs):
        if request.method == "POST":
            form= SnippetForm(request.POST)
            if form.is_valid():
                post=form.save(commit=False)
                slug_language =  get_object_or_404(Language, id=request.POST['language'])
                print(slug_language)
                post.user = request.user
                post.slug = slug_language.slug
                post.save()
                return redirect("index")

def language(request, slug_url, id):
    snippets = Snippet.objects.filter(slug=slug_url)
    snippets_all = Snippet.objects.get(id=id)
    print(snippets)
    print(snippets_all)
    context = {
        'snippets':snippets,
        'snippets_all':snippets_all,
    }
    return render(request, 'snippets/snippet.html', context)

        
""" def user_snippets(request, id):
    if request.user.is_authenticated:
        user = User.objects.get(id=id)
        #snippets = Snippet.objects.get(id=id)
        snippets_all = Snippet.objects.all()
        print(snippets_all)
        publico = 'Publico'
        privado = 'Privado'
        context = {
            #'snippets':snippets,
            'publico':publico,
            'privado':privado,
            'snippets_all':snippets_all,
        }                
        return render(request, 'snippets/user_snippets.html', context) """
            
                
class UserListView(ListView):
    model = Snippet
    template_name = 'snippets/user_snippets.html'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['publico'] = 'publico'
        context['privado'] = 'privado'
        return context

                


def snippet_edit(request, id):
    snippet = Snippet.objects.get(pk = id)

    if request.method == "GET":
        form = SnippetForm(instance = snippet)
        #print(form)
        contexto = {
            "form" : form
        }
        return render(request, 'snippets/snippet_add.html', contexto)

    elif request.method == "POST":
        form = SnippetForm(request.POST, instance=snippet)
        print(form)

        if form.is_valid():
            post=form.save(commit=False)
            slug_language =  get_object_or_404(Language, id=request.POST['language'])
            print(slug_language)
            post.slug = slug_language.slug
            post.save()
            return redirect("index")

    
def snippet_delete(request,id):
    post = Snippet.objects.get(pk=id)
    if request.method == "POST":
        if post.user == request.user:
            post.delete()
            return redirect("index")
