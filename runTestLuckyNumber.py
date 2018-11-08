import binascii
import csv
import json
import os
import sys, getopt
from time import time
import time
from collections import namedtuple
import time
import unittest
from ontology.smart_contract.native_contract.asset import Asset
from ontology.account.account import Account
from ontology.common.address import Address
from ontology.core.transaction import Transaction
from ontology.ont_sdk import OntologySdk
from ontology.smart_contract.neo_contract.abi.abi_info import AbiInfo
from ontology.smart_contract.neo_contract.abi.build_params import BuildParams
from ontology.crypto.signature_scheme import SignatureScheme
from ontology.smart_contract.neo_vm import NeoVm
import requests
import re
import random
from ontology.smart_contract.neo_contract.abi.abi_function import AbiFunction
from multiprocess import *

# rpc_address = "http://127.0.0.1:20336"
# rpc_address = "http://polaris3.ont.io:20336"
rpc_address = "http://139.219.139.170:20336"
sdk = OntologySdk()
sdk.set_rpc((rpc_address))
from datetime import datetime

# first contract
# luckyNumberContractAddress = "96df6058ed643b1a74e3d56ae0c3f2687ca8678f"

luckyNumberContractAddress = "b7737d095fa8067fa58d62752f870b23d35e0c78"  # without magnitude
# luckyNumberContractAddress = "b8bd3ca229e3a50f53a8ff47272949883c8b3b29"  # with magnitude

# luckyNumberContractAddress = "fd1b0d9475688e9f55a8441a2dd3bfb5886b91e2"

# second contract
# luckyNumberContractAddress = "4e95261813564464932f99692b6329fe680e3a64"

contract_address_str = luckyNumberContractAddress
contract_address_bytearray = bytearray.fromhex(contract_address_str)
contract_address = contract_address_bytearray
contract_address.reverse()

wallet_path = "C:\\Go_WorkSpace\\src\\github.com\\ontio\\ontology\\_Wallet_\\wallet.dat"
wallet_path1 = "D:\\SmartX_accounts\\Cyano Wallet\\lucknumberAccount\\wallet1.dat"
wallet_path10000 = "C:\\Go_WorkSpace\\src\\github.com\\ontio\\ontology\\_Wallet_\\wallet10000.dat"
sdk.wallet_manager.open_wallet(wallet_path10000)
# sdk.wallet_manager.open_wallet(wallet_path1)


admin_addr = "AQf4Mzu1YJrhz9f3aRkkwSm9n3qhXGSh4p"
admin_pwd = "xinhao"
pwd = admin_pwd
adminAcct = sdk.wallet_manager.get_account(admin_addr, admin_pwd)


# admin_addr1 = "AYqCVffRcbPkf1BVCYPJqqoiFTFmvwYKhG"
# admin_pwd1 = "111111"
# adminAcct1 = sdk.wallet_manager.get_account(admin_addr1, admin_pwd1)
# # payerAcct = sdk.wallet_manager.get_account("AUnhXaudVSBFqjH92a6HrhQySUTiQjf5VR", pwd)

admin_addr2 = "AGsnRLY3CqSJzsVZKPJeyvxiy2pq537rsi"
admin_pwd2 = "xinhao"
adminAcct2 = sdk.wallet_manager.get_account(admin_addr2, admin_pwd2)
# payerAcct = sdk.wallet_manager.get_account("AUnhXaudVSBFqjH92a6HrhQySUTiQjf5VR", pwd)

accountNum = 2
accountAvgPaperNum = 10
accountAvgFillPaperNum = 5



