from django import forms
from .models import Comment, Blog

class FeedbackForm(forms.Form):
    name = forms.CharField(label="Ваше имя", max_length=100, required=True)
    email = forms.EmailField(label="Email", required=True)
    rating = forms.ChoiceField(
        label="Оцените сайт",
        choices=[('1', 'Плохо'), ('2', 'Нормально'), ('3', 'Хорошо')],
        widget=forms.RadioSelect,
        required=True
    )
    improvements = forms.MultipleChoiceField(
        label="Что можно улучшить?",
        choices=[('design', 'Дизайн'), ('speed', 'Скорость'), ('content', 'Контент')],
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    comments = forms.CharField(label="Комментарий", widget=forms.Textarea, required=False)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        labels = {'text': 'Оставьте комментарий:'}
        widgets = {'text': forms.Textarea(attrs={'rows': 4})}

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'description', 'content', 'image']
        labels = {
            'title': 'Заголовок',
            'description': 'Краткое описание',
            'content': 'Полный текст',
            'image': 'Изображение',
        }
