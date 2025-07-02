"""
Nike Shoe Store - Main UI Application
Modern e-commerce interface with shopping cart functionality
"""

from nicegui import ui, app
from typing import Dict, List, Optional
import asyncio
from datetime import datetime

from core.store import StoreManager
from core.cart import CartManager
from models.product import Product
from services.product_service import ProductService
from app.components.header import create_header
from app.components.product_grid import create_product_grid
from app.components.cart_sidebar import create_cart_sidebar
from app.components.product_modal import create_product_modal
from app.config import get_settings

# Global state management
store_manager = StoreManager()
cart_manager = CartManager()
product_service = ProductService()

# UI State
current_category = "all"
search_query = ""
cart_visible = False
selected_product: Optional[Product] = None

async def initialize_store():
    """Initialize store with product data"""
    await product_service.load_products()
    store_manager.set_products(product_service.get_all_products())

@ui.page('/')
async def home_page():
    """Main store page with product catalog"""
    await initialize_store()
    
    # Add custom CSS for Nike branding
    ui.add_head_html('''
        <style>
            .nike-header {
                background: linear-gradient(135deg, #000000 0%, #1a1a1a 100%);
                color: white;
                padding: 1rem 0;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            .nike-logo {
                font-size: 2rem;
                font-weight: bold;
                color: #ff6b35;
            }
            .product-card {
                transition: transform 0.3s ease, box-shadow 0.3s ease;
                border-radius: 12px;
                overflow: hidden;
                background: white;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            }
            .product-card:hover {
                transform: translateY(-5px);
                box-shadow: 0 8px 25px rgba(0,0,0,0.15);
            }
            .price-tag {
                color: #ff6b35;
                font-weight: bold;
                font-size: 1.2rem;
            }
            .cart-button {
                background: #ff6b35;
                color: white;
                border: none;
                padding: 0.75rem 1.5rem;
                border-radius: 8px;
                font-weight: bold;
                transition: background 0.3s ease;
            }
            .cart-button:hover {
                background: #e55a2b;
            }
            .category-filter {
                background: #f8f9fa;
                border-radius: 8px;
                padding: 0.5rem 1rem;
                margin: 0.25rem;
                border: 2px solid transparent;
                transition: all 0.3s ease;
            }
            .category-filter.active {
                background: #ff6b35;
                color: white;
                border-color: #ff6b35;
            }
            .search-container {
                max-width: 400px;
                margin: 0 auto;
            }
            .cart-sidebar {
                position: fixed;
                right: 0;
                top: 0;
                height: 100vh;
                width: 400px;
                background: white;
                box-shadow: -5px 0 15px rgba(0,0,0,0.1);
                transform: translateX(100%);
                transition: transform 0.3s ease;
                z-index: 1000;
                overflow-y: auto;
            }
            .cart-sidebar.visible {
                transform: translateX(0);
            }
            .overlay {
                position: fixed;
                top: 0;
                left: 0;
                width: 100vw;
                height: 100vh;
                background: rgba(0,0,0,0.5);
                z-index: 999;
                opacity: 0;
                visibility: hidden;
                transition: all 0.3s ease;
            }
            .overlay.visible {
                opacity: 1;
                visibility: visible;
            }
        </style>
    ''')
    
    # Create main layout
    with ui.column().classes('w-full min-h-screen bg-gray-50'):
        # Header
        await create_header()
        
        # Main content
        with ui.row().classes('w-full max-w-7xl mx-auto px-4 py-8 gap-8'):
            # Sidebar filters
            with ui.column().classes('w-64 space-y-4'):
                ui.label('Categories').classes('text-xl font-bold text-gray-800')
                
                categories = ['all', 'running', 'basketball', 'lifestyle', 'training']
                for category in categories:
                    with ui.button(
                        category.title(), 
                        on_click=lambda c=category: filter_by_category(c)
                    ).classes(f'category-filter w-full text-left {"active" if category == current_category else ""}'):
                        pass
                
                ui.separator()
                
                # Price filter
                ui.label('Price Range').classes('text-lg font-semibold text-gray-700 mt-6')
                with ui.column().classes('space-y-2'):
                    ui.button('Under $100', on_click=lambda: filter_by_price(0, 100)).classes('category-filter w-full text-left')
                    ui.button('$100 - $150', on_click=lambda: filter_by_price(100, 150)).classes('category-filter w-full text-left')
                    ui.button('$150 - $200', on_click=lambda: filter_by_price(150, 200)).classes('category-filter w-full text-left')
                    ui.button('Over $200', on_click=lambda: filter_by_price(200, 999)).classes('category-filter w-full text-left')
            
            # Product grid
            with ui.column().classes('flex-1'):
                # Search bar
                with ui.row().classes('search-container mb-6'):
                    search_input = ui.input(
                        placeholder='Search Nike shoes...',
                        on_change=lambda e: search_products(e.value)
                    ).classes('flex-1')
                    search_input.props('outlined dense')
                
                # Products container
                products_container = ui.column().classes('w-full')
                await render_products(products_container)
        
        # Cart sidebar
        cart_sidebar = ui.column().classes('cart-sidebar')
        await create_cart_sidebar(cart_sidebar)
        
        # Overlay
        overlay = ui.element('div').classes('overlay')
        overlay.on('click', toggle_cart)

