from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import *
from .filters import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout 
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user, allowed_users
from django.contrib.auth.models import Group
from django.db.models import Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
#extracode
#from django.template import RequestContext
from .forms import *


# Create your views here.
#=======================================================
# Home without login
def home(request):
    context = {}
    return render(request,'homepage.html',context)

#@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            group = request.POST.get('groups')
            user.groups.add(group)
            Customer.objects.create(user=user)
            messages.success(request,'account created')
            return redirect('login')
        else:
            messages.warning(request,'error!')
    context = {'form':form}
    return render(request,'accounts/register.html',context)
    #return render_to_response('accounts/register.html', context,  RequestContext(request))

def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        groups = request.POST.get('groups')
        print(groups)
        user = authenticate(request,username=username,password=password,groups=groups)    
        if user is not None:
            login(request,user)
            # if (username == 'admin'):
            #     return redirect('home')
            if (groups == 'Sinh viên'):
                return redirect('http://127.0.0.1:8000/Student/Home/')
            if (groups == 'Quản lý'):
                return redirect('http://127.0.0.1:8000/RoomManagement/')
            if (groups == 'Giám đốc'):
                return redirect('http://127.0.0.1:8000/GD/')
            else:
                messages.warning(request,'Phải lựa chọn 1 group')
        else:
            messages.warning(request,'Sai tên đăng nhập hoặc mật khẩu')
            #return render(request,'accounts/login.html',context)

        context = {'user':user}
    context = {}
    return render(request,'accounts/login.html',context)

# @allowed_users(allowed_roles=['Sinh viên'])
# def SVpage(request):
#     context = {}
#     return render(request,'accounts/SVpage.html',context)

# @allowed_users(allowed_roles=['Quản lý'])
# def QLpage(request):
#     context = {}
#     return render(request,'accounts/QLpage.html',context)

# @allowed_users(allowed_roles=['Giám đốc'])
# def GDpage(request):
#     return redirect('http://127.0.0.1:8000/GD/')

def userPage(request):
    orders = request.user.customer.order_set.all()
    print('orders',orders)
    context = {'orders':orders}
    return render(request,'accounts/user.html',context)

@allowed_users(allowed_roles=['customers'])
def accountSettings(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)
    if request.method == 'POST':
        form = CustomerForm(request.POST,request.FILES,instance=customer)
        if form.is_valid:
            form.save()
    context = {'form':form}
    return render(request,'accounts/account_settings.html',context)

# def home(request):  
#     return redirect('http://127.0.0.1:8000/login/')

#=================================================================
# Manager Views

# def Home(request):
#     '''
#         Trang chủ cho nhà quản lý
#     '''
#     return render(request, 'Manager/index.html')

def Contact(request):
    '''
        Trang thông tin liên lạc
    '''
    return render(request, 'Manager/contact.html')

#----------------------------------------------
# Student Management views
@allowed_users(allowed_roles=['Quản lý'])
def StudentManagement(request):
    '''
        Quản lý sinh viên
    '''
    dataStudent = SINHVIEN.objects.all()
    context = {'data': dataStudent}
    return render(request, 'Manager/StudentManagement.html', context)

@allowed_users(allowed_roles=['Quản lý'])
def createNewStudent(request):
    '''
        Thêm sinh viên mới
    '''
    form = AddNewStudent()
    context = {'form': form}
    if request.method == 'POST':
        form = AddNewStudent(request.POST)
        if form.is_valid():
            form.save()
            return redirect('StudentManagement')
        else:
            messages.error(request, "Error")
    return render(request, 'Manager/createStudent.html', context)

@allowed_users(allowed_roles=['Quản lý'])
def deleteStudent(request, MSSV):
    '''
        Xoá sinh viên
    '''
    Student = SINHVIEN.objects.get(MaSV=MSSV)
    HoTen = Student.HoTen
    context = {'MaSV': MSSV, 'StudentName': HoTen}
    if request.method == 'POST':
        Student.delete()
        return redirect('StudentManagement')
    return render(request, 'Manager/deleteStudent.html', context)

