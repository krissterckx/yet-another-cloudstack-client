from base import Base


class Settings(Base):

    def flag(self, name, default=False):
        return self.get_flag(name, default)

    def set_until_completion(self, poll=True):
        self.set_flag('until_completion', poll)

    def get_until_completion(self):
        return self.flag('until_completion')