async def render_products(container):
    """Render product grid"""
    container.clear()
    
    products = store_manager.get_filtered_products(
        category=current_category if current_category != 'all' else None,
        search_query=search_query if search_query else None
    )
    
    if not products:
        with container:
            ui.label('No products found').classes('text-center text-gray-500 text-xl py-12')
        return
    
    with container:
        with ui.grid(columns=3).classes('w-full gap-6'):
            for product in products:
                await create_product_card(product)

async def create_product_card(product: Product):
    """Create individual product card"""
    with ui.card().classes('product-card cursor-pointer').on('click', lambda p=product: show_product_details(p)):
        # Product image
        ui.image(product.image_url).classes('w-full h-64 object-cover')
        
        with ui.card_section().classes('p-4'):
            # Product name
            ui.label(product.name).classes('text-lg font-semibold text-gray-800 mb-2')
            
            # Product category
            ui.label(product.category.title()).classes('text-sm text-gray-500 mb-2')
            
            # Price and cart button
            with ui.row().classes('w-full justify-between items-center'):
                ui.label(f'${product.price:.2f}').classes('price-tag')
                
                ui.button(
                    'Add to Cart',
                    on_click=lambda p=product: add_to_cart(p)
                ).classes('cart-button').props('dense')

def filter_by_category(category: str):
    """Filter products by category"""
    global current_category
    current_category = category
    # Trigger re-render
    ui.run_javascript('location.reload()')

def filter_by_price(min_price: float, max_price: float):
    """Filter products by price range"""
    # Implementation for price filtering
    pass

def search_products(query: str):
    """Search products by name"""
    global search_query
    search_query = query
    # Trigger re-render
    ui.run_javascript('location.reload()')

def add_to_cart(product: Product):
    """Add product to shopping cart"""
    cart_manager.add_item(product)
    ui.notify(f'Added {product.name} to cart!', type='positive')
    update_cart_display()

def show_product_details(product: Product):
    """Show product details modal"""
    global selected_product
    selected_product = product
    create_product_modal(product)

def toggle_cart():
    """Toggle cart sidebar visibility"""
    global cart_visible
    cart_visible = not cart_visible
    
    # Update UI classes
    ui.run_javascript(f'''
        document.querySelector('.cart-sidebar').classList.toggle('visible', {str(cart_visible).lower()});
        document.querySelector('.overlay').classList.toggle('visible', {str(cart_visible).lower()});
    ''')

def update_cart_display():
    """Update cart display with current items"""
    # This will be implemented in the cart sidebar component
    pass

@ui.page('/checkout')
async def checkout_page():
    """Checkout page"""
    ui.label('Checkout').classes('text-3xl font-bold text-center py-8')
    
    with ui.column().classes('max-w-2xl mx-auto p-6'):
        ui.label('Order Summary').classes('text-xl font-semibold mb-4')
        
        # Cart items
        cart_items = cart_manager.get_items()
        total = 0
        
        for item in cart_items:
            with ui.row().classes('w-full justify-between items-center py-2 border-b'):
                ui.label(f'{item.product.name} x{item.quantity}')
                item_total = item.product.price * item.quantity
                ui.label(f'${item_total:.2f}')
                total += item_total
        
        # Total
        with ui.row().classes('w-full justify-between items-center py-4 text-xl font-bold'):
            ui.label('Total:')
            ui.label(f'${total:.2f}').classes('price-tag')
        
        # Checkout form
        ui.separator()
        ui.label('Shipping Information').classes('text-lg font-semibold mt-6 mb-4')
        
        with ui.grid(columns=2).classes('gap-4'):
            ui.input('First Name').props('outlined')
            ui.input('Last Name').props('outlined')
            ui.input('Email').props('outlined')
            ui.input('Phone').props('outlined')
        
        ui.input('Address').props('outlined').classes('w-full mt-4')
        
        with ui.grid(columns=3).classes('gap-4 mt-4'):
            ui.input('City').props('outlined')
            ui.input('State').props('outlined')
            ui.input('ZIP Code').props('outlined')
        
        # Payment simulation
        ui.label('Payment Information').classes('text-lg font-semibold mt-6 mb-4')
        ui.label('(This is a demo - no real payment processing)').classes('text-sm text-gray-500 mb-4')
        
        ui.input('Card Number').props('outlined').classes('w-full')
        
        with ui.grid(columns=2).classes('gap-4 mt-4'):
            ui.input('Expiry Date').props('outlined')
            ui.input('CVV').props('outlined')
        
        # Place order button
        ui.button(
            'Place Order',
            on_click=lambda: place_order()
        ).classes('w-full mt-8 bg-orange-500 text-white py-3 text-lg font-bold rounded-lg hover:bg-orange-600')

def place_order():
    """Simulate order placement"""
    cart_manager.clear()
    ui.notify('Order placed successfully! Thank you for your purchase.', type='positive')
    ui.navigate.to('/')

def start_app():
    """Start the Nike Shoe Store application"""
    settings = get_settings()
    
    # Configure the app
    app.add_static_files('/static', 'static')
    
    # Run the application
    ui.run(
        host=settings.host,
        port=settings.port,
        title=settings.store_name,
        favicon='🏃',
        dark=False,
        show=False
    )