@allowed_users(allowed_roles=['Quản lý'])
def editStudentInfo(request, ID):
    '''
        Chỉnh sửa thông tin sinh viên
    '''
    dataInfo = SINHVIEN.objects.get(MaSV=ID)
    StudentName = SINHVIEN.objects.get(MaSV=ID).HoTen
    form = EditStudentInfo(instance=dataInfo)
    context = {'StudentName': StudentName, 'form': form}
    if request.method == 'POST':
        form = EditStudentInfo(request.POST, instance=dataInfo)
        if form.is_valid():
            form.save()
            return redirect('StudentManagement')
        else:
            messages.error(request, "Error")
    return render(request, 'Manager/editStudentInfo.html', context)

@allowed_users(allowed_roles=['Quản lý'])
def viewBreakRule(request, MSSV):
    '''
        xem lịch sử vi phạm sinh viên
    '''
    data = VIPHAM.objects.filter(MaSV_id=MSSV)
    StudentName = SINHVIEN.objects.get(MaSV=MSSV).HoTen
    context = {'data': data, 'StudentName': StudentName, 'MSSV': MSSV}
    return render(request, 'Manager/viewBreakRule.html', context)

@allowed_users(allowed_roles=['Quản lý'])
def viewAllBreakRule(request):
    '''
        Xem lỗi vi phạm của tất cả sinh viên
    '''
    pass

@allowed_users(allowed_roles=['Quản lý'])
def addBreakRule(request, MSSV):
    '''
        Thêm lỗi vi phạm cho sinh viên
    '''
    form = AddNewBreakRule()
    context = {'form': form}
    if request.method == 'POST':
        form = AddNewBreakRule(request.POST)
        if form.is_valid:
            form.save()
            return redirect('http://127.0.0.1:8000/StudentManagement/' + str(MSSV) +'/viewBreakRule/')
    return render(request, 'Manager/addBreakRule.html', context)

@allowed_users(allowed_roles=['Quản lý'])
def editBreakRule(request):
    '''
        Chỉnh sửa thông tin chi tiết lỗi vi phạm
    '''
    pass

@allowed_users(allowed_roles=['Quản lý'])
def deleteBreakRule(request):
    '''
        Xoá lỗi vi phạm của sinh viên
    '''
    pass

#----------------------------------------------
# Room Management views
@allowed_users(allowed_roles=['Quản lý'])
def RoomManagement(request):
    '''
        Quản lý các phòng
    '''
    dataRoom = PHONG.objects.all()
    dataCount = XEPPHONG.objects.all().values('MaPhong_id').annotate(total=Count('MaPhong_id'))
    context = {'data': dataRoom, 'count': dataCount}
    return render(request, 'Manager/RoomManagement.html', context)

@allowed_users(allowed_roles=['Quản lý'])
def createNewRoom(request):
    '''
        Tạo thêm phòng mới
    '''
    form = AddNewRoom()
    context = {'form': form}
    if request.method == 'POST':
        form = EditRoomInfo(request.POST)
        if form.is_valid():
            form.save()
            return redirect('RoomManagement')
        else:
            messages.error(request, "Error")
    return render(request, 'Manager/createRoom.html', context)

@allowed_users(allowed_roles=['Quản lý'])
def deleteRoom(request, ID):
    '''
        Xoá phòng
    '''
    Room = PHONG.objects.get(MaPhong=ID)
    RoomName = Room.TenPhong
    context = {'RoomID': ID, 'RoomName': RoomName}
    if request.method == 'POST':
        Room.delete()
        return redirect('RoomManagement')
    return render(request, 'Manager/deleteRoom.html', context)

@allowed_users(allowed_roles=['Quản lý'])
def addStudentToRoom(request, ID):
    '''
        Thêm sinh viên vào phòng
    '''
    RoomName = PHONG.objects.get(MaPhong=ID).__str__
    context = {'RoomID': ID, 'RoomName': RoomName}
    if request.method == 'POST':
        XEPPHONG.objects.create(MaPhong_id=ID, MaSV_id=request.POST['MSSV'], NgayVao=request.POST['DateIn'])
        return redirect('http://127.0.0.1:8000/RoomManagement/' + str(ID) +'/RoomListStudent/')
    return render(request, 'Manager/addStudentToRoom.html', context)

