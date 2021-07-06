from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# Giới tính
Gender = (
    ('Nam', 'Nam'),
    ('Nữ', 'Nữ')
)

class Customer(models.Model):
    POSITION = (
        ('Sinh viên', 'Sinh viên'),
        ('Quản lý', 'Quản lý'),
        ('Giám đốc', 'Giám đốc'),
    )
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length = 100, null = True)
    phone = models.CharField(max_length = 100, null = True)
    profile_pic = models.ImageField(null = True, blank = True)
    date_created = models.DateTimeField(auto_now_add = True, null = True)
    position = models.CharField(max_length = 100, null = True, choices = POSITION)
    
    def __str__(self):
        return self.name
 

# Quan hệ Nhân sự
class NHANSU(models.Model):
    MaNV = models.IntegerField(primary_key=True)
    HoTen = models.CharField(max_length=25)
    CMND = models.IntegerField()
    NgaySinh = models.DateField()
    GioiTinh = models.CharField(max_length=6, choices=Gender)
    QueQuan = models.CharField(max_length=50)
    ChucVu = models.CharField(max_length=15)
    SDT = models.CharField(max_length = 100)
    
    def __str__(self):
        return str(self.HoTen) + " - " + str(self.MaNV)

    class Meta:
        db_table = 'NHANSU'

# Quan hệ dãy nhà
class DAYNHA (models.Model):
    DayNha = models.CharField(max_length = 100, primary_key = True, null = False)
    
    def __str__(self):
        return self.DayNha

    class Meta:
        db_table = 'DAYNHA'

# Quan hệ Phòng ký túc xá
class PHONG(models.Model):
    MaPhong = models.IntegerField(primary_key=True)
    TenPhong = models.CharField(max_length=10)
    DayNha = models.ForeignKey(DAYNHA, on_delete=models.CASCADE, null=True)
    SoLuongSV = models.IntegerField()
    LoaiPhong = models.IntegerField()
    GiaPhong = models.IntegerField()
    GioiTinhSV = models.CharField(max_length=6, choices=Gender)

    def __str__(self):
        return str(self.TenPhong) + " - " + str(self.DayNha)

    class Meta:
        db_table = 'PHONG'

# Quan hệ Sinh viên
class SINHVIEN(models.Model):
    MaSV = models.IntegerField(primary_key=True)
    HoTen = models.CharField(max_length=50)
    CMND = models.IntegerField()
    NgaySinh = models.DateField()
    GioiTinh = models.CharField(max_length=6, choices=Gender)
    QueQuan = models.CharField(max_length=50)

    def __str__(self):
        return str(self.HoTen) + " - " + str(self.MaSV)

    class Meta:
        db_table = 'SINHVIEN'

# Quan hệ Quản lý
class QUANLY (models.Model):
    MaQL = models.CharField(max_length = 100, default = "0") 
    MaNV = models.ForeignKey(NHANSU, on_delete = models.CASCADE, null = True)
    DayNha = models.ForeignKey(DAYNHA, on_delete = models.CASCADE, null = True)
    def __NHANSU__(self):
        return self.MaNV
    class Meta:
        db_table = 'QUANLY'

# Quan hệ Kỷ luật nhân viên
class KYLUAT(models.Model):
    ID = models.IntegerField(primary_key=True)
    MaNV = models.ForeignKey(NHANSU, on_delete=models.CASCADE)
    TenLoi = models.CharField(max_length=50)

    class Meta:
        db_table = 'KYLUAT'

# Quan hệ Tài sản
class TAISAN(models.Model):
    MaPhong = models.ForeignKey(PHONG, on_delete=models.CASCADE)
    TenTS = models.CharField(max_length=50)
    SoLuong = models.IntegerField()

    class Meta:
        unique_together = (('MaPhong', 'TenTS'),)
        db_table = 'TAISAN'

# Quan hệ Chi tiết tài sản
class CTTAISAN(models.Model):
    Change = (
        ('New', 'Thay mới'),
        ('Fix', 'Sửa chữa')
    )

    ID = models.IntegerField(primary_key=True)
    MaPhong = models.ForeignKey(PHONG, on_delete=models.CASCADE)
    TenTS = models.CharField(max_length=20)
    TinhTrang = models.CharField(max_length=20)
    SoLuong = models.IntegerField()
    NgayTao = models.DateField()
    NgaySua = models.DateField()

    class Meta:
        db_table = 'CTTAISAN'

# Quan hệ Xếp phòng
class XEPPHONG(models.Model):
    MaPhong = models.ForeignKey(PHONG, on_delete=models.CASCADE)
    MaSV = models.ForeignKey(SINHVIEN, on_delete=models.CASCADE)
    NgayVao = models.DateField()
    NgayRa = models.DateField(null = True)
    
    class Meta:
        db_table = 'XEPPHONG'

# Quan hệ Tiền phòng
class TIENPHONG(models.Model):
    Status = (
        ('Paied', 'Paied'),
        ('Not paid', 'Not paid')
    )

    NgayLap = models.DateField()
    MaSV = models.ForeignKey(SINHVIEN, on_delete=models.CASCADE)
    SoTien = models.IntegerField()
    TrangThai = models.CharField(max_length=10, choices=Status)

    class Meta:
        unique_together = (('NgayLap', 'MaSV'),)
        db_table = 'TIENPHONG'

class TIENDIEN(models.Model):
    Status = (
        ('Paied', 'Đã nộp'),
        ('Not paid', 'Chưa nộp')
    )

    MaPhong = models.ForeignKey(PHONG, on_delete=models.CASCADE)
    NgayLap = models.DateField()
    SoTien = models.IntegerField()
    TrangThai = models.CharField(max_length=10, choices=Status)

    class Meta:
        db_table = 'TIENDIEN'

# Quan hệ Vi phạm của sinh viên
class VIPHAM(models.Model):
    MaSV = models.ForeignKey(SINHVIEN, on_delete=models.CASCADE)
    NgayVP = models.DateField()
    TenLoi = models.CharField(max_length=50)

    class Meta:
        db_table = 'VIPHAM'
