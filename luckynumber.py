'''
Lucky Number Game
'''
from boa.interop.Ontology.Contract import Migrate
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
ROUND_PREFIX = "G1"
# GAS_VAULT_KEY -- store the fee for calculating the winner
GAS_VAULT_KEY = "G02"

TOTAL_PAPER = "G03"
# CURRET_ROUND_NUM_KEY -- store the current round number
CURRET_ROUND_NUM_KEY = "G04"


PRICE_PER_PAPER = "G05"

# PROFIT_PER_PAPER_KEY -- store the profit per paper (when it is bought)
PROFIT_PER_PAPER_KEY = "G06"

# TOTAL_DIVIDEND_OF_PREFIX + account -- store the total accumulated dividend of account
# when user withdraws, the total dividend will go to ZERO
TOTAL_DIVIDEND_OF_PREFIX = "G07"
REFERRAL_BALANCE_OF_PREFIX = "G08"
# PAPER_BALANCE_PREFIX + account -- store the current blank paper amount of account
PAPER_BALANCE_PREFIX = "G09"
AWARD_BALANCE_OF_PREFFIX = "G10"
# WITHDRAWN_BALANCEOF_PREFFIX + account -- store the asset value that has been withdrawn
WITHDRAWN_BALANCEOF_PREFFIX = "G11"
INVEST_BALANCE_PREFFIX = "G12"
REFERRAL_PREFIX = "G13"

# PROFIT_PER_PAPER_FROM_PREFIX + account -- store the filled paper amount in round i
PROFIT_PER_PAPER_FROM_PREFIX = "G14"


################## Round i User info ##################
# ROUND_PREFIX + CURRET_ROUND_NUM_KEY + FILLED_PAPER_BALANCE_PREFIX + account -- store the filled paper amount in round i
FILLED_PAPER_BALANCE_PREFIX = "U01"


# ROUND_PREFIX + CURRET_ROUND_NUM_KEY + ROUND_DIVIDEND_PREFIX + account -- store the filled paper amount in round i,
# when user withdraws, the dividend in round i will be cleared to ZERO
ROUND_DIVIDEND_PREFIX = "U02"


###################### Round i Public info ###########################
# ROUND_PREFIX + CURRET_ROUND_NUM_KEY + AWARD_VAULT_KEY -- store the total award for the winner in roung i
AWARD_VAULT_KEY = "R01"

# ROUND_PREFIX + CURRET_ROUND_NUM_KEY + NEXT_VAULT_KEY -- store the asset for the next round in round i+1
NEXT_VAULT_KEY = "R02"


# ROUND_PREFIX + CURRET_ROUND_NUM_KEY + ROUND_PAPER_AMOUNT -- store the paper amount sold in this round
ROUND_PAPER_AMOUNT = "R03"

# ROUND_PREFIX + CURRET_ROUND_NUM_KEY + FILLED_PAPER_AMOUNT -- store the asset for the next round in round i+1
FILLED_PAPER_AMOUNT = "R04"

# ROUND_PREFIX + CURRET_ROUND_NUM_KEY + FILLED_NUMBER_LIST_KEY -- store the filled number on papers
FILLED_NUMBER_LIST_KEY = "R05"

# ROUND_PREFIX + CURRET_ROUND_NUM_KEY + FILLED_NUMBER_KEY + number -- store the accounts that filled number
# key = ROUND_PREFIX + CURRET_ROUND_NUM_KEY + FILLED_NUMBER_KEY + number
# value = [account1, account2, account3]
FILLED_NUMBER_KEY = "R06"


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
# Skyinglyh account
Admin = ToScriptHash('AQf4Mzu1YJrhz9f3aRkkwSm9n3qhXGSh4p')
# LuckyNumber  account
# Admin = ToScriptHash('AYqCVffRcbPkf1BVCYPJqqoiFTFmvwYKhG')

# PurchaseEvent = RegisterAction("buy", "account", "ongAmount", "paperAmount")

