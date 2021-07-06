from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('register/', views.registerPage,name='register'),    
    path('login/', views.loginPage,name='login'),  
    path("logout/", LogoutView.as_view(), name="logout"),  
    path('', views.home,name='home'),
    # path('SV/',views.SVpage,name='SVpage'),
    # path('QL/',views.QLpage,name='QLpage'),
    # path('GD/',views.GDpage,name='GDpage'),
    path('accountSettings/',views.accountSettings,name='accountSettings'),

#==========================================================
# Manager urls
    # path('', views.Home), # Manager Home
    path('Contact/', views.Contact),
    
    path('RoomManagement/', views.RoomManagement, name='RoomManagement'),
    path('RoomManagement/createRoom/', views.createNewRoom),
    path('RoomManagement/<int:ID>/deleteRoom/', views.deleteRoom),
    path('RoomManagement/<int:ID>/RoomInfo/', views.editRoomInfo),
    
    path('RoomManagement/<int:ID>/RoomListStudent/', views.viewListStudent),
    path('RoomManagement/<int:ID>/addStudent/', views.addStudentToRoom),
    path('RoomManagement/<int:ID>/RoomListStudent/removeStudent/<int:MSSV>/', views.kickStudent),
    path('RoomManagement/<int:ID>/RoomListStudent/changeRoom/<int:MSSV>/', views.moveStudent),
    
    path('RoomManagement/<int:ID>/RoomCharge/', views.RoomCharge, name='RoomCharge'),
    path('RoomManagement/newMonthCharge/', views.newMonthCharge),
    path('RoomManagement/<int:ID>/RoomCharge/acceptRoomCharge/<int:MSSV>/', views.acceptRoomCharge),
    path('RoomManagement/<int:ID>/RoomCharge/returnRoomCharge/<int:MSSV>/', views.returnRoomCharge),
    
    path('RoomManagement/ElectricityBill/', views.ElectricityBill, name='ElectricityBill'),
    path('RoomManagement/ElectricityBill/inputElectricityBill/', views.updateElectricityBill),
    path('RoomManagement/ElectricityBill/<int:ID>/acceptElectricityBill/', views.acceptElectricityBill),
    path('RoomManagement/ElectricityBill/<int:ID>/returnElectricityBill/', views.returnElectricityBill),
    
    path('StudentManagement/', views.StudentManagement, name='StudentManagement'),
    path('StudentManagement/createStudent/', views.createNewStudent),
    path('StudentManagement/<int:ID>/editStudentInfo/', views.editStudentInfo),
    path('StudentManagement/<int:MSSV>/deleteStudent/', views.deleteStudent),
    
    path('StudentManagement/viewAllBreakRule/', views.viewAllBreakRule),
    path('StudentManagement/<int:MSSV>/viewBreakRule/', views.viewBreakRule),
    path('StudentManagement/<int:MSSV>/addBreakRule/', views.addBreakRule),

    path('QL2/',views.QLpage2,name='QLpage2'),
    path('AddTS/',views.AddTS,name='AddTS'),
    path('UpdateTS/<str:pk>/',views.UpdateTS,name='UpdateTS'),
    path('DeleteTS/<str:pk>/',views.DeleteTS,name='DeleteTS'),
    path('QL3/',views.QLpage3,name='QLpage3'),
    path('AddSCTS/', views.AddSCTS, name='AddSCTS'),
    path('UpdateSCTS/<str:pk>/', views.UpdateSCTS, name='UpdateSCTS'),
    path('DeleteSCTS/<str:pk>/', views.DeleteSCTS, name='DeleteSCTS'),

#==========================================================
# Director urls    
    # path('SV/',views.SVpage,name='SVpage'),
    # path('QL/',views.QLpage,name='QLpage'),
    path('GD/',views.GDpage,name='GDpage'),
    path('AddNV/',views.AddNV,name='AddNV'),
    path('UpdateNV/<str:pk>/',views.UpdateNV,name='UpdateNV'),
    path('DeleteNV/<str:pk>/',views.DeleteNV,name='DeleteNV'),
    path('GD2/',views.GDpage2,name='GDpage2'),
    path('AddKL/',views.AddKL,name='AddKL'),
    path('UpdateKL/<str:pk>/',views.UpdateKL,name='UpdateKL'),
    path('DeleteKL/<str:pk>/',views.DeleteKL,name='DeleteKL'),
    path('GD3/',views.GDpage3,name='GDpage3'),
    path('UpdateGiaPhong/<str:pk>/',views.UpdateGiaPhong,name='UpdateGiaPhong'),
    path('GD4/',views.GDpage4,name='GDpage4'),
    path('AddQL/',views.AddQL,name='AddQL'),
    path('UpdateQL/<str:pk>/',views.UpdateQL,name='UpdateQL'),
    path('DeleteQL/<str:pk>/',views.DeleteQL,name='DeleteQL'),
    path('roomRegister/',views.roomRegister,name='roomRegister'),


#==========================================================
# Student urls
    path('Student/Home/', views.StudentHome),
    path('Student/Room/', views.StudentRoom),
    path('Student/Room/ListStudent/', views.ListStudentRoom),
    path('Student/ManagerContact/', views.ManagerContact),
    path('Student/StudentInfo/', views.StudentInfo),
    path('Student/AllCharge/', views.AllCharge),
]