class TestAsset(unittest.TestCase):

    def test_check_hash(self):
        hash = "dd20005e729d6988bb58f8183f91382725704826b5a04142a6afe80d40700f46"
        res = sdk.rpc.get_smart_contract_event_by_tx_hash(hash)
        print("Check-res is ", res)
        return True
    def test_check_endCurrentRound_hash1_1(self):
        hash = "64c3e4b6ec762a0cdb013040f12e57304562214d0b1387fe14473ee178cb7578"
        print("************** Round 1_1 *************** \n")
        self.test_handleEvent("endCurrentRound", hash)
        return True
    def test_check_endCurrentRound_hash1_2(self):
        hash = "cbe9ee7087cbf8a125cafabb0afdeff465ebe05539078affca67ac30a94153a3"
        print("************** Round 1_2 *************** \n")
        self.test_handleEvent("endCurrentRound", hash)
        return True
    def test_check_endCurrentRound_hash1_4(self):
        hash = "cb0ef3bdf321b082a2c48055ed799ba99bd1f98faf087a9db2cc56f55e0efaea"
        print("************** Round 1_4 *************** \n")
        self.test_handleEvent("endCurrentRound", hash)
        return True
    def test_check_endCurrentRound_hash1_5(self):
        hash = "f2468eef8768e51f46aacd1bf21e9e46b3ff20432e5d246ac00cdf3c6b6fdd62"
        hash = "1d97f5b05de00c79395a74265dbfea6770e2b15380933f9151e0a5bb45cf747e"
        print("************** Round 1_5 *************** \n")
        self.test_handleEvent("endCurrentRound", hash)
        return True
    def test_check_endCurrentRound_hash2_1(self):
        hash = "9de11b0762027e5039379e76613272849f9127e625d23fdbd6eaaca5b95fb88c"
        print("************** Round 2_1 *************** \n")
        self.test_handleEvent("endCurrentRound", hash)
        return True
    def test_check_endCurrentRound_hash3_1(self):
        hash = "119afc8849aaec85515d112e687ce38400f4e0d31d3250511c76cd0f918385ba"
        print("************** Round 3_1 *************** \n")
        self.test_handleEvent("endCurrentRound", hash)
        return True
    def test_check_endCurrentRound_hash3_2(self):
        hash = "88700f32d22c681357e78c6fd1fe9f18edcd59be8fd0b908ab0498a4debec2f4"
        print("************** Round 3_2 *************** \n")
        self.test_handleEvent("endCurrentRound", hash)
        return True
    def test_check_withdraw_hash(self):
        hash = "eb03a15796586f4b9067937487d1f4a211a9acde041bbfcc689f13d71122fe41"
        print("************** Round 2_1 *************** \n")
        res = sdk.rpc.get_smart_contract_event_by_tx_hash(hash)
        print("res is ", res)




    def test_fillSomePaper(self):

        rpc_address = "http://139.219.139.170:20336"
        sdk1 = OntologySdk()
        sdk1.set_rpc((rpc_address))
        sdk.wallet_manager.open_wallet(wallet_path1)
        admin_addr1 = "AYqCVffRcbPkf1BVCYPJqqoiFTFmvwYKhG"
        admin_pwd1 = "111111"
        adminAcct1 = sdk.wallet_manager.get_account(admin_addr1, admin_pwd1)
        self.test_fillPaper(adminAcct1, 5)



    def test_init(self):
        param_list = []
        # when pre-execute, don't use 0x67
        abi_function = AbiFunction("init", "",param_list)
        hash = sdk.neo_vm().send_transaction(contract_address, adminAcct, adminAcct, 20000, 500, abi_function, False)
        # res = sdk.rpc.send_raw_transaction(tx)
        time.sleep(6)
        res = sdk.rpc.get_smart_contract_event_by_tx_hash(hash)
        print("init-res is ", res)
        events = res["Notify"]
        for event in events:
            if event["ContractAddress"] == luckyNumberContractAddress:
                notifyContent = (bytearray.fromhex(event["States"][0])).decode('utf-8')
                print("init-res-event is : ", notifyContent)
        return True

    def test_startNewRound(self):
        param_list = []
        # when pre-execute, don't use 0x67
        abi_function = AbiFunction("startNewRound", "", param_list)
        hash = sdk.neo_vm().send_transaction(contract_address, adminAcct, adminAcct, 200000, 500, abi_function, False)
        # res = sdk.rpc.send_raw_transaction(tx)
        time.sleep(6)
        res = sdk.rpc.get_smart_contract_event_by_tx_hash(hash)
        print("startNewRound-res is ", res)
        events = res["Notify"]
        for event in events:
            if event["ContractAddress"] == luckyNumberContractAddress:
                notifyContent1 = (bytearray.fromhex(event["States"][0])).decode('utf-8')
                tmp = str(event["States"][1])
                if not tmp:
                    tmp = "0"
                tmp = bytearray.fromhex(tmp)
                tmp.reverse()
                notifyContent2 = int(tmp.hex(), 16)
                print("startNewRound-res-event is : ", notifyContent1, " ", notifyContent2)
        return True

    def test_endCurrentRound(self):

        roundNum = self.test_getCurrentRound()
        print("test-getCurrentRound is ", roundNum)
        print("test-getFilledPaperAmount is ", self.test_getFilledPaperAmount(roundNum))

        # return True
        # when pre-execute, don't use 0x67
        AdminAcct = sdk.wallet_manager.get_account(admin_addr, admin_pwd)
        param_list = []
        param_list.append("endCurrentRound".encode())
        param_list1 = []
        param_list.append(param_list1)

        # print("*****\n", param_list)
        params = BuildParams.create_code_params_script(param_list)

        # tx = NeoVm.make_invoke_transaction(bytearray(contract_address), bytearray(params), b'', 20000, 500)
        # sdk.sign_transaction(tx, AdminAcct)
        # gaslimit = 0
        # loopFlag = True
        # while loopFlag:
        #     try:
        #         nil, gaslimit = sdk.rpc.send_raw_transaction_pre_exec(tx)
        #     except requests.exceptions.ConnectTimeout or requests.exceptions.ConnectionError:
        #         loopFlag = True
        #     if gaslimit != 0:
        #         loopFlag = False

        gaslimit = 200000000000

        # print("*** gaslimit is **** ", gaslimit)
        gaslimit = gaslimit * 2

        params.append(0x67)
        for i in contract_address:
            params.append(i)

        unix_time_now = int(time.time())
        tx = Transaction(0, 0xd1, unix_time_now, 500, gaslimit, AdminAcct.get_address().to_array(), params, bytearray(), [], bytearray())
        sdk.sign_transaction(tx, AdminAcct)

        hash = tx.hash256_explorer()
        print("endCurrentRound -> hash : ", hash)

        hash = sdk.rpc.send_raw_transaction(tx)
        time.sleep(18)
        self.test_handleEvent("endCurrentRound", hash)
        return True


    def test_withdrawGas(self):
        param_list = []
        abi_function = AbiFunction("withdrawGas", "", param_list)
        hash = sdk.neo_vm().send_transaction(contract_address, adminAcct, adminAcct, 200000, 500, abi_function, False)
        time.sleep(6)
        res = sdk.rpc.get_smart_contract_event_by_tx_hash(hash)
        print("withrawGas-res is ", res)
        return True


    def test_buyPapers(self):

        # wm = sdk.wallet_manager.open_wallet(wallet_path)
        # fakeAccountList = wm.get_accounts()
        accountListToBeUsed = []
        addressList = []
        roundNum = self.test_getCurrentRound()
        # i = 10023
        # fakeAccountListToBeUsed = fakeAccountList[i - 1:len(fakeAccountList) - 1]
        ### export and save private key
        # # fakeAccountListToBeUsed = fakeAccountList[0:10]
        # print("there are ", len(fakeAccountList), "accounts")
        # with open("C:\\Go_WorkSpace\\src\\github.com\\ontio\\ontology\\_Wallet_\\privateKey10000.csv", "a", newline="") as csvfile:
        #     writer = csv.writer(csvfile)
        #     for fakeAccount in fakeAccountListToBeUsed:
        #         # print("\naccountList", fakeAccount.get_address())
        #         base58Address = fakeAccount.get_address()
        #         # print(i, "base58", base58Address)
        #         # addressList.append(base58Address)
        #         account = sdk.wallet_manager.get_account(base58Address, pwd)
        #
        #         wif = account.export_wif()
        #         privatekeybyte = account.get_private_key_from_wif(wif)
        #         privateKey = privatekeybyte.hex()
        #         print(i, ":", base58Address, ":", privateKey)
        #
        #         writer.writerow([i, base58Address, privateKey])
        #
        #         accountListToBeUsed.append(account)
        #         i = i + 1
        # print("***** finished read account from wallet.dat ***********\n")
        # return True
        accountListToBeUsed = []
        accountFromIndex = 2
        accountEndIndex = 3
        line_num = 0
        with open("privateKey10000.csv") as csvfile:
            csvFile = csv.reader(csvfile, delimiter=',')
            rowsToBeUsed = [row for idx, row in enumerate(csvFile) if idx in range(accountFromIndex-1, accountEndIndex)]
            for line in rowsToBeUsed:
                # i = line[0]
                # base58Address = line[1]
                # privateKey = line[2]
                # print(i, base58Address, privateKey)
                print(line[0], " account is loading... ")
                accountListToBeUsed.append(Account(line[2], SignatureScheme.SHA256withECDSA))

        ongUnit = 1000000000
        ongAmount = 200 * ongUnit
        i = 1
        for account in accountListToBeUsed :
            print("transfer", i)
            balance = self.test_getONGBalance(account.get_address_base58())
            if balance < ongAmount:
                self.test_transferONG(adminAcct, account, ongAmount - balance)
            elif balance > ongAmount:
                self.test_transferONG(account, adminAcct, balance - ongAmount)
            i = i + 1
        print("***** finished transfer ONG to these accounts ***********\n")
        time.sleep(30)
        i = 1
        for account in accountListToBeUsed:
            print("<", i, "> ", "Balance -- ", account.get_address_base58(), " -- ", self.test_getONGBalance(account.get_address_base58()))
            i = i + 1
        # return True

        unfilledPaperBalanceList = []
        hashBuyPaperList = []
        hashFillPaperList = []
        hashFillPaper1List = []
        paperAmount = 1
        i = 0
        for account in accountListToBeUsed:
            unfilledPaperBalance = self.test_getPaperBalance(account)
            filledPaperBalance = self.test_getFilledPaperBalance(account, roundNum)
            paperBalance = unfilledPaperBalance + filledPaperBalance
            hash = None
            if paperBalance < paperAmount:
                hash = self.test_buyPaper(account, paperAmount - paperBalance)
                print("hash is ", hash)
                return True
            hashBuyPaperList.append(hash)
            i = i + 1
            print("<Player", i, ">", "buy -- ",hash)
            print("Before Buy, paperBalance : ", paperBalance, " filledPaperBalance : ", filledPaperBalance, " unfilledPaperBalance : ", unfilledPaperBalance)
            # time.sleep(0.1)
        time.sleep(30)

        i = 0

        for account in accountListToBeUsed:
            # print("\naccount base58 address", account.get_address_base58())

            # hashFillPaperList.append(self.test_fillPaper(account, paperAmount))

            unfilledPaperBalance = self.test_getPaperBalance(account)
            filledPaperBalance = self.test_getFilledPaperBalance(account, roundNum)
            paperBalance = unfilledPaperBalance + filledPaperBalance

            paperNumberFrom = i * 100
            hash = None
            if unfilledPaperBalance > 0:

               # hash = self.test_fillPaper(account, paperAmount)

                hash = self.test_fillPaper1(account, unfilledPaperBalance, paperNumberFrom + filledPaperBalance)

            hashFillPaper1List.append(hash)

            i = i + 1
            print("<Player", i , ">", "fill -- ", hash )
            print("After Buy, paperBalance : ", paperBalance, " filledPaperBalance : ", filledPaperBalance, " unfilledPaperBalance : ", unfilledPaperBalance)
            # time.sleep(0.1)
        time.sleep(30)

        i = 0
        for index in range(len(hashBuyPaperList)):
            i = i + 1
            print("<Player", i, ">", "********************")
            hash = hashBuyPaperList[index]
            if hash:
                self.test_handleEvent("buyPaper", hash)
            # self.test_handleEvent("fillPaper", hashFillPaperList[index])
            hash = hashFillPaper1List[index]
            if hash:
                self.test_handleEvent("fillPaper1", hash)

        time.sleep(10)
        roundNum = self.test_getCurrentRound()
        print("test-getCurrentRound is ", roundNum)
        print("test-getFilledPaperAmount is ", self.test_getFilledPaperAmount(roundNum))
        return True


    def test_buyPaper(self, invokeAcct, paperAmount):

        param_list = []
        param_list.append("buyPaper".encode())
        param_list1 = []
        param_list1.append(invokeAcct.get_address().to_array())
        param_list1.append(paperAmount)
        param_list.append(param_list1)

        # print("*****\n", param_list)
        params = BuildParams.create_code_params_script(param_list)
        tx = NeoVm.make_invoke_transaction(bytearray(contract_address), bytearray(params), b'', 0, 0)
        sdk.sign_transaction(tx, invokeAcct)
        nil, gaslimit = sdk.rpc.send_raw_transaction_pre_exec(tx)
        # print("gasLimit2 in buy paper is ", gaslimit, type(gaslimit))
        # gaslimit = 2000000

        params.append(0x67)
        for i in contract_address:
            params.append(i)

        gaslimit = gaslimit * 2
        unix_time_now = int(time.time())
        tx = Transaction(0, 0xd1, unix_time_now, 500, gaslimit, invokeAcct.get_address().to_array(), params, bytearray(), [], bytearray())
        sdk.sign_transaction(tx, invokeAcct)

        loopFlag = True
        hash = None
        while loopFlag:
            try:

                hash = sdk.rpc.send_raw_transaction(tx)

            except requests.exceptions.ConnectTimeout or requests.exceptions.ConnectionError:
                loopFlag = True
            if hash != None:
                loopFlag = False
        return hash

    def test_handleEvent(self, action, hash):
        res = sdk.rpc.get_smart_contract_event_by_tx_hash(hash)
        if action == "buyPaper":
            events = res["Notify"]
            # print("buyPaper-res-events is ", events)
            notifyContents = []
            i = 1
            for event in events:
                notifyContent = []
                if event["ContractAddress"] == luckyNumberContractAddress:
                    first = (bytearray.fromhex(event["States"][0])).decode('utf-8')
                    notifyContent.append(first)
                    if first == "buyPaper":
                        address1 = Address(binascii.a2b_hex(event["States"][1]))
                        account = address1.b58encode()
                        notifyContent.append(account)

                        ongAmount = str(event["States"][2])
                        if not ongAmount:
                            ongAmount = "0"
                        ongAmount = bytearray.fromhex(ongAmount)
                        ongAmount.reverse()
                        ongAmount = int(ongAmount.hex(), 16)
                        notifyContent.append(ongAmount)

                        paperAmoung = str(event["States"][3])
                        if not paperAmoung:
                            paperAmoung = "0"
                        paperAmoung = bytearray.fromhex(paperAmoung)
                        paperAmoung.reverse()
                        paperAmoung = int(paperAmoung.hex(), 16)
                        notifyContent.append(paperAmoung)

                        timeStamp = str(event["States"][4])
                        if not timeStamp:
                            timeStamp = "0"
                        timeStamp = bytearray.fromhex(timeStamp)
                        timeStamp.reverse()
                        timeStamp = int(timeStamp.hex(), 16)
                        dateTime = datetime.utcfromtimestamp(timeStamp).strftime('%Y-%m-%d %H:%M:%S')
                        notifyContent.append(dateTime)
                    elif first == "BuyPaperError":
                        errorMsg = (bytearray.fromhex(event["States"][1])).decode('utf-8')
                        notifyContent.append(errorMsg)
                    else:
                        print("test notify message is : ", event['States'])
                        notifyContent.append(event["States"])
                    print("buyPaper-res-event", i, " is : ", notifyContent)
                    i = i + 1
                    notifyContents.append(notifyContent)
            print("buyPaper-res-events is : ", notifyContents)
        elif action == "fillPaper" or action == "fillPaper1":
            events = res["Notify"]

            # print("fillPaper-res-events is ", events)
            # return True
            notifyContents = []
            i = 1
            for event in events:
                notifyContent = []
                if event["ContractAddress"] == luckyNumberContractAddress:
                    first = (bytearray.fromhex(event["States"][0])).decode('utf-8')
                    if first == "fillPaper":
                        notifyContent.append(first)

                        address1 = Address(binascii.a2b_hex(event["States"][1]))
                        account = address1.b58encode()
                        notifyContent.append(account)

                        guessNumberList = event["States"][2]
                        returnedNumberList = []
                        for guessNumber in guessNumberList:
                            if not guessNumber:
                                guessNumber = "0"
                            guessNumber = bytearray.fromhex(guessNumber)
                            guessNumber.reverse()
                            guessNumber = int(guessNumber.hex(), 16)
                            returnedNumberList.append(guessNumber)
                        notifyContent.append(returnedNumberList)

                        timeStamp = str(event["States"][3])
                        if not timeStamp:
                            timeStamp = "0"
                        timeStamp = bytearray.fromhex(timeStamp)
                        timeStamp.reverse()
                        timeStamp = int(timeStamp.hex(), 16)
                        dateTime = datetime.utcfromtimestamp(timeStamp).strftime('%Y-%m-%d %H:%M:%S')
                        notifyContent.append(dateTime)
                    elif first == "FillPaperError":
                        errorMsg = (bytearray.fromhex(event["States"][1])).decode('utf-8')
                        notifyContent.append(errorMsg)
                    else:
                        print("test notify message is : ", event)
                    i = i + 1
                    print("random fillPaper-res-event", i, " is : ", notifyContent)
                    notifyContents.append(notifyContent)
            if action == "fillPaper":
                print("random fillPaper-res-event is : ", notifyContents)
            elif action == "fillPaper1":
                print("continus fillPaper-res-event is : ", notifyContents)
        elif action == "endCurrentRound":
            print("endCurrentRound-hash is ", hash)
            res = sdk.rpc.get_smart_contract_event_by_tx_hash(hash)
            print("endCurrentRound-res is ", res)
            events = res["Notify"]
            notifyContents = []
            i = 1
            # print("events === ", events)
            for event in events:
                notifyContent = []
                if event["ContractAddress"] == luckyNumberContractAddress:
                    first = (bytearray.fromhex(event["States"][0])).decode('utf-8')
                    notifyContent.append(first)
                    if first == "endRound":
                        tmp = str(event["States"][1])
                        if not tmp:
                            tmp = "0"
                        tmp = bytearray.fromhex(tmp)
                        tmp.reverse()
                        roundNumber = int(tmp.hex(), 16)
                        notifyContent.append(roundNumber)

                        if len(event["States"]) == 2:
                            continue

                        luckyNumber = str(event["States"][2])
                        if not luckyNumber:
                            luckyNumber = "0"
                        luckyNumber = bytearray.fromhex(luckyNumber)
                        luckyNumber.reverse()
                        luckyNumber = int(luckyNumber.hex(), 16)
                        notifyContent.append(luckyNumber)

                        actualLuckyNumberList = event["States"][3]
                        actualLuckyNumberList1 = []
                        for actualLuckyNumber in actualLuckyNumberList:
                            if not actualLuckyNumber:
                                actualLuckyNumber = "0"
                            actualLuckyNumber = bytearray.fromhex(actualLuckyNumber)
                            actualLuckyNumber.reverse()
                            actualLuckyNumber = int(actualLuckyNumber.hex(), 16)
                            actualLuckyNumberList1.append(actualLuckyNumber)
                        notifyContent.append(actualLuckyNumberList1)

                        winAwardList = str(event["States"][4])
                        notifyContent.append(winAwardList)

                        time = str(event["States"][5])
                        time = bytearray.fromhex(time)
                        time.reverse()
                        time = int(time.hex(), 16)
                        notifyContent.append(time)

                        # print("endCurrentRound-res-event is : ", notifyContent)
                    elif first == "destroyPaper":
                        address1 = Address(binascii.a2b_hex(event["States"][1]))
                        account = address1.b58encode()
                        notifyContent.append(account)

                        filledPaperBalance = str(event["States"][2])
                        if not filledPaperBalance:
                            filledPaperBalance = "0"
                        filledPaperBalance = bytearray.fromhex(filledPaperBalance)
                        filledPaperBalance.reverse()
                        filledPaperBalance = int(filledPaperBalance.hex(), 16)
                        notifyContent.append(filledPaperBalance)

                        timeStamp = str(event["States"][3])
                        if not timeStamp:
                            timeStamp = "0"
                        timeStamp = bytearray.fromhex(timeStamp)
                        timeStamp.reverse()
                        timeStamp = int(timeStamp.hex(), 16)
                        dateTime = datetime.utcfromtimestamp(timeStamp).strftime('%Y-%m-%d %H:%M:%S')
                        notifyContent.append(dateTime)
                    elif first == "startRound":
                        tmp = str(event["States"][1])
                        if not tmp:
                            tmp = "0"
                        tmp = bytearray.fromhex(tmp)
                        tmp.reverse()
                        roundNumber = int(tmp.hex(), 16)
                        notifyContent.append(roundNumber)
                    elif first == "EndCurrentRoundError":
                        errorMsg = (bytearray.fromhex(event["States"][1])).decode('utf-8')
                        notifyContent.append(errorMsg)
                    print("endCurrentRound event - <", i, ">", " -- endCurrentRound-res-event is : ", notifyContent)
                    i = i + 1
                    notifyContents.append(notifyContent)
            print("endCurrentRound-res-events is : ", notifyContents)
            consumedONG = res["GasConsumed"]
            print("endCurrentRound-consume-ong-amount is : ", consumedONG / 10 ** 9, " ONG")

    def test_fillPaper(self, fillAcct, fillAmount):
        payerAcct = fillAcct
        fillAddr = fillAcct.get_address().to_array()

        param_list = []
        param_list.append("fillPaper".encode())
        param_list1 = []
        param_list1.append(fillAddr)
        param_list2 = []
        for i in range(fillAmount):
            randNum = random.randint(0, 9999)
            while randNum in param_list:
                randNum = random.randint(0, 9999)
            param_list2.append(randNum)
        param_list1.append(param_list2)
        param_list.append(param_list1)
        # print("***** fillPaper", param_list)



        # unix_time_now = int(time.time())
        # tx = Transaction(0, 0xd1, unix_time_now, 500, 200000, payerAcct.get_address().to_array(), params, bytearray(), [], bytearray())
        # sdk.sign_transaction(tx, payerAcct)
        # nouse, gaslimit = sdk.rpc.send_raw_transaction_pre_exec(tx)
        # print("gasLimit1 in fill paper is ", gaslimit, type(gaslimit))
        params = BuildParams.create_code_params_script(param_list)
        tx = NeoVm.make_invoke_transaction(bytearray(contract_address), bytearray(params), b'', 20000, 500)
        sdk.sign_transaction(tx, payerAcct)
        nil, gaslimit = sdk.rpc.send_raw_transaction_pre_exec(tx)
        # print("gasLimit2 in fill paper is ", gaslimit, type(gaslimit))

        params.append(0x67)
        for i in contract_address:
            params.append(i)

        gaslimit = 20000000
        gaslimit = gaslimit * 2
        unix_time_now = int(time.time())
        tx = Transaction(0, 0xd1, unix_time_now, 500, gaslimit, payerAcct.get_address().to_array(), params, bytearray(), [], bytearray())
        sdk.sign_transaction(tx, payerAcct)
        loopFlag = True
        hash = None
        while loopFlag:
            try:

                hash = sdk.rpc.send_raw_transaction(tx)

            except requests.exceptions.ConnectTimeout or requests.exceptions.ConnectionError:
                loopFlag = True
            if hash != None:
                loopFlag = False

        return hash


    def test_fillPaper1(self, fillAcct, fillAmount, paperNumberFrom):
        fillAddr = fillAcct.get_address().to_array()

        param_list = []
        param_list.append("fillPaper".encode())
        param_list1 = []
        param_list1.append(fillAddr)
        param_list2 = []
        for i in range(fillAmount):
            num = paperNumberFrom + i
            num = num % 10000
            num = int(num)
            param_list2.append(num)

        param_list1.append(param_list2)
        param_list.append(param_list1)
        print("***** fillPaper1", param_list)


        # tx = NeoVm.make_invoke_transaction(bytearray(contract_address), bytearray(params), b'', 20000, 500)
        # sdk.sign_transaction(tx, payerAcct)
        # nil, gaslimit = sdk.rpc.send_raw_transaction_pre_exec(tx)
        # # print("gasLimit2 in fill paper1 is ", gaslimit, type(gaslimit))

        params = BuildParams.create_code_params_script(param_list)

        params.append(0x67)
        for i in contract_address:
            params.append(i)

        gaslimit = 2000000
        gaslimit = gaslimit * 2
        unix_time_now = int(time.time())
        tx = Transaction(0, 0xd1, unix_time_now, 500, gaslimit, fillAcct.get_address().to_array(), params, bytearray(), [], bytearray())
        sdk.sign_transaction(tx, fillAcct)

        loopFlag = True
        hash = None
        # while loopFlag:
        #     try:
        #
        #         hash = sdk.rpc.send_raw_transaction(tx)
        #     except requests.exceptions.ConnectTimeout or requests.exceptions.ConnectionError:
        #         loopFlag = True
        #     if hash != None:
        #         loopFlag = False
        #
        hash = sdk.rpc.send_raw_transaction(tx)
        return hash



    def test_migrateContract(self):
        # code, needStorage, name, version, author, email, description
        code = "02ae00c56b6a00527ac46a51527ac46a00c304696e69749c6417006a51c3c0009e640700006c756661652b356c7566616a00c30d73746172744e6577526f756e649c6417006a51c3c0009e640700006c75666165aa326c7566616a00c30b616464526566657272616c9c6432006a51c3c0529e640700006c7566616a51c300c36a52527ac46a51c351c36a53527ac46a52c36a53c37c65af316c7566616a00c3106164644d756c7469526566657272616c9c640c006a51c36598306c7566616a00c30b61737369676e50617065729c6432006a51c3c0529e640700006c7566616a51c300c36a54527ac46a51c351c36a55527ac46a54c36a55c37c65a92e6c7566616a00c3106d756c746941737369676e50617065729c640c006a51c365ee2d6c7566616a00c30b77697468647261774761739c6417006a51c3c0009e640700006c756661652b2d6c7566616a00c30f656e6443757272656e74526f756e649c6417006a51c3c0009e640700006c7566616513256c7566616a00c30862757950617065729c6432006a51c3c0529e640700006c7566616a51c300c36a54527ac46a51c351c36a55527ac46a54c36a55c37c65b91f6c7566616a00c3087265696e766573749c6432006a51c3c0529e640700006c7566616a51c300c36a54527ac46a51c351c36a55527ac46a54c36a55c37c6537196c7566616a00c30966696c6c50617065729c6432006a51c3c0529e640700006c7566616a51c300c36a54527ac46a51c351c36a56527ac46a54c36a56c37c65ca146c7566616a00c30877697468647261779c6424006a51c3c0519e640700006c7566616a51c300c36a54527ac46a54c36580126c7566616a00c30f6d696772617465436f6e74726163749c6490006a51c3c0579e640700006c7566616a51c300c36a57527ac46a51c351c36a58527ac46a51c352c36a59527ac46a51c353c36a5a527ac46a51c354c36a5b527ac46a51c355c36a5c527ac46a51c356c36a5d527ac46a57c36a58c36a59c36a5ac36a5bc36a5cc36a5dc356795179587275517275557952795772755272755479537956727553727565c7106c7566616a00c30d676574546f74616c50617065729c6417006a51c3c0009e640700006c75666165140f6c7566616a00c30b6765744761735661756c749c6417006a51c3c0009e640700006c75666165a80e6c7566616a00c30f67657443757272656e74526f756e649c6417006a51c3c0009e640700006c75666165380e6c7566616a00c30f67657443757272656e7450726963659c6417006a51c3c0009e640700006c75666165d60d6c7566616a00c31667657443757272656e74526f756e64456e6454696d659c64090065830d6c7566616a00c30f676574506170657242616c616e63659c6424006a51c3c0519e640700006c7566616a51c300c36a54527ac46a54c365fa0c6c7566616a00c313676574496e766573744f6e6742616c616e63659c6424006a51c3c0519e640700006c7566616a51c300c36a54527ac46a54c3656d0c6c7566616a00c312676574526566657272616c42616c616e63659c6424006a51c3c0519e640700006c7566616a51c300c36a54527ac46a54c365e10b6c7566616a00c3126765744469766964656e6442616c616e63659c6424006a51c3c0519e640700006c7566616a51c300c36a54527ac46a54c3658c0a6c7566616a00c30f676574417761726442616c616e63659c6424006a51c3c0519e640700006c7566616a51c300c36a54527ac46a54c365030a6c7566616a00c3136765744469766964656e647342616c616e63659c6424006a51c3c0519e640700006c7566616a51c300c36a54527ac46a54c365a5096c7566616a00c31367657457697468647261776e42616c616e63659c6424006a51c3c0519e640700006c7566616a51c300c36a54527ac46a54c36518096c7566616a00c30b676574526566657272616c9c6424006a51c3c0519e640700006c7566616a51c300c36a54527ac46a54c36593086c7566616a00c30d67657441776172645661756c749c6424006a51c3c0519e640700006c7566616a51c300c36a5e527ac46a5ec36582076c7566616a00c30c6765744e6578745661756c749c6424006a51c3c0519e640700006c7566616a51c300c36a5e527ac46a5ec365ed066c7566616a00c30d67657447616d655374617475739c6424006a51c3c0519e640700006c7566616a51c300c36a5e527ac46a5ec36554066c7566616a00c317676574526f756e64536f6c645061706572416d6f756e749c6424006a51c3c0519e640700006c7566616a51c300c36a5e527ac46a5ec365ac056c7566616a00c31467657446696c6c65645061706572416d6f756e749c6424006a51c3c0519e640700006c7566616a51c300c36a5e527ac46a5ec36507056c7566616a00c3157570646174654469766964656e6442616c616e63659c6424006a51c3c0519e640700006c7566616a51c300c36a54527ac46a54c3657b0b6c7566616a00c31567657446696c6c6564506170657242616c616e63659c6432006a51c3c0529e640700006c7566616a51c300c36a54527ac46a51c351c36a5e527ac46a54c36a5ec37c6569066c7566616a00c30e6765744c75636b794e756d6265729c6409006521026c7566616a00c31367657446696c6c65644e756d6265724c6973749c6416006a51c300c36a5e527ac46a5ec3658b036c7566616a00c30e676574506c61796572734c6973749c6424006a51c300c36a5f527ac46a51c351c36a60527ac46a5fc36a60c37c654e026c756661006c756655c56b6a00527ac46a51527ac46a00c3015f7e6a51c37e6c75665bc56b6a00527ac46a51527ac4682d53797374656d2e457865637574696f6e456e67696e652e476574457865637574696e6753637269707448617368616a52527ac41400000000000000000000000000000000000000026a53527ac46a52c36a00c36a51c353c66b6a52527ac46a51527ac46a00527ac46c6a54527ac4006a53c3087472616e736665726a54c351c176c9537951795572755172755279527954727552727568164f6e746f6c6f67792e4e61746976652e496e766f6b65616a55527ac46a55c36410006a55c301019c640700516c756661006c7566006c75665cc56b6a00527ac46a51527ac46a52527ac41400000000000000000000000000000000000000026a53527ac46a00c365612f756a00c36a51c36a52c353c66b6a52527ac46a51527ac46a00527ac46c6a54527ac4006a53c3087472616e736665726a54c351c176c9537951795572755172755279527954727552727568164f6e746f6c6f67792e4e61746976652e496e766f6b65616a55527ac46a55c36410006a55c301019c640700516c756661006c7566006c756656c56b681e4f6e746f6c6f67792e52756e74696d652e47657452616e646f6d48617368616a00527ac46a00c3021027976a51527ac46a51c3906a51527ac46a51c36c756659c56b6a00527ac46a51527ac40400ca9a3b6a52527ac46a00c36546026a53527ac46a52c3022c246a53c395930216126a51c39593021612946a54527ac46a54c36a51c3956a55527ac46a55c36c75665ec56b6a00527ac46a51527ac40247316a52527ac4035230366a53527ac46a52c36a00c37c6598fd6a53c36a51c37c658efd7c658afd6a54527ac4681953797374656d2e53746f726167652e476574436f6e74657874616a54c37c681253797374656d2e53746f726167652e476574616a55527ac400c176c96a56527ac46a55c36428006a55c3681a53797374656d2e52756e74696d652e446573657269616c697a65616a56527ac461006a58527ac46a56c3c06a59527ac4616a58c36a59c39f643b006a56c36a58c3c36a57527ac46a58c351936a58527ac46a57c351c176c9681553797374656d2e52756e74696d652e4e6f746966796162c0ff6161616a56c36c75665bc56b6a00527ac40247316a51527ac4035230356a52527ac46a51c36a00c37c6598fc6a52c37c6591fc6a53527ac4681953797374656d2e53746f726167652e476574436f6e74657874616a53c37c681253797374656d2e53746f726167652e476574616a54527ac400c176c96a55527ac46a54c36428006a54c3681a53797374656d2e52756e74696d652e446573657269616c697a65616a55527ac4616a55c36c756657c56b6a00527ac40247316a51527ac4035230346a52527ac46a51c36a00c37c65f4fb6a52c37c65edfb6a53527ac4681953797374656d2e53746f726167652e476574436f6e74657874616a53c37c681253797374656d2e53746f726167652e476574616c756657c56b6a00527ac40247316a51527ac4035230336a52527ac46a51c36a00c37c658dfb6a52c37c6586fb6a53527ac4681953797374656d2e53746f726167652e476574436f6e74657874616a53c37c681253797374656d2e53746f726167652e476574616c756656c56b6a00527ac40247316a51527ac4065374617475736a52527ac4681953797374656d2e53746f726167652e476574436f6e74657874616a51c36a00c37c6507fb6a52c37c6500fb7c681253797374656d2e53746f726167652e476574616c756656c56b6a00527ac40247316a51527ac4035230326a52527ac4681953797374656d2e53746f726167652e476574436f6e74657874616a51c36a00c37c65a8fa6a52c37c65a1fa7c681253797374656d2e53746f726167652e476574616c756656c56b6a00527ac40247316a51527ac4035230316a52527ac4681953797374656d2e53746f726167652e476574436f6e74657874616a51c36a00c37c6549fa6a52c37c6542fa7c681253797374656d2e53746f726167652e476574616c756659c56b6a00527ac46a51527ac40247316a52527ac4035530316a53527ac46a52c36a51c37c6501fa6a54527ac46a53c36a00c37c65f2f96a55527ac4681953797374656d2e53746f726167652e476574436f6e74657874616a54c36a55c37c65c7f97c681253797374656d2e53746f726167652e476574616c756655c56b6a00527ac4034731336a51527ac4681953797374656d2e53746f726167652e476574436f6e74657874616a51c36a00c37c6577f97c681253797374656d2e53746f726167652e476574616c756655c56b6a00527ac4034731316a51527ac4681953797374656d2e53746f726167652e476574436f6e74657874616a51c36a00c37c6527f97c681253797374656d2e53746f726167652e476574616c756654c56b6a00527ac46a00c36555ff6a00c36560006a00c3650a0053c176c96c756655c56b6a00527ac4034731306a51527ac4681953797374656d2e53746f726167652e476574436f6e74657874616a51c36a00c37c65b6f87c681253797374656d2e53746f726167652e476574616c75665ec56b6a00527ac4034730366a51527ac4034730376a52527ac4034731346a53527ac46a53c36a00c37c6570f86a54527ac4681953797374656d2e53746f726167652e476574436f6e74657874616a54c37c681253797374656d2e53746f726167652e476574616a55527ac4681953797374656d2e53746f726167652e476574436f6e74657874616a51c37c681253797374656d2e53746f726167652e476574616a56527ac46a56c36a55c3946a57527ac4006a58527ac46a57c3009e6415006a57c36a00c365f3007c6593276a58527ac461681953797374656d2e53746f726167652e476574436f6e74657874616a52c36a00c37c65a4f77c681253797374656d2e53746f726167652e476574616a58c37c65e6276c756655c56b6a00527ac4034730386a51527ac4681953797374656d2e53746f726167652e476574436f6e74657874616a51c36a00c37c654df77c681253797374656d2e53746f726167652e476574616c756655c56b6a00527ac4034731326a51527ac4681953797374656d2e53746f726167652e476574436f6e74657874616a51c36a00c37c65fdf67c681253797374656d2e53746f726167652e476574616c756655c56b6a00527ac4034730396a51527ac4681953797374656d2e53746f726167652e476574436f6e74657874616a51c36a00c37c65adf67c681253797374656d2e53746f726167652e476574616c756656c56b04090bdc5b6a00527ac46557006a51527ac46a00c36a51c30208077c653526936a52527ac46a52c36c756657c56b0400ca9a3b6a00527ac46529006a51527ac46a51c3659efa6a52527ac46a00c3022c246a52c395936a53527ac46a53c36c756654c56b034730346a00527ac4681953797374656d2e53746f726167652e476574436f6e74657874616a00c37c681253797374656d2e53746f726167652e476574616c756654c56b034730326a00527ac4681953797374656d2e53746f726167652e476574436f6e74657874616a00c37c681253797374656d2e53746f726167652e476574616c756654c56b034730336a00527ac4681953797374656d2e53746f726167652e476574436f6e74657874616a00c37c681253797374656d2e53746f726167652e476574616c75665ec56b6a00527ac4034730366a51527ac4034730376a52527ac4034731346a53527ac46a53c36a00c37c6537f56a54527ac4681953797374656d2e53746f726167652e476574436f6e74657874616a54c37c681253797374656d2e53746f726167652e476574616a55527ac4681953797374656d2e53746f726167652e476574436f6e74657874616a51c37c681253797374656d2e53746f726167652e476574616a56527ac46a56c36a55c37c65f1246a57527ac46a57c3009e648600681953797374656d2e53746f726167652e476574436f6e74657874616a52c36a00c37c6581f46a00c365e1fb5272681253797374656d2e53746f726167652e50757461681953797374656d2e53746f726167652e476574436f6e74657874616a53c36a00c37c653ef46a56c35272681253797374656d2e53746f726167652e5075746161516c75665ec56b6a00527ac46a51527ac46a52527ac46a53527ac46a54527ac46a55527ac46a56527ac422415166344d7a7531594a72687a39663361526b6b77536d396e3371685847536834707514616f2a4a38396ff203ea01e6c070ae421bb8ce2d6a57527ac46a57c3653e24756a00c36a51c36a52c36a53c36a54c36a55c36a56c356795179587275517275557952795772755272755479537956727553727568194f6e746f6c6f67792e436f6e74726163742e4d696772617465611d4d69677261746520436f6e7472616374207375636365737366756c6c796a57c3681653797374656d2e52756e74696d652e47657454696d656153c176c9681553797374656d2e52756e74696d652e4e6f7469667961516c75660117c56b6a00527ac4034730376a51527ac4034730386a52527ac4034731306a53527ac4034731316a54527ac4682d53797374656d2e457865637574696f6e456e67696e652e476574457865637574696e6753637269707448617368616a55527ac46a00c3652c23756a00c3653bfd756a00c365fbf96a56527ac46a00c365a0f96a57527ac46a00c365fefa6a58527ac46a56c36a57c37c65cf226a58c37c65c8226a59527ac46a59c300a06414006a00c36a59c37c656cf26520237562080061516c756661681953797374656d2e53746f726167652e476574436f6e74657874616a51c36a00c37c651ff27c681553797374656d2e53746f726167652e44656c65746561681953797374656d2e53746f726167652e476574436f6e74657874616a53c36a00c37c65e0f17c681553797374656d2e53746f726167652e44656c65746561681953797374656d2e53746f726167652e476574436f6e74657874616a52c36a00c37c65a1f17c681553797374656d2e53746f726167652e44656c65746561681953797374656d2e53746f726167652e476574436f6e74657874616a54c36a00c37c6562f16a59c36a00c365fef77c65b4215272681253797374656d2e53746f726167652e507574610877697468647261776a55c36a00c36a59c3681653797374656d2e52756e74696d652e47657454696d656155c176c9681553797374656d2e52756e74696d652e4e6f7469667961516c7566012ec56b6a00527ac46a51527ac40247316a52527ac4035530316a53527ac4035230346a54527ac4035230356a55527ac4035230366a56527ac40752554e4e494e476a57527ac46a00c3652f21756575fa6a58527ac46a58c36551f56a57c39c656121756a51c3c06a59527ac46a59c351a2654f21756a00c36a58c37c654df66a5a527ac46a00c36587f96a5ac36a59c37c65bd20a2652b21756a52c36a58c37c654ff06a55c37c6548f06a5b527ac4681953797374656d2e53746f726167652e476574436f6e74657874616a5bc37c681253797374656d2e53746f726167652e476574616a5c527ac400c176c96a5d527ac46a5cc36428006a5cc3681a53797374656d2e52756e74696d652e446573657269616c697a65616a5d527ac461006a0116527ac46a51c3c06a0117527ac4616a0116c36a0117c39f647c016a51c36a0116c3c36a5e527ac46a0116c351936a0116527ac46a5ec30210279f656420756a5ec300a2655b20756a52c36a58c37c657fef6a56c36a5ec37c6575ef7c6571ef6a5f527ac4681953797374656d2e53746f726167652e476574436f6e74657874616a5fc37c681253797374656d2e53746f726167652e476574616a60527ac400c176c96a0111527ac46a60c36477006a60c3681a53797374656d2e52756e74696d652e446573657269616c697a65616a0111527ac4006a0118527ac46a0111c3c06a0119527ac4616a0118c36a0119c39f642d006a0111c36a0118c3c36a0112527ac46a0118c351936a0118527ac46a0112c36a00c39e65881f7562ccff6161620b00616a5dc36a5ec3c8616a0111c36a00c3c86a0111c3681853797374656d2e52756e74696d652e53657269616c697a65616a60527ac4681953797374656d2e53746f726167652e476574436f6e74657874616a5fc36a60c35272681253797374656d2e53746f726167652e50757461627dfe6161616a5dc3681853797374656d2e52756e74696d652e53657269616c697a65616a5c527ac4681953797374656d2e53746f726167652e476574436f6e74657874616a5bc36a5cc35272681253797374656d2e53746f726167652e507574616a52c36a58c37c65d4ed6a54c37c65cded6a0113527ac4681953797374656d2e53746f726167652e476574436f6e74657874616a0113c36a59c36a58c3658af17c65f91d5272681253797374656d2e53746f726167652e507574616a52c36a58c37c6579ed6a0114527ac46a53c36a00c37c6569ed6a0115527ac46a0114c36a0115c37c6557ed6a0113527ac4681953797374656d2e53746f726167652e476574436f6e74657874616a0113c36a59c36a5ac37c65861d5272681253797374656d2e53746f726167652e507574610966696c6c50617065726a00c36a51c3681653797374656d2e52756e74696d652e47657454696d656154c176c9681553797374656d2e52756e74696d652e4e6f7469667961516c7566013dc56b6a00527ac46a51527ac40247316a52527ac4034730326a53527ac4034730336a54527ac4034730366a55527ac4034730376a56527ac4034730386a57527ac4034730396a58527ac4034731306a59527ac4034731326a5a527ac4034731336a5b527ac4035230316a5c527ac4035230326a5d527ac4035230336a5e527ac40752554e4e494e476a5f527ac401326a60527ac4516a0111527ac401236a0112527ac45a6a0113527ac46a00c3659e1c7565e4f56a0114527ac46a0114c365bef06a5fc39c65ce1c756a0114c36a51c37c65e4ed6a0115527ac46a00c36584f6756a00c36544f36a0116527ac46a00c365e8f26a0117527ac46a00c36545f46a0118527ac46a0116c36a0117c37c65131c6a0118c37c650b1c6a0119527ac46a0119c36a0115c3a2656b1c756a0115c36a60c37c65511b01647c65231b6a011a527ac4681953797374656d2e53746f726167652e476574436f6e74657874616a5bc36a00c37c655ceb7c681253797374656d2e53746f726167652e476574616a011b527ac4006a011c527ac46a011bc36468006a0115c36a0111c37c65e91a01647c65bb1a6a011c527ac4681953797374656d2e53746f726167652e476574436f6e74657874616a57c36a011bc37c65f3ea6a011cc36a011bc36567f37c65431b5272681253797374656d2e53746f726167652e50757461616a011ac36a011cc37c65fd1a6a011d527ac46a0115c36a0113c37c65711a01647c65431a6a011e527ac46a52c36a0114c37c6597ea6a5dc37c6590ea6a011f527ac4681953797374656d2e53746f726167652e476574436f6e74657874616a011fc36a011ec36a0114c3657bef7c65ba1a5272681253797374656d2e53746f726167652e507574616a0115c36a0112c37c65fb1901647c65cd196a060527ac46a52c36a0114c37c6521ea6a5cc37c651aea6a0121527ac4681953797374656d2e53746f726167652e476574436f6e74657874616a0121c36a060c36a0114c36564ef7c65441a5272681253797374656d2e53746f726167652e507574616a0115c36a011ac37c65ff196a011ec37c65f7196a060c37c65ef196a0122527ac4681953797374656d2e53746f726167652e476574436f6e74657874616a53c36a0122c3659df37c65e1195272681253797374656d2e53746f726167652e50757461681953797374656d2e53746f726167652e476574436f6e74657874616a54c36a51c365a1f37c65a1195272681253797374656d2e53746f726167652e507574616a52c36a0114c37c6520e96a5ec37c6519e96a0123527ac4681953797374656d2e53746f726167652e476574436f6e74657874616a0123c36a51c36a0114c3653ced7c6544195272681253797374656d2e53746f726167652e507574616a00c36567f375681953797374656d2e53746f726167652e476574436f6e74657874616a58c36a00c37c65a1e86a51c36a00c365b7f17c65f3185272681253797374656d2e53746f726167652e50757461681953797374656d2e53746f726167652e476574436f6e74657874616a55c37c681253797374656d2e53746f726167652e476574616a0124527ac46a011dc36596f27c65d2176a0125527ac4681953797374656d2e53746f726167652e476574436f6e74657874616a55c36a0125c36a0124c37c6565185272681253797374656d2e53746f726167652e50757461681953797374656d2e53746f726167652e476574436f6e74657874616a59c36a00c37c65c9e77c681553797374656d2e53746f726167652e44656c65746561681953797374656d2e53746f726167652e476574436f6e74657874616a57c36a00c37c658ae77c681553797374656d2e53746f726167652e44656c657465616a0119c36a0115c37c65a2176a0126527ac4681953797374656d2e53746f726167652e476574436f6e74657874616a56c36a00c37c6539e76a0126c35272681253797374656d2e53746f726167652e50757461681953797374656d2e53746f726167652e476574436f6e74657874616a5ac36a00c37c65f8e66a0115c36a00c365bdef7c6549175272681253797374656d2e53746f726167652e507574610a726542757950617065726a00c36a0115c36a51c3681653797374656d2e52756e74696d652e47657454696d656155c176c9681553797374656d2e52756e74696d652e4e6f7469667961006c75660134c56b6a00527ac46a51527ac40247316a52527ac4034730326a53527ac4034730336a54527ac4034730366a55527ac4034730386a56527ac4034730396a57527ac4034731326a58527ac4035230316a59527ac4035230326a5a527ac4035230336a5b527ac40752554e4e494e476a5c527ac401326a5d527ac4516a5e527ac401236a5f527ac45a6a60527ac4682d53797374656d2e457865637574696f6e456e67696e652e476574457865637574696e6753637269707448617368616a0111527ac46a00c365441675658aef6a0112527ac46a0112c36564ea6a5cc39c657416756a0112c36a51c37c658ae76a0113527ac46a00c36a0111c36a0113c35272657ae6654f16756a0113c36a5dc37c65351501647c6507156a0114527ac46a00c365b5eb6a0115527ac4006a0116527ac46a0115c36467006a0113c36a5ec37c65041501647c65d6146a0116527ac4681953797374656d2e53746f726167652e476574436f6e74657874616a56c36a0115c37c650ee56a0116c36a0115c36582ed7c655e155272681253797374656d2e53746f726167652e50757461616a0114c36a0116c37c6518156a0117527ac46a0113c36a60c37c658d1401647c655f146a0118527ac46a52c36a0112c37c65b3e46a5ac37c65ace46a0119527ac4681953797374656d2e53746f726167652e476574436f6e74657874616a0119c36a0118c36a0112c36597e97c65d6145272681253797374656d2e53746f726167652e507574616a0113c36a5fc37c65181401647c65ea136a011a527ac46a52c36a0112c37c653ee46a59c37c6537e46a011b527ac4681953797374656d2e53746f726167652e476574436f6e74657874616a011bc36a011ac36a0112c36581e97c6561145272681253797374656d2e53746f726167652e507574616a0113c36a0114c37c651c146a0118c37c6514146a011ac37c650c146a011c527ac4681953797374656d2e53746f726167652e476574436f6e74657874616a53c36a011cc365baed7c65fe135272681253797374656d2e53746f726167652e50757461681953797374656d2e53746f726167652e476574436f6e74657874616a54c36a51c365beed7c65be135272681253797374656d2e53746f726167652e50757461681953797374656d2e53746f726167652e476574436f6e74657874616a58c36a00c37c6522e36a0113c36a00c365e7eb7c6573135272681253797374656d2e53746f726167652e507574616a52c36a0112c37c65f2e26a5bc37c65ebe26a011d527ac4681953797374656d2e53746f726167652e476574436f6e74657874616a011dc36a51c36a0112c3650ee77c6516135272681253797374656d2e53746f726167652e507574616a00c36539ed75681953797374656d2e53746f726167652e476574436f6e74657874616a57c36a00c37c6573e26a51c36a00c36589eb7c65c5125272681253797374656d2e53746f726167652e50757461681953797374656d2e53746f726167652e476574436f6e74657874616a55c37c681253797374656d2e53746f726167652e476574616a011e527ac4656cec6a011f527ac46a0117c36a011fc37c659a116a060527ac4681953797374656d2e53746f726167652e476574436f6e74657874616a55c36a060c36a011ec37c652d125272681253797374656d2e53746f726167652e507574610862757950617065726a00c36a0113c36a51c3681653797374656d2e52756e74696d652e47657454696d656155c176c9681553797374656d2e52756e74696d652e4e6f7469667961516c7566014cc56b0247316a00527ac4034730336a51527ac4034730376a52527ac4034730396a53527ac4034731306a54527ac4035530316a55527ac4035230356a56527ac4035230366a57527ac4065374617475736a58527ac40752554e4e494e476a59527ac403454e446a5a527ac45a6a5b527ac4556a5c527ac422415166344d7a7531594a72687a39663361526b6b77536d396e3371685847536834707514616f2a4a38396ff203ea01e6c070ae421bb8ce2d6a5d527ac46a5dc36537117565c1ea6a5e527ac46a5ec3640a00652007656a1175616567ea6a5f527ac4681653797374656d2e52756e74696d652e47657454696d656165e2e9013c94a0653d11756a5fc3651fe56a59c39c652f11756a00c36a5fc37c6553e06a56c37c654ce06a60527ac4681953797374656d2e53746f726167652e476574436f6e74657874616a60c37c681253797374656d2e53746f726167652e476574616a0111527ac46a0111c3642d006a0111c3681a53797374656d2e52756e74696d652e446573657269616c697a65616a0112527ac4627b0061681953797374656d2e53746f726167652e476574436f6e74657874616a00c36a5fc37c65b4df6a58c37c65addf6a5ac35272681253797374656d2e53746f726167652e5075746108656e64526f756e646a5fc352c176c9681553797374656d2e52756e74696d652e4e6f746966796165790a75516c7566610210276a0113527ac40210276a0114527ac465fce06a0115527ac4006a012a527ac46a0112c3c06a012b527ac4616a012ac36a012bc39f6453006a0112c36a012ac3c36a0116527ac46a012ac351936a012a527ac46a0116c36a0115c37c65ff0e6a0117527ac46a0117c36a0113c39f64bdff6a0117c36a0113527ac46a0116c36a0114527ac462a6ff6161616a00c36a5fc37c65cbde6a57c36a0114c37c65c0de7c65bcde6a0118527ac4681953797374656d2e53746f726167652e476574436f6e74657874616a0118c37c681253797374656d2e53746f726167652e476574616a0119527ac46a0119c3681a53797374656d2e52756e74696d652e446573657269616c697a65616a011a527ac4006a011b527ac4006a012c527ac46a011ac3c06a012d527ac4616a012cc36a012dc39f6436006a011ac36a012cc3c36a011c527ac46a012cc351936a012c527ac46a011bc36a011cc36526e77c65620e6a011b527ac462c3ff6161616a5fc3656ce36a011d527ac4006a011e527ac4006a012e527ac46a011ac3c06a012f527ac4616a012ec36a012fc39f646016a011ac36a012ec3c36a011c527ac46a012ec351936a012e527ac46a011cc365c2e66a011f527ac46a011dc36a011fc37c65540d6a011bc37c65240d6a060527ac46a060c30164956a011cc36544e6966a0121527ac4006a0122527ac46a0121c30164a0641d006a060c36a5bc37c65150d01647c65e70c6a0122527ac4621b00616a060c36a5cc37c65fa0c01647c65cc0c6a0122527ac4616a060c36a0122c37c655b0d6a0123527ac46a011ec36a0123c37c656b0d6a011e527ac4681953797374656d2e53746f726167652e476574436f6e74657874616a54c36a011cc37c65dfdc6a0123c36a011cc365eae37c652f0d5272681253797374656d2e53746f726167652e5075746162e7fe6161616a011dc36a011ec37c65e40c6a0124527ac4681953797374656d2e53746f726167652e476574436f6e74657874616a52c36a5dc37c657bdc6a0124c36a5dc365d7e37c65cc0c5272681253797374656d2e53746f726167652e50757461006a0130527ac46a0112c3c06a0131527ac4616a0130c36a0131c39f64f6016a0112c36a0130c3c36a0116527ac46a0130c351936a0130527ac46a00c36a5fc37c6512dc6a57c36a0116c37c6507dc7c6503dc6a0125527ac4681953797374656d2e53746f726167652e476574436f6e74657874616a0125c37c681253797374656d2e53746f726167652e476574616a0126527ac46a0126c3681a53797374656d2e52756e74696d652e446573657269616c697a65616a0127527ac4006a0132527ac46a0127c3c06a0133527ac4616a0132c36a0133c39f6434016a0127c36a0132c3c36a0128527ac46a0132c351936a0132527ac46a0128c36a5fc37c652fe164cdff6a0128c365eae575681953797374656d2e53746f726167652e476574436f6e74657874616a53c36a0128c37c6523db6a0128c3653be46a0128c36a5fc37c65ebe07c654a0b5272681253797374656d2e53746f726167652e507574616a00c36a5fc37c65ecda6a55c36a0128c37c65e1da7c65ddda6a0129527ac40c64657374726f7950617065726a0128c36a0128c36a5fc37c6595e0681653797374656d2e52756e74696d652e47657454696d656154c176c9681553797374656d2e52756e74696d652e4e6f7469667961681953797374656d2e53746f726167652e476574436f6e74657874616a0129c37c681553797374656d2e53746f726167652e44656c6574656162c5fe6161616203fe616161681953797374656d2e53746f726167652e476574436f6e74657874616a51c3657ae46a5fc36505de7c65520a5272681253797374656d2e53746f726167652e50757461681953797374656d2e53746f726167652e476574436f6e74657874616a00c36a5fc37c65d8d96a58c37c65d1d96a5ac35272681253797374656d2e53746f726167652e5075746108656e64526f756e646a5fc36a0115c36a011ac354c176c9681553797374656d2e52756e74696d652e4e6f746966796165950475516c756658c56b034730326a00527ac422415166344d7a7531594a72687a39663361526b6b77536d396e3371685847536834707514616f2a4a38396ff203ea01e6c070ae421bb8ce2d6a51527ac46a51c365b809756a51c3653fe37c653ed965f20975681953797374656d2e53746f726167652e476574436f6e74657874616a00c37c681553797374656d2e53746f726167652e44656c65746561516c756658c56b6a00527ac422415166344d7a7531594a72687a39663361526b6b77536d396e3371685847536834707514616f2a4a38396ff203ea01e6c070ae421bb8ce2d6a51527ac46a51c365210975006a53527ac46a00c3c06a54527ac4616a53c36a54c39f642e006a00c36a53c3c36a52527ac46a53c351936a53527ac46a52c300c36a52c351c37c6511006527097562cdff616161516c75660111c56b6a00527ac46a51527ac40247316a52527ac4034730336a53527ac4034730396a54527ac4035230336a55527ac422415166344d7a7531594a72687a39663361526b6b77536d396e3371685847536834707514616f2a4a38396ff203ea01e6c070ae421bb8ce2d6a56527ac46a56c3655f08756a54c36a00c37c65cbd76a57527ac4681953797374656d2e53746f726167652e476574436f6e74657874616a57c36a51c36a00c365bde07c65f9075272681253797374656d2e53746f726167652e50757461681953797374656d2e53746f726167652e476574436f6e74657874616a53c36a51c365b9e17c65b9075272681253797374656d2e53746f726167652e507574616513e16a58527ac4681953797374656d2e53746f726167652e476574436f6e74657874616a52c36a58c37c6515d76a55c37c650ed76a51c36a58c36558db7c6560075272681253797374656d2e53746f726167652e507574610b61737369676e50617065726a00c36a51c3681653797374656d2e52756e74696d652e47657454696d656154c176c9681553797374656d2e52756e74696d652e4e6f7469667961516c75665cc56b6a00527ac4034731336a51527ac422415166344d7a7531594a72687a39663361526b6b77536d396e3371685847536834707514616f2a4a38396ff203ea01e6c070ae421bb8ce2d6a52527ac46a52c365d30675006a54527ac46a00c3c06a55527ac4616a54c36a55c39f6481006a00c36a54c3c36a53527ac46a54c351936a54527ac46a53c300c365cb06756a53c351c365c206756a53c300c36a53c351c39e65ca0675681953797374656d2e53746f726167652e476574436f6e74657874616a51c36a53c300c37c65d0d56a53c351c35272681253797374656d2e53746f726167652e50757461627aff616161516c75665cc56b6a00527ac46a51527ac4034731336a52527ac422415166344d7a7531594a72687a39663361526b6b77536d396e3371685847536834707514616f2a4a38396ff203ea01e6c070ae421bb8ce2d6a53527ac46a53c365d905756a00c3650306756a51c365fc05756a00c36a51c39e65080675681953797374656d2e53746f726167652e476574436f6e74657874616a52c36a00c37c6510d56a51c35272681253797374656d2e53746f726167652e50757461516c75660118c56b0247316a00527ac4034730346a51527ac4034730356a52527ac4035230316a53527ac4035230326a54527ac4065374617475736a55527ac40752554e4e494e476a56527ac40400ca9a3b6a57527ac422415166344d7a7531594a72687a39663361526b6b77536d396e3371685847536834707514616f2a4a38396ff203ea01e6c070ae421bb8ce2d6a58527ac46a58c3681b53797374656d2e52756e74696d652e436865636b5769746e65737361650e0575650cde6a59527ac46a59c351936a5a527ac46a59c3009e64a2006a00c36a59c37c6518d46a54c37c6511d46a5b527ac4681953797374656d2e53746f726167652e476574436f6e74657874616a5bc37c681253797374656d2e53746f726167652e476574616a5c527ac46a00c36a5ac37c65c8d36a53c37c65c1d36a5d527ac4681953797374656d2e53746f726167652e476574436f6e74657874616a5dc36a5cc35272681253797374656d2e53746f726167652e5075746161681953797374656d2e53746f726167652e476574436f6e74657874616a00c36a5ac37c655cd36a55c37c6555d36a56c35272681253797374656d2e53746f726167652e50757461681953797374656d2e53746f726167652e476574436f6e74657874616a51c36a5ac35272681253797374656d2e53746f726167652e50757461681953797374656d2e53746f726167652e476574436f6e74657874616a52c36a57c35272681253797374656d2e53746f726167652e507574610a7374617274526f756e646a5ac352c176c9681553797374656d2e52756e74696d652e4e6f7469667961516c75665cc56b0b496e697469616c697a65646a00527ac422415166344d7a7531594a72687a39663361526b6b77536d396e3371685847536834707514616f2a4a38396ff203ea01e6c070ae421bb8ce2d6a51527ac46a51c365cc0275681953797374656d2e53746f726167652e476574436f6e74657874616a00c37c681253797374656d2e53746f726167652e476574616a52527ac46a52c36452002e6964696f742061646d696e2c20796f75206861766520696e697469616c697a65642074686520636f6e747261637451c176c9681553797374656d2e52756e74696d652e4e6f7469667961006c756661681953797374656d2e53746f726167652e476574436f6e74657874616a00c3515272681253797374656d2e53746f726167652e5075746121496e697469616c697a656420636f6e7472616374207375636365737366756c6c7951c176c9681553797374656d2e52756e74696d652e4e6f7469667961516c756659c56b6a00527ac46a00c3517c658801527c65bf006a51527ac46a00c36a52527ac461616a51c36a52c39f6429006a51c36a52527ac46a00c36a51c37c6594006a51c37c655101527c6588006a51527ac462d2ff6161616a51c36c75665fc56b6a00527ac46a51527ac4006a52527ac46a00c3009c640c00006a52527ac4624c00616a51c3009c640c00516a52527ac4623a0061006a53527ac4516a52527ac461616a53c36a51c39f641f006a52c36a00c37c6546006a52527ac46a53c351936a53527ac462dcff6161616a52c36c756657c56b6a00527ac46a51527ac46a51c300a0652401756a00c36a51c3966a52527ac46a52c36c756659c56b6a00527ac46a51527ac46a00c3009c640700006c7566616a00c36a51c3956a52527ac46a52c36a00c3966a51c39c65dd00756a52c36c756659c56b6a00527ac46a51527ac46a00c36a51c3a0640d006a00c36a51c3946c7566616a00c36a51c39f640d006a51c36a00c3946c756661006c7566006c756656c56b6a00527ac46a51527ac46a00c36a51c3a2658000756a00c36a51c3946c756657c56b6a00527ac46a51527ac46a00c36a51c3936a52527ac46a52c36a00c3a2655200756a52c36c756655c56b6a00527ac46a00c3681b53797374656d2e52756e74696d652e436865636b5769746e65737361651f0075516c756655c56b6a00527ac46a00c3c001149c65080075516c756656c56b6a00527ac46a00c36307006509007561516c756653c56b09f4f4f3f3f2f2f1f100f0006c75665ec56b6a00527ac46a51527ac46a51c36a00c3946a52527ac46a52c3c56a53527ac4006a54527ac46a00c36a55527ac461616a00c36a51c39f6433006a54c36a55c3936a56527ac46a56c36a53c36a54c37bc46a54c351936a54527ac46a55c36a54c3936a00527ac462c8ff6161616a53c36c7566"
        needStorage = "True"
        name = "testName"
        version = "2.0"
        author = "testAuthor"
        email = "testEmail"
        description = "testDescription"
        param_list = []
        param_list.append("migrateContrat".encode())
        param_list1 = [bytearray.fromhex(code)]
        param_list1.append(str(needStorage).encode())
        param_list1.append(name.encode())
        param_list1.append(version.encode())
        param_list1.append(author.encode())
        param_list1.append(email.encode())
        param_list1.append(description.encode())
        param_list.append(param_list1)

        # print("*****\n", param_list)
        params = BuildParams.create_code_params_script(param_list)

        # unix_time_now = int(time.time())
        # tx = Transaction(0, 0xd1, unix_time_now, 500, 20000, payerAcct.get_address().to_array(), params, bytearray(), [], bytearray())
        # sdk.sign_transaction(tx, payerAcct)
        # nil, gaslimit = sdk.rpc.send_raw_transaction_pre_exec(tx)
        # print("gasLimit1 in buy paper is ", gaslimit, type(gaslimit))

        tx = NeoVm.make_invoke_transaction(bytearray(contract_address), bytearray(params), b'', 0, 0)
        sdk.sign_transaction(tx, adminAcct)
        nil, gaslimit = sdk.rpc.send_raw_transaction_pre_exec(tx)
        # print("gasLimit2 in buy paper is ", gaslimit, type(gaslimit))
        # gaslimit = 2000000

        params.append(0x67)
        for i in contract_address:
            params.append(i)

        gaslimit = gaslimit * 2
        unix_time_now = int(time.time())
        tx = Transaction(0, 0xd1, unix_time_now, 500, gaslimit, adminAcct.get_address().to_array(), params, bytearray(), [], bytearray())
        sdk.sign_transaction(tx, adminAcct)
        hash = sdk.rpc.send_raw_transaction(tx)
        time.sleep(6)
        res = sdk.rpc.get_smart_contract_event_by_tx_hash(hash)
        print("buyPaper-res is ", res)
        events = res["Notify"]
        print("buyPaper-res-events is ", events)

        return True


    def test_getCurrentRound(self):
        param_list = []
        # when pre-execute, don't use 0x67
        abi_function = AbiFunction("getCurrentRound", "", param_list)
        res, nil = sdk.neo_vm().send_transaction(contract_address, adminAcct, adminAcct, 0, 0, abi_function, True)
        # print("getCurrentRound-res is ", res)
        tmp = str(res)
        if not tmp:
            tmp = "0"
        tmp = bytearray.fromhex(tmp)
        tmp.reverse()
        returnedInt = int(tmp.hex(), 16)
        print("test-getCurrentRound is ", returnedInt)
        return returnedInt

    def test_getTotalPaper(self):
        param_list = []
        # when pre-execute, don't use 0x67
        abi_function = AbiFunction("getTotalPaper", "", param_list)
        res, nil = sdk.neo_vm().send_transaction(contract_address, adminAcct, adminAcct, 0, 0, abi_function, True)
        print("getTotalPaper-res is ", res)
        tmp = res
        if not tmp:
            tmp = "00"
        else:
            tmp = res
        tmp = bytearray.fromhex(tmp)
        tmp.reverse()
        returnedInt = int(tmp.hex(), 16)
        print("test-getTotalPaper is ", returnedInt)
        return True
    def test_getGameStatus(self):

        roundNum = self.test_getCurrentRound()
        abi_function = AbiFunction("getGameStatus", "", [{"name": "roundNum", "type": ""}])
        abi_function.set_params_value((roundNum,))
        res, nil = sdk.neo_vm().send_transaction(contract_address, adminAcct, adminAcct, 0, 0, abi_function, True)
        status = (bytearray.fromhex(res)).decode('utf-8')
        print("test-getGameStatus is : ", status, " in round ", roundNum)
        return True

    def test_GetTotalPaper(self):
        roundNum = self.test_getCurrentRound()
        filledPaperAmount = self.test_getFilledPaperAmount(roundNum)
        print("test-getFilledPaperAmount is ", filledPaperAmount, " in round ", roundNum)

    def test_getFilledPaperAmount(self, roundNum):
        # roundNum = self.test_getCurrentRound()
        abi_function = AbiFunction("getFilledPaperAmount", "", [{"name": "roundNum", "type": ""}])
        abi_function.set_params_value((roundNum,))
        res,nil = sdk.neo_vm().send_transaction(contract_address, adminAcct, adminAcct, 0, 0, abi_function, True)
        tmp = res
        if not tmp:
            tmp = "00"
        tmp = bytearray.fromhex(tmp)
        tmp.reverse()
        returnedInt = int(tmp.hex(), 16)
        # print("test-getFilledPaperAmount is ", returnedInt, " in round ", roundNum)
        return returnedInt

    def test_getPaperBalance(self, account):
        abi_function = AbiFunction("getPaperBalance", "", [{"name": "account", "type": ""}])
        abi_function.set_params_value((account.get_address().to_array(),))
        res, nil = sdk.neo_vm().send_transaction(contract_address, adminAcct, adminAcct, 0, 0, abi_function, True)
        tmp = res
        if not tmp:
            tmp = "00"
        tmp = bytearray.fromhex(tmp)
        tmp.reverse()
        returnedInt = int(tmp.hex(), 16)
        return returnedInt

    def test_getFilledPaperBalance(self, account, roundNum):
        # roundNum = self.test_getCurrentRound()
        abi_function = AbiFunction("getFilledPaperBalance", "", [{"name": "account", "type": ""}, {"name": "roundNum", "type": ""}])
        abi_function.set_params_value((account.get_address().to_array(),roundNum,))
        res,nil = sdk.neo_vm().send_transaction(contract_address, adminAcct, adminAcct, 0, 0, abi_function, True)
        tmp = res
        if not tmp:
            tmp = "00"
        tmp = bytearray.fromhex(tmp)
        tmp.reverse()
        returnedInt = int(tmp.hex(), 16)
        # print("test-getFilledPaperAmount is ", returnedInt, " in round ", roundNum)
        return returnedInt
    def test_getDividendsBalance(self):
        account = adminAcct2
        abi_function = AbiFunction("getDividendsBalance", "", [{"name": "account", "type": ""}])
        abi_function.set_params_value((account.get_address().to_array(),))
        res, nil = sdk.neo_vm().send_transaction(contract_address, adminAcct, adminAcct, 0, 0, abi_function, True)
        print("res is ", res)
        tmp = res
    def test_getReferralBalance(self):
        account = adminAcct
        abi_function = AbiFunction("getReferralBalance", "", [{"name": "account", "type": ""}])
        abi_function.set_params_value((account.get_address().to_array(),))
        res, nil = sdk.neo_vm().send_transaction(contract_address, adminAcct, adminAcct, 0, 0, abi_function, True)
        print("res is ", res)
        tmp = res
    def test_getDividendBalance(self):
        account = adminAcct
        abi_function = AbiFunction("getDividendBalance", "", [{"name": "account", "type": ""}])
        abi_function.set_params_value((account.get_address().to_array(),))
        res, nil = sdk.neo_vm().send_transaction(contract_address, adminAcct, adminAcct, 0, 0, abi_function, True)
        print("res is ", res)
        tmp = res
    def test_getAwardBalance(self):
        account = adminAcct
        abi_function = AbiFunction("getAwardBalance", "", [{"name": "account", "type": ""}])
        abi_function.set_params_value((account.get_address().to_array(),))
        res, nil = sdk.neo_vm().send_transaction(contract_address, adminAcct, adminAcct, 0, 0, abi_function, True)
        print("res is ", res)
        tmp = res
    def test_withdraw(self):
        account = adminAcct
        abi_function = AbiFunction("withdraw", "", [{"name": "account", "type": ""}])
        abi_function.set_params_value((account.get_address().to_array(),))
        hash = sdk.neo_vm().send_transaction(contract_address, account, account, 200000, 500, abi_function, False)
        time.sleep(6)
        res = sdk.rpc.get_smart_contract_event_by_tx_hash(hash)
        print("withraw-res is ", res)
        return True

    def test_getWinInfo(self):
        currentRound = self.test_getCurrentRound()
        roundNum = self.test_getCurrentRound() - 1
        abi_function = AbiFunction("getWinInfo", "", [{"name": "roundNum", "type": ""}])
        abi_function.set_params_value((roundNum,))
        res, nil = sdk.neo_vm().send_transaction(contract_address, adminAcct, adminAcct, 0, 0, abi_function, True)
        print("test-getGameStatus is : ", res, " in round ", roundNum)
        return True











    def test_transferONG(self, fromAcct, toAcct, ongAmount):

        fromAddr = fromAcct.get_address_base58()
        toAddr = toAcct.get_address_base58()
        asset = "ong"
        ass = Asset(sdk)
        payerAddr = fromAddr
        gaslimit = 20000000
        gasprice = 500
        tx = ass.new_transfer_transaction(asset, fromAddr, toAddr, ongAmount, payerAddr, gaslimit, gasprice)
        sdk.sign_transaction(tx, fromAcct)
        res = sdk.rpc.send_raw_transaction(tx)
        # time.sleep(6)
        # print("res in test_transfer_Ont is ", res)
        return True
    def test_getONGBalance(self, address):
        balances = sdk.rpc.get_balance(address)
        ongBalance = balances["ong"]
        ongBalance = int(ongBalance)
        return ongBalance

    def test_getCurrentRound2(self):
        contract_address_str = luckyNumberContractAddress
        contract_address_bytearray = bytearray.fromhex(contract_address_str)
        contract_address = contract_address_bytearray
        contract_address.reverse()
        params_list = []
        params_list.append(str("getCurrentRound").encode())
        param = []
        params_list.append(param)
        params = BuildParams.create_code_params_script(params_list)
        # when pre-execute, don't use 0x67
        tx = NeoVm.make_invoke_transaction(bytearray(contract_address), bytearray(params), b'', 20000000, 0)
        res = sdk.rpc.send_raw_transaction_pre_exec(tx)
        returnedHexString = res['result']["Result"]
        tmp = returnedHexString
        if not tmp:
            tmp = "00"
        else:
            tmp = returnedHexString
        tmp = bytearray.fromhex(tmp)
        tmp.reverse()
        returnedInt = int(tmp.hex(), 16)
        print("test-getCurrentRound is ", returnedInt)
        return True