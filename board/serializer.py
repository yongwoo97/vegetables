from rest_framework import serializers
from .models import Product, ProductList, Unit, Location

class ProductPureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = '__all__'

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'

class ProductListSerializer(serializers.ModelSerializer):

    location = serializers.SlugRelatedField(read_only=True, slug_field='name')
    unit = serializers.SlugRelatedField(read_only=True, slug_field='name')

    class Meta:
        model = ProductList
        fields = '__all__'

class ProductAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductList
        fields = '__all__'
        extra_kwargs = {
            'date': {'required': True},
            'in_date': {'required': True}
        }
#판매완료, 장소이동 기능만 있음
class ProductUpdateSerializer(serializers.ModelSerializer):
    location = serializers.SlugRelatedField(read_only=True, slug_field='name')
    unit = serializers.SlugRelatedField(read_only=True, slug_field='name')
    class Meta:
        model = ProductList
        fields = '__all__'
        extra_kwargs = {'location' : {'required': True}}

class ProductSerialzer(serializers.ModelSerializer):
    product_list = ProductListSerializer(many=True, read_only=True)
    class Meta:
        model = Product
        fields = '__all__'
