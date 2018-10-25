'''
Lucky Number Game
'''
from boa.interop.System.Storage import GetContext, Get, Put, Delete
from boa.interop.System.Runtime import CheckWitness, GetTime, Notify, Serialize, Deserialize
from boa.interop.System.ExecutionEngine import GetExecutingScriptHash
from boa.interop.Ontology.Native import Invoke
from boa.interop.Ontology.Runtime import GetRandomHash
from boa.interop.System.Blockchain import GetHeight, GetHeader, GetBlock
from boa.interop.System.Header import GetHash
from boa.builtins import ToScriptHash, concat, state
from boa.interop.System.Action import RegisterAction


"""
https://github.com/tonyclarking/python-template/blob/master/libs/Utils.py
"""
def Revert():
    """
    Revert the transaction. The opcodes of this function is `09f7f6f5f4f3f2f1f000f0`,
    but it will be changed to `ffffffffffffffffffffff` since opcode THROW doesn't
    work, so, revert by calling unused opcode.
    """
    raise Exception(0xF1F1F2F2F3F3F4F4)


"""
https://github.com/tonyclarking/python-template/blob/master/libs/SafeCheck.py
"""
def Require(condition):
    """
	If condition is not satisfied, return false
	:param condition: required condition
	:return: True or false
	"""
    if not condition:
        Revert()
    return True

def RequireScriptHash(key):
    """
    Checks the bytearray parameter is script hash or not. Script Hash
    length should be equal to 20.
    :param key: bytearray parameter to check script hash format.
    :return: True if script hash or revert the transaction.
    """
    Require(len(key) == 20)
    return True

def RequireWitness(witness):
    """
	Checks the transaction sender is equal to the witness. If not
	satisfying, revert the transaction.
	:param witness: required transaction sender
	:return: True if transaction sender or revert the transaction.
	"""
    Require(CheckWitness(witness))
    return True
"""
SafeMath 
"""

def Add(a, b):
	"""
	Adds two numbers, throws on overflow.
	"""
	c = a + b
	Require(c >= a)
	return c

def Sub(a, b):
	"""
	Substracts two numbers, throws on overflow (i.e. if subtrahend is greater than minuend).
    :param a: operand a
    :param b: operand b
    :return: a - b if a - b > 0 or revert the transaction.
	"""
	Require(a>=b)
	return a-b

def ASub(a, b):
    if a > b:
        return a - b
    if a < b:
        return b - a
    else:
        return 0

def Mul(a, b):
	"""
	Multiplies two numbers, throws on overflow.
    :param a: operand a
    :param b: operand b
    :return: a - b if a - b > 0 or revert the transaction.
	"""
	if a == 0:
		return 0
	c = a * b
	Require(c / a == b)
	return c

def Div(a, b):
	"""
	Integer division of two numbers, truncating the quotient.
	"""
	Require(b > 0)
	c = a / b
	return c

def Pwr(a, b):
    """
    a to the power of b
    :param a the base
    :param b the power value
    :return a^b
    """
    c = 0
    if a == 0:
        c = 0
    elif b == 0:
        c = 1
    else:
        i = 0
        c = 1
        while i < b:
            c = Mul(c, a)
            i = i + 1
    return c

def Sqrt(a):
    """
    Return sqrt of a
    :param a:
    :return: sqrt(a)
    """
    c = Div(Add(a, 1), 2)
    b = a
    while(c < b):
        b = c
        c = Div(Add(Div(a, c), c), 2)
    return c


######################### Global game info ########################
ROUND_PREFIX = 'round'
# GAS_VAULT_KEY -- store the fee for calculating the winner
GAS_VAULT_KEY = "GasVault"

TOTAL_PAPER = "TotalPaper"
# CURRET_ROUND_NUM_KEY -- store the current round number
CURRET_ROUND_NUM_KEY = 'CurrentRoundNumber'


PRICE_PER_PAPER = "PricePerPaper"

# PROFIT_PER_PAPER_KEY -- store the profit per paper (when it is bought)
PROFIT_PER_PAPER_KEY = "ProfitPerPaper"

# TOTAL_DIVIDEND_OF_PREFIX + account -- store the total accumulated dividend of account
# when user withdraws, the total dividend will go to ZERO
TOTAL_DIVIDEND_OF_PREFIX = "TotalDividend"
REFERRAL_BALANCE_OF_PREFIX = "ReferralBalance"
# PAPER_BALANCE_PREFIX + account -- store the current blank paper amount of account
PAPER_BALANCE_PREFIX = "PaperBalanceOf"
AWARD_BALANCE_OF_PREFFIX = "AwardOf"
# WITHDRAWN_BALANCEOF_PREFFIX + account -- store the asset value that has been withdrawn
WITHDRAWN_BALANCEOF_PREFFIX = "withdrawnOf"
INVEST_BALANCE_PREFFIX = "InvestAmount"
REFERRAL_PREFIX = "Referral"

