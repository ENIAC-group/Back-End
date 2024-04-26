from rest_framework import serializers 
from .models import TreatementHistory , MedicalRecord 
import json


class TreatementHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TreatementHistory
        fields = '__all__'

    def is_valid(self, *, raise_exception=False):
        
        return super().is_valid(raise_exception=raise_exception)
    
    def run_validation(self, data=...):
        
        return super().run_validation(data)
    
    def validate(self, attrs):
        return super().validate(attrs)

    def validate(self, attrs):
        return super().validate(attrs)


class MedicalRecordSerializer(serializers.ModelSerializer):
    
    def __init__(self, instance=None, data=..., **kwargs):
        self.treatementHistory1 = TreatementHistorySerializer()
        self.treatementHistory2 = TreatementHistorySerializer()
        self.treatementHistory3 = TreatementHistorySerializer()
        self.stored_validated_data = None
        super().__init__(instance, data, **kwargs)

    class Meta:
        model = MedicalRecord
        fields = ['child_num' , 'family_history' , 'nationalID' , 'id' ] # , 'treatementHistory1' , 'treatementHistory2' , 'treatementHistory3' 
        extra_kwargs = {
            'treatementHistory1': {'required': False}, 
            'treatementHistory2': {'required': False},
            'treatementHistory3': {'required': False}
        }
    
    def is_valid(self, *, raise_exception=False):
        validated_data = self.run_validation(self.initial_data)
        self.stored_validated_data = validated_data
        valid = super().is_valid(raise_exception=raise_exception)
        return valid
    
    def run_validation(self, data=...):
        data_dict = {key: value[0] for key, value in data.lists()}
        serializer = self.__class__()
        child_num = data.get('child_num')
        family_history = data.get('family_history')
        nationalID = data.get('nationalID')
        medical_record = {}
        # Validate child_num
        try:
            validated_child_num = serializer.fields['child_num'].run_validation(child_num)
            medical_record['child_num'] = validated_child_num
        except serializers.ValidationError as exc:
            raise serializers.ValidationError({'child_num': exc.detail})

        # Validate family_history
        try:
            validated_family_history = serializer.fields['family_history'].run_validation(family_history)
            medical_record['family_history']  = validated_family_history
        except serializers.ValidationError as exc:
            raise serializers.ValidationError({'family_history': exc.detail})

        # Validate nationalID
        try:
            validated_nationalID = serializer.fields['nationalID'].run_validation(nationalID)
            medical_record['nationalID'] = validated_nationalID
        except serializers.ValidationError as exc:
            raise serializers.ValidationError({'nationalID': exc.detail})


        if 'treatementHistory1' in data_dict.keys() :             
            treatementHistory1 = json.loads(data_dict['treatementHistory1']) 
            seializer1 = TreatementHistorySerializer(data= treatementHistory1 )
            seializer1.is_valid(raise_exception=True )
            value = seializer1.validated_data
            medical_record['treatementHistory1'] = dict(value)
           
        if 'treatementHistory2' in data_dict.keys() : 
            treatementHistory2 = json.loads(data_dict['treatementHistory2']) 
            seializer2 = TreatementHistorySerializer(data= treatementHistory2 )
            seializer2.is_valid(raise_exception=True )
            value = (seializer2.validated_data)
            medical_record['treatementHistory2'] = dict(value)


        if 'treatementHistory3' in data_dict.keys() : 
            treatementHistory3 = json.loads(data_dict['treatementHistory3'])
            data_dict.pop('treatementHistory3')
            seializer3 = TreatementHistorySerializer(data= treatementHistory3 )
            seializer3.is_valid(raise_exception=True )
            value = seializer3.validated_data
            value = (seializer3.validated_data)
            medical_record['treatementHistory3'] = dict(value)

        return medical_record
    

    def validate_empty_values(self, data):
        print("data 2222  : " , data )
        return super().validate_empty_values(data)
    
    def create(self, validated_data):
        print("in creaet methoooooooooooooooooood ")
        treatement_history1 = validated_data.pop('treatementHistory1')
        treatement_history2 = validated_data.pop('treatementHistory2')
        treatement_history3 = validated_data.pop("treatementHistory3")
        medical_record = MedicalRecord.objects.create(**validated_data)
        if treatement_history1 : 
            tr1 = TreatementHistory.objects.create(**treatement_history1)
            medical_record.treatementHistory3 = tr1
        if treatement_history2 : 
            tr2 = TreatementHistory.objects.create(**treatement_history2)
            medical_record.treatementHistory3 = tr2
        if treatement_history3 : 
            tr3 = TreatementHistory.objects.create(**treatement_history3)
            medical_record.treatementHistory3 = tr3
        return medical_record


    # def update(self, instance, validated_data):
    #     treatement_history1 = validated_data.pop('treatementHistory1')
    #     treatement_history2 = validated_data.pop('treatementHistory2')
    #     treatement_history3 = validated_data.pop('treatementHistory3')

    #     instance.child_num = validated_data.get('child_num', instance.child_num)
    #     instance.family_history = validated_data.get('family_history', instance.family_history)
    #     instance.nationalID = validated_data.get('nationalID', instance.nationalID)
    #     instance.save()

    #     treatements_pool = []
    #     old_ids = []

    #     if instance.treatementHistory1 : 
    #         old_ids.append(instance.treatementHistory1.id)
    #     if instance.treatementHistory2 : 
    #         old_ids.append(instance.treatementHistory2.id)
    #     if instance.treatementHistory3 : 
    #         old_ids.append(instance.treatementHistory3.id)

    #     if treatement_history1 : 
    #         treatements_pool.append(treatement_history1)
    #     if treatement_history2 : 
    #         treatements_pool.append(treatement_history2)
    #     if treatement_history3 : 
    #         treatements_pool.append(treatement_history3)
        

    #     for treatement in treatements_pool:
    #         if treatement['id'] in old_ids : 
    #             if TreatementHistory.objects.filter(id = treatement['id'] ).exists():
    #                 treatement_instance = TreatementHistory.objects.get(id=treatement['id'])
    #                 treatement_instance.end_date = treatement.get('end_date', treatement_instance.end_date)
    #                 treatement_instance.length = treatement.get('length',treatement_instance.length)
    #                 treatement_instance.is_finished = treatement.get('is_finished' , treatement_instance.is_finished)
    #                 treatement_instance.reason_to_leave = treatement.get('reason_to_leave' , treatement_instance.reason_to_leave)
    #                 treatement_instance.approach = treatement.get('approach' , treatement_instance.approach )
    #                 treatement_instance.special_drugs = treatement.get('special_drugs' , treatement_instance.special_drugs ) 
    #                 treatement_instance.save()
    #             else:
    #                 continue
    #         else:
    #             new_treatement = TreatementHistory.objects.create( **treatement)
    #             if not instance.treatementHistory1: 
    #                 instance.treatementHistory1 = new_treatement
    #             elif not instance.treatementHistory2 : 
    #                 instance.treatementHistory2 = new_treatement
                
    #             elif not instance.treatementHistory3 : 
    #                 instance.treatementHistory3 = new_treatement 

    #     return instance
    

    