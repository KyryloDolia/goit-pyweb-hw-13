from django import forms
from django.core.exceptions import ValidationError
from .models import Author, Quote, Tag

class QuoteForm(forms.Form):
    quote = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'placeholder': 'Write your quote here...',
                'class': 'quote',
            }
        ),
        required=True
    )

    author = forms.CharField(
        max_length=50,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Author'
            }
        ),
        required=True
    )

    tags = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Tags ( life, world, love )'
            }
        ),
        required=False
    )

    def clean_tags(self):
        tags_str = self.cleaned_data.get('tags', '')
        if tags_str:
            tags = [tag.strip() for tag in tags_str.split(',')]
            if any(len(tag) > 50 for tag in tags):
                raise ValidationError("Each tag must be less than 50 characters.")
        return tags_str

    def save(self, user, commit=True):
        quote_text = self.cleaned_data['quote']
        author_fullname = self.cleaned_data['author']
        tags_str = self.cleaned_data['tags']

        # Retrieve or create the author
        author, _ = Author.objects.get_or_create(fullname=author_fullname, user=user)

        # Create the quote
        quote = Quote(quote=quote_text, author=author, user=user)

        if commit:
            quote.save()

            # Process tags
            if tags_str:
                tags = [tag.strip() for tag in tags_str.split(',')]
                for tag_name in tags:
                    tag, _ = Tag.objects.get_or_create(name=tag_name, user=user)
                    quote.tags.add(tag)

        return quote