# PROFIT_PER_PAPER_FROM_PREFIX + account -- store the filled paper amount in round i
PROFIT_PER_PAPER_FROM_PREFIX = "ProfitPerPaperFrom"


################## Round i User info ##################
# ROUND_PREFIX + CURRET_ROUND_NUM_KEY + FILLED_PAPER_BALANCE_PREFIX + account -- store the filled paper amount in round i
FILLED_PAPER_BALANCE_PREFIX = "FilledPaperBalanceOf"


# ROUND_PREFIX + CURRET_ROUND_NUM_KEY + ROUND_DIVIDEND_PREFIX + account -- store the filled paper amount in round i,
# when user withdraws, the dividend in round i will be cleared to ZERO
ROUND_DIVIDEND_PREFIX = "RoundDividendOf"


###################### Round i Public info ###########################
# ROUND_PREFIX + CURRET_ROUND_NUM_KEY + AWARD_VAULT_KEY -- store the total award for the winner in roung i
AWARD_VAULT_KEY = "AwardVault"

# ROUND_PREFIX + CURRET_ROUND_NUM_KEY + NEXT_VAULT_KEY -- store the asset for the next round in round i+1
NEXT_VAULT_KEY = "NextVault"


# ROUND_PREFIX + CURRET_ROUND_NUM_KEY + ROUND_PAPER_AMOUNT -- store the paper amount sold in this round
ROUND_PAPER_AMOUNT = "PaperAmount"

# ROUND_PREFIX + CURRET_ROUND_NUM_KEY + FILLED_PAPER_AMOUNT -- store the asset for the next round in round i+1
FILLED_PAPER_AMOUNT = "FilledPaperAmount"

# ROUND_PREFIX + CURRET_ROUND_NUM_KEY + FILLED_NUMBER_LIST_KEY -- store the filled number on papers
FILLED_NUMBER_LIST_KEY = "NumberList"

# ROUND_PREFIX + CURRET_ROUND_NUM_KEY + FILLED_NUMBER_KEY + number -- store the accounts that filled number
# key = ROUND_PREFIX + CURRET_ROUND_NUM_KEY + FILLED_NUMBER_KEY + number
# value = [account1, account2, account3]
FILLED_NUMBER_KEY = "FilledNumber"


############################### other info ###################################
INIIT = "Initialized"
ROUND_STATUS_KEY = "Status"
STATUS_ON = "RUNNING"
STATUS_OFF = "END"

InitialPrice = 1000000000
PriceIncremental = 9260
PaperHolderPercentage = 50
ReferralAwardPercentage = 1
AwardPercentage = 35
NextPercentage = 10


WinnerFeeLarge = 10
WinnerFeeSmall = 5


# the script hash of this contract
ContractAddress = GetExecutingScriptHash()
ONGAddress = bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02')
Admin = ToScriptHash('AQf4Mzu1YJrhz9f3aRkkwSm9n3qhXGSh4p')

# PurchaseEvent = RegisterAction("buy", "account", "ongAmount", "paperAmount")


