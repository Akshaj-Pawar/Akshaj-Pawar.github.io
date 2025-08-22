from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.template.defaultfilters import linebreaksbr
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from firstapp.models import Posts, Comment
from django.views.generic.edit import CreateView
import docx
from .forms import CommentForm, SearchForm

posts = Posts.objects.all()
def index(request):
    return render(request, 'index.html', {'postss': posts})

def wip(request):
    post = get_object_or_404(Posts, pk=2)
    doc = docx.Document(post.file)
    text = []
    for para in doc.paragraphs:
        text.append(para.text) #where para is the text from the file - hopefully with formatting intact
    blog_txt_py = '\n'.join(text) #make sure to convert to a string like so - special command cause you cant otherwise turn lists into strings
    blog_txt_html = linebreaksbr(blog_txt_py)

    return render(request, 'content-p.html', {'blog_text': blog_txt_html}) #here is where we use the file command - this is linked to the new function in urls

    post.views += 1
    post.save()

def post_content(request, pk):
    post = get_object_or_404(Posts, pk=pk)
    post.views += 1
    post.save()
    return render(request, 'document_display.html', {'post': post}) #this was a bit fiddly - the issue revolved around the post1 variable havign to be sent to the html template as a directory
    #this is just going to take the current url and save it as a name

    #now we get the view updater - currently doesn't seem to be updating


def like(request, pk):
    post = get_object_or_404(Posts, id=request.POST.get('post_id'))
    post.likes.add(request.user)
    return HttpResponseRedirect(reverse('post_page', args=[str(pk)]))

    # it's actually going to the template and pulling the post id of the post from the button.
    # So we've generated a post via a different method and as part fo the tmeplate we have a button that we coded to store the id function
    # now we're getting that information from the button

    #this request user stuff is largely precoded as part of django


#def display_total_likes(self): - unhash this is somehting goes wrong and it might work, i got rid of this cause it didnt seem to be doing anything but maybe it is its hard to remember
    #return self.likes.count()

class AddComment(CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'comment_form.html'

    def form_valid(self, form):
        post = get_object_or_404(Posts, pk=self.kwargs['pk'])
        form.instance.Posts = post
        return super().form_valid(form)

    def get_success_url(self):
        pk_value = self.kwargs['pk']
        return reverse('post_page', kwargs={'pk': pk_value})

    #fields = '__all__'

def Search(request):
    form = SearchForm(request.POST)
    return render(request, 'searching_form.html', {'form': form})
    if form.is_valid():
        search_Q = form.cleaned_data['Q']
        post = search_content(request, search_Q)
        return render(request, 'document_display.html', {'post': post})
    else:
        form = SearchForm


def search_content(request, search_Q):
    post = get_object_or_404(Posts, pk=search_Q)
    post.views += 1
    post.save()
    return post
