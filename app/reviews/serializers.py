from rest_framework import serializers
from .models import Review
from app.advocates.serializers import AdvocateProfileSerializer


# ================================
# Review Read Serializer
# ================================
class ReviewSerializer(serializers.ModelSerializer):
    client_name = serializers.CharField(source='client.username', read_only=True)
    advocate = AdvocateProfileSerializer(read_only=True)

    class Meta:
        model = Review
        fields = [
            'id',
            'client',
            'client_name',
            'advocate',
            'appointment',
            'rating',
            'comment',
            'created_at'
        ]
        read_only_fields = [
            'id',
            'client',
            'created_at',
            'advocate',
            'client_name'
        ]


# ================================
# Review Create Serializer
# ================================
class ReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['advocate', 'appointment', 'rating', 'comment']

    def validate_rating(self, value):
        if not 1 <= value <= 5:
            raise serializers.ValidationError(
                "Rating must be between 1 and 5"
            )
        return value

    def validate(self, attrs):
        request = self.context['request']
        appointment = attrs.get('appointment')
        advocate = attrs.get('advocate')

        if appointment:
            if appointment.client != request.user:
                raise serializers.ValidationError(
                    "You can review only your own appointment."
                )
            if appointment.advocate != advocate:
                raise serializers.ValidationError(
                    "Appointment does not belong to this advocate."
                )

        return attrs

    def create(self, validated_data):
        validated_data['client'] = self.context['request'].user
        return super().create(validated_data)
