from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from item.models import Item, Category

@login_required
def index(request):
    items = Item.objects.filter(created_by=request.user)
    category_ids = []

    for test in items:
        category_ids += str(test.category.id)

    categories = Category.objects.filter(id__in=category_ids).filter(items__created_by=request.user).distinct()

    context = {
        'items': items,
        'categories': categories
    }

    return render(request, 'dashboard/index.html', context)