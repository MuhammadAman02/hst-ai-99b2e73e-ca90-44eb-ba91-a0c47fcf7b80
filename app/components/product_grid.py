"""Product grid component"""

from nicegui import ui
from typing import List
from models.product import Product

async def create_product_grid(products: List[Product]):
    """Create a responsive product grid"""
    
    if not products:
        with ui.column().classes('w-full text-center py-12'):
            ui.label('No products found').classes('text-xl text-gray-500')
            ui.label('Try adjusting your filters or search terms').classes('text-gray-400')
        return
    
    with ui.grid(columns='repeat(auto-fill, minmax(300px, 1fr))').classes('w-full gap-6'):
        for product in products:
            await create_product_card(product)

async def create_product_card(product: Product):
    """Create individual product card"""
    with ui.card().classes('product-card cursor-pointer hover:shadow-lg transition-all duration-300'):
        # Product image
        with ui.element('div').classes('relative overflow-hidden'):
            ui.image(product.image_url).classes('w-full h-64 object-cover')
            
            # Quick view overlay
            with ui.element('div').classes('absolute inset-0 bg-black bg-opacity-50 opacity-0 hover:opacity-100 transition-opacity duration-300 flex items-center justify-center'):
                ui.button('Quick View', icon='visibility').classes('bg-white text-black hover:bg-gray-100')
        
        with ui.card_section().classes('p-4'):
            # Product name
            ui.label(product.name).classes('text-lg font-semibold text-gray-800 mb-1 line-clamp-2')
            
            # Product category
            ui.label(product.category.title()).classes('text-sm text-gray-500 mb-2')
            
            # Product description (truncated)
            if product.description:
                ui.label(product.description[:100] + '...' if len(product.description) > 100 else product.description).classes('text-sm text-gray-600 mb-3 line-clamp-2')
            
            # Price and actions
            with ui.row().classes('w-full justify-between items-center'):
                ui.label(f'${product.price:.2f}').classes('price-tag text-xl')
                
                with ui.row().classes('gap-2'):
                    # Wishlist button
                    ui.button(icon='favorite_border').props('flat round dense').classes('text-gray-400 hover:text-red-500')
                    
                    # Add to cart button
                    ui.button(
                        'Add to Cart',
                        icon='add_shopping_cart',
                        on_click=lambda p=product: add_to_cart(p)
                    ).classes('cart-button')

def add_to_cart(product: Product):
    """Add product to cart"""
    # This will be connected to the cart manager
    ui.notify(f'Added {product.name} to cart!', type='positive')