from django.conf.urls import url
from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator, OriginValidator

#from order.consumers import ReceiveOrderConsumer
#from yearend.consumers import YearendConsumer
from strip.consumers import FahkeekConsumer, BoothConsumer

application = ProtocolTypeRouter({
    # Empty for now (http->django views is added by default)
    'websocket': AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                [
                    url(r"^alpha/$", FahkeekConsumer),
                    path('', FahkeekConsumer),
                    path('/postcard/', BoothConsumer),
                ]
            )
        )
    )
})

