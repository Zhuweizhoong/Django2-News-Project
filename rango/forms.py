#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author:49429
# datetime:2019/5/13 16:20
# software: PyCharm

from django import forms
from rango.models import Page,Category
from django.views.decorators.csrf import csrf_protect


class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=64, help_text='Plz enter category name!')
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)
    # slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Category
        # fields = ('title', 'url', 'views')
        fields = ('name', )


class PageForm(forms.ModelForm):
    title = forms.CharField(max_length=128, help_text="Please enter the title of the page.")
    url = forms.URLField(max_length=200, help_text="Please enter the URL of the page.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    def clean(self):
        cleaned_data = self.cleaned_data
        url = cleaned_data.get('url')

        # If url is not empty and doesn't start with 'http://',
        # then prepend 'http://'.
        if url and not url.startswith('http://'):
            url = 'http://' + url
            cleaned_data['url'] = url
        return cleaned_data

    class Meta:
        # Provide an association between the ModelForm and a model
        model = Page
        # What fields do we want to include in our form?
        # This way we don't need every field in the model present.
        # Some fields may allow NULL values, so we may not want to include them...
        # Here, we are hiding the foreign key.
        # we can either exclude the category field from the form,

        exclude = ('category',)
        #or specify the fields to include (i.e. not include the category field)
        # fields = ('title', 'url', 'views')