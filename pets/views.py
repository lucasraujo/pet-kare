from rest_framework.views import APIView, status
from rest_framework.response import Response
from .serializers import PetSerializer
from traits.models import Trait
from groups.models import Group
from .models import Pet
from rest_framework.pagination import PageNumberPagination


class PetsView(APIView, PageNumberPagination):
    def post(self, request):
        pet_serializer = PetSerializer(data=request.data)
        pet_serializer.is_valid(raise_exception=True)
        pet_data = pet_serializer.validated_data
        group_data = pet_data.pop("group")
        traits_data = pet_data.pop("traits")

        group_to_pet = Group.objects.filter(scientific_name__iexact=group_data["scientific_name"]).first()
        if not group_to_pet:
            group_to_pet = Group.objects.create(**group_data)
        pet_data["group"] = group_to_pet

        new_pet = Pet.objects.create(**pet_data)
        
        for trait in traits_data:
            trait_to_insert = Trait.objects.filter(name__iexact=trait["name"]).first()
            if not trait_to_insert:
                trait_to_insert = Trait.objects.create(**trait)
            new_pet.traits.add(trait_to_insert)
        
        new_pet.save()
        res = PetSerializer(new_pet)
        return Response(res.data, status=status.HTTP_201_CREATED)
    
    def get(self, request):
        trait = request.query_params.get("trait", None)
        if trait:
            allPets = Pet.objects.filter(traits__name=trait)
        else:
            allPets = Pet.objects.all()
        result_page = self.paginate_queryset(allPets, request)
        res = PetSerializer(result_page, many=True)
        return self.get_paginated_response(res.data)


class PetsViewWhithId(APIView):
    def get(self, request, pet_id):
        pet = Pet.objects.filter(id__exact=pet_id).first()
        if not pet: 
            return Response({"detail": "Not found."}, status.HTTP_404_NOT_FOUND)
        else:
            res = PetSerializer(pet)
            print(res.data)
            return Response(res.data)
        
    def patch(self, request, pet_id):
        pet_serializer = PetSerializer(data=request.data, partial=True)
        pet_serializer.is_valid(raise_exception=True)
        pet_find = Pet.objects.filter(id__exact=pet_id).first()
        pet_data = pet_serializer.validated_data
        group_data = pet_data.pop("group", None)
        traits_data = pet_data.pop("traits", None)

        if not pet_find: 
            return Response({"detail": "Not found."}, status.HTTP_404_NOT_FOUND)
        
        if group_data:
            group = Group.objects.filter(scientific_name__iexact=group_data["scientific_name"]).first()
            if not group:
                group = Group.objects.create(**group_data)
                pet_data["group"] = group

        for key, value in pet_data.items():
            setattr(pet_find, key, value)

        if traits_data:
            for traits in traits_data:
                tra = Trait.objects.filter(name__iexact=traits["name"]).first()
                if not tra:
                    tra = Trait.objects.create(**traits)
                    pet_find.traits.add(tra)

        pet_find.save()
        res = PetSerializer(pet_find)
        return Response(res.data, status=status.HTTP_200_OK)
    
    def delete(self, request, pet_id):
        pet_find = Pet.objects.filter(id__exact=pet_id).first()
        if not pet_find: 
            return Response({"detail": "Not found."}, status.HTTP_404_NOT_FOUND)
        pet_find.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)