def Main(operation, args):
    ######################## for Admin to invoke Begin ###############
    if operation == "init":
        # if len(args) != 0:
        #     return False
        return init()
    if operation == "startNewRound":
        # if len(args) != 0:
        #     return False
        return startNewRound()
    if operation =="addReferral":
        if len(args) != 2:
            return False
        toBeReferred = args[0]
        referral = args[1]
        return addReferral(toBeReferred, referral)
    if operation == "addMultiReferral":
        return addMultiReferral(args)
    if operation == "withdrawGas":
        # if len(args) != 0:
        #     return False
        return  withdrawGas()
    if operation == "endCurrentRound":
        # if len(args) != 0:
        #     return False
        return endCurrentRound()
    ######################## for Admin to invoke End ###############
    ######################## for User to invoke Begin ###############

    if operation == "buyPaper":
        if len(args) != 2:
            return False
        account = args[0]
        paperAmount = args[1]
        return buyPaper(account, paperAmount)
    if operation == "reinvest":
        if len(args) != 2:
            return False
        account = args[0]
        paperAmount = args[1]
        return reinvest(account, paperAmount)
    if operation == "fillPaper":
        if len(args) != 2:
            return False
        account = args[0]
        guessNumberList = args[1]
        return fillPaper(account, guessNumberList)
    if operation == "withdraw":
        if len(args) != 1:
            return False
        account = args[0]
        return withdraw(account)
    ######################## for User to invoke End ###############
    ######################### General Info to pre-execute Begin ##############
    if operation == "getTotalPaper":
        # if len(args) != 0:
        #     return False
        return getTotalPaper()
    if operation == "getGasVault":
        # if len(args) != 0:
        #     return False
        return getGasVault()

    if operation == "getCurrentRound":
        # if len(args) != 0:
        #     return False
        return getCurrentRound()
    if operation == "getCurrentPrice":
        # if len(args) != 0:
        #     return False
        return getCurrentPrice()
    if operation == "getPaperBalance":
        if len(args) != 1:
            return False
        account = args[0]
        return getPaperBalance(account)
    if operation == "getInvestOngBalance":
        if len(args) != 1:
            return False
        account = args[0]
        return getInvestOngBalance(account)
    if operation == "getReferralBalance":
        if len(args) != 1:
            return False
        account = args[0]
        return getReferralBalance(account)
    if operation == "getDividendBalance":
        if len(args) != 1:
            return False
        account = args[0]
        return getDividendBalance(account)
    if operation == "getAwardBalance":
        if len(args) != 1:
            return False
        account = args[0]
        return getAwardBalance(account)
    if operation == "getWithdrawnBalance":
        if len(args) != 1:
            return False
        account = args[0]
        return getWithdrawnBalance(account)
    if operation == "getReferral":
        if len(args) != 1:
            return False
        account = args[0]
        return getReferral(account)
    if operation == "getAwardVault":
        if len(args) != 1:
            return False
        currentRound = args[0]
        return getAwardVault(currentRound)
    if operation == "getNextVault":
        if len(args) != 1:
            return False
        currentRound = args[0]
        return getNextVault(currentRound)
    if operation == "getGameStatus":
        if len(args) != 1:
            return False
        currentRound = args[0]
        return getGameStatus(currentRound)
    if operation == "getRoundSoldPaperAmount":
        if len(args) != 1:
            return False
        currentRound = args[0]
        return getRoundSoldPaperAmount(currentRound)
    if operation == "getFilledPaperAmount":
        if len(args) != 1:
            return False
        currentRound = args[0]
        return getFilledPaperAmount(currentRound)
    ######################### General Info to pre-execute Begin ##############


    ######################### For testing purchase Begin ##############
    if operation == "updateDividendBalance":
        if len(args) != 1:
            return False
        account = args[0]
        return updateDividendBalance(account)
    if operation == "getFilledPaperBalance":
        if len(args) != 2:
            return False
        account = args[0]
        currentRound = args[1]
        return getFilledPaperBalance(account, currentRound)
    if operation == "getLuckyNumber":
        return getLuckyNumber()
    if operation == "getFilledNumberList":
        currentRound = args[0]
        return getFilledNumberList(currentRound)
    if operation == "getPlayersList":
        roundNum = args[0]
        guessNumber = args[1]
        return getPlayersList(roundNum, guessNumber)

    ######################### For testing purchase Begin ##############
    return False



####################### Methods that only Admin can invoke Start #######################
def init():
    RequireWitness(Admin)
    inited = Get(GetContext(), INIIT)
    if inited:
        Notify(["idiot admin, you have initialized the contract"])
        return False
    else:
        Put(GetContext(), INIIT, 1)
        Notify(["Initialized contract successfully"])
        startNewRound()
    return True


def startNewRound():
    """
    Only admin can start new round
    :return:
    """

    Require(CheckWitness(Admin))
    currentRound = getCurrentRound()
    nextRoundNum = currentRound + 1

    if currentRound != 0:
        currentVaultForNext = concatKey(concatKey(ROUND_PREFIX, currentRound), NEXT_VAULT_KEY)
        nextAwardVault = Get(GetContext(), currentVaultForNext)
        nextAwardVaultKey = concatKey(concatKey(ROUND_PREFIX, nextRoundNum), AWARD_VAULT_KEY)
        Put(GetContext(), nextAwardVaultKey, nextAwardVault)

    Put(GetContext(), concatKey(concatKey(ROUND_PREFIX, nextRoundNum), ROUND_STATUS_KEY), STATUS_ON)
    Put(GetContext(), CURRET_ROUND_NUM_KEY, nextRoundNum)
    Put(GetContext(), PRICE_PER_PAPER, InitialPrice)

    return True


def addReferral(toBeReferred, referral):
    """
    only Admin can add referral
    :param toBeReferred:
    :param referral:
    :return:
    """
    RequireWitness(Admin)
    RequireScriptHash(toBeReferred)
    RequireScriptHash(referral)
    Require(toBeReferred != referral)
    Put(GetContext(), concatKey(REFERRAL_PREFIX, toBeReferred), referral)
    return True


def addMultiReferral(args):
    """
    only Admin can add referral multiple times
    :param args:
    :return:
    """
    RequireWitness(Admin)
    for p in args:
        RequireScriptHash(p[0])
        RequireScriptHash(p[1])
        Require(p[0] != p[1])
        Put(GetContext(), concatKey(REFERRAL_PREFIX, p[0]), p[1])
    return True


def withdrawGas():
    """
    Only admin can withdraw
    :return:
    """
    Require(CheckWitness(Admin))
    Require(transferONGFromContact(Admin, getGasVault()))
    Delete(GetContext(), GAS_VAULT_KEY)
    return True


