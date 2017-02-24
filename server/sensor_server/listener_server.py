from twisted.internet import protocol, reactor, endpoints
import json
import os
import sys
import importlib
import inspect


def should_listener_be_instantiated(class_object):
    if class_object is None:
        return False
    if not inspect.isclass(class_object):
        return False
    if 'receive_message' not in class_object.__dict__:
        return False
    if inspect.isabstract(class_object):
        return False
    return True


class SensorListener(protocol.Protocol):
    def __init__(self, factory):
        self._factory = factory

    def dataReceived(self, data):
        try:
            data_json = json.loads(data)
        except ValueError:
            return
        self._factory.notify_listeners(data_json)


class SensorListenerFactory(protocol.Factory):
    def __init__(self, applications):
        self._listeners = []
        self.register_listeners(applications)
    
    def buildProtocol(self, addr):
        return SensorListener(self)

    def notify_listeners(self, message):
        for lst in self._listeners:
            lst.receive_message(message)
    
    def register_listeners(self, applications):
        for app in applications:
            try:
                listener_module = importlib.import_module('.listener', app)
            except ImportError:
                continue

            for member in dir(listener_module):
                class_obj = getattr(listener_module, member)
                if should_listener_be_instantiated(class_obj):
                    self._listeners.append(class_obj())


if __name__ == "__main__":
    proj_path = "../"
    sys.path.append(proj_path)
    os.chdir(proj_path)

    from secureauto import wsgi
    
    settings = importlib.import_module(os.environ["DJANGO_SETTINGS_MODULE"])
    
    endpoint = endpoints.TCP4ServerEndpoint(reactor, 10475)
    endpoint.listen(SensorListenerFactory(settings.INSTALLED_APPS))
    reactor.run()