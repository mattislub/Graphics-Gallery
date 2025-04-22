from rest_framework import serializers  # type: ignore

from shop.models import (
    BalanceProduct,
    ImageCategory,
    ImageOrientation,
    ImageProduct,
    SubscriptionPlan,
)


class ImageOrientationSerializer(serializers.ModelSerializer):
    '''Serializer for ImageOrientation.'''
    class Meta:
        model = ImageOrientation
        fields = ('name', 'slug')


class ImageCategorySerializer(serializers.ModelSerializer):
    '''Serializer for Category.'''
    class Meta:
        model = ImageCategory
        fields = ('name', 'slug', 'preview_image')


class ImageProductSerializer(serializers.ModelSerializer):
    '''Serializer for Product: Image.'''
    orientation = ImageOrientationSerializer()
    category = ImageCategorySerializer()

    class Meta:
        model = ImageProduct
        fields = ('name', 'price', 'code', 'premium', 'preview_image_url', 'orientation', 'category')


class BalanceProductSerializer(serializers.ModelSerializer):
    '''Serializer for BalanceProduct.'''
    class Meta:
        model = BalanceProduct
        fields = ('main_text', 'help_text', 'badge_text', 'price', 'replenishment')


class SubscriptionPlanSerializer(serializers.ModelSerializer):
    '''Serializer for SubscriptionPlan.'''
    class Meta:
        model = SubscriptionPlan
        fields = ('main_text', 'help_text', 'badge_text', 'price', 'download_limit', 'unlimited', 'duration_days')
