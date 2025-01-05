from django.urls import path
from .views import  get_all_data_filter, create_data, data_detail, filter_data, credit_analysis, main_page

urlpatterns = [
    path("", main_page, name="main_page"),  # Main page
    path("data/", get_all_data_filter, name="get_all_data_filter"),
    path("data/create/", create_data, name="create_data"),
    path("data/<int:pk>/", data_detail, name="data_detail"), # Pass in the primary key of the data
    path("data/filter/", filter_data, name="filter_data"), #enter query paramaters
    path("data/credit_analysis/", credit_analysis, name="credit_analysis_graphs"), #outputs graphs
]