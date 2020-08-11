from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, JsonResponse
from django.template import loader
from .models import Bet, Match
from django.contrib import messages

from django.utils import timezone
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.db import models
from django.contrib.auth.models import User



@login_required
def streamer(request):
    pk = request.user.id 
    user = User.objects.get(pk=pk)
  
    if request.user.profile.is_streamer:
        return redirect('/streamer')
    else:
        return render(request, 'bets/activate.html')

@login_required
def activate(request):
    referral = request.POST.get("referral")
    if referral == 'stream':
        prof = request.user.profile
        prof.is_streamer = True
        prof.save()
   
        return redirect('/streamer')
    else:
        messages.warning(request, f'Referral code note accepted!')
        return redirect('/bets')


@login_required
def find(request):
    if 'term' in request.GET:
    
        qs = Match.objects.filter(name__istartswith=request.GET.get('term'))
        matches = list()
        for match in qs:
            matches.append(match.name)
      
        return JsonResponse(matches, safe=False)


    if request.method == "POST":

        match_list = Match.objects.filter(name=request.POST.get('match_name')).filter(is_active=True)
        if match_list is None:
            print('here')
            messages.warning(request, f'No match that name!')
            return render(request, 'bets/find_bets.html')
    else:
        match_list = Match.objects.filter(is_active=True).order_by('-pub_date')
    
    match_dict = {}
    for m in match_list:
        
        match_bets = Bet.objects.filter(match_id=m.id).filter(is_taken=False).filter(is_active=True).filter(is_started=False)

        if match_bets:
            match_dict[m] = match_bets
        else:
            match_dict[m] = None

  
    context = {
        'match_dict': match_dict,
    }
  
    return render(request, 'bets/find_bets.html', context)


@login_required
def select(request):
    match_list = Match.objects.order_by('-pub_date')
    context = {
        'match_list': match_list,
    }
  
    return render(request, 'bets/select_match.html', context)

@login_required
def create(request):
    match_id = request.POST.get("match_id")
   
    context = {
        'match_id': match_id,
    }
    return render(request, 'bets/create_bet.html', context)

@login_required
def details(request):

    bet_type = request.POST.get("types")
    match_id = request.POST.get("match_id")
   
    context = {'bet_type': bet_type, 'match_id' : match_id}
    
    return render(request, 'bets/bet_details.html', context)

@login_required
def finalize(request):

    if request.method == "POST":
        
        usr = request.user.username
        match_id = request.POST.get("match_id")
        bet_type = request.POST.get("bet_type")
        bet_wager = request.POST.get("wager")
        bet_payout = request.POST.get("win")
        bet_kills = request.POST.get("kills") if request.POST.get("kills") else 0
        bet_finish = request.POST.get("position") if request.POST.get("position") else 0
        bet_over_position = request.POST.get("ou_yes_no") if request.POST.get("ou_yes_no") else 0
        bet_over_kills = request.POST.get("kills_yes_no") if request.POST.get("kills_yes_no") else 0
        
        
        if request.user.profile.coins < int(bet_wager):
            messages.warning(request, f'You do not have enough coins to place this bet!')
            return redirect('/bets')
        else:    
        
            new_bet = Bet(usr = usr, match_id=match_id, bet_type=bet_type, bet_wager=bet_wager, bet_payout=bet_payout, bet_kills=bet_kills, 
                bet_finish=bet_finish, bet_over_position=bet_over_position, 
                bet_over_kills=bet_over_kills, pub_date=timezone.now())
            new_bet.save()

            messages.success(request, f'Bet has been placed!')
            return redirect('/bets')


        
@login_required
def execute(request):

    bet_id = request.POST.get("bet_id")

    obj = Bet.objects.get(pk=bet_id)

    context = {'obj': obj, 'bet_id' : bet_id}

    if obj.is_taken:
        messages.warning(request, f'Bet has already been taken!')
        return redirect('/bets')

    elif request.user.profile.coins < obj.bet_payout:
        messages.warning(request, f'You do not have enough coins to take this bet!')
        return redirect('/bets')

    elif request.user.username == obj.usr:
        messages.warning(request, f"You cannot take your own bet!")
        return redirect('/bets')
    else:
        return render(request, 'bets/execute_stage1.html', context)


@login_required
def send_execute(request):
    bet_id = request.POST.get("bet_id")

    obj = Bet.objects.get(pk=bet_id)
    match_id = obj.match_id
    obj.taker = request.user.username

    obj.is_taken = True
    obj.save()

    prof = request.user.profile
    prof.coins -= obj.bet_payout
    prof.save()
   
    user = User.objects.get(username=obj.usr)
    user.profile.coins -= obj.bet_wager
    user.profile.save()

    messages.success(request, f'Bet has been taken!')
    return redirect('/bets')

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('/bets')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'bets/change_password.html', {
        'form': form
    })

@login_required
def history(request):
    live = Bet.objects.filter(usr=request.user.username).filter(is_active=True).filter(is_taken=True)
    taken = Bet.objects.filter(taker=request.user.username).filter(is_active=True).filter(is_taken=True)
    pending = Bet.objects.filter(usr=request.user.username).filter(is_active=True).filter(is_taken=False)
    past = Bet.objects.filter(usr=request.user.username).filter(is_finished=True).filter(is_taken=True)
    past_taken = Bet.objects.filter(taker=request.user.username).filter(is_finished=True).filter(is_taken=True)
    
    print('pending')
    print(pending)
    context = {
        'live' : live | taken,
        'pending' : pending,
        'past' : past | past_taken
    }

    return render(request, 'bets/history.html', context)




