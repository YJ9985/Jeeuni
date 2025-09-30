from rest_framework import serializers
from .models import Book, Category, Post, Comment


class BookListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'
        read_only_fields = ('category',)


class BookSerializer(serializers.ModelSerializer):
    class CategorySerializer(serializers.ModelSerializer):
        class Meta:
            model = Category
            fields = ('id', 'name', )
    category = CategorySerializer(read_only=True)

    class PostListSerializer(serializers.ModelSerializer):
        class Meta:
            model = Post
            fields = ('id', 'title', 'content', 'created_at', 'user', )
    posts = PostListSerializer(source='post_set', many=True, read_only=True)

    # 현재 사용자 정보 (선택적)
    current_user = serializers.SerializerMethodField()
    
    class Meta:
        model = Book
        fields = '__all__'

    def get_current_user(self, obj):
        request = self.context.get('request')
        if request and request.user.id:
            return {
                'id': request.user.id,
                'email': request.user.email,
                'name': request.user.name,
            }
        return None


class PostSerializer(serializers.ModelSerializer):
    class BookTitleSerializer(serializers.ModelSerializer):
        class Meta:
            model = Book
            fields = ('id', 'title', 'author', 'pub_date', 'cover', )
    
    book = BookTitleSerializer(read_only=True)

    class CommentListSerializer(serializers.ModelSerializer):
        # 현재 사용자가 댓글 삭제 권한이 있는지 표시
        # can_delete = serializers.SerializerMethodField()
        
        class Meta:
            model = Comment
            fields = ('id', 'content', 'user', 'created_at', )
        
        # def get_can_delete(self, obj):
        #     request = self.context.get('request')
        #     if request and request.user.id:
        #         return obj.user == request.user.id
        #     return False
    
    comments = CommentListSerializer(source='comment_set', many=True, read_only=True)
    
    # 현재 사용자가 포스트 수정/삭제 권한이 있는지 표시
    # can_edit = serializers.SerializerMethodField()
    # can_delete = serializers.SerializerMethodField()
    
    # 현재 사용자 정보 (선택적)
    current_user = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ('id', 'title', 'content', 'user', 'book', 'created_at', 'updated_at', 'comments', 'current_user', )

    def get_current_user(self, obj):
        request = self.context.get('request')
        if request and request.user.id:
            return {
                'id': request.user.id,
                'email': request.user.email,
                'name': request.user.name,
                # 필요한 다른 사용자 정보들
            }
        return None
    
    # def get_can_edit(self, obj):
    #     request = self.context.get('request')
    #     if request and request.user.id:
    #         return obj.user == request.user.id
    #     return False

    # def get_can_delete(self, obj):
    #     request = self.context.get('request')
    #     if request and request.user.id:
    #         return obj.user == request.user.id
    #     return False



class PostUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ('user', 'book', 'created_at', 'updated_at', )


class CommentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('user', 'post', 'created_at')


class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ('user', 'book', 'created_at', 'updated_at', )


class BookCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('title', 'author', 'cover', 'description', 'pub_date', 'category',)
        read_only_fields = ('id', )


class BookReturnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'


class PostListSerializer(serializers.ModelSerializer):
    class BookTitleSerializer(serializers.ModelSerializer):
        class Meta:
            model = Book
            fields = ('title', 'author', )

    book = BookTitleSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'title', 'content', 'created_at', 'book', )


class BookUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('title', 'author', 'cover', 'description', )


class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', )
