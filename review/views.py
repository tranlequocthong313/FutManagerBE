from datetime import datetime

from django.db.models import Avg, Count
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Field, Review
from .serializers import ReviewSerializer


class ReviewPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


class RatingView(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def create(self, request, field_pk=None):
        field = get_object_or_404(Field, pk=field_pk)
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, field=field)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, field_pk=None):
        field = get_object_or_404(Field, pk=field_pk)
        reviews = Review.objects.filter(field=field)
        average_rating = reviews.aggregate(Avg("rating"))["rating__avg"] or 0
        total_rating = reviews.count()

        paginator = ReviewPagination()
        page = paginator.paginate_queryset(reviews, request)
        if page is not None:
            serializer = ReviewSerializer(page, many=True)
            response_data = paginator.get_paginated_response(serializer.data).data
            response_data["average_rating"] = average_rating
            response_data["total_rating"] = total_rating
            return Response(response_data)

        serializer = ReviewSerializer(reviews, many=True)
        return Response(
            {
                "count": total_rating,
                "next": None,
                "previous": None,
                "average_rating": average_rating,
                "total_rating": total_rating,
                "results": serializer.data,
            }
        )


class RatingStatsView(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @action(
        methods=["get"],
        detail=True,
        url_path="ratings/stats",
        url_name="ratings_stats",
        permission_classes=[IsAuthenticated],
    )
    def stats(self, request, pk=None):
        month = request.query_params.get("month")
        year = request.query_params.get("year")

        if not month or not year:
            current_date = datetime.now()
            month = month or current_date.month
            year = year or current_date.year
        else:
            try:
                month = int(month)
                year = int(year)
            except ValueError:
                return Response(
                    {"status": 400, "message": "Invalid query params"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        if not (1 <= month <= 12) or year < 1900 or year > 2100:
            return Response(
                {"status": 400, "message": "Invalid query params"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        field = get_object_or_404(Field, pk=pk)

        reviews = Review.objects.filter(
            field=field, created_date__year=year, created_date__month=month
        )
        ratings_count = reviews.values("rating").annotate(count=Count("rating"))

        report = {str(i): 0 for i in range(1, 6)}
        for entry in ratings_count:
            report[str(entry["rating"])] = entry["count"]

        response_data = {
            "field_id": field.id,
            "field_name": field.name,
            "month": str(month).zfill(2),
            "year": str(year),
            "report": report,
        }

        return Response(response_data, status=status.HTTP_200_OK)
