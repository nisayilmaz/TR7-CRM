from datetime import date
from wsgiref.util import FileWrapper

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Sum, Count, Q
from django.db.models.functions import TruncMonth, ExtractMonth, Lower
from django.http import FileResponse, HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework import permissions
from .models import Company, People, Project, FinishedProject, FileModel
from .serializers import *
from knox.auth import TokenAuthentication as KnoxTokenAuthentication
from knox.models import AuthToken
from django.core.mail import send_mail
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from crm.settings import EMAIL_HOST_USER
import os
import pandas
import openpyxl


class CompanyApiView(APIView):
    authentication_classes = [KnoxTokenAuthentication]
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        companies = Company.objects.all().order_by(Lower('name')).values()
        serializer = CompanySerializer(companies, many=True)
        return Response({'status': 'success', 'data': serializer.data}, status=status.HTTP_200_OK)

    # 2. Create
    def post(self, request, *args, **kwargs):
        token = request.META.get('HTTP_AUTHORIZATION', None)
        user = None
        if token:
            token = token.split(" ")[1]
            user = AuthToken.objects.get(token_key=token[0:8]).user

        data = {
            'name': request.data.get('name'),
            'role': request.data.get('role'),
            'email': request.data.get('email'),
            'phone': request.data.get('phone'),
            'address': request.data.get('address'),
            'registered_by': user.id
        }
        serializer = CompanySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'success', 'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'status': 'failed', 'data': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class CompanyByRoleList(APIView):
    authentication_classes = [KnoxTokenAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = CompanySerializer

    def get(self, request, role):
        try:
            companies = Company.objects.filter(role=role).order_by(Lower('name')).values()
            serializer = CompanySerializer(companies, many=True)
            return Response({'status': 'success', 'data': serializer.data}, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'status': 'failed', 'data': []}, status=status.HTTP_404_NOT_FOUND)


