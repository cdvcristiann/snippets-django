from django.forms import  ModelForm
from snippets.models import Snippet

class SnippetForm(ModelForm):
    class Meta:
        model = Snippet
        fields = '__all__'
        exclude = ('user',)

