from __future__ import unicode_literals

from django.contrib.auth import get_user_model
from django import forms
from django.utils.translation import ugettext_lazy as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field

from .models import Entry

User = get_user_model()


class EntryForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(EntryForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        # self.fields["username"].widget.input_type = "email"  # ugly hack

        self.helper.layout = Layout(
            Field('title', placeholder=_("Enter entry title"), autofocus=""),
            Field('categories'),
            Field('text', placeholder=_("Enter entry content")),
            Submit('button_save', _('Save'),
                   css_class="btn btn-lg btn-primary btn-block"),
            )

    class Meta:
        model = Entry
        fields = ['title', 'categories', 'text']
