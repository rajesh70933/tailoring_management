from django.shortcuts import render,redirect
from .models import *
# Create your views here.

def customer_list(request):
    customers=Customer.objects.all()
    return render(request,'customer_list.html', {'customers': customers})

def add_customer(request):
    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")

        Customer.objects.create(
            name=name,
            phone=phone
        )

        return redirect("/")

    return render(request, "add_customer.html")

def measurement_list(request):
    measurements = Measurement.objects.all()
    return render(request, 'measurement_list.html', {'measurements': measurements})

def customer_detail(request, id):
    customer = Customer.objects.get(id=id)
    measurement = Measurement.objects.filter(customer=customer).first()

    return render(request, 'customer_detail.html', {
        'customer': customer,
        'measurement': measurement
    })

def order_list(request):

    query = request.GET.get('q')

    if query:
        orders = Order.objects.filter(customer__name__icontains=query)
    else:
        orders = Order.objects.all()

    return render(request, 'order_list.html', {'orders': orders})


def pending_orders(request):
    orders = Order.objects.filter(status='pending')
    return render(request, 'order_list.html', {'orders': orders})

def ready_orders(request):
    orders = Order.objects.filter(status='ready')
    return render(request, 'order_list.html', {'orders': orders})

def dashboard(request):
    total = Order.objects.count()
    pending = Order.objects.filter(status='pending').count()
    stitching = Order.objects.filter(status='stitching').count()
    ready = Order.objects.filter(status='ready').count()
    delivered = Order.objects.filter(status='delivered').count()
    paid = Order.objects.filter(payment_status='paid').count()

    return render(request, 'dashboard.html', {
        'total': total,
        'pending': pending,
        'stitching': stitching,
        'ready': ready,
        'delivered': delivered,
        'paid': paid
    })


    return render(request, 'dashboard.html', context)

def customer_orders(request, customer_id):

    customer = Customer.objects.get(id=customer_id)
    orders = Order.objects.filter(customer=customer)

    context = {
        'customer': customer,
        'orders': orders
    }

    return render(request, 'customer_orders.html', context)

from .forms import OrderForm
from django.shortcuts import redirect

from datetime import date
from .forms import OrderForm

from .models import Measurement

def add_order(request):

    if request.method == 'POST':
        form = OrderForm(request.POST)

        if form.is_valid():
            order = form.save()

            # Save measurement
            Measurement.objects.create(
                customer=order.customer,
                chest=request.POST.get('chest'),
                waist=request.POST.get('waist'),
                hip=request.POST.get('hip'),
                shoulder=request.POST.get('shoulder'),
                sleeve_length=request.POST.get('sleeve_length'),
                dress_type=order.dress_type
            )

            return redirect('/orders/')
    else:
        form = OrderForm()

    return render(request, 'add_order.html', {'form': form})


def customer_measurements(request, customer_id):

    measurements = Measurement.objects.filter(customer_id=customer_id)

    return render(request, 'customer_measurements.html', {
        'measurements': measurements
    })





from django.shortcuts import get_object_or_404

def edit_order(request, order_id):

    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)

        if form.is_valid():
            form.save()
            return redirect('/orders/')

    else:
        form = OrderForm(instance=order)

    return render(request, 'edit_order.html', {'form': form})

from .models import History

def delete_order(request, order_id):

    order = Order.objects.get(id=order_id)
    print("DELETE FUNCTION CALLED ")

    # ✅ SAVE TO HISTORY FIRST
    History.objects.create(
        customer_name=order.customer.name,
        phone=order.customer.phone,
        dress_type=order.dress_type,
        price=order.price,
        delivery_date=order.delivery_date
    )

    # ✅ THEN DELETE
    order.delete()

    return redirect('/orders/')


from datetime import date

def today_deliveries(request):
    today = date.today()

    orders = Order.objects.filter(delivery_date=today)

    return render(request, 'today_deliveries.html', {'orders': orders})


def edit_measurement(request, measurement_id):

    measurement = Measurement.objects.get(id=measurement_id)

    if request.method == 'POST':
        measurement.chest = request.POST.get('chest')
        measurement.waist = request.POST.get('waist')
        measurement.hip = request.POST.get('hip')
        measurement.shoulder = request.POST.get('shoulder')
        measurement.sleeve_length = request.POST.get('sleeve_length')

        measurement.save()

        return redirect('/customer-measurements/' + str(measurement.customer.id))

    return render(request, 'edit_measurement.html', {
        'm': measurement
    })




from .models import Customer, Order, History

def delete_customer(request, customer_id):

    customer = Customer.objects.get(id=customer_id)

    # Save all orders into history BEFORE delete
    orders = Order.objects.filter(customer=customer)

    for order in orders:
        History.objects.create(
            customer_name=customer.name,
            phone=customer.phone,
            dress_type=order.dress_type,
            price=order.price,
            delivery_date=order.delivery_date
        )

    # Now delete
    customer.delete()

    return redirect('/customers')

def history_list(request):
    history = History.objects.all().order_by('-deleted_at')
    return render(request, 'history_list.html', {'history': history})



def home(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    return render(request,'home.html')



from django.shortcuts import get_object_or_404, redirect
from .models import Order

def mark_paid(request, id):
    order = Order.objects.get(id=id)
    order.payment_status = 'paid'
    order.save()
    return redirect('/orders/')

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Order
from datetime import date, timedelta
from django.db.models import Sum

@login_required
def dashboard(request):
    total = Order.objects.count()
    pending = Order.objects.filter(status='pending').count()
    stitching = Order.objects.filter(status='stitching').count()
    ready = Order.objects.filter(status='ready').count()
    delivered = Order.objects.filter(status='delivered').count()
    paid = Order.objects.filter(payment_status='paid').count()

    today = date.today()

    # 🎯 Today deliveries
    today_deliveries = Order.objects.filter(delivery_date=today).count()

    # 💰 TODAY REVENUE
    today_revenue = Order.objects.filter(
        payment_status='paid',
        delivery_date=today
    ).aggregate(total=Sum('price'))['total'] or 0

    # 📅 WEEKLY REVENUE
    week_start = today - timedelta(days=7)

    weekly_revenue = Order.objects.filter(
        payment_status='paid',
        delivery_date__gte=week_start
    ).aggregate(total=Sum('price'))['total'] or 0

    # 📆 MONTHLY REVENUE
    monthly_revenue = Order.objects.filter(
        payment_status='paid',
        delivery_date__month=today.month,
        delivery_date__year=today.year
    ).aggregate(total=Sum('price'))['total'] or 0

    context = {
        'total': total,
        'pending': pending,
        'stitching': stitching,
        'ready': ready,
        'delivered': delivered,
        'paid': paid,
        'today_deliveries': today_deliveries,

        'today_revenue': today_revenue,
        'weekly_revenue': weekly_revenue,
        'monthly_revenue': monthly_revenue,
    }

    return render(request, 'dashboard.html', context)
