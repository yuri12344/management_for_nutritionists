from email import message
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.contrib import auth
from .utils import password_is_valid, email_html
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.messages import constants
from django.contrib import messages
import os
from django.conf import settings
from .models import Ativacao
from hashlib import sha256
import ipdb


def cadastro(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('/pacientes')
        return render(request, 'cadastro.html')
    
    elif request.method == 'POST':
        usuario = request.POST.get('usuario')
        email = request.POST.get('email')
        confirmar_senha = request.POST.get('confirmar_senha')
        senha = request.POST.get('senha')

        if not password_is_valid(request, senha, confirmar_senha):
            return redirect('cadastro')

        try:
            user = User.objects.create_user(usuario, email, senha, is_active=False)
            user.save()

            token = sha256(f"{usuario} + {email}".encode()).hexdigest()
            Ativacao(token=token, user=user).save()


            template_path = os.path.join(settings.BASE_DIR, 'autenticacao/templates/emails/cadastro_confirmado.html')
            email_html(template_path, 'Confirmação de cadastro', [email], usuario=usuario, link_ativacao=f"127.0.0.1:8000/auth/ativar_conta/{token}")
            messages.add_message(request, constants.SUCCESS, 'Usuario cadastrado com sucesso.') 
            return redirect('logar')
        except Exception as e:
            print(e)
            messages.add_message(request, constants.ERROR, 'Usuário já existe.') 
            return redirect('cadastro')


def logar(request):
    if request.method == 'GET':
        if request.user.is_authenticated: return redirect('/pacientes')
        return render(request, "logar.html")

    elif request.method == 'POST':
        username = request.POST.get('usuario')
        password = request.POST.get('senha')

        usuario = auth.authenticate(username=username, password=password)
        

        if not usuario:
            messages.add_message(request, constants.ERROR, 'Usuário ou senha inválidos.')
            return redirect('logar')
        else:
            auth.login(request, usuario)
            return redirect('pacientes')

def sair(request):
    auth.logout(request)
    return redirect('logar')


def ativar_conta(request, token):
    token = get_object_or_404(Ativacao, token=token)
    if token.ativo:
        messages.add_message(request, constants.ERROR, 'Conta já ativada.')
        return redirect('logar')
    user = User.objects.get(username=token.user.username)
    user.is_active = True
    user.save()
    token.ativo = True
    token.save()
    messages.add_message(request, constants.SUCCESS, 'Conta ativa com sucesso')
    return redirect('logar')


