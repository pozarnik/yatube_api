from datetime import datetime

from posts.models import Post, Group, Comment
from rest_framework import viewsets

from .serializers import PostSerializer, GroupSerializer, CommentSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, pub_date=datetime.now())

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionError('Изменение чужого поста запрещено!')
        super(PostViewSet, self).perform_update(serializer)

    def perform_destroy(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionError('Удаление чужого поста запрещено!')
        super(PostViewSet, self).perform_destroy(serializer)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        post_id = self.kwargs.get("post_id")
        new_queryset = Comment.objects.filter(post=post_id)
        return new_queryset

    def perform_create(self, serializer):
        post_id = self.kwargs.get("post_id")
        post = Post.objects.get(id=post_id)
        serializer.save(author=self.request.user, created=datetime.now(), post=post)

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionError('Изменение чужого контента запрещено!')
        super(CommentViewSet, self).perform_update(serializer)

    def perform_destroy(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionError('Удаление чужого комментария запрещено!')
        super(CommentViewSet, self).perform_destroy(serializer)
