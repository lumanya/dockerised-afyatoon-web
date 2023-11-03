# Generated by Django 4.2.7 on 2023-11-02 14:34

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields
import wagtail.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('comics', '0008_alter_comicseries_author_alter_comicseries_category'),
        ('wagtailimages', '0025_alter_image_file_alter_rendition_file'),
        ('wagtailcore', '0089_log_entry_data_json_null_to_object'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnimationEpisode',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('description', wagtail.fields.RichTextField(help_text='Enter description of the episode', null=True)),
                ('created_date', models.DateField(auto_now=True, null=True, verbose_name='Created date')),
                ('updated_date', models.DateField(auto_now=True, null=True, verbose_name='Updated date')),
                ('episode_number', models.IntegerField(null=True)),
                ('episode_image', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image')),
            ],
            options={
                'verbose_name': 'Anaimation Episode',
                'verbose_name_plural': 'Animation Episodes',
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='AnimationSeriesPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
            ],
            options={
                'verbose_name': 'Animation Series Page',
                'verbose_name_plural': 'Animation Series Pages',
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='EpisodeImageOrderable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('image', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image')),
                ('page', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='episode_images', to='animations.animationepisode')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AnimationSeries',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('description', wagtail.fields.RichTextField(help_text='Enter description of the series', null=True)),
                ('created_date', models.DateField(auto_now=True, null=True, verbose_name='Created date')),
                ('updated_date', models.DateField(auto_now=True, null=True, verbose_name='Updated date')),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='authors', to='comics.author')),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='categories', to='comics.category')),
                ('series_image', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='wagtailimages.image')),
            ],
            options={
                'verbose_name': 'Animation Series',
                'verbose_name_plural': 'Animation Series(s)',
            },
            bases=('wagtailcore.page',),
        ),
    ]