# Beijing time 2018-11-2-16:30:01
# each round will last 30 minutes
StartTime = 1541147401

def Main(operation, args):
    ######################## for Admin to invoke Begin ###############
    if operation == "init":
        if len(args) != 0:
            return False
        return init()
    if operation == "startNewRound":
        if len(args) != 0:
            return False
        return startNewRound()
    if operation =="addReferral":
        if len(args) != 2:
            return False
        toBeReferred = args[0]
        referral = args[1]
        return addReferral(toBeReferred, referral)
    if operation == "addMultiReferral":
        return addMultiReferral(args)
    if operation == "assignPaper":
        if len(args) != 2:
            return False
        account = args[0]
        paperAmount = args[1]
        return assignPaper(account, paperAmount)
    if operation == "multiAssignPaper":
        return multiAssignPaper(args)
    if operation == "withdrawGas":
        if len(args) != 0:
            return False
        return  withdrawGas()
    if operation == "endCurrentRound":
        if len(args) != 0:
            return False
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
    if operation == "migrateContract":
        if len(args)!= 7:
            return False
        code = args[0]
        needStorage = args[1]
        name = args[2]
        version = args[3]
        author = args[4]
        email = args[5]
        description = args[6]
        return migrateContract(code, needStorage, name, version, author, email, description)
    ######################## for User to invoke End ###############
    ######################### General Info to pre-execute Begin ##############
    if operation == "getTotalPaper":
        if len(args) != 0:
            return False
        return getTotalPaper()
    if operation == "getGasVault":
        if len(args) != 0:
            return False
        return getGasVault()

    if operation == "getCurrentRound":
        if len(args) != 0:
            return False
        return getCurrentRound()
    if operation == "getCurrentPrice":
        if len(args) != 0:
            return False
        return getCurrentPrice()
    if operation == "getCurrentRoundEndTime":
        return getCurrentRoundEndTime()
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
    if operation == "getDividendsBalance":
        if len(args) != 1:
            return False
        account = args[0]
        return getDividendsBalance(account)
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
    ######################### For testing purchase End ##############
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
        # startNewRound()
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
    Notify(["startRound", nextRoundNum])
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
    # key = concatKey(REFERRAL_PREFIX, toBeReferred),
    # value = referral
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


def assignPaper(account, paperAmount):
    RequireWitness(Admin)
    # update account paper balance
    accountKey = concatKey(PAPER_BALANCE_PREFIX, account)
    Put(GetContext(), accountKey, Add(paperAmount, getPaperBalance(account)))

    # update total paper amount
    Put(GetContext(), TOTAL_PAPER, Add(paperAmount, getTotalPaper()))
    # update the sold paper amount in this round
    currentRound = getCurrentRound()
    Put(GetContext(), concatKey(concatKey(ROUND_PREFIX, currentRound), ROUND_PAPER_AMOUNT), Add(paperAmount, getRoundSoldPaperAmount(currentRound)))
    Notify(["assignPaper", account, paperAmount, GetTime()])

    return True


def multiAssignPaper(args):
    RequireWitness(Admin)
    for p in args:
        Require(assignPaper(p[0], p[1]))
    return True

def withdrawGas():
    """
    Only admin can withdraw
    :return:
    """
    RequireWitness(Admin)
    Require(transferONGFromContact(Admin, getGasVault()))
    Delete(GetContext(), GAS_VAULT_KEY)
    return True


