class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (CustomUserPermission,)

    @action(detail=False, methods=['post'])
    def login(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        user = authenticate(email=email, password=password)
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            login(request, user)
            return Response({'token': token.key, 'email': user.email}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'User does not exist.'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['delete'])
    def logout(self, request):
        try:
            request.user.auth_token.delete()
        except (AttributeError, ObjectDoesNotExist):
            return Response({"detail": "Not authorized User."},
                            status=status.HTTP_400_BAD_REQUEST)
        if getattr(settings, 'REST_SESSION_LOGIN', True):
            django_logout(request)
            return Response({"detail": "Successfully logged out."},
                            status=status.HTTP_200_OK)

    @action(detail=True, methods=['delete'])
    def deactivate(self, request, *args, **kwargs):
        try:
            user = self.get_object()
            user.delete()
        except (AttributeError, ObjectDoesNotExist):
            return Response({"detail": "Not authorized User."}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "Account successfully deleted."}, status=status.HTTP_204_NO_CONTENT)