### contracts
luckynumber1.py is the original contract.

luckynumber2.py is the improved version of luckynumber1.py, but the problem that the invocation fee of ```endCurrentRound``` is still so high.

luckynumber3.py is the vertion after some rules are modified in order to decrease the invocation fee of ```endCurrentRound``` method.


### testing results
The results are in ```python-test-config-result```, which is from the python-testing-framework and ```Invocation Fee Test for endCurrentRound``` folder, which is from the testing script, ```runTestLuckyNumber.py```.


### abi.json
Please note in abi.json file, the followings are for your reference.
```
SpecificArray1 = [[toBeReferred1, referral1],[toBeReferred2, referral2]... ]

SpecificArray2 = [[account1, paperAmount1],[account2, paperAmount2]...]

SpecificList = [generatedLuckyNumber, actualLuckyNumberList,allWinnerList, winAwardList]

NumberList = [num1, num2, num3...]

AccountList = [account1, account2, account3...])
```