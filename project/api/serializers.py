from rest_framework import serializers

from api import models

#serializers are very similar to django forms
# also validates data
class HelloSerializer(serializers.Serializer):
    """Serializes a name field for testing our API View"""
    name =serializers.CharField(max_length=10)

class UserProfileSerializer(serializers.ModelSerializer):
    """Serializes a user profile object"""

    class Meta:
            model= models.UserProfile
            fields= ('id', 'email', 'name', 'password')

            #set password to write only so it can not be retrived or GET
            #only create, delete and update password is possible
            extra_kwargs={
                'password': {
                       'write_only':True,
                       'style':{'input_type': 'password'}
                    }
             }


    def create(self, validated_data):
            """Create and return a new user"""
            user = models.UserProfile.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password']
            )

            return user


    def update(self, instance, validated_data):
        """Handle updating user account"""
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)

        return super().update(instance, validated_data)


class ProfileFeedItemSerializer(serializers.ModelSerializer):
    """Serializes profile feed items"""
    class Meta:
        model=models.ProfileFeedItem
        fields=('id', 'user_profile','status_text', 'created_on')

        extra_kwargs={
        'user_profile': {'read_only':True}
        }
