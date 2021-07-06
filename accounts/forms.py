from django.forms import ModelForm 
from .models import *
from django.contrib.auth.forms import User
from django.contrib.auth.forms import UserCreationForm
from django import forms

class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        exclude = ['user']
        
class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','password1','password2','groups']


#------------------------------------------------------------
# Manager Forms
class EditRoomInfo(ModelForm):
    class Meta:
        model = PHONG
        fields = '__all__'
        
        widgets = {
            'MaPhong': forms.NumberInput(attrs={'class': 'form-control'}),
            'TenPhong': forms.TextInput(attrs={'class': 'form-control'}),
            'DayNha': forms.Select(attrs={'class': 'form-control'}),
            'SoLuongSV': forms.NumberInput(attrs={'class': 'form-control'}),
            'LoaiPhong': forms.NumberInput(attrs={'class': 'form-control'}),
            'GiaPhong': forms.NumberInput(attrs={'class': 'form-control'}),
            'GioiTinhSV': forms.Select(attrs={'class': 'form-control'}),
        }

        labels = {
            'MaPhong': "Mã phòng",
            'TenPhong': "Tên phòng",
            'DayNha': "Dãy nhà",
            'SoLuongSV': "Số lượng sinh viên tối đa",
            'LoaiPhong': "Loại phòng",
            'GiaPhong': "Giá phòng",
            'GioiTinhSV': "Giới tính sinh viên",
        }

class AddNewRoom(ModelForm):
    class Meta:
        model = PHONG
        fields = '__all__'
        
        widgets = {
            'MaPhong': forms.NumberInput(attrs={'class': 'form-control'}),
            'TenPhong': forms.TextInput(attrs={'class': 'form-control'}),
            'DayNha': forms.Select(attrs={'class': 'form-control'}),
            'SoLuongSV': forms.NumberInput(attrs={'class': 'form-control'}),
            'LoaiPhong': forms.NumberInput(attrs={'class': 'form-control'}),
            'GiaPhong': forms.NumberInput(attrs={'class': 'form-control'}),
            'GioiTinhSV': forms.Select(attrs={'class': 'form-control'}),
        }

        labels = {
            'MaPhong': "Mã phòng",
            'TenPhong': "Tên phòng",
            'DayNha': "Dãy nhà",
            'SoLuongSV': "Số lượng sinh viên tối đa",
            'LoaiPhong': "Loại phòng",
            'GiaPhong': "Giá phòng",
            'GioiTinhSV': "Giới tính sinh viên",
        }

class EditStudentInfo(ModelForm):
    class Meta:
        model = SINHVIEN
        fields = '__all__'

        widgets = {
            'MaSV': forms.NumberInput(attrs={'class': 'form-control'}),
            'HoTen': forms.TextInput(attrs={'class': 'form-control'}),
            'CMND': forms.NumberInput(attrs={'class': 'form-control'}),
            'NgaySinh': forms.DateInput(attrs={'class': 'form-control'}),
            'GioiTinh': forms.Select(attrs={'class': 'form-control'}),
            'QueQuan': forms.TextInput(attrs={'class': 'form-control'}),
        }

        labels = {
            'MaSV': 'Mã sinh viên',
            'HoTen': 'Họ và tên',
            'CMND': 'Số chứng minh nhân dân/Căn cước công dân',
            'NgaySinh': 'Ngày tháng năm sinh',
            'GioiTinh': 'Giới tính',
            'QueQuan': 'Quê quán',
        }

class AddNewStudent(ModelForm):
    class Meta:
        model = SINHVIEN
        fields = '__all__'
        
        widgets = {
            'MaSV': forms.NumberInput(attrs={'class': 'form-control'}),
            'HoTen': forms.TextInput(attrs={'class': 'form-control'}),
            'CMND': forms.TextInput(attrs={'class': 'form-control'}),
            'NgaySinh': forms.DateInput(attrs={'class': 'form-control'}),
            'GioiTinh': forms.Select(attrs={'class': 'form-control'}),
            'QueQuan': forms.TextInput(attrs={'class': 'form-control'}),
        }

        labels = {
            'MaSV': 'Mã số sinh viên',
            'HoTen': 'Họ và tên',
            'CMND': 'Số chứng minh nhân dân/căn cước công dân',
            'NgaySinh': 'Ngày sinh',
            'GioiTinh': 'Giới tính',
            'QueQuan': 'Quê quán',
        }

