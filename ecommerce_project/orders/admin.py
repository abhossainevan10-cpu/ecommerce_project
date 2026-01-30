from django.contrib import admin
from django.db.models import Sum
from django.db.models.functions import TruncDay
from .models import Order, OrderItem
from django.utils import timezone # সময় ফিল্টার করার জন্য
from datetime import timedelta    # দিনের হিসাব করার জন্য
import json

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

    # --- ড্যাশবোর্ড লজিক (ফিল্টারসহ ঠিক করা হয়েছে) ---
    def changelist_view(self, request, extra_context=None):
        orders = Order.objects.filter(paid=True)

        # ১. বাটন ফিল্টার লজিক (URL থেকে days প্যারামিটার নেওয়া)
        days_filter = request.GET.get('days')
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')

        if days_filter and days_filter != 'all':
            # নির্দিষ্ট দিনের ডাটা ফিল্টার
            start_from = timezone.now() - timedelta(days=int(days_filter))
            orders = orders.filter(created_at__gte=start_from)
        elif start_date and end_date:
            # ক্যালেন্ডার থেকে ডেট রেঞ্জ ফিল্টার
            orders = orders.filter(created_at__range=[start_date, end_date])

        # ২. টোটাল রেভিনিউ হিসাব (ফিল্টার অনুযায়ী)
        total_revenue = orders.aggregate(total=Sum('total_amount'))['total'] or 0

        # ৩. গ্রাফের ডাটা (ফিল্টার অনুযায়ী)
        revenue_data = (
            orders.annotate(day=TruncDay('created_at'))
            .values('day')
            .annotate(total=Sum('total_amount'))
            .order_by('day')
        )

        chart_data = {
            "labels": [data['day'].strftime("%d %b") for data in revenue_data],
            "values": [float(data['total']) for data in revenue_data],
        }

        extra_context = extra_context or {}
        extra_context['total_revenue'] = total_revenue
        extra_context['chart_data'] = json.dumps(chart_data)
        
        return super().changelist_view(request, extra_context=extra_context)

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'product', 'price', 'quantity']