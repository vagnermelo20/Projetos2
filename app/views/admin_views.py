from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpRequest, HttpResponseNotAllowed, Http404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.db.models import Count, F
from django.utils.dateparse import parse_date, parse_time
import json
import logging

from ..models import UserRegistration, Batch, BatchAssignment
from .utils import _send_whatsapp_approval_notification, format_phone

logger = logging.getLogger(__name__)

@csrf_exempt
@login_required
def approve_user(request: HttpRequest, user_id: int):
    """
    Aprova um usuário pendente, atribui a um lote e envia notificação.
    (Geralmente usado por uma interface administrativa ou API interna)
    """
    if request.method == 'POST':
        user = get_object_or_404(UserRegistration, id=user_id)

        if user.status != 'pending':
            logger.warning(f"Tentativa de aprovar usuário já processado: {user_id}")
            return JsonResponse({'error': 'Usuário já foi processado.'}, status=400)

        # Encontra um lote disponível (com vagas)
        available_batch = Batch.objects.annotate(
            users_count=Count('batchassignment')
        ).filter(users_count__lt=F('max_participants')).order_by('date', 'time').first()

        if not available_batch:
            logger.warning("Nenhum lote disponível para aprovação de usuário.")
            return JsonResponse({'error': 'Nenhum lote disponível. Crie um novo lote primeiro.'}, status=400)

        # Atribui o usuário ao lote
        BatchAssignment.objects.create(user=user, batch=available_batch)
        user.status = 'approved'
        user.save()
        logger.info(f"Usuário {user.id} aprovado e atribuído ao lote {available_batch.id}")

        # Envia notificação via WhatsApp usando a função auxiliar
        _send_whatsapp_approval_notification(user, available_batch)
        
        return JsonResponse({'message': f'Usuário {user.name} aprovado e notificado.'})

    return HttpResponseNotAllowed(['POST'])

@csrf_exempt
@login_required
def create_batch(request: HttpRequest):
    """Cria um novo lote."""
    if request.method == 'POST':
        try:
            # Tenta ler como JSON primeiro (comum em APIs)
            try:
                data = json.loads(request.body)
                is_json = True
            except json.JSONDecodeError:
                # Se falhar, tenta ler como dados de formulário
                data = request.POST
                is_json = False

            date_str = data.get('date')
            time_str = data.get('time')
            max_participants_str = data.get('max_participants')
            message_template = data.get('message_template', 'Olá {nome}, seu agendamento foi confirmado para {data} às {hora}.') # Template padrão

            if not all([date_str, time_str, max_participants_str]):
                 return JsonResponse({'error': 'Data, hora e capacidade são obrigatórios.'}, status=400)

            batch = Batch.objects.create(
                date=parse_date(date_str),
                time=parse_time(time_str),
                max_participants=int(max_participants_str),
                message_template=message_template
            )
            logger.info(f"Lote criado: {batch.id} - {batch.date} {batch.time}")

            # Responde de acordo com o tipo de requisição
            if is_json or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'message': 'Lote criado com sucesso!', 'batch_id': batch.id})
            else:
                # Redireciona se for um envio de formulário HTML padrão
                return redirect('admin_dashboard') # Use o nome da URL

        except (ValueError, TypeError) as e:
             logger.error(f"Erro de valor/tipo ao criar lote: {e}")
             return JsonResponse({'error': 'Dados inválidos fornecidos.'}, status=400)
        except Exception as e:
            logger.error(f"Erro ao criar lote: {e}")
            return JsonResponse({'error': 'Ocorreu um erro interno.'}, status=500)

    return HttpResponseNotAllowed(['POST'])

@login_required
def admin_dashboard(request: HttpRequest):
    """Exibe o painel administrativo com usuários pendentes e lotes."""
    pending_users = UserRegistration.objects.filter(status='pending').order_by('created_at')
    batches = Batch.objects.annotate(users_count=Count('batchassignment')).order_by('date', 'time')
    
    # Busca o último lote criado para referência do template de mensagem
    last_batch = Batch.objects.order_by('-created_at').first()

    # Format phone numbers for display
    for user in pending_users:
        user.formatted_phone = format_phone(user.phone_number)

    context = {
        'pending_users': pending_users,
        'batches': batches,
        'last_batch': last_batch,
        'error_message': request.GET.get('error') # Para exibir mensagens de erro (ex: no_batches)
    }
    
    return render(request, 'admin_dashboard.html', context)

@login_required
def admin_approve_user(request: HttpRequest, user_id: int):
    """Aprova um usuário a partir do painel administrativo."""
    if request.method == 'POST':
        user = get_object_or_404(UserRegistration, id=user_id)

        if user.status != 'pending':
            logger.warning(f"Admin tentou aprovar usuário já processado: {user_id}")
            return redirect('admin_dashboard') # Redireciona de volta

        # Encontra um lote disponível
        available_batch = Batch.objects.annotate(
            users_count=Count('batchassignment')
        ).filter(users_count__lt=F('max_participants')).order_by('date', 'time').first()

        if not available_batch:
            logger.warning("Admin tentou aprovar usuário sem lote disponível.")
            return redirect('/admin/dashboard/?error=no_batches') # Ou use reverse('admin_dashboard') + query params

        # Atribui o usuário ao lote
        BatchAssignment.objects.create(user=user, batch=available_batch)
        user.status = 'approved'
        user.save()
        logger.info(f"Admin aprovou usuário {user.id} para o lote {available_batch.id}")

        # Envia notificação via WhatsApp
        _send_whatsapp_approval_notification(user, available_batch)
        
        return redirect('admin_dashboard')

    # Redireciona se não for POST
    return redirect('admin_dashboard')