def endCurrentRound():
    RequireWitness(Admin)

    # transfer Gas vault to admin to prepare for calculating winner of current round
    gasVault = getGasVault()
    # Notify(["111_endCurrentRound", gasVault])
    if gasVault:
        Require(transferONGFromContact(Admin, gasVault))

    currentRound = getCurrentRound()
    Require(getGameStatus(currentRound) == STATUS_ON)

    numberListKey = concatKey(concatKey(ROUND_PREFIX, currentRound), FILLED_NUMBER_LIST_KEY)
    numberListInfo = Get(GetContext(), numberListKey)
    if numberListInfo:
        numberList = Deserialize(numberListInfo)
    else:
        # if no one participate this round of game
        Put(GetContext(), concatKey(concatKey(ROUND_PREFIX, currentRound), ROUND_STATUS_KEY), STATUS_OFF)
        startNewRound()
        return True

    # to record the minimum distance
    minDistance = 10000
    # to record the number corresponding with minimum distance
    minIndex = 10000
    luckyNumber = getLuckyNumber()
    for number in numberList:
        # the absolute value of sub(a, b)
        distance = ASub(number, luckyNumber)

        if distance < minDistance:
            minDistance = distance
            minIndex = number
        Notify(["112", number, distance, minDistance, minIndex])

    # Notify(["222_endCurrentEnd", luckyNumber, minIndex])

    winnersListKey = concatKey(concatKey(ROUND_PREFIX, currentRound), concatKey(FILLED_NUMBER_KEY, minIndex))
    winnersListInfo = Get(GetContext(), winnersListKey)
    winnersList = Deserialize(winnersListInfo)
    #           concatKey(concatKey(ROUND_PREFIX, currentRound), concatKey(FILLED_NUMBER_KEY, guessNumber))
    winnersTotalPaper = 0
    for winner in winnersList:
        winnersTotalPaper = Add(winnersTotalPaper, getPaperBalance(winner))

    # Notify(["333_endCurrentEnd", winnersList])
    # split the Award Vault to the winners
    awardVault = getAwardVault(currentRound)

    totalAward = 0
    for winner in winnersList:
        paperBalance = getPaperBalance(winner)
        winnerAward = Div(Mul(awardVault, paperBalance), winnersTotalPaper)
        winnerPercentage = winnerAward * 100 / getInvestOngBalance(winner)
        fee = 0
        if winnerPercentage > 100:
            fee = Div(Mul(winnerAward, WinnerFeeLarge), 100)
        else:
            fee = Div(Mul(winnerAward, WinnerFeeSmall), 100)

        pureWinnerAwardToBeAdd = Sub(winnerAward, fee)
        totalAward = Add(totalAward, pureWinnerAwardToBeAdd)
        Put(GetContext(), concatKey(AWARD_BALANCE_OF_PREFFIX, winner), Add(pureWinnerAwardToBeAdd, getAwardBalance(winner)))
        # Notify(["444_endCurrentEnd", getInvestOngBalance(winner), winnerAward, fee, pureWinnerAwardToBeAdd, winner])

    # give Admin some fee from winner
    totalFee = Sub(awardVault, totalAward)
    Put(GetContext(), concatKey(TOTAL_DIVIDEND_OF_PREFIX, Admin), Add(totalFee, getDividendBalance(Admin)))

    # delete the filled paper in current round
    for number in numberList:
        numberPlayersKey = concatKey(concatKey(ROUND_PREFIX, currentRound), concatKey(FILLED_NUMBER_KEY, number))
        numberPlayersInfo = Get(GetContext(), numberPlayersKey)
        numberPlayers = Deserialize(numberListInfo)

        for player in numberPlayers:
            if getFilledPaperBalance(player, currentRound):
                # update the player's paper balance
                Put(GetContext(), concatKey(PAPER_BALANCE_PREFIX, player), Sub(getPaperBalance(player), getFilledPaperBalance(player, currentRound)))
                # delete the filled paper balance of this round
                key1 = concatKey(ROUND_PREFIX, currentRound)
                key2 = concatKey(FILLED_PAPER_BALANCE_PREFIX, player)
                key = concatKey(key1, key2)
                Delete(GetContext(), key)

    # Notify(["555_endCurrentEnd"])
    # update the paper total amount
    Put(GetContext(), TOTAL_PAPER, Sub(getTotalPaper(), getFilledPaperAmount(currentRound)))
    # mark this round game as END
    Put(GetContext(), concatKey(concatKey(ROUND_PREFIX, currentRound), ROUND_STATUS_KEY), STATUS_OFF)

    startNewRound()

    # Notify(["666_endCurrentEnd"])

    return True
####################### Methods that only Admin can invoke End #######################


