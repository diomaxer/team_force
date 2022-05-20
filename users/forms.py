from django import forms
from django.contrib.auth.forms import AuthenticationForm

from .models import User, Skills


class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'name', 'surname', 'patronymic', 'languages', 'skills', 'hobie', 'password')

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.get_skills_query()
        return user


class LoginForm(forms.Form):
    email = forms.EmailField(max_length=255, required=True)
    password = forms.CharField(widget=forms.PasswordInput())


class UpdateUserSkills(forms.ModelForm):
    """Форма для добавления нвыков через checkbox"""
    skills = forms.ModelMultipleChoiceField(
        queryset=Skills.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label='Все навыки кторые мы знаем',
        required=False,
    )

    class Meta:
        model = User
        fields = ('skills',)


    def add_skills(self, user, old_skills, str_skills):
        """
        Спиксок навыков пользователя очищается и добовлятся заново, чтобы неделать новый url для удаления
        досточно просто убрать галочку
        """
        if str_skills:  # проверка наличия навыков добавленных через строку
            old_skills |= str_skills
        user.skills.clear()
        user.skills.add(*old_skills)
        return user


class UpdateSkills(forms.Form):
    """Форма для добавления навыков через строку"""
    new_skills = forms.CharField(
        max_length=255,
        label='Добавить навыки которого у нас нет',
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Навык1, Навык2'})
    )

    def get_skills_query(self):
        """
        Проверка ноых навыков добавленных в форму на уникальность и поиск старх навыков.
        Создается Queryset из старых и новых наыков
        """
        empty_check = self.cleaned_data['new_skills']
        if empty_check:
            new_user_skills = empty_check.split(', ')   # Получение навыков из строки
            all_skills = [skill.name for skill in Skills.objects.all()]     # Все навыки из модели
            no_repeat_skills = [skill for skill in new_user_skills if skill not in all_skills]  # Новые навыки
            repeat_skills = [skill for skill in new_user_skills if skill in all_skills]     # Старные навыки
            repeat_skills_query = Skills.objects.filter(name__in=repeat_skills)     # query старных навыков
            no_repeat_skills_create_instance = Skills.objects.bulk_create(
                [Skills(name=new_skill) for new_skill in no_repeat_skills]  # создане instance новых навыков
            )
            no_repeat_skills_query = Skills.objects.filter(
                name__in=[skill.name for skill in no_repeat_skills_create_instance]  # получение query навыки
            )
            return repeat_skills_query | no_repeat_skills_query  # объединение query старых и новых навыков
