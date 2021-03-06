from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

PATH_SEPARATOR = getattr(settings, 'COMMENT_PATH_SEPARATOR', '/')
PATH_DIGITS = getattr(settings, 'COMMENT_PATH_DIGITS', 10)

# Create your models here.
class Post(models.Model): 
	""" Blog entry """ 
	title = models.CharField(max_length=255) 
	text = models.TextField() 
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return str(self.title)

class ThreadedComment(models.Model): 
	""" Threaded comments for blog posts """ 
	post = models.ForeignKey(Post) 
	comment = models.TextField() 
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	parent = models.ForeignKey('self', null=True, blank=True, default=None, related_name='children', verbose_name=_('Parent'))
	last_child = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='end child', verbose_name=_('Last child'))
	tree_path = models.TextField(_('Tree path'), editable=False)

	@property
	def depth(self):
		return len(self.tree_path.split(PATH_SEPARATOR))

	@property
	def depth_adjusted(self):
		return len(self.tree_path.split(PATH_SEPARATOR)) - 1

	@property
	def root_id(self):
		return int(self.tree_path.split(PATH_SEPARATOR)[0])

	@property
	def root_path(self):
		return ThreadedComment.objects.filter(pk__in=self.tree_path.split(PATH_SEPARATOR)[:-1])

	def save(self, *args, **kwargs):
		skip_tree_path = kwargs.pop('skip_tree_path', False)
		super(ThreadedComment, self).save(*args, **kwargs)
		if skip_tree_path:
			return None

		tree_path = unicode(self.pk).zfill(PATH_DIGITS)
		if self.parent:
			tree_path = PATH_SEPARATOR.join((self.parent.tree_path, tree_path))

			self.parent.last_child = self
			ThreadedComment.objects.filter(pk=self.parent_id).update(last_child=self)

		self.tree_path = tree_path
		ThreadedComment.objects.filter(pk=self.pk).update(tree_path=self.tree_path)

	class Meta(object):
		ordering = ('tree_path',)
		verbose_name = _('Threaded comment')
		verbose_name_plural = _('Threaded comments')

	def __unicode__(self):
		return str(self.comment[:100])