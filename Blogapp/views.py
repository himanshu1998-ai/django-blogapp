from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Blog
from .serializers import BlogSerializer
from rest_framework import status
from django.db.models import Q
from django.core.paginator import Paginator


class PublicBlogView(APIView):
    def get(self, request):
        
        try:
            # Fetching random blogs for user to view
            blogs = Blog.objects.all().order_by('?')
            
            if request.GET.get('search'):
                search = request.GET.get('search')
                blogs = blogs.filter(Q(title__icontains=search) | Q(description__icontains=search))
            
            # Pagination
            page_number = request.GET.get('page',1)
            paginator = Paginator(blogs, 5)
            
            serializer = BlogSerializer(paginator.page(page_number), many=True)
            return Response({"payload": serializer.data, "message": "Blogs Fetched Successfully"},status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({"errors": str(e),"message": "Something went wrong"},status=status.HTTP_400_BAD_REQUEST)
            

class BlogsView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        
        try:
            blogs = Blog.objects.filter(user=request.user)
            if request.GET.get('search'):
                search = request.GET.get('search')
                blogs = blogs.filter(Q(title__icontains=search) | Q(description__icontains=search))
                
            serializer = BlogSerializer(blogs, many=True)
            return Response({"payload": serializer.data, "message": "Blogs Fetched Successfully"},status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({"message": "Something went wrong"},status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        try:
            data = request.data
            data['user'] = request.user.id
            serializer = BlogSerializer(data=data)
            
            if not serializer.is_valid():
                return Response({"errors": serializer.errors, "message": "Something went wrong"}, status=status.HTTP_400_BAD_REQUEST,)
            
            serializer.save()

            return Response({"payload": serializer.data, "message": "Blog created"},status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"message": "Something went wrong"},status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        try:
            data = request.data
            blog = Blog.objects.filter(uid= data.get('uid'))
            if not blog.exists():
                return Response({"data": {}, "message": "Invalid Blog Id"},status=status.HTTP_400_BAD_REQUEST)
            
            if request.user != blog[0].user:
                return Response({"data": {}, "message": "You are Not Authorized"},status=status.HTTP_400_BAD_REQUEST)
                
            serializer = BlogSerializer(blog[0], data=data, partial=True)
            
            if not serializer.is_valid():
                return Response({ "errors": serializer.errors, "message": "Something went wrong"},status=status.HTTP_400_BAD_REQUEST,)
            
            serializer.save()

            return Response({"data": serializer.data, "message": "Blog Updated Successfully"},status=status.HTTP_201_CREATED)
        
        except Exception as e:
            return Response({"message": "Something went wrong"},status=status.HTTP_400_BAD_REQUEST)
            

    def delete(self, request):
        try:
            data = request.data
            blog = Blog.objects.filter(uid= data.get('uid'))
            
            if not blog.exists():
                return Response({"data": {}, "message": "Invalid Blog Id"},status=status.HTTP_400_BAD_REQUEST)
            
            if request.user != blog[0].user:
                return Response({"data": {}, "message": "You are Not Authorized"},status=status.HTTP_400_BAD_REQUEST)
            
            blog[0].delete()
            
            return Response({"data": {}, "message": "Blog Deleted"},status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response({"error": "Something Went Wrong"}, status=status.HTTP_400_BAD_REQUEST)
        