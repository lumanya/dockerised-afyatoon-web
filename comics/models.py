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


@register_snippet
class Category(models.Model):
    """ Category snippet """
    name = models.CharField(max_length=255, blank=False)
    description = RichTextField(blank=True, help_text='Enter description of the category')

    panels = [
        MultiFieldPanel([
            FieldPanel('name'),
            FieldPanel('description'),
        ], heading='Category information'),
    ]

    def __str__(self):
        return self.name

@register_snippet
class Author(models.Model):
    """ Author snippet """
    name = models.CharField(max_length=255, blank=False)
    author_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    description = RichTextField(blank=True)

    panels = [
        MultiFieldPanel([
            FieldPanel('name'),
            FieldPanel('description'),
            FieldPanel('author_image'),
        ], heading='Author information'),
    ]

    def __str__(self):
        return self.name
    
class ComicEpisode(Page):
    """ Page that contains a comic episode """
    parent_page_type = ['comics.ComicSeries']
    subpage_types = []

    description = RichTextField(blank=False, null=True, help_text='Enter description of the episode')
    episode_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    created_date = models.DateField("Created date", blank=False, null=True, auto_now=True)
    updated_date = models.DateField("Updated date", blank=False, null=True, auto_now=True)
    episode_number = models.IntegerField(blank=False, null=True)

    # editor panels configuration
    content_panels = [
        FieldPanel('title'),
        FieldPanel('description'),
        FieldPanel('episode_image'),
        FieldPanel('episode_number'),
        MultiFieldPanel([
            InlinePanel('episode_images', min_num=1),
        ], heading='Episode Images'),
       
    ]

    def get_absolute_url(self):
        return self.get_url()

    def __str__(self):
        return self.title
    
    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        all_episodes = ComicEpisode.objects.sibling_of(self).live().public().order_by('-first_published_at')
        context['episodes'] = all_episodes
        return context
    
    class Meta:
        verbose_name = 'Comic Episode'
        verbose_name_plural = 'Comic Episodes'

    template = 'comics/comic_episode.html'


class ComicSeries(Page):
    """ Comic Series Page """
    parent_page_type = ['comics.ComicSeriesPage']
    subpage_types = ['comics.ComicEpisode']
    
    description = RichTextField(blank=False, null=True, help_text='Enter description of the series')
    series_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
    )
    created_date = models.DateField("Created date", blank=False, null=True, auto_now=True)
    updated_date = models.DateField("Updated date", blank=False, null=True, auto_now=True)
    category = models.ForeignKey(Category, related_name='animation_categories', on_delete=models.SET_NULL, null=True)
    author = models.ForeignKey(Author, related_name='animation_authors', on_delete=models.SET_NULL, null=True)

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
        verbose_name = 'Comic Series'
        verbose_name_plural = 'Comic Series(s)'

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context['episodes'] = ComicSeries.get_descendants(self).live().public().order_by('-first_published_at')
        return context
    
    template = 'comics/comic_series.html'

                  



class ComicSeriesPage(Page):
    """ List all Series """
    max_count_per_parent = 1

    parent_page_type = ['home.HomePage']
    subpage_types = ['comics.ComicSeries']

    class Meta:
        verbose_name = 'Comic Series Page'
        verbose_name_plural = 'Comic Series Pages'

    def get_context(self,request, *args, **kwargs):

        context = super().get_context(self, request, *args, **kwargs)
        context['series_list'] = ComicSeries.objects.live().public().order_by('-first_published_at')
        
        context['categories'] = Category.objects.all()

        return context 
    template = 'comics/comic_series_page.html'

class EpisodeImageOrderable(Orderable):
    """ Orderable comics images of particlar episode """
    page = ParentalKey(ComicEpisode, on_delete=models.CASCADE, related_name='episode_images')
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    panels = [
        FieldPanel('image'),
    ]