######################## Methods for Users Start ######################################
def buyPaper(account, paperAmount):
    RequireWitness(account)
    currentRound = getCurrentRound()

    Require(getGameStatus(currentRound) == STATUS_ON)

    ongAmount = paperToONG(currentRound, paperAmount)

    Require(transferONG(account, ContractAddress, ongAmount))

    # PaperHolderPercentage = 50
    dividend1 = Div(Mul(ongAmount, PaperHolderPercentage), 100)
    # update referral balance
    referral = Get(GetContext(), concatKey(REFERRAL_PREFIX, account))
    referralAmount = 0
    if referral:
        # ReferralAwardPercentage = 1
        referralAmount = Div(Mul(ongAmount, ReferralAwardPercentage), 100)
        Put(GetContext(), concatKey(REFERRAL_BALANCE_OF_PREFIX, referral), Add(referralAmount, getReferralBalance(account)))
    dividend = Sub(dividend1, referralAmount)

    # update next vault, NextPercentage = 10
    nextVaultToBeAdd = Div(Mul(ongAmount, NextPercentage), 100)
    nextVaultKey = concatKey(concatKey(ROUND_PREFIX, currentRound), NEXT_VAULT_KEY)
    Put(GetContext(), nextVaultKey, Add(nextVaultToBeAdd, getNextVault(currentRound)))

    # update award vault, AwardPercentage = 35
    awardVaultToBeAdd = Div(Mul(ongAmount, AwardPercentage), 100)
    awardVaultKey = concatKey(concatKey(ROUND_PREFIX, currentRound), AWARD_VAULT_KEY)
    Put(GetContext(), awardVaultKey, Add(awardVaultToBeAdd, getAwardVault(currentRound)))

    # update gas vault
    gasVaultToBeAdd = Sub(Sub(Sub(ongAmount, dividend1), nextVaultToBeAdd), awardVaultToBeAdd)
    Put(GetContext(), GAS_VAULT_KEY, Add(gasVaultToBeAdd, getGasVault()))

    # update total paper amount
    Put(GetContext(), TOTAL_PAPER, Add(paperAmount, getTotalPaper()))

    # update total invest ONG amount
    Put(GetContext(), concatKey(INVEST_BALANCE_PREFFIX, account), Add(ongAmount, getInvestOngBalance(account)))

    # update sold paper amount for the usage of calculating the price
    key = concatKey(concatKey(ROUND_PREFIX, currentRound), ROUND_PAPER_AMOUNT)
    Put(GetContext(), key, Add(paperAmount, getRoundSoldPaperAmount(currentRound)))

    # # # update the paper price in current round
    # currentPrice = getCurrentPrice()
    # Put(GetContext(), PRICE_PER_PAPER, Add(currentPrice, Mul(ongAmount, PriceIncremental)))

    # update paper balance of account
    Put(GetContext(), concatKey(PAPER_BALANCE_PREFIX, account), Add(paperAmount, getPaperBalance(account)))

    updateDividendBalance(account)
    # Notify(["111_buy", dividend1, dividend, nextVaultToBeAdd, awardVaultToBeAdd, gasVaultToBeAdd, getGasVault()])
    # update profitPerPaper
    oldProfitPerPaper = Get(GetContext(), PROFIT_PER_PAPER_KEY)
    totalPaper = getTotalPaper()
    # profitPerPaperToBeAdd = 0
    # if totalPaper == 0:
    #     # if totalPaper is ZERO, the dividend will go to the Gas Vault
    #     Put(GetContext(), GAS_VAULT_KEY, Add(dividend, getGasVault()))
    # else:
    #     profitPerPaperToBeAdd = Div(dividend, totalPaper)
    profitPerPaperToBeAdd = Div(dividend, totalPaper)
    Put(GetContext(), PROFIT_PER_PAPER_KEY, Add(profitPerPaperToBeAdd, oldProfitPerPaper))

    # Notify(["222_buy", getGasVault()])
    # # update profitPerPaperFrom of account
    # key = concatKey(PROFIT_PER_PAPER_FROM_PREFIX, account)
    # Put(GetContext(), key, oldProfitPerPaper)

    # PurchaseEvent(account, ongAmount, paperAmount)
    Notify(["buy", account, ongAmount, paperAmount])

    return True


