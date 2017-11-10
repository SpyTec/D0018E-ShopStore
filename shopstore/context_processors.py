

def category(request):
    from shop.models import Category
    categories = Category.objects.all()

    return {
        'categories': categories,  # Add 'contacts' to the context
    }