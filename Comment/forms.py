from django import forms
import mistune
from .models import Comment

class CommentForm(forms. ModelForm):
    nickname = forms.CharField(
        label='昵称',
        max_length=10,
        widget=forms.widgets.Input(
            attrs={'rows':6,'cols':60,'class':'form-control','placeholder':"昵称",'aria-describedby':"basic-addon1"},
        )
    )
    # email = forms.CharField(
    #     label='Email',
    #     max_length=50,
    #     widget=forms.widgets.Input(
    #         attrs={'class': 'form-control', 'style': "width:60%;"},
    #     )
    # )
    # website = forms.CharField(
    #     label='网站',
    #     max_length=100,
    #     widget=forms.widgets.Input(
    #         attrs={'class': 'form-control', 'style': "width:60%;"},
    #     )
    # )
    content = forms.CharField(
        label='内容',
        max_length=200,
        widget=forms.widgets.Textarea(
            attrs={'rows':6,'cols':60,'class':'form-control','placeholder':"评论内容",'aria-describedby':"basic-addon1"},
        )
    )
    def clean_content(self):
        content = self.cleaned_data.get('content')
        if len(content)<5:
            raise forms.ValidationError('太短了吧，根本不能满足呢')
        content = mistune.markdown(content)
        return content
    class Meta:
        model = Comment
        fields = ['nickname','content']