def reinvest(account, paperAmount):
    RequireWitness(account)
    currentRound = getCurrentRound()

    Require(getGameStatus(currentRound) == STATUS_ON)

    ongAmount = paperToONG(currentRound, paperAmount)

    updateDividendBalance(account)
    dividendBalance = getDividendBalance(account)
    awardBalance = getAwardBalance(account)
    referralBalance = getReferralBalance(account)
    assetToBeReinvest = Add(Add(dividendBalance, awardBalance), referralBalance)


    Require(assetToBeReinvest >= ongAmount)

    # Delete(GetContext(), concatKey(TOTAL_DIVIDEND_OF_PREFIX, account))
    # Delete(GetContext(), concatKey(AWARD_BALANCE_OF_PREFFIX, account))
    # Delete(GetContext(), concatKey(REFERRAL_BALANCE_OF_PREFIX, account))

    dividend1 = Div(Mul(ongAmount, PaperHolderPercentage), 100)
    # update referral balance
    referral = Get(GetContext(), concatKey(REFERRAL_PREFIX, account))
    referralAmount = 0
    if referral:
        referralAmount = Div(Mul(ongAmount, ReferralAwardPercentage), 100)
        Put(GetContext(), concatKey(REFERRAL_BALANCE_OF_PREFIX, referral), Add(referralAmount, getReferralBalance(account)))
    dividend = Sub(dividend1, referralAmount)

    # update next vault
    nextVaultToBeAdd = Div(Mul(ongAmount, NextPercentage), 100)
    nextVaultKey = concatKey(concatKey(ROUND_PREFIX, currentRound), NEXT_VAULT_KEY)
    Put(GetContext(), nextVaultKey, Add(nextVaultToBeAdd, getNextVault(currentRound)))

    # update award vault
    awardVaultToBeAdd = Div(Mul(ongAmount, AwardPercentage), 100)
    awardVaultKey = concatKey(concatKey(ROUND_PREFIX, currentRound), AWARD_VAULT_KEY)
    Put(GetContext(), awardVaultKey, Add(awardVaultToBeAdd, getAwardVault(currentRound)))

    # update gas vault
    gasVaultToBeAdd = Sub(Sub(Sub(ongAmount, dividend1), nextVaultToBeAdd), awardVaultToBeAdd)
    Put(GetContext(), GAS_VAULT_KEY, Add(gasVaultToBeAdd, getGasVault()))

    # update total paper amount
    Put(GetContext(), TOTAL_PAPER, Add(paperAmount, getTotalPaper()))

    # update sold paper amount for the usage of calculating the price
    key = concatKey(concatKey(ROUND_PREFIX, currentRound), ROUND_PAPER_AMOUNT)
    Put(GetContext(), key, Add(paperAmount, getRoundSoldPaperAmount(currentRound)))

    # update paper balance of account
    Put(GetContext(), concatKey(PAPER_BALANCE_PREFIX, account), Add(paperAmount, getPaperBalance(account)))

    updateDividendBalance(account)

    # update profitPerPaper
    oldProfitPerPaper = Get(GetContext(), PROFIT_PER_PAPER_KEY)
    totalPaper = getTotalPaper()
    # profitPerPaperToBeAdd = 0
    # if totalPaper == 0:
    #     # if totalPaper is ZERO, the dividend will go to the Gas Vault
    #     Put(GetContext(), GAS_VAULT_KEY, Add(dividend, getGasVault()))
    # else:
    #     profitPerPaperToBeAdd = Div(dividend, totalPaper)
    profitPerPaperToBeAdd = Div(dividend, totalPaper)
    Put(GetContext(), PROFIT_PER_PAPER_KEY, Add(profitPerPaperToBeAdd, oldProfitPerPaper))

    # # update profitPerPaperFrom of account
    # key = concatKey(PROFIT_PER_PAPER_FROM_PREFIX, account)
    # Put(GetContext(), key, oldProfitPerPaper)

    # update the account balances of dividend, award, referral
    Delete(GetContext(), concatKey(AWARD_BALANCE_OF_PREFFIX, account))
    Delete(GetContext(), concatKey(REFERRAL_BALANCE_OF_PREFIX, account))
    ongAmountLeft = Sub(assetToBeReinvest, ongAmount)
    Put(GetContext(), concatKey(TOTAL_DIVIDEND_OF_PREFIX, account), ongAmountLeft)

    # update the invested ong amount for account
    Put(GetContext(), concatKey(INVEST_BALANCE_PREFFIX, account), Add(ongAmount, getInvestOngBalance(account)))

    # PurchaseEvent(account, ongAmount, paperAmount)
    Notify(["rebuy", account, ongAmount, paperAmount])


