from rest_framework import serializers

class CardSerializer(serializers.Serializer):
    name = serializers.CharField(required=False,
                                  max_length=100)
    set = serializers.CharField(max_length=100000)
    image_url = serializers.CharField(max_length=100000)
    multiverse_id = serializers.CharField(max_length=100000)
