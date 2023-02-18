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