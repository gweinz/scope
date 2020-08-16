
from django.db import models


class Bet(models.Model):
    usr = models.CharField(max_length=200, default='none')
    taker = models.CharField(max_length=200, default='none')
    match_id = models.IntegerField(default=0, null=0, blank=0)
    bet_type = models.IntegerField(default=0, null=0, blank=0)
    bet_wager = models.IntegerField(default=0, null=0, blank=0)
    bet_payout = models.IntegerField(default=0, null=0, blank=0)
    bet_kills = models.IntegerField(default=0, null=0, blank=0)
    bet_finish = models.IntegerField(default=0, null=0, blank=0)
    bet_over_position = models.IntegerField(default=0, null=0, blank=0)
    bet_over_kills = models.IntegerField(default=0, null=0, blank=0)
   
    pub_date = models.DateTimeField('date published')
    is_active = models.BooleanField(default=True)
    is_taken = models.BooleanField(default=False)
    is_started = models.BooleanField(default=False)
    is_finished = models.BooleanField(default=False)

    user_winner = models.BooleanField(default=False)
    


    def __str__(self):
        if self.bet_type == 1:
            return 'Streamer Victory  ' + '(' + str(self.bet_wager) + ' to win ' + str(self.bet_payout) + ')'
         
        elif self.bet_type == 2:   
            return 'Top 3 Finish ' + '(' + str(self.bet_wager) + ' to win ' + str(self.bet_payout) + ')'

        elif self.bet_type == 3:  
            return 'Top 5 Finish ' + '(' + str(self.bet_wager) + ' to win ' + str(self.bet_payout) + ')'

        elif self.bet_type == 4:  
            return 'Top 10 Finish ' + '(' + str(self.bet_wager) + ' to win ' + str(self.bet_payout) + ')'

        elif self.bet_type == 5: 
            if self.bet_over_position: 
                to_return = 'Finish Outside Top ' + str(self.bet_finish) + ' (' + str(self.bet_wager) + ' to win ' + str(self.bet_payout) + ')'
            else:
                to_return = 'Finish Inside Top ' + str(self.bet_finish) + ' (' + str(self.bet_wager) + ' to win ' + str(self.bet_payout) + ')'

            return to_return

        else: 
            if self.bet_over_kills:
                to_return = 'Over '+ str(self.bet_kills) + ' Kills ' + '(' + str(self.bet_wager) + ' to win ' + str(self.bet_payout) + ')'
            else:
                to_return = 'Under '+ str(self.bet_kills) + ' Kills ' + '(' + str(self.bet_wager) + ' to win ' + str(self.bet_payout) + ')'

            return to_return

    def take(self):
        if self.bet_type == 1:
            return 'No Streamer Victory  ' + '(' + str(self.bet_payout) + ' to win ' + str(self.bet_wager) + ')'
         
        elif self.bet_type == 2:   
            return 'No Top 3 Finish ' + '(' + str(self.bet_payout) + ' to win ' + str(self.bet_wager) + ')'

        elif self.bet_type == 3:  
            return 'No Top 5 Finish ' + '(' + str(self.bet_payout) + ' to win ' + str(self.bet_wager) + ')'

        elif self.bet_type == 4:  
            return 'No Top 10 Finish ' + '(' + str(self.bet_payout) + ' to win ' + str(self.bet_wager) + ')'

        elif self.bet_type == 5: 
            if self.bet_over_position: 
                to_return = 'Finish Inside Top ' + str(self.bet_finish) + ' (' + str(self.bet_payout) + ' to win ' + str(self.bet_wager) + ')'
            else:
                to_return = 'Finish Outside Top ' + str(self.bet_finish) + ' (' + str(self.bet_payout) + ' to win ' + str(self.bet_wager) + ')'

            return to_return

        else: 
            if self.bet_over_kills:
                to_return = 'Under '+ str(self.bet_kills) + ' Kills ' + '(' + str(self.bet_payout) + ' to win ' + str(self.bet_wager) + ')'
            else:
                to_return = 'Over '+ str(self.bet_kills) + ' Kills ' + '(' + str(self.bet_payout) + ' to win ' + str(self.bet_wager) + ')'

            return to_return

    



class Match(models.Model):
    streamer_id = models.IntegerField(default=0, null=0, blank=0)
    streamer_name = models.CharField(max_length=200, default='none')
    name = models.CharField(max_length=200, default='none')
    kills = models.IntegerField(default=0, null=0, blank=0)
    position = models.IntegerField(default=0, null=0, blank=0)
    pub_date = models.DateTimeField('date published')
    is_active = models.BooleanField(default=True)
    in_progress = models.BooleanField(default=False)
    is_finished = models.BooleanField(default=False)
    is_entered = models.BooleanField(default=False)

    def return_bets(self):
        match_bets = Bet.objects.filter(self.id)
        return match_bets

    def __str__(self):
        return self.name

    

    

    

