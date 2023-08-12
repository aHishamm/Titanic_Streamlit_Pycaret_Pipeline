def replace_titles(x):
    title=x['Title']
    if title in ['Don', 'Major', 'Capt', 'Jonkheer', 'Rev', 'Col']:
        return 'Mr'
    if title in ['Countess', 'Mme']:
        return 'Mrs'
    if title in ['Mlle', 'Ms']:
        return 'Miss'
    if title =='Dr':
        if x['Sex']=='Male':
            return 'Mr'
        else:
            return 'Mrs'
    else:
        return title
