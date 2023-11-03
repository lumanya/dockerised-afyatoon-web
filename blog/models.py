from django.db import models
from django import forms 
from django.shortcuts import render
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase
from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.snippets.models import register_snippet
from wagtail import hooks

from comics.models import Author, Category
from .blocks import ImageBlocks, BlockQuoteBlock, ParagraphBlock, TitleBlock


class BlogListingPage(Page):
    """ List all blogs """
    max_count_per_parent = 1

    parent_page_type = ['home.HomePage']
    subpage_types = ['blog.BlogPage']

    class Meta:
        verbose_name = 'Blog Listing Page'
        verbose_name_plural = 'Blog Listing Pages'

    def get_context(self,request, *args, **kwargs):

        context = super().get_context(self, request, *args, **kwargs)
        context['blog_list'] = BlogPage.objects.live().public().order_by('-first_published_at') 
        context['categories'] = Category.objects.all()      
        

        return context 
    template = 'blog/blog_listing_page.html'


class BlogPage(Page):
    """ Blog Detail Page"""
    parent_page_type = ['blog.BlogListingPage']
    subpage_types = []

    post_summary = models.CharField(max_length=250, blank=True, null=True)
    blog_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    blog_author = models.ForeignKey(
        'comics.Author',
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name='blog_authors'
    )
    created_date = models.DateField("Post Date", auto_now=True)
    updated_date = models.DateField("Updated Date", auto_now=True)

    content = StreamField([
        ('image', ImageBlocks()),
        ('blockquote', BlockQuoteBlock()),
        ('paragraph', ParagraphBlock()),
        ('title', TitleBlock()),
    ], null=True, blank=True, use_json_field=True
    )


    content_panels =  [
        FieldPanel('title'),
        FieldPanel('post_summary'),
        FieldPanel('blog_image'),
        FieldPanel('blog_author'),
        FieldPanel('content'),
    ]

    class Meta:
        verbose_name = 'Blog Page'
        verbose_name_plural = 'Blog Pages'


    template = 'blog/blog_page.html'