def endCurrentRound():
    RequireWitness(Admin)

    # transfer Gas vault to admin to prepare for calculating winner of current round
    gasVault = getGasVault()
    if gasVault:
        Require(withdrawGas())

    currentRound = getCurrentRound()
    Require(GetTime() > getCurrentRoundEndTime() - 60)
    Require(getGameStatus(currentRound) == STATUS_ON)

    numberListKey = concatKey(concatKey(ROUND_PREFIX, currentRound), FILLED_NUMBER_LIST_KEY)
    numberListInfo = Get(GetContext(), numberListKey)
    if numberListInfo:
        numberList = Deserialize(numberListInfo)
    else:
        # if no one participate this round of game
        Put(GetContext(), concatKey(concatKey(ROUND_PREFIX, currentRound), ROUND_STATUS_KEY), STATUS_OFF)
        Notify(["endRound", currentRound])
        startNewRound()
        return True

    # to record the minimum distance
    minDistance = 10000
    # to record the number corresponding with minimum distance
    minIndex = 10000
    luckyNumber = getLuckyNumber()
    for number in numberList:
        # get the L1 norm of the distance between number and luckyNumber
        distance = ASub(number, luckyNumber)

        if distance < minDistance:
            minDistance = distance
            minIndex = number

    winnersListKey = concatKey(concatKey(ROUND_PREFIX, currentRound), concatKey(FILLED_NUMBER_KEY, minIndex))
    winnersListInfo = Get(GetContext(), winnersListKey)
    winnersList = Deserialize(winnersListInfo)
    winnersTotalPaper = 0
    for winner in winnersList:
        winnersTotalPaper = Add(winnersTotalPaper, getPaperBalance(winner))

    # split the Award Vault to the winners
    awardVault = getAwardVault(currentRound)

    totalTaxedAward = 0
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
        totalTaxedAward = Add(totalTaxedAward, pureWinnerAwardToBeAdd)
        Put(GetContext(), concatKey(AWARD_BALANCE_OF_PREFFIX, winner), Add(pureWinnerAwardToBeAdd, getAwardBalance(winner)))

    # give Admin some fee from winner
    totalFee = Sub(awardVault, totalTaxedAward)
    Put(GetContext(), concatKey(TOTAL_DIVIDEND_OF_PREFIX, Admin), Add(totalFee, getDividendBalance(Admin)))

    # delete the filled paper in current round and update their PROFIT_PER_PAPER_FROM_PREFIX

    for number in numberList:
        numberPlayersKey = concatKey(concatKey(ROUND_PREFIX, currentRound), concatKey(FILLED_NUMBER_KEY, number))
        numberPlayersInfo = Get(GetContext(), numberPlayersKey)
        numberPlayers = Deserialize(numberPlayersInfo)

        for player in numberPlayers:
            if getFilledPaperBalance(player, currentRound):

                updateDividendBalance(player)

                # update the player's paper balance
                Put(GetContext(), concatKey(PAPER_BALANCE_PREFIX, player), Sub(getPaperBalance(player), getFilledPaperBalance(player, currentRound)))
                # delete the filled paper balance of this round
                key = concatKey(concatKey(ROUND_PREFIX, currentRound), concatKey(FILLED_PAPER_BALANCE_PREFIX, player))
                Notify(["destroyPaper", player, getFilledPaperBalance(player, currentRound), GetTime()])
                Delete(GetContext(), key)

    # update the paper total amount
    Put(GetContext(), TOTAL_PAPER, Sub(getTotalPaper(), getFilledPaperAmount(currentRound)))

    # Notify(["destroy",getFilledPaperAmount(currentRound), GetTime()])
    # mark this round game as END
    Put(GetContext(), concatKey(concatKey(ROUND_PREFIX, currentRound), ROUND_STATUS_KEY), STATUS_OFF)
    Notify(["endRound", currentRound, luckyNumber, winnersList])
    startNewRound()

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
    # update referral balance <---> Get(GetContext(), concatKey(REFERRAL_PREFIX, account))
    referral = getReferral(account)
    referralAmount = 0

    if referral:
        # ReferralAwardPercentage = 1
        referralAmount = Div(Mul(ongAmount, ReferralAwardPercentage), 100)
        Put(GetContext(), concatKey(REFERRAL_BALANCE_OF_PREFIX, referral), Add(referralAmount, getReferralBalance(referral)))
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

    updateDividendBalance(account)

    # update paper balance of account
    Put(GetContext(), concatKey(PAPER_BALANCE_PREFIX, account), Add(paperAmount, getPaperBalance(account)))

    # updateDividendBalance(account)
    # Notify(["111_buy", dividend1, dividend, nextVaultToBeAdd, awardVaultToBeAdd, gasVaultToBeAdd, getGasVault()])
    # update profitPerPaper
    oldProfitPerPaper = Get(GetContext(), PROFIT_PER_PAPER_KEY)
    totalPaper = getTotalPaper()

    profitPerPaperToBeAdd = Div(dividend, totalPaper)
    Put(GetContext(), PROFIT_PER_PAPER_KEY, Add(profitPerPaperToBeAdd, oldProfitPerPaper))

    # Notify(["222_buy", getGasVault()])
    # # update profitPerPaperFrom of account
    # Put(GetContext(), concatKey(PROFIT_PER_PAPER_FROM_PREFIX, account), oldProfitPerPaper)

    # PurchaseEvent(account, ongAmount, paperAmount)
    Notify(["buyPaper", account, ongAmount, paperAmount, GetTime()])

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

    dividend1 = Div(Mul(ongAmount, PaperHolderPercentage), 100)
    # update referral balance
    referral = Get(GetContext(), concatKey(REFERRAL_PREFIX, account))
    referralAmount = 0
    if referral:
        referralAmount = Div(Mul(ongAmount, ReferralAwardPercentage), 100)
        Put(GetContext(), concatKey(REFERRAL_BALANCE_OF_PREFIX, referral), Add(referralAmount, getReferralBalance(referral)))
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

    updateDividendBalance(account)

    # update paper balance of account
    Put(GetContext(), concatKey(PAPER_BALANCE_PREFIX, account), Add(paperAmount, getPaperBalance(account)))

    # update profitPerPaper
    oldProfitPerPaper = Get(GetContext(), PROFIT_PER_PAPER_KEY)
    profitPerPaperToBeAdd = Div(dividend, getTotalPaper())
    Put(GetContext(), PROFIT_PER_PAPER_KEY, Add(profitPerPaperToBeAdd, oldProfitPerPaper))

    # update profitPerPaperFrom of account
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
    Notify(["reBuyPaper", account, ongAmount, paperAmount, GetTime()])


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

    Require(guessNumberLen >= 1)

    currentFilledPaperBalance = getFilledPaperBalance(account, currentRound)
    # make sure his balance is greater or equal to current filled paper balance + guessNumberList length
    Require(getPaperBalance(account) >= Add(currentFilledPaperBalance, guessNumberLen))

    numberListKey = concatKey(concatKey(ROUND_PREFIX, currentRound), FILLED_NUMBER_LIST_KEY)
    numberListInfo = Get(GetContext(), numberListKey)
    numberList = []
    if numberListInfo:
        numberList = Deserialize(numberListInfo)

    for guessNumber in guessNumberList:

        Require(guessNumber < 10000)
        Require(guessNumber >= 0)

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

    Notify(["fillPaper", account, guessNumberList, GetTime()])

    return True


