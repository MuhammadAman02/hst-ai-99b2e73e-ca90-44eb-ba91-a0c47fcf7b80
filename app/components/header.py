"""Header component for the Nike store"""

from nicegui import ui
from app.config import get_settings

async def create_header():
    """Create the main header with navigation and cart"""
    settings = get_settings()
    
    with ui.row().classes('nike-header w-full'):
        with ui.row().classes('w-full max-w-7xl mx-auto px-4 justify-between items-center'):
            # Logo and brand
            with ui.row().classes('items-center gap-4'):
                ui.label('✓').classes('nike-logo text-3xl')
                with ui.column().classes('gap-0'):
                    ui.label(settings.store_name).classes('text-xl font-bold')
                    ui.label(settings.store_tagline).classes('text-sm text-gray-300')
            
            # Navigation
            with ui.row().classes('items-center gap-6'):
                ui.link('Home', '/').classes('text-white hover:text-orange-300 font-medium')
                ui.link('Men', '/').classes('text-white hover:text-orange-300 font-medium')
                ui.link('Women', '/').classes('text-white hover:text-orange-300 font-medium')
                ui.link('Kids', '/').classes('text-white hover:text-orange-300 font-medium')
                ui.link('Sale', '/').classes('text-white hover:text-orange-300 font-medium')
            
            # Cart and user actions
            with ui.row().classes('items-center gap-4'):
                # Search icon
                ui.button(icon='search').props('flat round').classes('text-white')
                
                # User account
                ui.button(icon='person').props('flat round').classes('text-white')
                
                # Shopping cart
                cart_button = ui.button(icon='shopping_cart').props('flat round').classes('text-white')
                cart_button.on('click', lambda: toggle_cart())
                
                # Cart count badge
                with ui.badge('0', color='orange').classes('absolute -top-2 -right-2'):
                    pass

def toggle_cart():
    """Toggle cart sidebar visibility"""
    # This will be connected to the main app's cart toggle function
    pass