def fillPaper(account, guessNumberList):
    """
    :param account:
    :param guessNumberList: can be a list of numbers
    :return:
    """
    RequireWitness(account)
    currentRound = getCurrentRound()
    Require(getGameStatus(currentRound) == STATUS_ON)
    guessNumberLen = len(guessNumberList)

    currentFilledPaperBalance = getFilledPaperBalance(account, currentRound)
    # make sure his balance is greater or equal to current filled paper balance + guessNumberList length
    Require(getPaperBalance(account) > Add(currentFilledPaperBalance, guessNumberLen))

    numberListKey = concatKey(concatKey(ROUND_PREFIX, currentRound), FILLED_NUMBER_LIST_KEY)
    numberListInfo = Get(GetContext(), numberListKey)
    numberList = []
    if numberListInfo:
        numberList = Deserialize(numberListInfo)

    for guessNumber in guessNumberList:
        Require(guessNumber < 10000)

        numberPlayersKey = concatKey(concatKey(ROUND_PREFIX, currentRound), concatKey(FILLED_NUMBER_KEY, guessNumber))
        numberPlayersInfo = Get(GetContext(), numberPlayersKey)

        numberPlayers = []
        if numberPlayersInfo:
            numberPlayers = Deserialize(numberPlayersInfo)

            # make sure account has NOT filled the number before in this round
            for player in numberPlayers:
                Require(player != account)
        else:
            numberList.append(guessNumber)

        # add account to the players list that filled the number in this round
        numberPlayers.append(account)

        # Store the numberPlayers List
        numberPlayersInfo = Serialize(numberPlayers)
        Put(GetContext(), numberPlayersKey, numberPlayersInfo)
    # Store the numberList
    numberListInfo = Serialize(numberList)
    Put(GetContext(), numberListKey, numberListInfo)

    # update the filled paper amount in current round
    key = concatKey(concatKey(ROUND_PREFIX, currentRound), FILLED_PAPER_AMOUNT)
    Put(GetContext(), key, Add(guessNumberLen, getFilledPaperAmount(currentRound)))

    # update the filled paper balance in current round
    key1 = concatKey(ROUND_PREFIX, currentRound)
    key2 = concatKey(FILLED_PAPER_BALANCE_PREFIX, account)
    key = concatKey(key1, key2)
    Put(GetContext(), key, Add(guessNumberLen, currentFilledPaperBalance))

    Notify(["fillPaper", account, guessNumberList])

    return True


def withdraw(account):
    """
    account will withdraw his dividend and award to his own account
    :param account:
    :return:
    """
    RequireWitness(account)
    Notify(["111_withdraw", getDividendBalance(account)])
    updateDividendBalance(account)
    dividendBalance = getDividendBalance(account)
    awardBalance = getAwardBalance(account)
    referralBalance = getReferralBalance(account)
    assetToBeWithdrawn = Add(Add(dividendBalance, awardBalance), referralBalance)
    Notify(["222_withdraw", dividendBalance])
    Require(transferONGFromContact(account, assetToBeWithdrawn))
    Notify(["333_withdraw", dividendBalance])
    Delete(GetContext(), concatKey(TOTAL_DIVIDEND_OF_PREFIX, account))
    Delete(GetContext(), concatKey(AWARD_BALANCE_OF_PREFFIX, account))
    Delete(GetContext(), concatKey(REFERRAL_BALANCE_OF_PREFIX, account))

    Put(GetContext(), concatKey(WITHDRAWN_BALANCEOF_PREFFIX, account), assetToBeWithdrawn)

    Notify(["withdraw", ContractAddress, account, assetToBeWithdrawn])

    return True


def updateDividendBalance(account):
    """
    reset PROFIT_PER_PAPER_FROM_PREFIX of account and update account's dividend till now
    :param account:
    :return:
    """
    RequireWitness(account)
    key = concatKey(PROFIT_PER_PAPER_FROM_PREFIX, account)
    profitPerPaperFrom = Get(GetContext(), key)
    profitPerPaperNow = Get(GetContext(), PROFIT_PER_PAPER_KEY)
    profitPerPaper = profitPerPaperNow - profitPerPaperFrom
    profit = 0
    if profitPerPaper != 0:
        profit = Mul(profitPerPaper, getPaperBalance(account))
        Put(GetContext(), concatKey(PROFIT_PER_PAPER_FROM_PREFIX, account), profitPerPaperNow)
        Put(GetContext(), concatKey(TOTAL_DIVIDEND_OF_PREFIX, account), Add(profit, getDividendBalance(account)))
    return True
######################## Methods for Users Start ######################################






################## Global Info Start #######################
def getTotalPaper():
    return Get(GetContext(), TOTAL_PAPER)

def getGasVault():
    return Get(GetContext(), GAS_VAULT_KEY)

def getCurrentRound():
    return Get(GetContext(), CURRET_ROUND_NUM_KEY)

def getCurrentPrice():
    currentRound = getCurrentRound()
    currentRouldSoldAmount = getRoundSoldPaperAmount(currentRound)
    currentPrice = InitialPrice + 9260 * currentRouldSoldAmount - 9260
    return currentPrice
################## Global Info End #######################


####################### User Info Start #####################
def getPaperBalance(account):
    return Get(GetContext(), concatKey(PAPER_BALANCE_PREFIX, account))

def getInvestOngBalance(account):
    return Get(GetContext(), concatKey(INVEST_BALANCE_PREFFIX, account))

def getReferralBalance(account):
    return Get(GetContext(), concatKey(REFERRAL_BALANCE_OF_PREFIX, account))

