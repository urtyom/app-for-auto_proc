import yaml
from django.core.management.base import BaseCommand
from procurement.models import Shop, Category, Product, ProductInfo, Parameter, ProductParameter


class Command(BaseCommand):
    help = 'Load data from a YAML file'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='The path to the YAML file')

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']

        with open(file_path, 'r', encoding='utf-8') as file:
            data = yaml.safe_load(file)

        shop_name = data['shop']
        shop, created = Shop.objects.get_or_create(name=shop_name)

        for category_data in data['categories']:
            category, created = Category.objects.get_or_create(id=category_data['id'],
                                                               defaults={'name': category_data['name']})
            category.shops.add(shop)

        for product_data in data['goods']:
            category = Category.objects.get(id=product_data['category'])
            product, created = Product.objects.get_or_create(id=product_data['id'], category=category,
                                                             defaults={'name': product_data['name']})
            product_info, created = ProductInfo.objects.get_or_create(
                product=product,
                shop=shop,
                defaults={
                    'name': product_data['name'],
                    'quantity': product_data['quantity'],
                    'price': product_data['price'],
                    'price_rrc': product_data['price_rrc']
                }
            )

            for param_name, param_value in product_data['parameters'].items():
                parameter, created = Parameter.objects.get_or_create(name=param_name)
                ProductParameter.objects.create(product_info=product_info, parameter=parameter, value=param_value)

        self.stdout.write(self.style.SUCCESS('Data loaded successfully'))