def withdraw(account):
    """
    account will withdraw his dividend and award to his own account
    :param account:
    :return:
    """
    RequireWitness(account)

    updateDividendBalance(account)
    dividendBalance = getDividendBalance(account)
    awardBalance = getAwardBalance(account)
    referralBalance = getReferralBalance(account)
    assetToBeWithdrawn = Add(Add(dividendBalance, awardBalance), referralBalance)
    if assetToBeWithdrawn > 0:
        Require(transferONGFromContact(account, assetToBeWithdrawn))
    else:
        return True

    Delete(GetContext(), concatKey(TOTAL_DIVIDEND_OF_PREFIX, account))
    Delete(GetContext(), concatKey(AWARD_BALANCE_OF_PREFFIX, account))
    Delete(GetContext(), concatKey(REFERRAL_BALANCE_OF_PREFIX, account))

    Put(GetContext(), concatKey(WITHDRAWN_BALANCEOF_PREFFIX, account), Add(assetToBeWithdrawn, getWithdrawnBalance(account)))

    Notify(["withdraw", ContractAddress, account, assetToBeWithdrawn, GetTime()])

    return True

def migrateContract(code, needStorage, name, version, author, email, description):
    RequireWitness(Admin)
    Migrate(code, needStorage, name, version, author, email, description)
    Notify(["Migrate Contract successfully", Admin, GetTime()])
    return True