@allowed_users(allowed_roles=['Quản lý'])
def moveStudent(request, ID, MSSV):
    '''
        Chuyển phòng cho sinh viên
    '''
    Room =PHONG.objects.get(MaPhong=ID)
    Student = SINHVIEN.objects.get(MaSV=MSSV)
    StudentName = Student.HoTen
    RoomName = Room.TenPhong
    TowerName = Room.DayNha
    context = {'RoomID': ID, 'RoomName': RoomName, 'MSSV': MSSV, 'StudentName': StudentName, 'TowerName': TowerName}
    if request.method == 'POST':
        newRoomID = PHONG.objects.get(TenPhong=request.POST['RoomName'], DayNha=request.POST['TowerName']).MaPhong
        XP = XEPPHONG.objects.filter(MaSV_id=MSSV)
        XP.update(MaPhong_id=newRoomID)
        return redirect('http://127.0.0.1:8000/RoomManagement/' + str(newRoomID) +'/RoomListStudent/')
    return render(request, 'Manager/changeRoom.html', context)

@allowed_users(allowed_roles=['Quản lý'])
def viewListStudent(request, ID):
    '''
       Danh sách sinh viên trong phòng
    '''
    dataRoom = XEPPHONG.objects.select_related('MaPhong').filter(MaPhong_id=ID)
    RoomName = PHONG.objects.get(MaPhong=ID).TenPhong
    context = {'RoomName': RoomName, 'RoomID': ID, 'StudentData': dataRoom}
    return render(request, 'Manager/RoomListStudent.html', context)

@allowed_users(allowed_roles=['Quản lý'])
def kickStudent(request, ID, MSSV):
    '''
        Xoá sinh viên khỏi phòng
    '''
    RoomName = PHONG.objects.get(MaPhong=ID).TenPhong
    StudentName = SINHVIEN.objects.get(MaSV=MSSV).HoTen
    context = {'RoomID':ID, 'RoomName': RoomName, 'StudentName': StudentName}
    rmStudent = XEPPHONG.objects.filter(MaSV_id=MSSV)
    if request.method == 'POST':
        rmStudent.delete()
        return redirect('http://127.0.0.1:8000/RoomManagement/' + str(ID) +'/RoomListStudent/')
    else:
        return render(request, 'Manager/kickStudent.html', context)

@allowed_users(allowed_roles=['Quản lý'])
def editRoomInfo(request, ID):
    '''
        Cập nhật thông tin phòng
    '''
    dataInfo = PHONG.objects.get(MaPhong=ID)
    RoomName = PHONG.objects.get(MaPhong=ID).TenPhong
    form = EditRoomInfo(instance=dataInfo)
    context = {'RoomName': RoomName, 'form': form}
    if request.method == 'POST':
        form = EditRoomInfo(request.POST, instance=dataInfo)
        if form.is_valid():
            form.save()
            return redirect('RoomManagement')
        else:
            messages.error(request, "Error")
    return render(request, 'Manager/RoomInfo.html', context)

@allowed_users(allowed_roles=['Quản lý'])
def RoomCharge(request, ID):
    '''
        Thu tiền phòng
    '''
    Room = PHONG.objects.get(MaPhong=ID)
    RoomName = Room.TenPhong
    TowerName = Room.DayNha
    Student = XEPPHONG.objects.get(MaPhong_id=ID).MaSV.MaSV
    data = TIENPHONG.objects.filter(MaSV_id=Student)
    context = {'data': data, 'RoomName': RoomName, 'TowerName': TowerName, 'RoomID': ID}
    return render(request, 'Manager/RoomCharge.html', context)

@allowed_users(allowed_roles=['Quản lý'])
def acceptRoomCharge(request, ID, MSSV):
    '''
        Ghi nhận thu tiền phòng
    '''
    RC = TIENPHONG.objects.filter(MaSV_id=MSSV)
    RC.update(TrangThai='Paied')
    return redirect('http://127.0.0.1:8000/RoomManagement/' + str(ID) + '/RoomCharge/')

@allowed_users(allowed_roles=['Quản lý'])
def returnRoomCharge(request, ID, MSSV):
    '''
        Hoàn tác thu tiền phòng
    '''
    RC = TIENPHONG.objects.filter(MaSV_id=MSSV)
    RC.update(TrangThai='Not paied')
    return redirect('http://127.0.0.1:8000/RoomManagement/' + str(ID) + '/RoomCharge/')

@allowed_users(allowed_roles=['Quản lý'])
def newMonthCharge(request):
    '''
        Xác thực việc bắt đầu thu tiền phòng tháng mới
    '''
    pass

