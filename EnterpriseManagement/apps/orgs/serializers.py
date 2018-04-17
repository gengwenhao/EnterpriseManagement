from rest_framework.serializers import ModelSerializer

from orgs.models import OrgProfile


class OrgProfileSerializer4(ModelSerializer):
    class Meta:
        model = OrgProfile
        fields = ('id', 'name', 'parent', 'code', 'org_type', 'category_type')


class OrgProfileSerializer3(ModelSerializer):
    children = OrgProfileSerializer4(many=True)

    class Meta:
        model = OrgProfile
        fields = ('id', 'name', 'parent', 'code', 'org_type', 'category_type', 'children')


class OrgProfileSerializer2(ModelSerializer):
    children = OrgProfileSerializer3(many=True)

    class Meta:
        model = OrgProfile
        fields = ('id', 'name', 'parent', 'code', 'org_type', 'category_type', 'children')


class OrgProfileSerializer(ModelSerializer):
    children = OrgProfileSerializer2(many=True)

    class Meta:
        model = OrgProfile
        fields = ('id', 'name', 'parent', 'code', 'org_type', 'category_type', 'children')
