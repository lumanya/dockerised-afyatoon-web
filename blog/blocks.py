""" Stream Field live here"""

from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock


class ImageBlocks(blocks.StructBlock):
    image = ImageChooserBlock(required=True)

    class Meta:
        template = 'blocks/image_block.html'
        icon = 'image'
        label = 'Add Image'

class BlockQuoteBlock(blocks.StructBlock):
    quote = blocks.TextBlock(required=True)    

    class Meta:
        template = 'blocks/blockquote_block.html'
        icon = 'openquote'
        label = 'Add Blockquote'

class ParagraphBlock(blocks.RichTextBlock):
    """  Rich Text Block with all features"" """

    

    class Meta:
        template = 'blocks/paragraph_block.html'
        icon = 'pilcrow'
        label = 'Add Paragraph'

class TitleBlock(blocks.StructBlock):

    title = blocks.CharBlock(required=True, help_text="add your title")  

    class Meta:

        template = 'blocks/title_block.html'
        icon='edit'
        label = "Add Title"
