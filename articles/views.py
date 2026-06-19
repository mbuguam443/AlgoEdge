from django.views.generic import ListView, DetailView
from .models import Post, Category

class BlogListView(ListView):
    model = Post
    template_name = 'articles/blog.html'
    context_object_name = 'posts'
    paginate_by = 9
    def get_queryset(self):
        qs = Post.objects.filter(status='published')
        cat = self.request.GET.get('category')
        if cat: qs = qs.filter(category__slug=cat)
        return qs
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['categories'] = Category.objects.all()
        ctx['featured'] = Post.objects.filter(status='published', is_featured=True)[:3]
        return ctx

class BlogDetailView(DetailView):
    model = Post
    template_name = 'articles/blog_detail.html'
    context_object_name = 'post'
    def get_object(self):
        obj = super().get_object()
        obj.views += 1
        obj.save(update_fields=['views'])
        return obj
