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

REFERRAL_PREFIX = "Referral"

################## Round i User info ##################
# ROUND_PREFIX + CURRET_ROUND_NUM_KEY + FILLED_PAPER_BALANCE_PREFIX + account -- store the filled paper amount in round i
FILLED_PAPER_BALANCE_PREFIX = "FilledPaperBalanceOf"

# ROUND_PREFIX + CURRET_ROUND_NUM_KEY + PROFIT_PER_PAPER_FROM_PREFIX + account -- store the filled paper amount in round i
PROFIT_PER_PAPER_FROM_PREFIX = "ProfitPerPaperFrom"

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

# ROUND_PREFIX + CURRET_ROUND_NUM_KEY + FILLED_NUMBER_MAP_KEY + number -- store the number filled in paper and the accounts
# key = ROUND_PREFIX + CURRET_ROUND_NUM_KEY + FILLED_NUMBER_MAP_KEY + number
# value = [account1, account2, account3]
FILLED_NUMBER_MAP_KEY = "FilledNumMap"


############################### other info ###################################
INIIT = "Initialized"
ROUND_STATUS_KEY = "Status"
STATUS_ON = "RUNNING"
STATUS_OFF = "END"

InitialPrice = 1000000000
PriceIncremental = 9260
WinnerFeeLarge = 10
WinnerFeeSmall = 5
ReferralAwardPercentage = 10

# the script hash of this contract
ContractAddress = GetExecutingScriptHash()
ONGAddress = bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02')
Admin = ToScriptHash('AeS7aUsTmf7egcGQGS88LZAGD8gNFmCJnD')

PurchaseEvent = RegisterAction("buy", "account", "ongAmount", "paperAmount")


def Main(operation, args):

    return False


def init():
    RequireWitness(Admin)
    inited = Get(GetContext(), INIIT)
    if inited:
        Notify(["idiot admin, you have initialized the contract"])
    else:
        Put(GetContext(), INIIT, 1)
        Notify(["Initialized contract successfully"])
        startNewRound(Admin)
    return True

def checkAdmin():
    if CheckWitness(Admin) == True:
        return True
    return False

def startNewRound(addr):
    """
    Only admin can start new round
    :param addr:
    :return:
    """

    Require(checkAdmin())
    currentRoundNum = getCurrentRound()
    nextRoundNum = currentRoundNum + 1
    Put(GetContext(), CURRET_ROUND_NUM_KEY, nextRoundNum)

    if currentRoundNum != 1:
        currentVaultForNext = concatKey(concatKey(ROUND_PREFIX, currentRoundNum), NEXT_VAULT_KEY)
        nextAwardVault = Get(GetContext(), currentVaultForNext)
        nextAwardVaultKey = concatKey(concatKey(ROUND_PREFIX, nextRoundNum), AWARD_VAULT_KEY)
        Put(GetContext(), nextAwardVaultKey, nextAwardVault)
        Put(GetContext(), concatKey(concatKey(ROUND_PREFIX, nextRoundNum), ROUND_STATUS_KEY), STATUS_ON)

    Put(GetContext(), PRICE_PER_PAPER, InitialPrice)
    # Put(GetContext(), PROFIT_PER_PAPER_KEY, 0)
    return True

def addReferral(toBeReferred, referral):
    RequireWitness(Admin)
    RequireScriptHash(toBeReferred)
    RequireScriptHash(referral)
    Require(toBeReferred != referral)
    Put(GetContext(), concatKey(REFERRAL_PREFIX, toBeReferred), referral)
    return True

