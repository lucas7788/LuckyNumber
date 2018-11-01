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
from ontology.smart_contract.neo_vm import NeoVm
import requests
import re
import random
from ontology.smart_contract.neo_contract.abi.abi_function import AbiFunction
rpc_address = "http://127.0.0.1:20336"
# rpc_address = "http://polaris3.ont.io:20336"
# rpc_address = "http://139.219.139.170:20336"
sdk = OntologySdk()
sdk.set_rpc((rpc_address))
from datetime import datetime


luckyNumberContractAddress = "a737692944454552e4bdf37d66a005f10d2ffe02"

# luckyNumberContractAddress = "38a8e857112eec18a2c02d1c83739f671779163d"

contract_address_str = luckyNumberContractAddress
contract_address_bytearray = bytearray.fromhex(contract_address_str)
contract_address = contract_address_bytearray
contract_address.reverse()

wallet_path = "C:\\Go_WorkSpace\\src\\github.com\\ontio\\ontology\\_Wallet_\\wallet.dat"
# wallet_path = "D:\\SmartX_accounts\\Cyano Wallet\\lucknumberAccount\\wallet.dat"
sdk.wallet_manager.open_wallet(wallet_path)
admin_addr = "AQf4Mzu1YJrhz9f3aRkkwSm9n3qhXGSh4p"
admin_pwd = "xinhao"
pwd = admin_pwd
# admin_addr = "AYqCVffRcbPkf1BVCYPJqqoiFTFmvwYKhG"
# admin_pwd = "111111"
adminAcct = sdk.wallet_manager.get_account(admin_addr, admin_pwd)
payerAcct = sdk.wallet_manager.get_account("AUnhXaudVSBFqjH92a6HrhQySUTiQjf5VR", pwd)

accountNum = 2
accountAvgPaperNum = 10
accountAvgFillPaperNum = 5



