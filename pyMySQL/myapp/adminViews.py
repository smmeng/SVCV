from django.db.models import Q
from myapp.utility import Utility
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, RequestContext
from django.contrib.auth.models import   User
from pip._vendor import requests

################## To generate all user list based on the current role
@login_required
def adminGetAllUsers(request):
    user = request.user
    print 'get_activity() ] user=[', user

    if user.is_staff or user.is_superuser:
        util = Utility()
        user_list = util.viewable_user_list(request)
    
    #allUserId_list = user_list['allUserId_list']
    #allUser_list = user_list['allUser_list']

    
    #activity_dict= {'allUserId_list', 'allUser_list':allUser_list, 'investorId':uid, 'investorName':userName}
    #print 'get_activity() activity_dict[', activity_dict
    # We also add the project object from the database to the context dictionary.
    # We'll use this in the template to verify that the project exists.
    #activity_dict['projects'] = activity_list

    # Go render the response and return it to the client.
    return user_list


from django.http import Http404
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import filters
from rest_framework.response import Response

from myapp.models import InvestmentActivity, PROJECT, UserProfile
from myapp.serializers import InvestorSerializer, ProjectSerializer, UserSerializer, UserProfileSerializer

class InvestorList(APIView):
    """
    List all investor details, or create a new snippet.
    """
    def get(self, request, Pid, format=None):
        print ' Get Pid=[', Pid
        investors = InvestmentActivity.objects.filter(ProjectId=Pid)
        serializer = InvestorSerializer(investors, many=True)
        return Response(serializer.data)

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
class InvestorViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    print ' InvestorViewSet=[', 
    serializer_class = InvestorSerializer
    
    queryset = InvestmentActivity.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('ProjectId', 'UserId', 'Type')
    #print queryset
    
    ##permission_classes = (permissions.IsAuthenticatedOrReadOnly)

class ProjectViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    serializer_class = ProjectSerializer
    
    queryset = PROJECT.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('Status',)
    
    
class UserProfileViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    serializer_class =UserProfileSerializer
    queryset = UserProfile.objects.all()
    
####
@login_required
def get_projectInvestors(request):
    return render(request, "admin/projectInvestors.html")

import json
from django.http import HttpResponse

@login_required
def get_projectInvestorSummary(request):
    return render(request, "admin/projectInvestorSummary.html")

@login_required
def get_projectInvestorSummaryData(request):
    #projectList = [{"UserId":"lsun011","first_name":"Lei","last_name":"Sun","Type":"Investment deposit of principal","ProjectId":"Black Square","Amount":50000.0,"Date":"2014-06-16"},{"UserId":"yqin2000","first_name":"Ying","last_name":"Qin","Type":"Investment deposit of principal","ProjectId":"Black Square","Amount":50000.0,"Date":"2014-06-09"}]
    
    activity_list = InvestmentActivity.objects.all().filter (Q(ProjectId__Status ="In Progress") | Q(ProjectId__Status ="Closed") ).filter(Q(Type='Deposit')|Q(Type='Check'))
    investorDict = {}
    projectDict = {}
    print 'activity_list=', activity_list
    
    for row in activity_list:
        userId = str(row.UserId)
        projectId = str(row.ProjectId)
        #print userId, ' - ', projectId
        
        if investorDict.has_key(userId):
            innerInvestorDict = investorDict[userId]
            
            if innerInvestorDict.has_key(projectId):
                innerInvestorDict[projectId] = innerInvestorDict[projectId] + row.Amount
            else:
                innerInvestorDict[projectId] = row.Amount
            #print 'Existing innerInvestorDict', innerInvestorDict
        else:
            innerInvestorDict = {projectId:row.Amount}
            investorDict[userId] = innerInvestorDict 
            #print 'New innerInvestorDict', innerInvestorDict
            
        if projectDict.has_key(projectId):
            innerProjectDict = projectDict[projectId]
            
            if innerProjectDict.has_key(userId):
                innerProjectDict[userId] = innerProjectDict[userId] + row.Amount
            else:
                innerProjectDict[userId] = row.Amount
            #print 'Existing innerProjectDict', innerProjectDict
        else:
            innerProjectDict = {userId:row.Amount}
            projectDict[projectId] = innerProjectDict 
            #print 'New innerProjectDict', innerProjectDict
        
    #### construct the final 2-D list for HTML report
    finalSummaryList = []    
    #first row is header
    userIds = investorDict.keys() # need to sort by highest outstanding principal later
    projectRow=[]
    projectRow.append('Project Name')#{'projectId':'Project Name'})
    projectRow.append('Project Total')        
    for userId in userIds: #columns
        projectRow.append(userId)
    
    print 'first row adds[', projectRow
    finalSummaryList.append(projectRow)
    grandProjectTotalAmount = 0
    grandUserTotal = {}
    
    for projectId in projectDict.keys():
        #projectId = str(projectId).replace('[', '').replace('\]', '')
        print 'prepare projectRow=', projectId
        innerProjectDict =  projectDict[projectId]
        projectRow=[]
        projectRow.append(projectId)
        projectTotalAmount = 0
        
        for userId in userIds: #columns
            innerInvestorDict = investorDict[userId]
            if innerProjectDict.has_key(userId):
                #print 'prepare user col=', userId
                projectRow.append(innerProjectDict[userId])
                projectTotalAmount += innerProjectDict[userId]
                if grandUserTotal.has_key(str(userId)):
                    grandUserTotal[str(userId)] = grandUserTotal[str(userId)]  +  innerProjectDict[userId]
                else:
                    grandUserTotal[str(userId)] = innerProjectDict[userId]
            else:
                projectRow.append('  ')
                
                
        print 'projectRow=[',projectRow
                
        projectRow.insert(1, projectTotalAmount)
        grandProjectTotalAmount += projectTotalAmount
        finalSummaryList.append(projectRow)
    
    # Grand Total row
    projectRow=[]
    projectRow.append('Grand Total')#{'projectId':'Project Name'})
    projectRow.append(grandProjectTotalAmount )    
    
    for userId in userIds:
        projectRow.append(grandUserTotal[str(userId)]);
        
    finalSummaryList.append(projectRow)
    
    return HttpResponse(
        json.dumps(finalSummaryList),
        content_type = 'text/javascript; charset=utf8'
    )
