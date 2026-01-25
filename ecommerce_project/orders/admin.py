from django.contrib import admin
from .models import Order, OrderItem

# অর্ডারের ভেতরে আইটেমগুলোকে টেবিল আকারে দেখানোর জন্য
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    # আইটেমগুলো যেন কেউ অ্যাডমিন প্যানেল থেকে এডিট করতে না পারে
    readonly_fields = ['product', 'price', 'quantity']
    can_delete = False

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    # অ্যাডমিন প্যানেলের মেইন লিস্টে যা যা দেখাবে
    # এখানে 'total_amount' আপনার মডেলে থাকলে সেটি সরাসরি দিতে পারেন, নয়তো 'get_total_cost' ফাংশনটি ব্যবহার করুন
    list_display = ['id', 'user', 'transaction_id', 'get_total_cost', 'paid', 'created_at']
    
    # সাইডবারে ফিল্টার করার অপশন
    list_filter = ['paid', 'created_at']
    
    # সার্চ করার অপশন (অর্ডার আইডি বা ইউজারনেম দিয়ে)
    search_fields = ['id', 'transaction_id', 'user__username']
    
    # অর্ডারের ভেতরে ঢুকলে অর্ডার আইটেমগুলো দেখাবে
    inlines = [OrderItemInline]

    # অর্ডারের মোট টাকা হিসাব করার ফাংশন (যদি মডেলে total_amount ফিল্ড না থাকে)
    def get_total_cost(self, obj):
        total = sum(item.price * item.quantity for item in obj.items.all())
        return f"{total} TK"
    
    get_total_cost.short_description = 'Total Amount'

# আলাদাভাবে OrderItem রেজিস্টার করার দরকার নেই যেহেতু এটি ইনলাইন হিসেবে আছে
# তবে চাইলে নিচে এটি রাখতে পারেন
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'product', 'price', 'quantity']