from django.db import models
from django import forms 
from django.shortcuts import render
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase
from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.snippets.models import register_snippet
from wagtail import hooks

from comics.models import ComicSeriesPage, ComicEpisode, Author, ComicSeries, Category



class HomePage(Page):
    """ Home page model """
    max_count_per_parent = 1

    parent_page_type = ['wagtailcore.Page']

    subpage_types = ['comics.ComicSeriesPage']

    def get_context(self, request, *args, **kwargs):
        context =  super().get_context(request, *args, **kwargs)
        context['episodes'] = ComicEpisode.objects.live().public().order_by('-first_published_at')[:10]
        context['series_list'] = ComicSeries.objects.live().public().order_by('-first_published_at')[:10]
        context['categories'] = Category.objects.all()
        return context
    
    template = 'home.html'