@login_required
def get_testAG(request):
    return render(request, "testAG.html")

######## Encryption Decryption
from Crypto.Cipher import AES
import base64
import os
import binascii

@login_required
def encryptIt(request):
    print 'In encryptIt()'
    info2Encrypt = ''
    EncryptPassword = ''
    seed = ''
    encryptedInfo = ''
    errorMsg = ''
    
    try:
        if request.method == 'POST':
            info2Encrypt = request.POST.get('info2Encrypt')
            EncryptPassword = request.POST.get('EncryptPassword')
            print 'info2Encrypt=', info2Encrypt, '  EncryptPassword=',EncryptPassword
            print 'info2Encrypt=[', len(info2Encrypt), '] EncryptPasswords[', len(EncryptPassword)
            #32 bytes = 256 bits
            #16 = 128 bits
            # the block size for cipher obj, can be 16 24 or 32. 16 matches 128 bit.
            BLOCK_SIZE = 16
            # the character used for padding
            # used to ensure that your value is always a multiple of BLOCK_SIZE
            PADDING = '{'
            # function to pad the functions. Lambda
            # is used for abstraction of functions.
            # basically, its a function, and you define it, followed by the param
            # followed by a colon,
            # ex = lambda x: x+5
            pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * PADDING
            # encrypt with AES, encode with base64
            EncodeAES = lambda c, s: base64.b64encode(c.encrypt(pad(s)))
            # generate a randomized secret key with urandom
            secret = os.urandom(BLOCK_SIZE)
            print 'encryption secret1:', secret
            seed = binascii.hexlify(secret)
            print 'encryption hexlify secret:', seed
        
            if len(EncryptPassword) > BLOCK_SIZE:
                EncryptPassword = EncryptPassword[0:BLOCK_SIZE]
            else:
                EncryptPassword = EncryptPassword.ljust(BLOCK_SIZE, '!')
            print 'DecryptPassword=', EncryptPassword
            
            secret = secret + str(EncryptPassword)
            print 'encryption secret22:', secret
            #print 'encryption secret encoded:',secret.encode('utf-8')
            # creates the cipher obj using the key
            cipher = AES.new(secret)
            print 'encryption cipher:', cipher
            # encodes you private info!
            encryptedInfo = EncodeAES(cipher, info2Encrypt)
            print 'Encrypted string:', encryptedInfo
        
    except Exception:
        errorMsg = 'Error occured during encryption'
        
    return render(request, "admin/encryption.html",  {'info2Encrypt':info2Encrypt, 'EncryptPassword':EncryptPassword, 'seed':seed, 'encryptedInfo':encryptedInfo, 'errorMsg':errorMsg} )

