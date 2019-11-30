from django import forms


class RegisterForm(forms.Form):
    DATABASE_ADMINISTRATOR = 'DBA'
    SALESPERSON = 'Sales'
    job_choice = (
        (DATABASE_ADMINISTRATOR, 'Database_Administrator'),
        (SALESPERSON, 'Salesperson')
    )
    username = forms.CharField(label="用户名", max_length=32, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label="密码", max_length=32, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="确认密码", max_length=32,
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="邮箱地址", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    phone = forms.IntegerField(label="phone", widget=forms.NumberInput(attrs={'class': 'form-control'}))
    job_title=forms.ChoiceField(label="title",choices=job_choice)
    street = forms.CharField(label="street",max_length=64,widget=forms.TextInput(attrs={'class': 'form-control'}))
    city = forms.CharField(label="city",max_length=32,widget=forms.TextInput(attrs={'class': 'form-control'}))
    state = forms.CharField(label="state",max_length=2,widget=forms.TextInput(attrs={'class': 'form-control'}))
    zip_code = forms.IntegerField(label="zip",max_length=5,widget=forms.NumberInput(attrs={'class': 'form-control'}))
