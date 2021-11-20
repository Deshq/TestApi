from django.db.models.fields import files
from file_sharing.models import File
import django.core.files
from unittest.mock import Mock
import pytest
from django.core.files.uploadedfile import SimpleUploadedFile

class TestFileViews:

    #FileCreateView

    @pytest.mark.django_db
    def test_create_file_unauthorized(self, api_client):

        mock_file = Mock(spec=django.core.files.File)
        mock_file.name = 'test.png'
        mock_file.read.return_value = ("fake file contents")

        response = api_client.post(  
            "/api/v1/files/file/create/",    
            {
                "title": "Deshq test file",
                "slug": "deshq-test-file",
                "docfile": mock_file
            })

        assert response.status_code == 403

    @pytest.mark.django_db
    def test_create_file(self, create_user, api_client_with_credentials):

        assert File.objects.count() == 0

        mock_file = Mock(spec=django.core.files.File)
        mock_file.name = 'test.png'
        mock_file.read.return_value = ("fake file contents")

        user = create_user()
        data = {
                "title": "Deshq test file",
                "slug": "deshq-test-file",
                "user": user.id,
                "docfile": mock_file
            }
        response = api_client_with_credentials.post("/api/v1/files/file/create/", data)
        assert response.status_code == 201, response.data
        assert File.objects.count() == 1

    @pytest.mark.django_db
    def test_create_file_authorized(self, auto_login_user):

        assert File.objects.count() == 0
        client, user = auto_login_user()

        mock_file = Mock(spec=django.core.files.File)
        mock_file.name = 'test.png'
        mock_file.read.return_value = ("fake file contents")
        
        response = client.post(
            "/api/v1/files/file/create/",    
            {
                "title": "Deshq test file",
                "slug": "deshq-test-file",
                "user": user.id,
                "docfile": mock_file
            }
        )

        assert response.status_code == 201, response.data
        assert File.objects.all().count() == 1

    @pytest.mark.django_db
    def test_create_file_in_archive_authorized(self, auto_login_user):

        assert File.objects.count() == 0

        mock_file = Mock(spec=django.core.files.File)
        mock_file.name = 'test.png'
        mock_file.read.return_value = ("fake file contents")
        
        client, user = auto_login_user()

        response = client.post(
            "/api/v1/files/file/create/",    
            {
                "title": "Deshq test file",
                "slug": "deshq-test-file",
                "user": user.id,
                "docfile": mock_file,
                "in_archive": True
            }
        )

        assert response.status_code == 201, response.data
        assert File.objects.count() == 1
        assert File.objects.all().count() == 0
    
    
    #FilesListView

    @pytest.mark.django_db
    def test_get_list_unauthorized(self, api_client, create_user):

        user = create_user()

        mock_file = Mock(spec=django.core.files.File)
        mock_file.name = 'test.png'
        mock_file.read.return_value = ("fake file contents")

        file = File.objects.create(
            title='Deshq',
            slug='d-d-d',
            docfile=mock_file.name,
            user=user 
        )

        response = api_client.get('/api/v1/files/file/all/')
        assert response.status_code == 403

    @pytest.mark.django_db
    def test_get_list_authorized(self, auto_login_user):

        client, user = auto_login_user()

        mock_file = Mock(spec=django.core.files.File)
        mock_file.name = 'test.png'
        mock_file.read.return_value = ("fake file contents")

        file = File.objects.create(
            title='Deshq',
            slug='d-d-d',
            docfile=mock_file.name,
            user=user 
        )

        file2 = File.objects.create(
            title='Deshq232',
            slug='d-df-d',
            docfile=mock_file.name,
            user=user,
            in_archive=True
        )

        response = client.get('/api/v1/files/file/all/')
        assert response.status_code == 200, response.data
        assert len(response.data) == 1

    #FileDetailView

    @pytest.mark.django_db
    def test_get_file_detail_unauthorized(self, api_client, create_user):

        user = create_user()

        mock_file = Mock(spec=django.core.files.File)
        mock_file.name = 'test.png'
        mock_file.read.return_value = ("fake file contents")

        file = File.objects.create(
            title='Deshq',
            slug='d-d-d',
            docfile=mock_file.name,
            user=user 
        )

        response = api_client.get(f'/api/v1/files/file/detail/{file.id}/')
        assert response.status_code == 403

    @pytest.mark.django_db
    def test_delete_file_detail_notOwner(self, auto_login_user, create_user):

        user_test = create_user()
        client, user = auto_login_user()
        mock_file = Mock(spec=django.core.files.File)
        mock_file.name = 'test.png'
        mock_file.read.return_value = ("fake file contents")
        file = File.objects.create(
            title='Deshq',
            slug='d-d-d',
            docfile=mock_file.name,
            user=user_test 
        )
        response = client.get(f'/api/v1/files/file/detail/{file.id}/')
        assert response.status_code == 200

        response = client.delete(f'/api/v1/files/file/detail/{file.id}/')
        assert response.status_code == 403

    @pytest.mark.django_db
    def test_get_file_detail(self, auto_login_user):

        client, user = auto_login_user()
        mock_file = Mock(spec=django.core.files.File)
        mock_file.name = 'test.png'
        mock_file.read.return_value = ("fake file contents")
        file = File.objects.create(
            title='Deshq',
            slug='d-d-d',
            docfile=mock_file.name,
            user=user 
        )
        response = client.get(f'/api/v1/files/file/detail/{file.id}/')

        assert response.status_code == 200

    @pytest.mark.django_db
    def test_get_file_detail_NotFound(self, auto_login_user):
       
        client, user = auto_login_user()
        response = client.get(f'/api/v1/files/file/detail/1/')
        assert response.status_code == 404

    
    #FileGetAPIView

    @pytest.mark.django_db
    def test_get_urlfile_unauthorized(self, api_client, create_user):

        user = create_user()
        mock_file = Mock(spec=django.core.files.File)
        mock_file.name = 'test.png'
        mock_file.read.return_value = ("fake file contents")
        file = File.objects.create(
            title='Deshq',
            slug='d-d-d',
            docfile=mock_file.name,
            user=user 
        )

        response = api_client.get(f'/api/v1/files/file/get/{file.id}/')
        assert response.status_code == 403

    @pytest.mark.django_db
    def test_get_urlfile(self, auto_login_user):

        client, user = auto_login_user()
        mock_file = Mock(spec=django.core.files.File)
        mock_file.name = 'test.png'
        mock_file.read.return_value = ("fake file contents")
        file = File.objects.create(
            title='Deshq',
            slug='d-d-d',
            docfile=mock_file.name,
            user=user,
            countOfdownloads=11,
        )

        response = client.get(f'/api/v1/files/file/get/{file.id}/')
        assert response.status_code == 200


    #StatisticsUserProfileView

    @pytest.mark.django_db
    def test_get_statisticsUser_unauthorized(self, api_client):

        response = api_client.get(f'/api/v1/files/user/statistics/profile/')
        assert response.status_code == 403

    @pytest.mark.django_db
    def test_get_statisticsUser_noFiles_authorized(self, auto_login_user):

        client, user = auto_login_user()

        response = client.get(f'/api/v1/files/user/statistics/profile/')
        assert response.status_code == 404

    @pytest.mark.django_db
    def test_get_statisticsUser_authorized(self, auto_login_user):

        client, user = auto_login_user()
        mock_file = Mock(spec=django.core.files.File)
        mock_file.name = 'test.png'
        mock_file.read.return_value = ("fake file contents")
        file = File.objects.create(
            title='Deshq',
            slug='d-d-d',
            docfile=mock_file.name,
            user=user,
            countOfdownloads=11,
        )

        file2 = File.objects.create(
            title='Deshq232',
            slug='d-df-d',
            docfile=mock_file.name,
            user=user,
            countOfdownloads=0,
        )

        response = client.get(f'/api/v1/files/user/statistics/profile/')
        assert response.status_code == 200
        assert len(response.data) == 1


    # StatisticsView

    @pytest.mark.django_db
    def test_getstatistic_noPermission(self, auto_login_user):

        client, user = auto_login_user()
        response = client.get("/api/v1/files/admin/statistics/")
        assert response.status_code == 403

    @pytest.mark.django_db
    def test_getstatistic_hasPermission(self, auto_login_superUser):

        client, superuser = auto_login_superUser()
        response = client.get("/api/v1/files/admin/statistics/")
        assert response.status_code == 200

    # StatisticsProfileView

    @pytest.mark.django_db
    def test_getprofilestatistic_noPermission(self, auto_login_user):

        client, user = auto_login_user()
        response = client.get("/api/v1/files/admin/statistics/profile/")
        assert response.status_code == 403

    @pytest.mark.django_db
    def test_getprofilestatistic_hasPermission(self, auto_login_superUser):

        client, superuser = auto_login_superUser()
        response = client.get("/api/v1/files/admin/statistics/profile/")
        assert response.status_code == 200





