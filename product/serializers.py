from rest_framework import serializers
from product.models import Category, Product, Brand, Variant


class CategorySerializer(serializers.ModelSerializer):
    count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = '__all__'

    def get_count(self, obj):
        return Product.objects.filter(category=obj).count()


class BrandSerializer(CategorySerializer):

    class Meta:
        model = Brand
        fields = '__all__'

    def get_count(self, obj):
        return Product.objects.filter(brand=obj).count()


class VariantSerializer(serializers.ModelSerializer):
    color = serializers.StringRelatedField()
    size = serializers.StringRelatedField()
    images = serializers.StringRelatedField(many=True)

    class Meta:
        model = Variant
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    variants = VariantSerializer(many=True)
    images = serializers.StringRelatedField(many=True)
    color = serializers.StringRelatedField()
    size = serializers.StringRelatedField()
    brand = BrandSerializer()
    category = CategorySerializer()

    class Meta:
        model = Product
        fields = '__all__'
