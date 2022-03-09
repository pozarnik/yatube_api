from rest_framework import viewsets
from datetime import datetime

from .serializers import PostSerializer, GroupSerializer, CommentSerializer
from posts.models import Post, Group, Comment


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, pub_date=datetime.now())

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionError('Изменение чужого контента запрещено!')
        super(PostViewSet, self).perform_update(serializer)

    def perform_destroy(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionError('Изменение чужого контента запрещено!')
        super(PostViewSet, self).perform_update(serializer)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, create=datetime.now())

    def get_queryset(self):
        post_id = self.kwargs.get("post_id")
        new_queryset = Comment.objects.filter(post=post_id)
        return new_queryset

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionError('Изменение чужого контента запрещено!')
        super(CommentViewSet, self).perform_update(serializer)

    def perform_destroy(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionError('Изменение чужого контента запрещено!')
        super(CommentViewSet, self).perform_update(serializer)