@allowed_users(allowed_roles=['Quản lý'])
def ElectricityBill(request):
    '''
        Tiền điện
    '''
    data = TIENDIEN.objects.select_related('MaPhong')
    context = {'data': data}
    return render(request, 'Manager/ElectricityBill.html', context)

@allowed_users(allowed_roles=['Quản lý'])
def acceptElectricityBill(request, ID):
    '''
        Ghi nhận thu tiền phòng
    '''
    EB = TIENDIEN.objects.filter(MaPhong_id=ID)
    EB.update(TrangThai='Paied')
    return redirect('ElectricityBill')

@allowed_users(allowed_roles=['Quản lý'])
def returnElectricityBill(request, ID):
    '''
        Hoàn tác thu tiền phòng
    '''
    EB = TIENDIEN.objects.filter(MaPhong_id=ID)
    EB.update(TrangThai='Not paied')
    return redirect('ElectricityBill')

@allowed_users(allowed_roles=['Quản lý'])
def updateElectricityBill(request):
    '''
        Cập nhật số điện
    '''
    form = newElectricityBill()
    if request.method == 'POST':
        form = newElectricityBill(request.POST)
        if form.is_valid:
            form.save()
            return redirect('ElectricityBill')
    context = {'form': form}
    return render(request, 'Manager/inputElectricityBill.html', context)

#----------------------------------------------
# Asset Management
@allowed_users(allowed_roles=['Quản lý'])
def QLpage2(request):
    taisan = TAISAN.objects.all()
    myFilter = TAISANFilter(request.GET,queryset=taisan)
    taisan = myFilter.qs
    page = request.GET.get('page', 1)
    paginator = Paginator(taisan, 4)
    try:
        taisan = paginator.page(page)
    except PageNotAnInteger:
        taisan = paginator.page(1)
    except EmptyPage:
        taisan = paginator.page(paginator.num_pages)
    context = {'taisan': taisan, 'myFilter': myFilter}
    return render(request, 'Manager/Quanly/QL2/QLpage2.html', context)



@allowed_users(allowed_roles=['Quản lý'])
def AddTS(request):
    form = TSForm()
    if request.method == 'POST':
        #print('Printing POST: ', request.POST)
        form = TSForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/QL2')
    context = {'form':form}
    return render(request,'Manager/Quanly/QL2/add_TS.html',context)

@allowed_users(allowed_roles=['Quản lý'])
def UpdateTS(request,pk):
    taisan = TAISAN.objects.get(ID=pk)
    form = TSForm(instance = taisan)
    if request.method == 'POST':
        form = TSForm(request.POST,instance = taisan)
        if form.is_valid():
            form.save()
            return redirect('/QL2')
    context = {'form':form}
    return render(request,'Manager/Quanly/QL2/add_TS.html',context)

@allowed_users(allowed_roles=['Quản lý'])
def DeleteTS(request,pk):
    taisan = TAISAN.objects.get(ID=pk)
    if request.method == 'POST':
        taisan.delete()
        return redirect('/QL2')
    context = {'taisan':taisan}
    return render(request,'Manager/Quanly/QL2/delete_TS.html',context)

@allowed_users(allowed_roles=['Quản lý'])
def QLpage3(request):
    sctaisan = CTTAISAN.objects.all()
    myFilter = SCTAISANFilter(request.GET,queryset=sctaisan)
    sctaisan = myFilter.qs
    page = request.GET.get('page', 1)
    paginator = Paginator(sctaisan, 4)
    try:
        sctaisan = paginator.page(page)
    except PageNotAnInteger:
        sctaisan = paginator.page(1)
    except EmptyPage:
        sctaisan = paginator.page(paginator.num_pages)
    context = {'sctaisan': sctaisan, 'myFilter': myFilter}
    return render(request, 'Manager/Quanly/QL3/QLpage3.html', context)



@allowed_users(allowed_roles=['Quản lý'])
def AddSCTS(request):
    form = SCTSForm()
    if request.method == 'POST':
        #print('Printing POST: ', request.POST)
        form = SCTSForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/QL3')
    context = {'form':form}
    return render(request,'Manager/Quanly/QL3/add_SCTS.html',context)

@allowed_users(allowed_roles=['Quản lý'])
def UpdateSCTS(request,pk):
    sctaisan = CTTAISAN.objects.get(ID=pk)
    form = SCTSForm(instance = sctaisan)
    if request.method == 'POST':
        form = SCTSForm(request.POST,instance = sctaisan)
        if form.is_valid():
            form.save()
            return redirect('/QL3')
    context = {'form':form}
    return render(request,'Manager/Quanly/QL3/add_SCTS.html',context)

