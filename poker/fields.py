from django import forms


POSITION_CHOICES = (
    ('SB', 'SB'),
    ('BB', 'BB'),
    ('UTG', 'UTG'),
    ('UTG1', 'UTG+1'),
    ('UTG2', 'UTG+2'),
    ('LJ', 'LJ'),
    ('HJ', 'HJ'),
    ('CO', 'CO'),
    ('BTN', 'BTN'),
    
)

STACK_CHOICES = (
    ('50', '50'),
    ('100', '100'),
    ('150', '150'),
    ('200', '200'),
    ('250', '250'),
    ('300', '300'),
    ('350', '350'),
    ('400', '400'),
    ('450', '450'),
    ('500', '500'),
    ('550', '550'),
    ('600', '600'),
    ('650', '650'),
    ('700', '700'),
    ('750', '750'),
    ('800', '800'),
    ('850', '850'),
    ('900', '900'),
    ('950', '950'),
    ('1000', '1000'),
)

ACTION_CHOICES = (
   {'check', 'Check'},
   {'bet', 'Bet'},
   {'call', 'Call'},
   {'raise', 'Raise'},
   ('fd', 'Fold'),
   {'3bet', '3 Bet'},
   {'4bet', '4 Bet'},
   ('sh', 'Shove')
)

STAKES_CHOICES = (
    ('00', 'All'),
    ('12', '1/2'),
    ('13', '1/3'),
    ('25', '2/5'),
    ('55', '5/5'),
    ('510', '5/10'),
    ('2040', '20/40'),
)

TYPE_CHOICES = (
    ('BET_SIZE', 'Bet Sizing'),
    ('COP', 'Cop'),
    ('ODDS', 'Odds'),
    ('HAND_SELECT', 'Hand Selection'),
    ('GAME_SELECT','Game Selection'),
    ('OTHER', 'Other'),
)
STREET_CHOICES = (
    ('PREFLOP','Preflop'),
    ('FLOP', 'FLOP'),
    ('TURN', 'Turn'),
    ('RIVER', 'River'),
)

RESULTS_CHOICES = (
     ('won', 'Won'),
     ('lost', 'Lost')
 )

IMAGE_CHOICES = (
    ('hro', 'Hero'),
    ('vil', 'Villian'),
    ('lag', 'Lag'),
    ('tag', 'Tag',),
    ('pro', 'Pro'), 
    ('yug', 'Young Gun'),
    ('cls', 'Calling Station'),
    ('tom', 'Tight Old Man'),
    ('nit', 'Nit'),
    ('lap', 'Loose Passive'),
    ('unk', 'Unknown'),
)

CARD_CHOICES = (
    ('Unk', '?'),
    ('As', 'A\u2660'),
    ('2s', '2\u2660'),
    ('3s', '3\u2660'),
    ('4s', '4\u2660'),
    ('5s', '5\u2660'),
    ('6s', '6\u2660'),
    ('7s', '7\u2660'),
    ('8s', '8\u2660'),
    ('9s', '9\u2660'),
    ('10s', '10\u2660'),
    ('Js', 'J\u2660'),
    ('Qs', 'Q\u2660'),
    ('Ks', 'K\u2660'),
    ('Ah', 'A\u2661'),
    ('2h', '2\u2661'),
    ('3h', '3\u2661'),
    ('4h', '4\u2661'),
    ('5h', '5\u2661'),
    ('6h', '6\u2661'),
    ('7h', '7\u2661'),
    ('8h', '8\u2661'),
    ('9h', '9\u2661'),
    ('10h', '10\u2661'),
    ('Jh', 'J\u2661'),
    ('Qh', 'Q\u2661'),
    ('Kh', 'K\u2661'),
    ('Ac', 'A\u2663'),
    ('2c', '2\u2663'),
    ('3c', '3\u2663'),
    ('4c', '4\u2663'),
    ('5c', '5\u2663'),
    ('6c', '6\u2663'),
    ('7c', '7\u2663'),
    ('8c', '8\u2663'),
    ('9c', '9\u2663'),
    ('10c', '10\u2663'),
    ('Jc', 'J\u2663'),
    ('Qc', 'Q\u2663'),
    ('Kc', 'K\u2663'),
    ('Ad', 'A\u2662'),
    ('2d', '2\u2662'),
    ('3d', '3\u2662'),
    ('4d', '4\u2662'),
    ('5d', '5\u2662'),
    ('6d', '6\u2662'),
    ('7d', '7\u2662'),
    ('8d', '8\u2662'),
    ('9d', '9\u2662'),
    ('10d', '10\u2662'),
    ('Jd', 'J\u2662'),
    ('Qd', 'Q\u2662'),
    ('Kd', 'K\u2662'),
)
class EmptyChoiceField(forms.ChoiceField):
    def __init__(self, choices=(), empty_label=None, required=True, widget=None, label=None,
                 initial=None, help_text=None, *args, **kwargs):

        # prepend an empty label if it exists (and field is not required!)
        if not required and empty_label is not None:
            choices = tuple([(u'', empty_label)] + list(choices))

        super(EmptyChoiceField, self).__init__(choices=choices, required=required, widget=widget, label=label,
                                        initial=initial, help_text=help_text, *args, **kwargs)