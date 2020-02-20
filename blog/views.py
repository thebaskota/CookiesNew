from django.shortcuts import render, get_object_or_404, HttpResponse
from .models import Post, StoreCoke as Store
from django.contrib.auth.models import User
from django.views.generic import ( 
    ListView, 
    DetailView, 
    CreateView,
    UpdateView,
    DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

# posts = [
#     {
#         'author': 'Ram Pd',
#         'title' : 'Blog post 1',
#         'content': 'First Post Content',
#         'date_posted': 'August 28 2019'
#     },
#     {
#         'author': 'Sita Maya',
#         'title' : 'Blog post 2',
#         'content': 'Second Post Content',
#         'date_posted': 'August 27 2019'
#     },
# ]  
#   data = request.POST.get("name")
#   print(data)

# Create your views here.
def home(request):
    
    context = {
        'posts_context': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)

class PostListView( ListView):
    model = Post
    template_name = 'blog/home.html' #<app>/<model>_<viewtype>.html
    context_object_name = 'posts_context'
    ordering = ['-date_posted']
    paginate_by = 2

class UserPostListView( ListView):
    model = Post
    template_name = 'blog/user_post.html' 
    context_object_name = 'posts_context'
    paginate_by = 2

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    # Overriding form_valid method to pass our logged in author as the author of the blog.
    # If we dont do this we will get an integrity error saying author is not passed
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    # How is this view Routing to post-detail ?
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form) 

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author: # Checking if current user is author of the post
            return True
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post

    success_url = '/'
    
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author: # Checking if current user is author of the post
            return True
        return False

def about(request):
    model = Store
    data = request.POST.get("name")
    print(data)
    print(" print this ")
    return render(request, 'blog/about.html',{'title_presented':'about'})