@allowed_users(allowed_roles=['Quản lý'])
def DeleteSCTS(request,pk):
    sctaisan = CTTAISAN.objects.get(ID=pk)
    if request.method == 'POST':
        sctaisan.delete()
        return redirect('/QL3')
    context = {'sctaisan':sctaisan}
    return render(request,'Manager/Quanly/QL3/delete_SCTS.html',context)

#========================================================
# Director views
@allowed_users(allowed_roles=['Giám đốc'])
def GDpage(request):
    nhansu = NHANSU.objects.order_by('MaNV')
    myFilter = NHANSUFilter(request.GET,queryset=nhansu) 
    nhansu = myFilter.qs
    context = {'nhansu':nhansu, 'myFilter':myFilter}
    return render(request,'Director/GD1/GDpage.html',context)

@allowed_users(allowed_roles=['Giám đốc'])
def AddNV(request):
    form = NVForm()
    if request.method == 'POST':
        #print('Printing POST: ', request.POST)
        form = NVForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/GD')
    context = {'form':form}
    return render(request,'Director/GD1/add_NV.html',context)

@allowed_users(allowed_roles=['Giám đốc'])
def UpdateNV(request,pk):
    nhansu = NHANSU.objects.get(MaNV=pk)
    form = NVForm(instance = nhansu)
    if request.method == 'POST':
        form = NVForm(request.POST,instance = nhansu)
        if form.is_valid():
            form.save()
            return redirect('/GD')
    context = {'form':form}
    return render(request,'Director/GD1/add_NV.html',context)

@allowed_users(allowed_roles=['Giám đốc'])
def DeleteNV(request,pk):
    nhansu = NHANSU.objects.get(MaNV=pk)
    if request.method == 'POST':
        nhansu.delete()
        return redirect('/GD')
    context = {'nhansu':nhansu}
    return render(request,'Director/GD1/delete_NV.html',context)

@allowed_users(allowed_roles=['Giám đốc'])
def GDpage2(request):
    kyluat = KYLUAT.objects.order_by('ID')
    myFilter = KYLUATFilter(request.GET,queryset=kyluat) 
    kyluat = myFilter.qs
    context = {'kyluat':kyluat,'myFilter':myFilter}
    return render(request,'Director/GD2/GDpage2.html',context)

@allowed_users(allowed_roles=['Giám đốc'])
def AddKL(request):
    form = KLForm()
    if request.method == 'POST':
        #print('Printing POST: ', request.POST)
        form = KLForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/GD2')
    context = {'form':form}
    return render(request,'Director/GD2/add_KL.html',context)

@allowed_users(allowed_roles=['Giám đốc'])
def UpdateKL(request,pk):
    kyluat = KYLUAT.objects.get(ID=pk)
    form = KLForm(instance = kyluat)
    if request.method == 'POST':
        form = KLForm(request.POST,instance = kyluat)
        if form.is_valid():
            form.save()
            return redirect('/GD2')
    context = {'form':form}
    return render(request,'Director/GD2/add_KL.html',context)

@allowed_users(allowed_roles=['Giám đốc'])
def DeleteKL(request,pk):
    kyluat = KYLUAT.objects.get(ID=pk)
    if request.method == 'POST':
        kyluat.delete()
        return redirect('/GD2')
    context = {'kyluat':kyluat}
    return render(request,'Director/GD2/delete_KL.html',context)

@allowed_users(allowed_roles=['Giám đốc'])
def GDpage3(request):
    phong = PHONG.objects.order_by('MaPhong')
    myFilter = PHONGFilter(request.GET,queryset=phong) 
    phong = myFilter.qs
    context = {'phong':phong,'myFilter':myFilter}
    return render(request,'Director/GD3/GDpage3.html',context)

@allowed_users(allowed_roles=['Giám đốc'])
def UpdateGiaPhong(request,pk):
    phong = PHONG.objects.get(MaPhong=pk)
    form = PhongForm(instance = phong)
    if request.method == 'POST':
        form = PhongForm(request.POST,instance = phong)
        if form.is_valid():
            form.save()
            return redirect('/GD3')
    context = {'form':form, 'phong':phong}
    return render(request,'Director/GD3/update_gia-phong.html',context)

