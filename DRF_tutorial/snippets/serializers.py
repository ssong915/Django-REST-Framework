from rest_framework import serializers
from snippets.models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES
from django.contrib.auth.models import User

#Snippet 인스턴스를 json으로 직렬화, 역 직렬화
# - '변환'으로 이해 -> forms.py 와 유사

class SnippetSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    #1.source: 해당 필드를 채우기위해 속성 명시, 뭐든 가능
    #2.ReadOnlyField: Char,Date같은 타입이 아니고 읽기 전용이라는 뜻
    #               : == CharField(read_only=True)
    highlight = serializers.HyperlinkedIdentityField(view_name='snippet-highlight', format='html')

    class Meta:
        model = Snippet
        # fields = ['id', 'title', 'code', 'linenos', 'language', 'style','owner']
        fields = ('url', 'highlight', 'owner',
                  'title', 'code', 'linenos', 'language', 'style')
        
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(required=False, allow_blank=True, max_length=100)
    code = serializers.CharField(style={'base_template': 'textarea.html'})
    linenos = serializers.BooleanField(required=False)
    language = serializers.ChoiceField(choices=LANGUAGE_CHOICES, default='python')
    style = serializers.ChoiceField(choices=STYLE_CHOICES, default='friendly')

    def create(self, validated_data):
        return Snippet.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.code = validated_data.get('code', instance.code)
        instance.linenos = validated_data.get('linenos', instance.linenos)
        instance.language = validated_data.get('language', instance.language)
        instance.style = validated_data.get('style', instance.style)
        instance.save()
        return instance

# -> serialize.save() 할때 위 처럼 create,update 됨.

class UserSerializer(serializers.HyperlinkedModelSerializer):
    # snippets = serializers.PrimaryKeyRelatedField(many=True, queryset=Snippet.objects.all())
    snippets = serializers.HyperlinkedRelatedField(many=True, view_name='snippet-detail', read_only=True)

    class Meta:
        model = User
        # fields = ['id', 'username', 'snippets']
        fields = ('url', 'username', 'snippets')
