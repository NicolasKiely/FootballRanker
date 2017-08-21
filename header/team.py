''' Team class '''

class Team(object):
    def __init__(self, name, home, mascot):
        self.name = name
        self.home = home
        self.mascot = mascot

    def __str__(self):
        return '%s, %s, %s' % (self.name, self.home, self.mascot)

    @classmethod
    def load_record(cls, record):
        ''' Creates team from string record '''
        fields = [x.strip() for x in record.split(',')]
        return Team(*fields)
