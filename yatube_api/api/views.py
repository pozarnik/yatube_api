from datetime import datetime

from posts.models import Post, Group, Comment
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status

from .serializers import PostSerializer, GroupSerializer, CommentSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, pub_date=datetime.now())

    def perform_update(self, serializer):
        post = self.get_object()
        if post.author != self.request.user:
            return Response(serializer.errors, status=status.HTTP_403_FORBIDDEN)
        super(PostViewSet, self).perform_update(serializer)

    def perform_destroy(self, serializer):
        instance = self.get_object()
        print(instance.author)
        if instance.author != self.request.user:
            return Response(serializer.errors, status=status.HTTP_403_FORBIDDEN)
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
        comment = self.get_object()
        if comment.author != self.request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        super(CommentViewSet, self).perform_update(serializer)

    def perform_destroy(self, serializer):
        comment = self.get_object()
        if comment.author != self.request.user:
            return Response(serializer.errors, status=status.HTTP_403_FORBIDDEN)
        super(CommentViewSet, self).perform_destroy(serializer)