class newElectricityBill(ModelForm):
    class Meta:
        model = TIENDIEN
        fields = '__all__'

        widgets = {
            'MaPhong': forms.Select(attrs={'class': 'form-control'}),
            'NgayLap': forms.DateInput(attrs={'class': 'form-control'}),
            'SoTien': forms.NumberInput(attrs={'class': 'form-control'}),
            'TrangThai': forms.Select(attrs={'class': 'form-control'}),
        }

        labels = {
            'MaPhong': 'Chọn phòng',
            'NgayLap': 'Ngày chốt số điện',
            'SoTien': 'Tiền điện tiêu thụ',
            'TrangThai': 'Trạng thái thu tiền',
        }

class AddNewBreakRule(ModelForm):
    class Meta:
        model = VIPHAM
        fields = '__all__'

        widgets = {
            'MaSV': forms.NumberInput(attrs={'class': 'form-control'}),
            'NgayVP': forms.DateInput(attrs={'class': 'form-control'}),
            'TenLoi': forms.TextInput(attrs={'class': 'form-control'}),
        }

        labels = {
            'MaSV': 'Mã số sinh viên',
            'NgayVP': 'Ngày vi phạm',
            'TenLoi': 'Tên lỗi vi phạm',
        }



#------------------------------------------------------------
# Director Forms
class NVForm(ModelForm):
    class Meta:
        model = NHANSU
        fields = '__all__'
        labels = {
            'MaNV': ('Mã nhân viên'),
            'HoTen': ('Họ tên'),
            'NgaySinh': ('Ngày Sinh'),
            'GioiTinh': ('Giới Tính'),
            'QueQuan': ('Quê quán'),
            'ChucVu': ('Chức vụ'),
            'SDT': ('Số điện thoại'),
        }
        
class KLForm(ModelForm):
    class Meta:
        model = KYLUAT
        fields = '__all__'
        labels = {
            'MaNV': ('Mã nhân viên'),
            'TenLoi': ('Tên lỗi'),
        }
        
class PhongForm(ModelForm):
    class Meta:
        model = PHONG
        fields = ['GiaPhong']
        labels = {
            'GiaPhong': ('Giá phòng'),
        }
        
class QLForm(ModelForm):
    class Meta:
        model = QUANLY
        fields = '__all__'
        labels = {
            'MaQL': ('Mã quản lý'),
            'MaNV': ('Mã nhân viên'),
            'DayNha': ('Dãy nhà'),
        }
        
class SVForm(ModelForm):
    class Meta:
        model = SINHVIEN
        fields = '__all__'
        
class PhongForm2(ModelForm):
    class Meta:
        model = PHONG
        fields = ['MaPhong']


# Tai San
class TSForm(ModelForm):
    class Meta:
        model = TAISAN
        fields = '__all__'
        labels = {
            'ID' : (' Mã ID'),
            'TenPhong' : (' Tên Phòng '),
            'TenTS' : ('Tên Tài sản'),
            'ThayDoi' : ('Thay đổi'),
            'SoLuong' : ('Số lượng'),
            'GiaTri' : ('Giá trị')
        }


class SCTSForm(ModelForm):
    class Meta:
        model = CTTAISAN
        fields = '__all__'
        labels = {
            'ID' : (' Mã ID'),
            'TenPhong' : (' Tên Phòng '),
            'TenTS' : ('Tên Tài sản'),
            'TinhTrang' : ('Tình trạng'),
            'SoLuong' : ('Số lượng'),
            'NgayTao' : ('Ngày tạo'),
            'NgaySua' : ('Ngày sửa')
        }
