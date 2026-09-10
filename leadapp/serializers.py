from rest_framework import serializers

from leadapp.models import Lead, LeadNote


class NoteSerializer(serializers.ModelSerializer):
    created_by_username = serializers.CharField(source='created_by.username',read_only=True )

    class Meta:
        model = LeadNote
        fields = ['id', 'content', 'created_by', 'created_by_username', 'created_at']
        read_only_fields = ['id', 'created_by', 'created_by_username', 'created_at']

    def validate_content(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Note content cannot be empty")
        return value
class LeadSerializer(serializers.ModelSerializer):
    owner_username = serializers.CharField(source='owner.username',read_only=True)
    notes = NoteSerializer(many=True,read_only=True)


    class Meta:
        model = Lead
        fields = ['id', 'name', 'email', 'company', 'phone', 'status', 'lost_reason', 'owner','owner_username', 'created_at', 'updated_at', 'notes']
        read_only_fields = ['id', 'owner', 'owner_username', 'created_at', 'updated_at', 'notes']
        extra_kwargs = {
            'name': {'required': True, 'allow_blank': False},
            'email': {'required': True, 'allow_blank': False},
            'company': {'required': True, 'allow_blank': False},
            'phone': {'required': False, 'allow_blank': True},
            'lost_reason': {'required': False, 'allow_blank': True},
        }

    def validate_name(self, name):
        if not name or not name.strip():
            raise serializers.ValidationError("Name cannot be empty or contain only spaces")
        return name.strip()

    def validate_email(self, email):
        if not email:
            raise serializers.ValidationError("Email cannot be empty")
        email_normalized = email.strip().lower()
        user = self.context.get('request').user
        if self.instance:
            duplicate = Lead.objects.filter(owner=user,email__iexact=email_normalized).exclude(pk=self.instance.pk).exists()
        else:
            duplicate = Lead.objects.filter(owner=user,email__iexact=email_normalized).exists()

        if duplicate:
            raise serializers.ValidationError("You already have a lead with this email address")

        return email_normalized

    def validate_company(self, company):
        if not company or not company.strip():
            raise serializers.ValidationError("Company cannot be empty or contain only spaces")
        return company.strip()



    def validate(self, data):

        if 'status' in data:
            status = data['status']
        elif self.instance:
            status = self.instance.status
        else:
            status = None
        if 'lost_reason' in data:
            lost_reason = data['lost_reason']
        elif self.instance:
            lost_reason = self.instance.lost_reason
        else:
            lost_reason = None
        if status == 'Lost':
            if not lost_reason or not lost_reason.strip():
                raise serializers.ValidationError({
                    'lost_reason': 'Lost reason is required when status is "Lost"'
                })

        return data