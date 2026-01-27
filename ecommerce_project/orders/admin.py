from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product', 'price', 'quantity']
    can_delete = False

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    
    list_display = ['id', 'user', 'transaction_id', 'get_total_cost', 'paid', 'created_at']
    
    
    list_filter = ['paid', 'created_at']
    
  
    search_fields = ['id', 'transaction_id', 'user__username']
    
    
    inlines = [OrderItemInline]

   
    def get_total_cost(self, obj):
        total = sum(item.price * item.quantity for item in obj.items.all())
        return f"{total} TK"
    
    get_total_cost.short_description = 'Total Amount'


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'product', 'price', 'quantity']