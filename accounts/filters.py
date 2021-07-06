import django_filters
from django_filters import DateFilter

from .models import *

class NHANSUFilter(django_filters.FilterSet):
    gioi_tinh = (
        ('Nam', 'Nam'),
        ('Nữ', 'Nữ'),        
    )
    
    MaNV = django_filters.CharFilter(label = 'Mã nhân viên')
    HoTen = django_filters.CharFilter(label = 'Họ tên') 
    CMND = django_filters.NumberFilter(label = 'CMND')
    NgaySinh = django_filters.DateFilter(label = 'Ngày sinh')
    GioiTinh = django_filters.ChoiceFilter(label = 'Giới tính', choices = gioi_tinh)
    QueQuan = django_filters.CharFilter(label = 'Quê quán') 
    ChucVu = django_filters.CharFilter(label = 'Chức vụ') 
    
    class Meta:
        model = NHANSU
        fields = '__all__'
        
class KYLUATFilter(django_filters.FilterSet):
    ID = django_filters.NumberFilter(label = 'ID')
    MaNV = django_filters.CharFilter(label = 'Mã nhân viên')
    TenLoi = django_filters.CharFilter(label = 'Tên lỗi')
    
    class Meta:
        model = KYLUAT
        fields = '__all__'
        
class PHONGFilter(django_filters.FilterSet):
    gioi_tinh = (
        ('Nam', 'Nam'),
        ('Nữ', 'Nữ'),        
    )
    day_nha = (
        ('B3', 'B3'),
        ('B4', 'B4'),
        ('B5', 'B5'),
        ('B6', 'B6'),
        ('B7', 'B7'),
        ('B7bis', 'B7bis'),
        ('B8', 'B8'),
        ('B9', 'B9'),
        ('B10', 'B10'),
        ('B13', 'B13'),
    )
    
    MaPhong = django_filters.NumberFilter(label='Mã phòng')
    TenPhong = django_filters.CharFilter(label='Tên phòng')
    DayNha = django_filters.ChoiceFilter(label='Dãy nhà', choices = day_nha)
    SoLuongSV = django_filters.NumberFilter(label='Số lượng SV')
    LoaiPhong = django_filters.NumberFilter(label='Loại phòng')
    GiaPhong = django_filters.NumberFilter(label='Giá phòng')
    GioiTinhSV = django_filters.ChoiceFilter(label = 'Giới tính SV', choices = gioi_tinh)
    
    class Meta:
        model = PHONG
        fields = '__all__'
        
class QUANLYFilter(django_filters.FilterSet):
    MaQL = django_filters.CharFilter(label='Mã quản lý')
    MaNV = django_filters.CharFilter(label='Mã nhân viên')
    DayNha = django_filters.CharFilter(label='Phụ trách dãy nhà')
    
    class Meta:
        model = QUANLY
        fields = '__all__'
   

class SINHVIENFilter(django_filters.FilterSet):
    gioi_tinh = (
        ('Nam', 'Nam'),
        ('Nữ', 'Nữ'),
    )

    MaSV = django_filters.CharFilter(label='Mã Sinh viên')
    HoTen = django_filters.CharFilter(label='Họ tên')
    CMND = django_filters.NumberFilter(label='CMND')
    Ngaysinh = django_filters.DateFilter(label='Ngày sinh')
    GioiTinh = django_filters.ChoiceFilter(label='Giới tính', choices=gioi_tinh)
    QueQuan = django_filters.CharFilter(label='Quê quán')

    class Meta:
        model = SINHVIEN
        fields = '__all__'


class TAISANFilter(django_filters.FilterSet):
    Change = (
        ('New', 'Thay mới'),
        ('Fix', 'Sửa chữa')
    )
    ID = django_filters.NumberFilter(label='ID')
    TenPhong = django_filters.NumberFilter(label='Mã Phòng')
    TenTS = django_filters.CharFilter(label='Tên Tài sản')
    SoLuong = django_filters.NumberFilter(label='Số lượng')
    ThayDoi = models.CharField(max_length=100, choices=Change)
    GiaTri = models.DecimalField(max_digits=10,decimal_places=0)

    class Meta:
        model = TAISAN
        fields = '__all__'


class SCTAISANFilter(django_filters.FilterSet):
    Change = (
        ('New', 'Thay mới'),
        ('Fix', 'Sửa chữa')
    )
    ID = django_filters.NumberFilter(label='ID')
    TenPhong = django_filters.NumberFilter(label='Tên Phòng')
    TenTS = django_filters.CharFilter(label='Tên Tài sản')
    SoLuong = django_filters.NumberFilter(label='Số lượng')
    ThayDoi = models.CharField(max_length=3, choices=Change)
    NgayTao = django_filters.DateFilter(label='Ngày tạo')
    NgaySua = django_filters.DateFilter(label='Ngày sửa')

    class Meta:
        model = CTTAISAN
        fields = '__all__'