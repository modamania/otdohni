from django import dispatch


user_voted = dispatch.Signal(providing_args=['user', 'voted_item'])
