from .health import router as health_router
from .pricing import router as pricing_router
from .products import router as products_router
from .catalog import router as catalog_router
from .auth import router as auth_router
from .voice import router as voice_router
from .social import router as social_router
from .chat import router as chat_router
from .commerce import router as commerce_router
from .orders import router as orders_router
from .commerce_hub import router as commerce_hub_router
from .bhashini import router as bhashini_router
from .cart import router as cart_router
from .address import router as address_router
from .checkout import router as checkout_router
from .marketplace import router as marketplace_router

__all__ = [
    "health_router",
    "pricing_router",
    "products_router",
    "catalog_router",
    "auth_router",
    "voice_router",
    "social_router",
    "chat_router",
    "commerce_router",
    "orders_router",
    "commerce_hub_router",
    "bhashini_router",
    "cart_router",
    "address_router",
    "checkout_router",
    "marketplace_router",
]