@login_required
def admin_create_batch_auto(request: HttpRequest):
    """Cria múltiplos lotes automaticamente baseado em seleção de dias, horários e capacidade."""
    if request.method == 'POST':
        try:
            # Obtém os dados do formulário
            selected_days = request.POST.getlist('selected_days')
            selected_hours = request.POST.getlist('selected_hours')
            max_participants = request.POST.get('max_participants')
            message_template = request.POST.get('message_template', 'Olá {nome}, seu agendamento foi confirmado para {data} às {hora}.')
            
            if not all([selected_days, selected_hours, max_participants]):
                logger.error("Dados incompletos para criação automática de lotes")
                return JsonResponse({'error': 'Selecione pelo menos um dia, um horário e a capacidade.'}, status=400)
            
            created_batches = []
            
            # Cria um lote para cada combinação dia/hora
            for day in selected_days:
                for hour in selected_hours:
                    try:
                        date = parse_date(day)
                        time = parse_time(hour)
                        
                        # Verifica se já existe um lote para esta data/hora
                        existing = Batch.objects.filter(date=date, time=time).exists()
                        if existing:
                            logger.info(f"Lote para {date} {time} já existe, pulando.")
                            continue
                            
                        batch = Batch.objects.create(
                            date=date,
                            time=time,
                            max_participants=int(max_participants),
                            message_template=message_template
                        )
                        created_batches.append(f"{batch.date.strftime('%d/%m/%Y')} {batch.time.strftime('%H:%M')}")
                        logger.info(f"Lote automático criado: {batch.id} - {batch.date} {batch.time}")
                    except Exception as e:
                        logger.error(f"Erro ao criar lote para {day} {hour}: {e}")
                        
            # Verifica se foi criado algum lote
            if not created_batches:
                return JsonResponse({
                    'message': 'Nenhum lote novo foi criado. Verifique se os lotes já existem.'
                }, status=200)
                
            # Responde de acordo com o tipo de requisição
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'message': 'Lotes criados com sucesso!', 
                    'count': len(created_batches),
                    'batches': created_batches
                })
            else:
                # Redireciona se for um envio de formulário HTML padrão
                return redirect('admin_dashboard')
                
        except (ValueError, TypeError) as e:
            logger.error(f"Erro de valor/tipo ao criar lotes automáticos: {e}")
            return JsonResponse({'error': 'Dados inválidos fornecidos.'}, status=400)
        except Exception as e:
            logger.error(f"Erro ao criar lotes automáticos: {e}")
            return JsonResponse({'error': 'Ocorreu um erro interno.'}, status=500)

    return HttpResponseNotAllowed(['POST'])

@login_required
def admin_delete_batch(request: HttpRequest, batch_id: int):
    """Deleta um lote existente, mas mantém as mensagens enviadas."""
    if request.method == 'POST':
        batch = get_object_or_404(Batch, id=batch_id)

        # Remove todas as associações de usuários ao lote
        BatchAssignment.objects.filter(batch=batch).delete()
        logger.info(f"Todas as associações de usuários ao lote {batch_id} foram removidas.")

        # Exclui o lote
        batch_date = batch.date
        batch_time = batch.time
        batch.delete()
        logger.info(f"Lote {batch_id} ({batch_date} {batch_time}) excluído com sucesso.")
        return redirect('admin_dashboard')

    # Redireciona se não for POST
    return redirect('admin_dashboard')

@login_required
def batch_details(request: HttpRequest, batch_id: int):
    """Exibe detalhes de um lote específico e seus usuários."""
    batch = get_object_or_404(Batch, id=batch_id)
    
    # Obter todos os usuários associados ao lote
    batch_assignments = BatchAssignment.objects.filter(batch=batch).select_related('user')
    
    # Format phone numbers for display
    for assignment in batch_assignments:
        assignment.user.formatted_phone = format_phone(assignment.user.phone_number)
    
    context = {
        'batch': batch,
        'assignments': batch_assignments
    }
    
    return render(request, 'batch_details.html', context)

@login_required
def admin_reject_user(request: HttpRequest, user_id: int):
    """Rejeita um usuário a partir do painel administrativo."""
    if request.method == 'POST':
        user = get_object_or_404(UserRegistration, id=user_id)

        if user.status != 'pending':
            logger.warning(f"Admin tentou rejeitar usuário já processado: {user_id}")
            return redirect('admin_dashboard')

        # Atualiza o status para rejeitado
        user.status = 'rejected'
        user.save()
        logger.info(f"Admin rejeitou usuário {user.id}")

        # Opcionalmente, enviar uma notificação ao usuário sobre a rejeição
        # Você pode criar uma função como _send_whatsapp_rejection_notification se desejar
        
        return redirect('admin_dashboard')

    # Redireciona se não for POST
    return redirect('admin_dashboard')