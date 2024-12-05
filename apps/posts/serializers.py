from rest_framework import serializers

from apps.posts.models import Post, Image


class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ["image"]


class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source="author.username")
    banner_image = serializers.SerializerMethodField()
    images = PostImageSerializer(many=True, read_only=True)
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(max_length=10 ** 6, allow_empty_file=False),
        write_only=True, required=False)
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()
    is_upvoted = serializers.SerializerMethodField()
    is_bookmarked = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "slug",
            "author",
            "body",
            "banner_image",
            "images",
            "uploaded_images",
            "upvotes",
            "downvotes",
            "is_upvoted",
            "is_bookmarked",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "slug",
            "author",
            "upvotes",
            "downvotes",
            "created_at",
            "updated_at",
        ]

    def get_banner_image(self, obj):
        try:
            return obj.banner_image.url
        except AttributeError:
            return None

    def get_created_at(self, obj):
        now = obj.created_at
        formatted_date = now.strftime("%m.%d.%Y, %H:%M:%S")
        return formatted_date

    def get_updated_at(self, obj):
        now = obj.created_at
        formatted_date = now.strftime("%m.%d.%Y, %H:%M:%S")
        return formatted_date

    def get_is_upvoted(self, obj):
        user = self.context["request"].user
        if user.is_authenticated:
            return obj.upvoted_by.filter(id=user.id).exists()
        return False

    def get_is_bookmarked(self, obj) -> bool:
        user = self.context["request"].user
        if user.is_authenticated:
            return obj.bookmarked_by.filter(id=user.id).exists()
        return False

    def create(self, validated_data):
        uploaded_images = validated_data.pop("uploaded_images", None)
        post = Post.objects.create(**validated_data)
        if uploaded_images:
            images = [Image(post=post, image=image) for image in uploaded_images]
            Image.objects.bulk_create(images)
        return post