@login_required
def decryptIt(request):
    BLOCK_SIZE = 16
    print 'In decryptIt()'
    info2Decrypt = ''
    DecryptPassword = ''
    seed2 = ''
    decryptedInfo = ''
    errorMsg = ''
    
    try:
        if request.method == 'POST':
            info2Decrypt = request.POST.get('info2Decrypt')
            DecryptPassword = request.POST.get('DecryptPassword')
            seed2 = request.POST.get('seed2')
            
            if len(DecryptPassword) > BLOCK_SIZE:
                DecryptPassword = DecryptPassword[0:BLOCK_SIZE]
            else:
                DecryptPassword = DecryptPassword.ljust(BLOCK_SIZE, '!')
            print 'DecryptPassword=', DecryptPassword
            
            print 'info2Decrypt=', info2Decrypt, '  DecryptPassword=',DecryptPassword, ' seed2=',seed2
    
            PADDING = '{'
            DecodeAES = lambda c, e: c.decrypt(base64.b64decode(e)).rstrip(PADDING)
            
            #Key is FROM the printout of 'secret' in encryption
            #below is the encryption.
            encryption = info2Decrypt
            key = binascii.unhexlify(seed2)
            print 'key: ', key
            password = str(DecryptPassword)
            cipher = AES.new(key+password)
            
            decryptedInfo = str(DecodeAES(cipher, encryption))
            print 'Decrypted string:', decryptedInfo
    except Exception:
        errorMsg = 'Error occured during decryption'
        
    return render(request, "admin/encryption.html",  {'info2Decrypt':info2Decrypt, 'DecryptPassword':DecryptPassword, 'seed2':seed2, 'decryptedInfo':decryptedInfo, 'errorMsg':errorMsg} )
    
################## To all investor profit
from django.db.models import Sum
def getInvestorProfitsData(sort=None):
    investorsProfits = InvestmentActivity.objects.filter(Q(Type='Interest')|Q(Type='Dividend')).values('UserId__username', 'UserId__first_name', 'UserId__last_name').annotate(Sum('Amount')).order_by('Amount__sum')
    
    #InvestmentActivity.objects.filter(UserId = userId).order_by(orderBy)
    #print 'Aggregate investorsProfits=[',investorsProfits
    investorsProfits.extra(select={'returnEquityAmount':0})
    investorsProfits.extra(select={'depositedEquityAmount':0})
    investorsProfits.extra(select={'remainingEquityAmount':0})
    #print 'Aggregate2 investorsProfits=[',investorsProfits
    

    returnedEquities = InvestmentActivity.objects.filter(Q(Type='Check')).values('UserId__username').annotate(Sum('Amount'))
    #print 'Aggregate returnedEquities=[',returnedEquities
    
    depositedEquities = InvestmentActivity.objects.filter(Q(Type='Deposit')).values('UserId__username').annotate(Sum('Amount'))
    #print 'Aggregate depositedEquities=[',depositedEquities
    
    #look for user name match and then insert the new field for return equity
    for profit in investorsProfits:
        for returnedEquity in returnedEquities:
            #print 'profit.user=', profit['UserId__username'], ' REUser=', returnedEquity['UserId__username']
            if profit['UserId__username'] == returnedEquity['UserId__username']:
                profit['returnEquityAmount']= returnedEquity['Amount__sum']
                break #break out the inner for loop
    
    #look for user name match and then insert the new field for return equity
    for profit in investorsProfits:
        for depositedEquity in depositedEquities:
            #print 'profit.user=', profit['UserId__username'], ' REUser=', returnedEquity['UserId__username']
            if profit['UserId__username'] == depositedEquity['UserId__username']:
                profit['depositedEquityAmount']= depositedEquity['Amount__sum']
                profit['remainingEquityAmount']= depositedEquity['Amount__sum'] + profit['returnEquityAmount']
                
                break #break out the inner for loop

    print 'Aggregate final investorsProfits=',investorsProfits
    
    return {'investorsProfits':investorsProfits}
    
from django.http import JsonResponse
    
def getInvestorProfitsJSON(request, sort=None):
    outcome = getInvestorProfitsData(sort)    
    
    list_of_outcome = outcome['investorsProfits'][0:]
    return  JsonResponse(list_of_outcome,safe=False  )

@login_required
def getInvestorProfits(request, sort=None):
    outcome = getInvestorProfitsData(None)
    print 'outcome=', outcome
    
    investorsProfits = outcome['investorsProfits']
    
    total= 0
    for profit in investorsProfits:
        #print 'profit=', profit
        total += profit['Amount__sum']
        
    print 'total=[', total
    
    return render(request, 'admin/investorProfit.html', {'investorsProfits':investorsProfits, 'total':total})
    
