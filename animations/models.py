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

from comics.models import Category, Author


    
class AnimationEpisode(Page):
    """ Page that contains a comic episode """
    parent_page_type = ['animations.AnimationSeries']
    subpage_types = []

    description = RichTextField(blank=False, null=True, help_text='Enter description of the episode')
    episode_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    video = models.CharField(null=True, blank=False, max_length=255, help_text='Enter video url')
    created_date = models.DateField("Created date", blank=False, null=True, auto_now=True)
    updated_date = models.DateField("Updated date", blank=False, null=True, auto_now=True)
    episode_number = models.IntegerField(blank=False, null=True)

    # editor panels configuration
    content_panels = [
        FieldPanel('title'),
        FieldPanel('description'),
        FieldPanel('episode_image'),
        FieldPanel('episode_number'),       
        FieldPanel('video'),
       
    ]

    def get_absolute_url(self):
        return self.get_url()

    def __str__(self):
        return self.title
    
    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        all_episodes = AnimationEpisode.objects.sibling_of(self).live().public().order_by('-first_published_at')
        context['episodes'] = all_episodes
        return context
    
    class Meta:
        verbose_name = 'Anaimation Episode'
        verbose_name_plural = 'Animation Episodes'

    template = 'animations/animation_episode.html'


class AnimationSeries(Page):
    """ Comic Series Page """
    parent_page_type = ['animations.AnimationSeriesPage']
    subpage_types = ['animations.AnimationEpisode']
    
    description = RichTextField(blank=False, null=True, help_text='Enter description of the series')
    series_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
    )
    created_date = models.DateField("Created date", blank=False, null=True, auto_now=True)
    updated_date = models.DateField("Updated date", blank=False, null=True, auto_now=True)
    category = models.ForeignKey(Category, related_name='categories', on_delete=models.SET_NULL, null=True)
    author = models.ForeignKey(Author, related_name='authors', on_delete=models.SET_NULL, null=True)

    content_panels = [
        MultiFieldPanel([
            FieldPanel('title'),
            FieldPanel('description'),
            FieldPanel('series_image'),          
        ], heading='Series information'),
        FieldPanel('author'),
        FieldPanel('category'),
    ]

    class Meta:
        verbose_name = 'Animation Series'
        verbose_name_plural = 'Animation Series(s)'

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context['episodes'] = AnimationSeries.get_descendants(self).live().public().order_by('-first_published_at')
        return context
    
    template = 'animations/animation_series.html'


class AnimationSeriesPage(Page):
    """ List all Series """
    max_count_per_parent = 1

    parent_page_type = ['home.HomePage']
    subpage_types = ['animations.AnimationSeries']

    class Meta:
        verbose_name = 'Animation Series Page'
        verbose_name_plural = 'Animation Series Pages'

    def get_context(self,request, *args, **kwargs):

        context = super().get_context(self, request, *args, **kwargs)
        context['series_list'] = AnimationSeries.objects.live().public().order_by('-first_published_at')
        
        context['categories'] = Category.objects.all()

        return context 
    template = 'animations/animation_series_page.html'