class CompanyApiDetailView(APIView):
    authentication_classes = [KnoxTokenAuthentication]
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, pk):
        try:
            company = Company.objects.get(pk=pk)
            serializer = CompanySerializer(company, many=False)
            return Response({'status': 'success', 'data': serializer.data}, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'status': 'failed', 'data': []}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            company = Company.objects.get(pk=pk)
            company.delete()
            return Response({'status': 'success', 'data': []}, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'status': 'failed', 'data': []}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        instance = Company.objects.get(pk=pk)
        if not instance:
            return Response(
                {"res": "Object with id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        data = {
            'name': request.data.get('name', None),
            'email': request.data.get('email', None),
            'phone': request.data.get('phone', None),
            'address': request.data.get('address', None),
            'registered_by': request.data.get('registered_by', None)
        }
        non_empty_data = {}
        for key, value in data.items():
            if value:
                non_empty_data[key] = value
        serializer = CompanySerializer(instance=instance, data=non_empty_data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PeopleApiView(APIView):
    authentication_classes = [KnoxTokenAuthentication]
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        people = People.objects.all().order_by(Lower('first_name'))
        serializer = PeopleSerializer(people, many=True)
        return Response({'status': 'success', 'data': serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = {
            'first_name': request.data.get('first_name'),
            'last_name': request.data.get('last_name'),
            'email': request.data.get('email'),
            'phone': request.data.get('phone'),
            'company': request.data.get('company')
        }
        serializer = PeopleSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'success', 'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'status': 'failed', 'data': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class PeopleApiDetailView(APIView):
    authentication_classes = [KnoxTokenAuthentication]
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, pk):
        try:
            person = People.objects.get(pk=pk)
            serializer = PeopleSerializer(person, many=False)
            return Response({'status': 'success', 'data': serializer.data}, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'status': 'failed', 'data': []}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            person = People.objects.get(pk=pk)
            person.delete()
            return Response({'status': 'success', 'data': []}, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'status': 'failed', 'data': []}, status=status.HTTP_404_NOT_FOUND)


class ProjectApiView(APIView):
    authentication_classes = [KnoxTokenAuthentication]
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        token = request.META.get('HTTP_AUTHORIZATION', None)
        user = None
        if token:
            token = token.split(" ")[1]
            user = AuthToken.objects.get(token_key=token[0:8]).user
        role = None
        if user:
            role = user.role

        if role == 1:
            projects = Project.objects.all()
        elif role == 2:
            projects = Project.objects.filter(registered_by=user)
        serializer = ProjectSerializer(projects, many=True)
        return Response({'status': 'success', 'data': serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        token = request.META.get('HTTP_AUTHORIZATION', None)
        user = None
        if token:
            token = token.split(" ")[1]
            user = AuthToken.objects.get(token_key=token[0:8]).user
        data = {
            'client': request.data.get('client'),
            'partner': request.data.get('partner'),
            'registration_date': request.data.get('registration_date'),
            'exp_end_date': request.data.get('exp_end_date'),
            'tender_date': request.data.get('tender_date'),
            'info': request.data.get('info'),
            'count': request.data.get('count'),
            'client_contact': request.data.get('client_contact'),
            'partner_contact': request.data.get('partner_contact'),
            'product': request.data.get('product'),
            'budget': request.data.get('budget'),
            'poc_request': request.data.get('poc_request'),
            'probability': request.data.get('probability'),
            'registered_by': user.id
        }
        serializer = ProjectSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'success', 'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'status': 'failed', 'data': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class ProjectApiDetailView(APIView):
    authentication_classes = [KnoxTokenAuthentication]
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, pk):
        try:
            project = Project.objects.get(pk=pk)
            serializer = ProjectSerializer(project, many=False)
            return Response({'status': 'success', 'data': serializer.data}, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'status': 'failed', 'data': []}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            project = Project.objects.get(pk=pk)
            project.delete()
            return Response({'status': 'success', 'data': []}, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'status': 'failed', 'data': []}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        instance = Project.objects.get(pk=pk)
        if not instance:
            return Response(
                {"res": "Object with id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        data = {
            'client': request.data.get('client', None),
            'partner': request.data.get('partner', None),
            'registration_date': request.data.get('registration_date', None),
            'exp_end_date': request.data.get('exp_end_date', None),
            'tender_date': request.data.get('tender_date', None),
            'info': request.data.get('info', None),
            'count': request.data.get('count', None),
            'client_contact': request.data.get('client_contact', None),
            'partner_contact': request.data.get('partner_contact', None),
            'product': request.data.get('product', None),
            'budget': request.data.get('budget', None),
            'poc_request': request.data.get('poc_request', None),
            'probability': request.data.get('probability', None),
            'registered_by': request.data.get('registered_by', None),
        }
        non_empty_data = {}
        for key, value in data.items():
            if value:
                non_empty_data[key] = value
        serializer = ProjectSerializer(instance=instance, data=non_empty_data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductApiView(APIView):
    authentication_classes = [KnoxTokenAuthentication]
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response({'status': 'success', 'data': serializer.data}, status=status.HTTP_200_OK)


class NotesApiView(APIView):
    authentication_classes = [KnoxTokenAuthentication]
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        data = {
            'title': request.data.get('title'),
            'note': request.data.get('note'),
            'project': request.data.get('project'),
            'category': request.data.get('category')
        }
        serializer = NotesSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'success', 'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'status': 'failed', 'data': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class NotesApiDetailView(APIView):
    # authentication_classes = [KnoxTokenAuthentication]
    # permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, pk, *args, **kwargs):
        notes = Notes.objects.filter(project=pk)
        notes = notes.order_by("-creation_date")
        serializer = NotesSerializer(notes, many=True)
        return Response({'status': 'success', 'data': serializer.data}, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        try:
            note = Notes.objects.get(pk=pk)
            note.delete()
            return Response({'status': 'success', 'data': []}, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'status': 'failed', 'data': []}, status=status.HTTP_404_NOT_FOUND)


class Statistics(APIView):
    authentication_classes = [KnoxTokenAuthentication]
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        companies = Company.objects
        client_cnt = companies.filter(role="client").count()
        partner_cnt = companies.filter(role="partner").count()
        projects = Project.objects.all()
        project_cnt = projects.count()
        active_projects = projects.filter(~Q(poc_request=8) & ~Q(poc_request=9) & ~Q(poc_request=10))
        budget = active_projects.aggregate(Sum('budget'))
        current_year = date.today().year
        finished_projects = FinishedProject.objects.all()
        total_sold = finished_projects.aggregate(Sum('invoice_amount'))
        fin_cnt = finished_projects.count()

        sales_by_month = finished_projects.filter(invoice_date__year=current_year) \
            .annotate(month=ExtractMonth('invoice_date')) \
            .values('month') \
            .annotate(count=Sum('invoice_amount')) \
            .values('month', 'count')

        registration_by_month = projects.filter(registration_date__year=current_year) \
            .annotate(month=ExtractMonth('registration_date')) \
            .values('month') \
            .annotate(count=Count('pk')) \
            .values('month', 'count')

        sales = [0] * 12
        registration =[0] * 12
        for item in sales_by_month:
            if item.get("month", None) is not None:
                sales[item.get("month", 0) - 1] = item.get("count", 0)

        for item in registration_by_month:
            if item.get("month", None) is not None:
                registration[item.get("month", 0) - 1] = item.get("count", 0)

        data = {
            "client_cnt": client_cnt,
            "partner_cnt": partner_cnt,
            "project_cnt": project_cnt,
            "fin_cnt": fin_cnt,
            "total_budget": budget["budget__sum"],
            "monthly_sales": sales,
            "monthly_reg": registration,
            "total_sold": total_sold["invoice_amount__sum"]
        }
        return Response({'status': 'success', 'data': data}, status=status.HTTP_200_OK)


class FinishedProjectApiView(APIView):
    authentication_classes = [KnoxTokenAuthentication]
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        token = request.META.get('HTTP_AUTHORIZATION', None)
        user = None
        if token:
            token = token.split(" ")[1]
            user = AuthToken.objects.get(token_key=token[0:8]).user
        role = None
        if user:
            role = user.role
        if role == 1:
            projects = FinishedProject.objects.all()
        elif role == 2:
            projects = FinishedProject.objects.filter(registered_by=user)
        serializer = FinishedProjectSerializer(projects, many=True)
        return Response({'status': 'success', 'data': serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = {
            'client': request.data.get('client'),
            'partner': request.data.get('partner', None),
            'count': request.data.get('count'),
            'product': request.data.get('product'),
            'budget': request.data.get('budget'),
            'invoice_date': request.data.get('invoice_date'),
            'invoice_amount': request.data.get('invoice_amount'),
            'end_date': request.data.get('end_date'),
            'project': request.data.get('project'),
            'registered_by': request.data.get('registered_by'),
        }
        serializer = FinishedProjectSerializer(data=data)
        if serializer.is_valid():
            project = serializer.save()
            files = request.FILES.getlist('files')

            for file in files:
                file_instance = FileModel(project=project, file=file)
                # Save each file instance
                file_instance.save()

            return Response({'status': 'success', 'data': serializer.data}, status=status.HTTP_201_CREATED)

        return Response({'status': 'failed', 'data': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class FilesView(APIView):
    def get(self, request):
        files = FileModel.objects.all()
        serializer = FileSerializer(files, many=True)
        return Response({'status': 'success', 'data': serializer.data}, status=status.HTTP_200_OK)


def download(request, pk):
    fileObj = FileModel.objects.get(pk=pk)
    file_handle = fileObj.file.open()
    file_name = os.path.basename(str(file_handle))
    # send file
    response = FileResponse(file_handle, content_type='application/pdf')
    response['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, responseType, Content-Disposition'
    response['Content-Disposition'] = 'attachment; filename="' + file_name + '"'
    response['Content-Length'] = fileObj.file.size
    return response


class MailerView(APIView):
    @csrf_exempt
    def post(self,request):
        email = request.data.get('email')
        password = request.data.get('password')
        subject = 'TR7 CRM Giriş Bilgileri'
        message = ''' TR7 CRM'e  giriş yapmak için aşağıdaki bilgileri kullanabilirsiniz.\n
        Email : {email}
        Şifre : {password}'''.format(email=email, password=password)
        sender_email = EMAIL_HOST_USER
        send_mail(subject, message, sender_email, [email])

        return JsonResponse({'message': 'Account created successfully and email sent'})


class DownloadDatabaseExcel(APIView):

    def get(self, request):
        # projects sheet
        projects = Project.objects.all()
        projects_list = []
        poc = {"1": "Toplantı Aşaması", "2": "POC Talebi", "3": "POC Aşaması", "4": "POC Gerçekleştirildi", "5": "Yaklaşık Maliyet",
         "6": "Alım Aşaması", "7": "Pazarlık Aşaması", "8": "Gerçekleşti", "9": "Kapandı", "10": "Kaybedildi"}
        for project in projects:
            partner = ""
            partner_contact = ""
            client_contact = ""
            start_date = ""
            end_date = ""
            tender_date = ""
            info = ""
            if project.partner_contact:
                partner_contact = project.partner_contact.first_name + project.partner_contact.last_name
            if project.partner:
                partner = project.partner.name
            if project.client_contact:
                client_contact = project.client_contact.first_name + project.client_contact.last_name
            if project.registration_date:
                start_date = project.registration_date
            if project.tender_date:
                end_date = project.tender_date
            if project.exp_end_date:
                tender_date = project.exp_end_date
            if project.info:
                info = project.info

            projects_list.append(
                {
                    'Son Kullanıcı': project.client.name,
                    'İş Ortağı': partner,
                    'Son Kullanıcı İlgili Kişi': client_contact,
                    'İş Ortağı İlgili Kişi': partner_contact,
                    'Account Manager': project.registered_by.first_name + " " + project.registered_by.last_name,
                    'Ürün': project.product.name,
                    'Adet': project.count,
                    'POC': poc.get(project.poc_request),
                    'Olasılık': project.probability,
                    'Bütçe': project.budget,
                    'Fırsat Tarihi': start_date,
                    'İhale Tarihi': tender_date,
                    'Tahmini Kapanış Tarihi': end_date,
                    'Açıklama': info

                }
            )

        clients = Company.objects.filter(role="client")
        clients_list = []
        for client in clients:
            address = ""
            phone = ""
            mail = ""

            if client.address:
                address = client.address
            if client.phone:
                phone = client.phone
            if client.email:
                mail = client.email
            clients_list.append(
                {
                    'Son Kullanıcı': client.name,
                    'Adres': address,
                    'Telefon': phone,
                    'Email': mail
                }
            )
        partners = Company.objects.filter(role="partner")
        partners_list = []
        for partner in partners:
            address = ""
            phone = ""
            mail = ""

            if partner.address:
                address = partner.address
            if partner.phone:
                phone = partner.phone
            if partner.email:
                mail = partner.email
            partners_list.append(
                {
                    'Son Kullanıcı': partner.name,
                    'Adres': address,
                    'Telefon': phone,
                    'Email': mail
                }
            )
        df = pandas.DataFrame(projects_list)
        clients_df = pandas.DataFrame(clients_list)
        partners_df = pandas.DataFrame(partners_list)
        file_path = '../reports/TR7_CRM_Ozet_{}.xlsx'.format(date.today())
        file_name = 'TR7_CRM_Ozet_{}.xlsx'.format(date.today())
        directory = os.path.dirname(file_path)

        # Create the directory if it doesn't exist
        if not os.path.exists(directory):
            os.makedirs(directory)

        writer = pandas.ExcelWriter(file_path)
        df.to_excel(writer, sheet_name='Fırsatlar', index=False, na_rep='NaN')
        clients_df.to_excel(writer, sheet_name='Kurumlar', index=False, na_rep='NaN')
        partners_df.to_excel(writer, sheet_name='İş Ortakları', index=False, na_rep='NaN')
        calculate_width(df, 'Fırsatlar', writer)
        calculate_width(clients_df, 'Kurumlar', writer)
        calculate_width(partners_df, 'İş Ortakları', writer)
        writer.close()
        with open(file_path, 'rb') as file:
            response = HttpResponse(FileWrapper(file),
                                    content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = f'attachment; filename={file_name}'
            return response


def calculate_width(df, sheet_name,writer):
    for column in df:
        column_width = max(df[column].astype(str).map(len).max(), len(column))
        col_idx = df.columns.get_loc(column)
        if column_width < 100:
            writer.sheets[sheet_name].set_column(col_idx, col_idx, column_width)
        else:
            writer.sheets[sheet_name].set_column(col_idx, col_idx, 100)