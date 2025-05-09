# Generated by Django 4.2.16 on 2024-11-26 01:54

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields
import wagtail.blocks
import wagtail.fields
import wagtail.images.blocks
import wagtailiconchooser.blocks
import wagtailmetadata.models
import wagtailvideos.blocks


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('wagtailcore', '0091_remove_revision_submitted_for_moderation'),
        ('wagtailimages', '0025_alter_image_file_alter_rendition_file'),
    ]

    operations = [
        migrations.CreateModel(
            name='LastAddedProducts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=255, verbose_name='Last added products title')),
                ('filters', models.CharField(blank=True, max_length=255, verbose_name='Additional filters')),
                ('display', models.PositiveIntegerField(default=8, verbose_name='Number of products in the block')),
            ],
        ),
        migrations.CreateModel(
            name='PopularCategories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=255, verbose_name='Popular categorues title')),
                ('filters', models.CharField(blank=True, max_length=255, verbose_name='Additional filters')),
                ('display', models.PositiveIntegerField(default=8, verbose_name='Number of categories in the block')),
            ],
        ),
        migrations.CreateModel(
            name='PopularProducts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=255, verbose_name='Popular products title')),
                ('filters', models.CharField(blank=True, max_length=255, verbose_name='Additional filters')),
                ('display', models.PositiveIntegerField(default=8, verbose_name='Number of products in the block')),
            ],
        ),
        migrations.CreateModel(
            name='PopularQueries',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=255, verbose_name='Popular queries title')),
                ('query_option', models.CharField(choices=[('tags', 'Tags'), ('categories', 'Categories'), ('random', 'Random')], max_length=20, verbose_name='Option')),
                ('display', models.PositiveIntegerField(default=8, verbose_name='Number of items in the block')),
                ('new_tab', models.BooleanField(default=True, verbose_name='Should be opened in a new tab?')),
            ],
        ),
        migrations.CreateModel(
            name='RootPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('keywords', models.CharField(blank=True, max_length=255, verbose_name='Meta keywords')),
                ('search_image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image', verbose_name='Search image')),
            ],
            options={
                'abstract': False,
            },
            bases=(wagtailmetadata.models.MetadataMixin, 'wagtailcore.page', models.Model),
        ),
        migrations.CreateModel(
            name='SimilarProducts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=255, verbose_name='Similar products title')),
                ('filters', models.CharField(blank=True, max_length=255, verbose_name='Additional filters')),
                ('display', models.PositiveIntegerField(default=8, verbose_name='Number of products in the block')),
            ],
        ),
        migrations.CreateModel(
            name='ImagesPage',
            fields=[
                ('rootpage_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='pages.rootpage')),
            ],
            options={
                'abstract': False,
            },
            bases=('pages.rootpage',),
        ),
        migrations.CreateModel(
            name='PaymentMethodsPage',
            fields=[
                ('rootpage_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='pages.rootpage')),
                ('sub_title', models.CharField(blank=True, verbose_name='Sub title')),
                ('body', wagtail.fields.StreamField([('cardpayment', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock()), ('text', wagtail.blocks.RichTextBlock(features=['h2', 'h3', 'h4', 'h5', 'h6', 'ol', 'ul', 'bold', 'italic', 'link']))])), ('balancepayment', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock()), ('text', wagtail.blocks.RichTextBlock(features=['h2', 'h3', 'h4', 'h5', 'h6', 'ol', 'ul', 'bold', 'italic', 'link']))])), ('subscriptions', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock()), ('text', wagtail.blocks.RichTextBlock(features=['h2', 'h3', 'h4', 'h5', 'h6', 'ol', 'ul', 'bold', 'italic', 'link']))]))], verbose_name='Body')),
            ],
            options={
                'abstract': False,
            },
            bases=('pages.rootpage',),
        ),
        migrations.CreateModel(
            name='ProductPage',
            fields=[
                ('rootpage_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='pages.rootpage')),
                ('popular_products', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='pages.popularproducts')),
                ('similar_products', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='pages.similarproducts')),
            ],
            options={
                'abstract': False,
            },
            bases=('pages.rootpage',),
        ),
        migrations.CreateModel(
            name='InformationPage',
            fields=[
                ('rootpage_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='pages.rootpage')),
                ('page_type', models.CharField(choices=[('privacy_and_security', 'Privacy and Security'), ('accessibility', 'Accessibility')], max_length=20, verbose_name='Page type')),
                ('body', wagtail.fields.StreamField([('text', wagtail.blocks.RichTextBlock(features=['h2', 'h3', 'h4', 'h5', 'h6', 'ol', 'ul', 'bold', 'italic', 'link']))], verbose_name='Page body')),
                ('image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image', verbose_name='Image')),
            ],
            options={
                'abstract': False,
            },
            bases=('pages.rootpage',),
        ),
        migrations.CreateModel(
            name='HomePage',
            fields=[
                ('rootpage_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='pages.rootpage')),
                ('sub_title', models.CharField(blank=True, max_length=255, verbose_name='Sub title')),
                ('advertising_blocks', wagtail.fields.StreamField([('singleimageblock', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock()), ('text', wagtail.blocks.RichTextBlock(features=['h2', 'h3', 'h4', 'h5', 'h6', 'ol', 'ul', 'bold', 'italic', 'link'])), ('icon', wagtail.blocks.StructBlock([('icon', wagtailiconchooser.blocks.IconChooserBlock()), ('icon_color', wagtail.blocks.CharBlock())])), ('image', wagtail.images.blocks.ImageChooserBlock()), ('image_position', wagtail.blocks.ChoiceBlock(choices=[('left', 'Left'), ('right', 'Right')]))], template='blocks/singleimageblock.html')), ('multiimagesblock', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock()), ('text', wagtail.blocks.RichTextBlock(features=['h2', 'h3', 'h4', 'h5', 'h6', 'ol', 'ul', 'bold', 'italic', 'link'])), ('icon', wagtail.blocks.StructBlock([('icon', wagtailiconchooser.blocks.IconChooserBlock()), ('icon_color', wagtail.blocks.CharBlock())])), ('images', wagtail.blocks.ListBlock(wagtail.images.blocks.ImageChooserBlock()))], template='blocks/multiimagesblock.html')), ('videoblock', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock()), ('text', wagtail.blocks.RichTextBlock(features=['h2', 'h3', 'h4', 'h5', 'h6', 'ol', 'ul', 'bold', 'italic', 'link'])), ('icon', wagtail.blocks.StructBlock([('icon', wagtailiconchooser.blocks.IconChooserBlock()), ('icon_color', wagtail.blocks.CharBlock())])), ('video', wagtailvideos.blocks.VideoChooserBlock()), ('video_position', wagtail.blocks.ChoiceBlock(choices=[('left', 'Left'), ('right', 'Right')]))], template='blocks/videoblock.html')), ('comparingblock', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock()), ('text', wagtail.blocks.RichTextBlock(features=['h2', 'h3', 'h4', 'h5', 'h6', 'ol', 'ul', 'bold', 'italic', 'link'])), ('icon', wagtail.blocks.StructBlock([('icon', wagtailiconchooser.blocks.IconChooserBlock()), ('icon_color', wagtail.blocks.CharBlock())])), ('image_1', wagtail.images.blocks.ImageChooserBlock()), ('image_2', wagtail.images.blocks.ImageChooserBlock())], template='blocks/comparingblock.html'))], verbose_name='Advertising block')),
                ('last_added_products', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='pages.lastaddedproducts')),
                ('popular_categories', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='pages.popularcategories')),
                ('popular_products', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='pages.popularproducts')),
                ('popular_queries', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='pages.popularqueries')),
            ],
            options={
                'abstract': False,
            },
            bases=('pages.rootpage',),
        ),
        migrations.CreateModel(
            name='FAQPage',
            fields=[
                ('rootpage_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='pages.rootpage')),
                ('sub_title', models.CharField(blank=True, max_length=255, verbose_name='Sub title')),
                ('body', wagtail.fields.StreamField([('block', wagtail.blocks.StructBlock([('question', wagtail.blocks.CharBlock()), ('answer', wagtail.blocks.TextBlock(required=False)), ('link', wagtail.blocks.StructBlock([('link_text', wagtail.blocks.CharBlock(required=False)), ('url', wagtail.blocks.URLBlock(required=False))]))])), ('html', wagtail.blocks.RawHTMLBlock(required=False))], verbose_name='Page body')),
                ('image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image', verbose_name='Image')),
            ],
            options={
                'abstract': False,
            },
            bases=('pages.rootpage',),
        ),
        migrations.CreateModel(
            name='ContactUsPage',
            fields=[
                ('rootpage_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='pages.rootpage')),
                ('sub_title', models.CharField(blank=True, verbose_name='Sub title')),
                ('image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image', verbose_name='Image')),
            ],
            options={
                'abstract': False,
            },
            bases=('pages.rootpage',),
        ),
        migrations.CreateModel(
            name='CategoriesPage',
            fields=[
                ('rootpage_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='pages.rootpage')),
                ('image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image', verbose_name='Image')),
            ],
            options={
                'abstract': False,
            },
            bases=('pages.rootpage',),
        ),
        migrations.CreateModel(
            name='BasketPage',
            fields=[
                ('rootpage_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='pages.rootpage')),
                ('similar_products', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='pages.similarproducts')),
            ],
            options={
                'abstract': False,
            },
            bases=('pages.rootpage',),
        ),
        migrations.CreateModel(
            name='AboutUsPage',
            fields=[
                ('rootpage_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='pages.rootpage')),
                ('about_us_description', models.TextField(blank=True, verbose_name='Short description')),
                ('about_us_detail_title', models.CharField(blank=True, max_length=255, verbose_name='About us detail title')),
                ('about_us_image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image')),
            ],
            options={
                'abstract': False,
            },
            bases=('pages.rootpage',),
        ),
        migrations.CreateModel(
            name='AboutUsDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('title', models.CharField(blank=True, max_length=255, verbose_name='Title')),
                ('text', models.TextField(blank=True, verbose_name='Text')),
                ('page', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='detail_items', to='pages.aboutuspage')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
    ]
