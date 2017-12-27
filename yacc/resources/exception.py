

class BadRequest(Exception):
    def __init__(self, error):
        super(BadRequest, self).__init__()
        self.error = 'Bad request'
        self.errortext = error

    def __repr__(self):
        return 'BadRequest: {}'.format(self.errortext)