@allowed_users(allowed_roles=['Giám đốc'])
def GDpage4(request):
    quanly = QUANLY.objects.order_by('MaQL')
    myFilter = QUANLYFilter(request.GET,queryset=quanly) 
    quanly = myFilter.qs
    context = {'quanly':quanly, 'myFilter':myFilter}
    return render(request,'Director/GD4/GDpage4.html',context)

@allowed_users(allowed_roles=['Giám đốc'])
def AddQL(request):
    form = QLForm()
    if request.method == 'POST':
        #print('Printing POST: ', request.POST)
        form = QLForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/GD4')
    context = {'form':form}
    return render(request,'Director/GD4/add_QL.html',context)

@allowed_users(allowed_roles=['Giám đốc'])
def DeleteQL(request,pk):
    quanly = QUANLY.objects.get(MaQL=pk)
    if request.method == 'POST':
        quanly.delete()
        return redirect('/GD4')
    context = {'quanly':quanly}
    return render(request,'Director/GD4/delete_QL.html',context)

@allowed_users(allowed_roles=['Giám đốc'])
def UpdateQL(request,pk):
    quanly = QUANLY.objects.get(MaQL=pk)
    form = QLForm(instance = quanly)
    if request.method == 'POST':
        form = QLForm(request.POST,instance = quanly)
        if form.is_valid():
            form.save()
            return redirect('/GD4')
    context = {'form':form}
    return render(request,'Director/GD4/add_QL.html',context)

@allowed_users(allowed_roles=['Giám đốc'])
def roomRegister(request):
    nhansu = NHANSU.objects.all()
    phong = PHONG.objects.all()
    quanly = QUANLY.objects.all()
    form = SVForm()
    form2 = PhongForm2
    myFilter = PHONGFilter(request.GET,queryset=phong) 
    phong = myFilter.qs
    context = {'phong':phong, 'myFilter':myFilter, 'form':form, 'form2':form2, 'nhansu':nhansu, 'quanly':quanly}
    return render(request,'Director/room.html',context)

#========================================================
# Student Views
@allowed_users(allowed_roles=['Sinh viên'])
def StudentHome(request):
   '''
      Trang chủ
   '''
   return render(request, 'Student/index.html')

StudentID = 20170001
@allowed_users(allowed_roles=['Sinh viên'])
def StudentRoom(request):
    RoomID = XEPPHONG.objects.filter(MaSV_id=StudentID).first().MaPhong.MaPhong
    dataRoom = PHONG.objects.all()
    dataCount = XEPPHONG.objects.all().values('MaPhong_id').annotate(total=Count('MaPhong_id'))
    context = {'data': dataRoom, 'count': dataCount, 'RoomID': RoomID}
    return render(request, 'Student/room.html', context)

@allowed_users(allowed_roles=['Sinh viên'])
def ListStudentRoom(request):
    RoomID = XEPPHONG.objects.filter(MaSV_id=StudentID).first().MaPhong.MaPhong
    dataRoom = XEPPHONG.objects.filter(MaPhong_id=RoomID)
    context = {'data': dataRoom}
    return render(request, 'Student/ListStudentRoom.html', context)

@allowed_users(allowed_roles=['Sinh viên'])
def StudentInfo(request):
    data = SINHVIEN.objects.get(MaSV=StudentID)
    context = {'data': data}
    return render(request, 'Student/StudentInfo.html', context)

@allowed_users(allowed_roles=['Sinh viên'])
def TTDN(request):
    ID = XEPPHONG.objects.filter(MaSV_id=StudentID).first().MaPhong
    dataDN = TIENDIEN.objects.filter(MaPhong_id=ID)
    context = {'data': dataDN}
    return render(request, 'templates/thanhtoandiennuoc.html', context)

@allowed_users(allowed_roles=['Sinh viên'])
def ManagerContact(request):
    data = QUANLY.objects.select_related('MaNV')
    context = {'data': data}
    return render(request, 'Student/ManagerContact.html', context)

@allowed_users(allowed_roles=['Sinh viên'])
def AllCharge(request):
    ID = XEPPHONG.objects.filter(MaSV_id=StudentID).first().MaPhong
    dataDN = TIENDIEN.objects.filter(MaPhong_id=ID)
    context = {'data': dataDN}
    return render(request, 'Student/AllCharge.html', context)