def getDividendBalance(account):
    key = concatKey(PROFIT_PER_PAPER_FROM_PREFIX, account)
    profitPerPaperFrom = Get(GetContext(), key)
    profitPerPaperNow = Get(GetContext(), PROFIT_PER_PAPER_KEY)
    profitPerPaper = profitPerPaperNow - profitPerPaperFrom
    profit = 0
    if profitPerPaper != 0:
        profit = Mul(profitPerPaper, getPaperBalance(account))
    return Add(Get(GetContext(), concatKey(TOTAL_DIVIDEND_OF_PREFIX, account)), profit)

def getAwardBalance(account):
    return Get(GetContext(), concatKey(AWARD_BALANCE_OF_PREFFIX, account))

def getWithdrawnBalance(account):
    return Get(GetContext(), concatKey(WITHDRAWN_BALANCEOF_PREFFIX, account))

def getReferral(account):
    return Get(GetContext, concatKey(REFERRAL_PREFIX, account))

def getFilledPaperBalance(account, roundNum):
    key1 = concatKey(ROUND_PREFIX, roundNum)
    key2 = concatKey(FILLED_PAPER_BALANCE_PREFIX, account)
    return Get(GetContext(), concatKey(key1, key2))
####################### User Info Start #####################

####################### Round Info Start #############################


def getAwardVault(roundNum):
    return Get(GetContext(), concatKey(concatKey(ROUND_PREFIX, roundNum), AWARD_VAULT_KEY))

def getNextVault(roundNum):
    return Get(GetContext(), concatKey(concatKey(ROUND_PREFIX, roundNum), NEXT_VAULT_KEY))

def getGameStatus(roundNum):
    return Get(GetContext(), concatKey(concatKey(ROUND_PREFIX, roundNum), ROUND_STATUS_KEY))

def getRoundSoldPaperAmount(roundNum):
    roundSoldPaperAmountKey = concatKey(concatKey(ROUND_PREFIX, roundNum), ROUND_PAPER_AMOUNT)
    return Get(GetContext(), roundSoldPaperAmountKey)

def getFilledPaperAmount(roundNum):
    key = concatKey(concatKey(ROUND_PREFIX, roundNum), FILLED_PAPER_AMOUNT)
    return Get(GetContext(), key)


def getFilledNumberList(roundNum):
    numberListKey = concatKey(concatKey(ROUND_PREFIX, roundNum), FILLED_NUMBER_LIST_KEY)
    numberListInfo = Get(GetContext(), numberListKey)
    numberList = []
    if numberListInfo:
        numberList = Deserialize(numberListInfo)
    Notify(["111_getFilledNumberList", numberList])
    return numberList

def getPlayersList(roundNum, guessNumber):
    numberPlayersKey = concatKey(concatKey(ROUND_PREFIX, roundNum), concatKey(FILLED_NUMBER_KEY, guessNumber))
    numberPlayersInfo = Get(GetContext(), numberPlayersKey)

    numberPlayers = []
    if numberPlayersInfo:
        numberPlayers = Deserialize(numberPlayersInfo)
    Notify(["111_getPlayersList", numberPlayers])
    for player in numberPlayers:
        Notify([player])

    return numberPlayers
####################### Round Info End #############################

######################### Utility Methods Start #########################
def paperToONG(round, paperAmount):
    currentPaperAmount = getRoundSoldPaperAmount(round)
    averagePrice = InitialPrice + 9260 * currentPaperAmount + 4630 * paperAmount - 9260
    ongAmount = averagePrice * paperAmount
    return ongAmount

def getLuckyNumber():
    '''
     Generate the lucky number in specific round
    :param round: the game round number
    :return: lucky number
    '''
    blockHash = GetRandomHash()
    # The number should be in the range from 0 to 9999
    luckyNumber = blockHash % 10000
    luckyNumber = abs(luckyNumber) % 10000
    Notify(["round lucky number is -- ", luckyNumber, getCurrentRound()])
    return luckyNumber


def transferONG(fromAcct, toAcct, amount):
    """
    transfer ONG
    :param fromacct:
    :param toacct:
    :param amount:
    :return:
    """
    RequireWitness(fromAcct)
    param = state(fromAcct, toAcct, amount)
    res = Invoke(0, ONGAddress, 'transfer', [param])
    if res and res == b'\x01':
        Notify(["transferONG success"])
        return True
    else:
        Notify(["transferONG failure"])
        return False

def transferONGFromContact(toAcct, amount):
    param = state(ContractAddress, toAcct, amount)
    res = Invoke(0, ONGAddress, 'transfer', [param])

    if res and res == b'\x01':
        Notify('transfer from contract succeed')
        return True
    else:
        Notify('transfer from contract failed')
        return False

def concatKey(str1,str2):
    """
    connect str1 and str2 together as a key
    :param str1: string1
    :param str2:  string2
    :return: string1_string2
    """
    return concat(concat(str1, '_'), str2)
######################### Utility Methods End #########################