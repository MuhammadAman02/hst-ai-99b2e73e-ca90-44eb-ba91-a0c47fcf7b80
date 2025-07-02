"""Application configuration management"""

import os
from typing import Optional
from dataclasses import dataclass

@dataclass
class Settings:
    """Application settings"""
    app_name: str = "Nike Shoe Store"
    app_version: str = "1.0.0"
    debug: bool = True
    
    # Server settings
    host: str = "0.0.0.0"
    port: int = 8000
    
    # Store settings
    store_name: str = "Nike Official Store"
    store_tagline: str = "Just Do It"
    currency: str = "USD"
    tax_rate: float = 0.08
    
    # Image settings
    default_image_size: str = "400x400"
    image_quality: str = "high"
    
    # Session settings
    session_timeout: int = 3600
    cart_expiry: int = 7200

def get_settings() -> Settings:
    """Get application settings from environment variables"""
    return Settings(
        app_name=os.getenv("APP_NAME", "Nike Shoe Store"),
        app_version=os.getenv("APP_VERSION", "1.0.0"),
        debug=os.getenv("DEBUG", "true").lower() == "true",
        
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", "8000")),
        
        store_name=os.getenv("STORE_NAME", "Nike Official Store"),
        store_tagline=os.getenv("STORE_TAGLINE", "Just Do It"),
        currency=os.getenv("CURRENCY", "USD"),
        tax_rate=float(os.getenv("TAX_RATE", "0.08")),
        
        default_image_size=os.getenv("DEFAULT_IMAGE_SIZE", "400x400"),
        image_quality=os.getenv("IMAGE_QUALITY", "high"),
        
        session_timeout=int(os.getenv("SESSION_TIMEOUT", "3600")),
        cart_expiry=int(os.getenv("CART_EXPIRY", "7200"))
    )