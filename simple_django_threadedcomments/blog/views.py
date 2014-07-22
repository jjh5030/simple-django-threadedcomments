from django.shortcuts import render
from .models import Post, ThreadedComment
from .forms import CommentForm

from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, render, redirect, get_object_or_404, RequestContext

def home(request):
	last_posts = Post.objects.all().order_by('-created_at')[:3]
	context_dict = {'last_posts': last_posts}
	return render(request, 'home.html', context_dict)

def single_post(request, post_id):

	single_post = get_object_or_404(Post, pk=post_id)

	if request.method == "POST":
		form = CommentForm(data=request.POST)
		if form.is_valid():
			comment = form.save(commit=False)

			parent = form['parent_id'].value()

			if form.cleaned_data['parent_id'] != '': 
				parent_comment = get_object_or_404(ThreadedComment, pk=parent)
				comment.parent = parent_comment
				comment.post = single_post
				comment.save()
			else:
				comment.post = single_post
				comment.save()

			return HttpResponseRedirect(reverse('single_post', args=(post_id,)))
		else:
			print "INVALID FORM"
	else:
		form = CommentForm()

	comment_tree = ThreadedComment.objects.filter(post=single_post)

	return render_to_response('post.html', locals(), context_instance=RequestContext(request))	