def buyPaper(account, paperAmount):
    RequireWitness(account)
    currentRound = getCurrentRound()
    ongAmount = paperToONG(currentRound, paperAmount)

    Require(transferONG(account, ContractAddress, ongAmount))

    dividend = Div(Mul(ongAmount, 50), 100)
    # update referral balance
    referral = Get(GetContext(), concatKey(REFERRAL_PREFIX, account))
    referralAmount = 0
    if referral:
        referralAmount = Div(Mul(ongAmount, 10), 100)
        Put(GetContext(), concatKey(REFERRAL_BALANCE_OF_PREFIX, referral), Add(referralAmount, getReferralBalance(account)))
    dividend = Sub(dividend, referralAmount)

    # update next vault
    nextVaultToBeAdd = Div(Mul(ongAmount, 10), 100)
    nextVaultKey = concatKey(concatKey(ROUND_PREFIX, currentRound), NEXT_VAULT_KEY)
    Put(GetContext(), nextVaultKey, Add(nextVaultToBeAdd, getNextVault(currentRound)))

    # update award vault
    awardVaultToBeAdd = Div(Mul(ongAmount, 35), 100)
    awardVaultKey = concatKey(concatKey(ROUND_PREFIX, currentRound), AWARD_VAULT_KEY)
    Put(GetContext(), awardVaultKey, Add(awardVaultToBeAdd, getAwardVault(currentRound)))

    # update gas vault
    gasVaultToBeAdd = Sub(Sub(Sub(ongAmount, dividend), nextVaultToBeAdd), awardVaultToBeAdd)
    Put(GetContext(), GAS_VAULT_KEY, Add(gasVaultToBeAdd, getGasVault()))

    # update total paper amount
    Put(GetContext(), TOTAL_PAPER, Add(paperAmount, getTotalPaper()))

    # update sold paper amount for the usage of calculating the price
    key = concatKey(concatKey(ROUND_PREFIX, currentRound), ROUND_PAPER_AMOUNT)
    Put(GetContext(), key, Add(paperAmount, getRoundSoldPaperAmount(currentRound)))

    # update paper balance of account
    Put(GetContext(), concatKey(PAPER_BALANCE_PREFIX, account), Add(paperAmount, getPaperBalance))

    updateDividendBalance(account, currentRound)

    # update profitPerPaper
    oldProfitPerPaper = Get(GetContext(), PROFIT_PER_PAPER_KEY)
    profitPerPaperToBeAdd = Div(dividend, getTotalPaper())
    Put(GetContext(), PROFIT_PER_PAPER_KEY, Add(profitPerPaperToBeAdd, oldProfitPerPaper))

    # update profitPerPaperFrom of account
    key1 = concatKey(ROUND_PREFIX, currentRound)
    key2 = concatKey(PROFIT_PER_PAPER_FROM_PREFIX, account)
    key = concatKey(key1, key2)
    Put(GetContext(), key, oldProfitPerPaper)

    PurchaseEvent(account, ongAmount, paperAmount)
    return True


def fillPaper(account, guessNumber):
    """
    :param account:
    :param number: should be 0 to 9999
    :return:
    """
    RequireWitness(account)
    Require(guessNumber < 9999)

    currentRound = getCurrentRound()
    numberListKey = concatKey(concatKey(ROUND_PREFIX, currentRound), FILLED_NUMBER_LIST_KEY)
    numberMapKey = concatKey(concatKey(ROUND_PREFIX, currentRound), FILLED_NUMBER_MAP_KEY)
    numberList = Get(GetContext(), numberListKey)
    numberMap = Get(GetContext(), numberMapKey)

    guessString = guessNumber + ""
    if numberMap[guessString]:
        numberMap[guessString].append(account)
    else:
        numberList.append(guessNumber)

    # update the filled paper amount in current round
    key = concatKey(concatKey(ROUND_PREFIX, currentRound), FILLED_PAPER_AMOUNT)
    Put(GetContext(), key, Add(1, getFilledPaperAmount(currentRound)))

    # update the filled paper balance in current round
    key = concatKey(concatKey(ROUND_PREFIX, currentRound), FILLED_PAPER_BALANCE_PREFIX)
    Put(GetContext(), key, Add(1, getFilledPaperBalance(currentRound)))


    return True

