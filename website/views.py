from django.views.generic import TemplateView, ListView

from website.models import MenuCategory, MenuItem, GalleryItem, AboutUs, Chef


class HomeView(TemplateView):
    template_name = "website/home.html"


class MenuView(TemplateView):
    template_name = "website/menu.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Fetching all menu categories
        categories = MenuCategory.objects.all()

        menu_items = {}
        for category in categories:
            menu_items[category.name] = MenuItem.objects.filter(category=category)

        context['menu_items'] = menu_items
        return context


class AboutView(TemplateView):
    template_name = "website/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        about_data = AboutUs.objects.first()  # Assuming there's only one AboutUs entry
        chefs = Chef.objects.all()

        context['about'] = about_data
        context['chefs'] = chefs
        return context


class GalleryView(ListView):
    model = GalleryItem
    template_name = 'website/gallery.html'
    context_object_name = 'gallery_items'  # This is the variable that will hold the gallery items in the template
    paginate_by = 6


class ContactView(TemplateView):
    template_name = "website/contact.html"
