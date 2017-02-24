import abc


class Listener(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def receive_message(self, message):
        pass