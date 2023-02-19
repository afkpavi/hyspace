from rest_framework.serializers import ModelSerializer
from .models import Account



class AccountSerializer(ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Account

    def create(self, data):
        
        password = data.pop('password')
        user = super().create(data)
        user.set_password(password)
        user.save()

        return user
    
    def update(self, instance, validated_data):
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)
        return super().update(instance, validated_data)