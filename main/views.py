from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import *
from .filters import PatientFilter
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def login(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method == 'POST':
            username=request.POST['username']
            password=request.POST['password']
            user=auth.authenticate(username=username,password=password)
            if user is not None:
                auth.login(request,user)
                return redirect('/')
            else:
                messages.error(request, 'Invalid username or password')
                return redirect('login')
        else:
            return render(request,'main/login.html')

@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect('/')

def dashboard(request):
    patients=Patient.objects.all()
    patient_counts=patients.count()
    patients_recovered=Patient.objects.filter(status="Recovered")
    patients_deceased=Patient.objects.filter(status="Deceased")
    deceased_count=patients_deceased.count()
    recovered_count=patients_recovered.count()
    beds=Bed.objects.all()
    beds_available=Bed.objects.filter(occupied=False).count()

    context={
        'patient_count': patient_counts,
        'recovered_count':recovered_count,
        'beds_available':beds_available,
        'deceased_count':deceased_count,
        'beds':beds
    }
    print(context)

    return render(request,'main/dashboard.html', context)

def add_ptient(request):
    beds=Bed.objects.filter(occupied=False)
    doctors=Doctor.objects.all()
    if request.method == 'POST':
        name=request.POST['name']
        phone_num=request.POST['phone_num']
        patient_relative_name=request.POST['patient_relative_name']
        patient_relative_contact=request.POST['patient_relative_contact']
        address=request.POST['address']
        symptoms=request.POST['symptoms']
        prior_aliments=request.POST['prior_aliments']
        bed_num_sent=request.POST['bed_num']
        bed_num=Bed.objects.get(bed_number=bed_num_sent)
        dob=request.POST['dob']
        status=request.POST['status']
        doctor=request.POST['doctor']
        doctor=Doctor.objects.get(name=doctor)
        print(request.POST)
        patient=Patient.objects.create(
            name=name,
            phone_num=phone_num,
            patient_relative_name=patient_relative_name,
            patient_relative_contact=patient_relative_contact,
            address=address,
            symptoms=symptoms,
            prior_aliments=prior_aliments,
            bed_num=bed_num,
            dob=dob,
            status=status,
            doctor=doctor
        )
        patient.save()

        print(patient.data,"patient")

        bed=Bed.objects.get(bed_number=bed_num_sent)
        bed.occupied=True
        bed.save()
        print(bed)
        id=patient.id
        return redirect(f"/patient/{id}")
    context={
        'beds':beds,
        'doctors':doctors
    }
    return render(request, 'main/add_patient.html', context)

def patient(request,pk):
    patient=Patient.objects.get(id=pk)
    if request.method =='POST':
        doctor=request.POST['doctor']
        doctor_times=request.POST['doctor_time']
        doctor_notes=request.POSt['doctor_notes']
        mobile=request.POST['mobile']
        mobile2=request.POST['mobile2']
        relativeName=request.POST['relativeName']
        address=request.POST['location']
        print(doctor_times)
        print(doctor_notes)
        status=request.POST['status']
        doctor=Doctor.objects.get(name=doctor)
        print(doctor)
        patient.phone_num=mobile
        patient.patient_relative_contact=mobile2
        patient.patient_relative_name=relativeName
        patient.address=address
        patient.doctor=doctor
        patient.doctors_visiting_time=doctor_times
        patient.doctors_notes=doctor_notes
        print(patient.doctors_visiting_time)
        print(patient.doctors_notes)
        patient.status=status
        patient.save()
    context={
        'patient':patient
    }
    return render(request,'main/patient.html', context)

def patient_list(request):
    patients=Patient.objects.all()

    myFilter=PatientFilter(request.GET, queryset=patients)

    patients=myFilter.qs
    context={
        'patients':patients,
        'myFilter': myFilter
    }

    return render(request, 'main/patient_list.html', context)

def autosuggest(request):
    query_orginal=request.GET.get('term')
    queryset=Patient.objects.filter(name__icontains=query_orginal)
    mylist=[]
    mylist += [x.name for x in queryset]
    return JsonResponse(mylist, safe=False)


def autodoctor(request):
    query_original=request.GET.get('term')
    queryset=Doctor.objects.filter(name__icontains=query_original)
    mylist=[]
    mylist+=[x.name for x in queryset]
    return JsonResponse(mylist,safe=False)

def info(request):
    return render(request, 'main/info.html')






