def updateDividendBalance(account):
    """
    reset PROFIT_PER_PAPER_FROM_PREFIX of account and update account's dividend till now
    :param account:
    :return:
    """
    # Require(CheckWitness(account) or CheckWitness(Admin))
    key = concatKey(PROFIT_PER_PAPER_FROM_PREFIX, account)
    profitPerPaperFrom = Get(GetContext(), key)
    profitPerPaperNow = Get(GetContext(), PROFIT_PER_PAPER_KEY)
    profitPerPaper = Sub(profitPerPaperNow, profitPerPaperFrom)
    # Notify(["update", profitPerPaperNow, profitPerPaperFrom, profitPerPaper])
    # profit = 0
    if profitPerPaper != 0:
        # profit = Mul(profitPerPaper, getPaperBalance(account))
        Put(GetContext(), concatKey(TOTAL_DIVIDEND_OF_PREFIX, account), getDividendBalance(account))
        Put(GetContext(), concatKey(PROFIT_PER_PAPER_FROM_PREFIX, account), profitPerPaperNow)

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
    currentRoundSoldAmount = getRoundSoldPaperAmount(currentRound)
    currentPrice = InitialPrice + 9260 * currentRoundSoldAmount
    return currentPrice

def getCurrentRoundEndTime():
    currentRound = getCurrentRound()
    currentRoundEndTime = StartTime + Mul(currentRound, 30 * 60)
    return currentRoundEndTime
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
    # Get(GetContext(), concatKey(TOTAL_DIVIDEND_OF_PREFIX, account))
    return Add(Get(GetContext(), concatKey(TOTAL_DIVIDEND_OF_PREFIX, account)), profit)

def getAwardBalance(account):
    return Get(GetContext(), concatKey(AWARD_BALANCE_OF_PREFFIX, account))

def getDividendsBalance(account):
    return [getReferral(account), getDividendBalance(account), getAwardBalance(account)]

def getWithdrawnBalance(account):
    return Get(GetContext(), concatKey(WITHDRAWN_BALANCEOF_PREFFIX, account))

def getReferral(account):
    return Get(GetContext(), concatKey(REFERRAL_PREFIX, account))

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

    return numberList

def getPlayersList(roundNum, guessNumber):
    numberPlayersKey = concatKey(concatKey(ROUND_PREFIX, roundNum), concatKey(FILLED_NUMBER_KEY, guessNumber))
    numberPlayersInfo = Get(GetContext(), numberPlayersKey)

    numberPlayers = []
    if numberPlayersInfo:
        numberPlayers = Deserialize(numberPlayersInfo)

    for player in numberPlayers:
        Notify([player])

    return numberPlayers
####################### Round Info End #############################

######################### Utility Methods Start #########################
def paperToONG(round, paperAmount):
    roundSoldPaperAmount = getRoundSoldPaperAmount(round)
    averagePrice = InitialPrice + 9260 * roundSoldPaperAmount + 4630 * paperAmount - 4630
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
    luckyNumber = abs(luckyNumber)
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
        return True
    else:
        return False

def transferONGFromContact(toAcct, amount):
    param = state(ContractAddress, toAcct, amount)
    res = Invoke(0, ONGAddress, 'transfer', [param])

    if res and res == b'\x01':
        return True
    else:
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