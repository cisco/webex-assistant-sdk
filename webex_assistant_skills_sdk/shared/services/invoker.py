from dependency_injector.wiring import Provide


class Invoker():
    crypto_service_: Provide[Types.CRYPTO_SERVICE]
