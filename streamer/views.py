from django.shortcuts import render, redirect
from django.utils import timezone
from bets.models import Match, Bet
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
# Create your views here.


@login_required
def streamer_home(request):
    matches = Match.objects.filter(streamer_id=request.user.id).filter(is_active=True)
    context = {
        'matches' : matches,
    }
    
    return render(request, 'streamer/home.html', context)

@login_required
def add_match(request):

    if request.method == "POST":
        streamer_id = request.user.id
        streamer_name = request.user.username
        name = request.POST.get("match_name")
        pub_date = timezone.now()
        new_match = Match(streamer_id=streamer_id, streamer_name=streamer_name, name=name, pub_date=pub_date)
        new_match.save()
        return redirect('home')

    else:
        return render(request, 'streamer/add_match.html')

@login_required
def begin_stream(request):


    match_id = request.POST.get("match_id")
    bets = Bet.objects.filter(match_id=match_id)
    match = Match.objects.get(pk=match_id)
    match.in_progress = True
    
    match.save()
    
    for bet in bets:
        bet.is_started=True
        bet.is_active=True
        bet.save()
   
    return redirect('home')

@login_required
def enter_stats(request):


    match_id = request.POST.get("match_id")
    match = Match.objects.get(pk=match_id)
 
    context = {
        'match' : match,
    }
   
    return render(request, 'streamer/enter_stats.html', context)

@login_required
def end_stream(request):
    match_id = request.POST.get("match_id")
    match = Match.objects.get(pk=match_id)
    match.in_progress=False
    match.is_finished=True
    match.save()
    return redirect('home')

@login_required
def confirm_stats(request):

    match_id = request.POST.get("match_id")
    match = Match.objects.filter(pk=match_id)
    kills = int(request.POST.get("kills"))
    pos = int(request.POST.get("position"))



    bets = Bet.objects.filter(match_id=match_id).filter(is_taken=True)

    for b in bets:
        usr1 = User.objects.get(username=b.usr)
        usr2 = User.objects.get(username=b.taker)
        b.is_active = False
        b.is_finished = True
        b.save()

        if b.is_taken:
            if b.bet_type == 1: #streamer vic

                total = b.bet_wager + b.bet_payout
                if pos == 1: #streamer won
                    usr1.profile.coins += total
                    b.user_winner = True
                else:
                    usr2.profile.coins += total

            elif  b.bet_type == 2:
                if pos <= 3: #streamer top 3
                    usr1.profile.coins += total
                    b.user_winner = True
                else:
                    usr2.profile.coins += total

            elif  b.bet_type == 3:
                if pos <= 5: #streamer top 5
                    usr1.profile.coins += total
                    b.user_winner = True
                else:
                    usr2.profile.coins += total

            elif  b.bet_type == 4:
                if pos <= 10: #streamer top 10
                    usr1.profile.coins += total
                    b.user_winner = True
                else:
                    usr2.profile.coins += total

            elif  b.bet_type == 5:
                if pos <= b.bet_finish: #under hit
                    if b.bet_over_position:
                        usr2.profile.coins += total
                    else:
                        usr1.profile.coins += total
                        b.user_winner = True
                else:
                    if b.bet_over_position:
                        usr1.profile.coins += total
                        b.user_winner = True
                    else:
                        usr2.profile.coins += total

            else:
                if kills <= b.bet_kills: #under hit
                    if b.bet_over_kills:
                        usr2.profile.coins += total
                    else:
                        usr1.profile.coins += total
                        b.user_winner = True
                else:
                    if b.bet_over_kills:
                        usr1.profile.coins += total
                        b.user_winner = True
                    else:
                        usr2.profile.coins += total
            b.save()
            usr1.profile.save()
            usr2.profile.save()

        else:
            usr1.profile.coins += b.bet_wager
            usr1.profile.save()
            continue

    match.update(is_entered=True)
    match.update(kills=kills)
    match.update(position=pos)
    match.update(is_active=False)
   
    messages.success(request, f'Stats have been entered!')
   

    return redirect('home')