class TestAsset(unittest.TestCase):

    def test_init(self):
        param_list = []
        # when pre-execute, don't use 0x67
        abi_function = AbiFunction("init", "",param_list)
        hash = sdk.neo_vm().send_transaction(contract_address, adminAcct, payerAcct, 20000, 500, abi_function, False)
        # res = sdk.rpc.send_raw_transaction(tx)
        time.sleep(7)
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
        hash = sdk.neo_vm().send_transaction(contract_address, adminAcct, payerAcct, 200000, 500, abi_function, False)
        # res = sdk.rpc.send_raw_transaction(tx)
        time.sleep(7)
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
        param_list = []
        # when pre-execute, don't use 0x67
        abi_function = AbiFunction("endCurrentRound", "", param_list)
        hash = sdk.neo_vm().send_transaction(contract_address, adminAcct, payerAcct, 2141780, 500, abi_function, False)
        # res = sdk.rpc.send_raw_transaction(tx)
        time.sleep(7)
        res = sdk.rpc.get_smart_contract_event_by_tx_hash(hash)
        # print("endCurrentRound-res is ", res)
        events = res["Notify"]
        notifyContents = []
        i = 1
        for event in events:
            notifyContent = []
            if event["ContractAddress"] == luckyNumberContractAddress:
                action = (bytearray.fromhex(event["States"][0])).decode('utf-8')
                notifyContent.append(action)
                if action == "endRound":
                    tmp = str(event["States"][1])
                    if not tmp:
                        tmp = "0"
                    tmp = bytearray.fromhex(tmp)
                    tmp.reverse()
                    roundNumber = int(tmp.hex(), 16)
                    notifyContent.append(roundNumber)
                    # print("endCurrentRound-res-event is : ", notifyContent)
                elif action == "destroyPaper":
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
                print("<",i, ">", " -- endCurrentRound-res-event is : ", notifyContent)
                i = i + 1
            notifyContents.append(notifyContent)
        print("endCurrentRound-res-events is : ", notifyContents)
        consumedONG = res["GasConsumed"]
        print("endCurrentRound-consume-ong-amount is : ", consumedONG/ 10 ** 9, " ONG")
        return True

    def test_withdrawGas(self):
        param_list = []
        abi_function = AbiFunction("withdrawGas", "", param_list)
        hash = sdk.neo_vm().send_transaction(contract_address, adminAcct, payerAcct, 200000, 500, abi_function, False)
        time.sleep(7)
        res = sdk.rpc.get_smart_contract_event_by_tx_hash(hash)
        print("withrawGas-res is ", res)
        return True


    def test_buyPapers(self):
        # self.test_buyPaper(adminAcct, 2)
        # self.test_fillPaper(adminAcct, 2)
        # # return True

        wm = sdk.wallet_manager.open_wallet(wallet_path)
        fakeAccountList = wm.get_accounts()
        accountList = []
        addressList = []
        for fakeAccount in fakeAccountList:
            # print("\naccountList", fakeAccount.get_address())
            base58Address = fakeAccount.get_address()
            addressList.append(base58Address)
            account = sdk.wallet_manager.get_account(base58Address, pwd)
            # print("\naccountList base58 address", account.get_address_base58())
            accountList.append(account)
        accountListToBeUsed = accountList[1:50]
        # transfer ONG to account 2 -> account 11, with ongAmount = 100000000000
        for account in accountListToBeUsed :
            balance = self.test_getONGBalance(account.get_address_base58())
            if balance < 10000000000000:
                self.test_transferONG(accountList[0], account, 10000000000000-balance)
                time.sleep(7)
            print("Balance -- ", account.get_address_base58(), " -- ", self.test_getONGBalance(account.get_address_base58()))
        # return True
        for account in accountListToBeUsed:
            # print("\naccount base58 address", account.get_address_base58())
            print("********************")
            self.test_buyPaper(account, 100)
            self.test_fillPaper(account, 100)
        self.test_getFilledPaperAmount()
        self.test_getTotalPaper()
        self.test_endCurrentRound()
        return True


    def test_buyPaper(self, invokeAcct, paperAmount):
        # payerAcct = invokeAcct
        # param_list = []
        # invokeAddr = invokeAcct.get_address().to_array()
        # param_list.append(invokeAddr)
        # # paperAmount = 1
        # param_list.append(paperAmount)
        # abi_function = AbiFunction("buyPaper", "", [{"name": "account", "type": ""},{"name":"paperAmount", "type":""}])
        # # abi_function.set_params_value((adminAcct.get_address().to_array(), 1))
        # abi_function.set_params_value(param_list)
        # hash = sdk.neo_vm().send_transaction(contract_address, invokeAcct, payerAcct, 200000, 500, abi_function, False)
        # time.sleep(7)
        # res = sdk.rpc.get_smart_contract_event_by_tx_hash(hash)

        payerAcct = invokeAcct
        param_list = []
        param_list.append("buyPaper".encode())
        param_list1 = []
        param_list1.append(invokeAcct.get_address().to_array())
        param_list1.append(paperAmount)
        param_list.append(param_list1)

        # print("*****\n", param_list)
        params = BuildParams.create_code_params_script(param_list)
        params.append(0x67)
        for i in contract_address:
            params.append(i)
        unix_time_now = int(time.time())
        tx = Transaction(0, 0xd1, unix_time_now, 500, 20000, payerAcct.get_address().to_array(), params, bytearray(), [], bytearray())
        sdk.sign_transaction(tx, payerAcct)
        nil, gaslimit = sdk.rpc.send_raw_transaction_pre_exec(tx)
        # print("gasLimit in buy paper is ", gaslimit, type(gaslimit))

        gaslimit = gaslimit + 100
        unix_time_now = int(time.time())
        tx = Transaction(0, 0xd1, unix_time_now, 500, gaslimit, payerAcct.get_address().to_array(), params, bytearray(), [], bytearray())
        sdk.sign_transaction(tx, payerAcct)
        hash = sdk.rpc.send_raw_transaction(tx)
        time.sleep(7)
        res = sdk.rpc.get_smart_contract_event_by_tx_hash(hash)
        # print("buyPaper-res is ", res)
        events = res["Notify"]
        # print("buyPaper-res-events is ", events)
        notifyContent = []
        for event in events:
            if event["ContractAddress"] == luckyNumberContractAddress:
                action = (bytearray.fromhex(event["States"][0])).decode('utf-8')
                notifyContent.append(action)

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
        print("buyPaper-res-event is : ", notifyContent)
        return True

    def test_fillPaper(self, fillAcct, fillAmount):
        payerAcct = fillAcct
        param_list = []
        fillAddr = fillAcct.get_address().to_array()

        param_list = list()
        param_list.append("fillPaper".encode())
        param_list1 = list()
        param_list1.append(fillAddr)
        param_list2 = []
        for i in range(fillAmount):
            randNum = random.randint(0, 9999)
            if randNum not in param_list:
                param_list2.append(randNum)
        param_list1.append(param_list2)
        param_list.append(param_list1)
        # print("*****\n", param_list)
        params = BuildParams.create_code_params_script(param_list)
        params.append(0x67)
        for i in contract_address:
            params.append(i)
        unix_time_now = int(time.time())
        tx = Transaction(0, 0xd1, unix_time_now, 500, 200000, payerAcct.get_address().to_array(), params, bytearray(), [], bytearray())
        sdk.sign_transaction(tx, payerAcct)
        nouse, gaslimit = sdk.rpc.send_raw_transaction_pre_exec(tx)

        tx = Transaction(0, 0xd1, unix_time_now, 500, gaslimit + 100, payerAcct.get_address().to_array(), params, bytearray(), [], bytearray())
        sdk.sign_transaction(tx, payerAcct)
        hash = sdk.rpc.send_raw_transaction(tx)

        time.sleep(7)
        res = sdk.rpc.get_smart_contract_event_by_tx_hash(hash)
        # print("fillPaper-res is ", res)
        events = res["Notify"]

        # print("fillPaper-res-events is ", events)
        # return True
        notifyContent = []
        for event in events:
            if event["ContractAddress"] == luckyNumberContractAddress:
                action = (bytearray.fromhex(event["States"][0])).decode('utf-8')
                notifyContent.append(action)

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
        print("fillPaper-res-event is : ", notifyContent)
        return True

    def test_getCurrentRound(self):
        param_list = []
        # when pre-execute, don't use 0x67
        abi_function = AbiFunction("getCurrentRound", "", param_list)
        res, nil = sdk.neo_vm().send_transaction(contract_address, adminAcct, payerAcct, 0, 0, abi_function, True)
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
        res, nil = sdk.neo_vm().send_transaction(contract_address, adminAcct, payerAcct, 0, 0, abi_function, True)
        # print("getTotalPaper-res is ", res)
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
    def test_getFilledPaperAmount(self):
        roundNum = self.test_getCurrentRound()
        abi_function = AbiFunction("getFilledPaperAmount", "", [{"name": "roundNum", "type": ""}])
        abi_function.set_params_value([roundNum])
        res,nil = sdk.neo_vm().send_transaction(contract_address, adminAcct, payerAcct, 0, 0, abi_function, True)
        tmp = res
        if not tmp:
            tmp = "00"
        tmp = bytearray.fromhex(tmp)
        tmp.reverse()
        returnedInt = int(tmp.hex(), 16)
        print("test-getFilledPaperAmount is ", returnedInt, " in round ", roundNum)
        return returnedInt















    def test_transferONG(self, fromAcct, toAcct, ongAmount):

        fromAddr = fromAcct.get_address_base58()
        toAddr = toAcct.get_address_base58()
        asset = "ong"
        ass = Asset(sdk)
        payerAddr = fromAddr
        gaslimit = 20000
        gasprice = 500
        tx = ass.new_transfer_transaction(asset, fromAddr, toAddr, ongAmount, payerAddr, gaslimit, gasprice)
        sdk.sign_transaction(tx, fromAcct)
        res = sdk.rpc.send_raw_transaction(tx)
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