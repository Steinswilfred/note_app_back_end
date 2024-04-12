from rest_framework import serializers
from .models import User_information,Items_Category
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

class SignupSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match")
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')  # Remove confirm_password from validated_data
        validated_data["password"] = make_password(validated_data.get("password"))
        return super(SignupSerializer, self).create(validated_data)

    class Meta:
        model = User
        fields = ['id','username', 'email', 'password', 'confirm_password']


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    class Meta:
        model = User
        fields = ['username','password']

class items(serializers.ModelSerializer):
    class Meta:
        model = Items_Category
        fields = '__all__'
class customer_information(serializers.ModelSerializer):
    category_name = serializers.CharField(source='Items.Item_name', read_only=True,)
    class Meta:
        model = User_information
        fields = '__all__'