def endGame():
    RequireWitness(Admin)

    # transfer Gas vault to admin to prepare for calculating winner of current round
    gasVault = getGasVault()
    Require(transferONG(ContractAddress, Admin, gasVault))

    currentRound = getCurrentRound()
    numberListKey = concatKey(concatKey(ROUND_PREFIX, currentRound), FILLED_NUMBER_LIST_KEY)
    numberMapKey = concatKey(concatKey(ROUND_PREFIX, currentRound), FILLED_NUMBER_MAP_KEY)
    numberList = Get(GetContext(), numberListKey)
    numberMap = Get(GetContext(), numberMapKey)
    # to record the minimum distance
    minDistance = 10000
    # to record the number corresponding with minimum distance
    minIndex = 10000
    luckyNumber = getLuckyNumber()
    for number in numberList:
        distance = ASub(number, luckyNumber)
        if distance < minDistance:
            minDistance = distance
            minIndex = number
    luckyString = luckyNumber + ""
    winnersList = numberMap[luckyString]
    winnersTotalPaper = 0
    for winner in winnersList:
        winnersTotalPaper = Add(winnersTotalPaper, getPaperBalance(winner))

    awardVault = getAwardVault(currentRound)
    for winner in winnersList:
        winnerAward = Div(Mul(awardVault, getPaperBalance(winner)), winnersTotalPaper)
        Put(GetContext(), concatKey(AWARD_BALANCE_OF_PREFFIX, winner), Add(winnerAward, getAwardBalance(winner)))


    # need to delete the filled papers





def updateDividendBalance(account, roundNum):
    RequireWitness(account)
    key1 = concatKey(ROUND_PREFIX, roundNum)
    key2 = concatKey(PROFIT_PER_PAPER_FROM_PREFIX, account)
    key = concatKey(key1, key2)
    profitPerPaperFrom = Get(GetContext(), key)
    profitPerPaperNow = Get(GetContext(), PROFIT_PER_PAPER_KEY)
    profitPerPaper = profitPerPaperNow - profitPerPaperFrom
    profit = Mul(profitPerPaper, getPaperBalance(account))
    Put(GetContext(), concatKey(TOTAL_DIVIDEND_OF_PREFIX, account), Add(profit, getDividendBalance(account)))
    return True


def getAddressByIndex(guessNum, roundNum):
    """
    :param guessNum: guessNum is the guessing number of user
    :param roundNum:
    :return:
    """

def getFilledPaperAmount(roundNum):
    key = concatKey(concatKey(ROUND_PREFIX, roundNum), FILLED_PAPER_AMOUNT)
    return Get(GetContext(), key)

def getFilledPaperBalance(roundNum):
    key = concatKey(concatKey(ROUND_PREFIX, roundNum), FILLED_PAPER_BALANCE_PREFIX)
    return Get(GetContext(), key)




def getTotalPaper():
    return Get(GetContext(), TOTAL_PAPER)

def getCurrentRound():
    return Get(GetContext(), CURRET_ROUND_NUM_KEY)



def getPaperBalance(account):
    return Get(GetContext(), concatKey(PAPER_BALANCE_PREFIX, account))

def getReferralBalance(account):
    return Get(GetContext(), concatKey(REFERRAL_BALANCE_OF_PREFIX, account))

def getDividendBalance(account):
    return Get(GetContext(), concatKey(TOTAL_DIVIDEND_OF_PREFIX, account))

def getAwardBalance(account):
    return Get(GetContext(), concatKey(AWARD_BALANCE_OF_PREFFIX, account))




def getAwardVault(roundNum):
    return Get(GetContext(), concatKey(concatKey(ROUND_PREFIX, roundNum), AWARD_VAULT_KEY))

def getNextVault(roundNum):
    return Get(GetContext(), concatKey(concatKey(ROUND_PREFIX, roundNum), NEXT_VAULT_KEY))

def getGasVault():
    return Get(GetContext(), GAS_VAULT_KEY)





def getLuckyNumber():
    '''
     Generate the lucky number in specific round
    :param round: the game round number
    :return: lucky number
    '''
    blockHash = GetRandomHash()
    # The number should be in the range from 0 to 9999
    luckyNumber = blockHash % 10000
    Notify(["round lucky number is -- ", luckyNumber, getCurrentRound()])
    return luckyNumber
def getRoundSoldPaperAmount(roundNum):
    roundSoldPaperAmountKey = concatKey(concatKey(ROUND_PREFIX, roundNum), ROUND_PAPER_AMOUNT)
    return Get(GetContext(), roundSoldPaperAmountKey)

def paperToONG(round, paperAmount):
    currentPaperAmount = getRoundSoldPaperAmount(round)
    ongAmount = InitialPrice + 9260 * currentPaperAmount + 4630 * paperAmount
    return ongAmount


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

def concatKey(str1,str2):
    """
    connect str1 and str2 together as a key
    :param str1: string1
    :param str2:  string2
    :return: string1_string2
    """
    return concat(concat(str1, '_'), str2)