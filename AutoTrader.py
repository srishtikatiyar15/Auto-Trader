


#Modules import
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
import subprocess
import time 
import openpyxl
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from autotradercredentials import credentials

#Function for speaking
def speak(text, voice, rate, var=''):
    subprocess.call(['say', '-v', voice, '-r', str(rate), f"{text} {var}"])

#Function for popup
def popup(title, message, variable):
    script = f'display dialog "{message} {variable}" with title "{title}" with icon file "Users:farhan_46:Desktop:Farhan_Python:AutuTrader.png"'
    subprocess.call(['osascript', '-e', script])

#Function for current balance
def currentBalance():
    currentBalance = driver.find_element(By.XPATH, "(//span[@dir='ltr'])[1]")
    currentBalance = currentBalance.text
    currentBalance = float(currentBalance.replace('Đ', '').replace(',', ''))
    return currentBalance

#Log Function for excel sheet     
def logger(date, profit, maxBet, tradesTaken, target):
    wb = openpyxl.load_workbook('AutoTrader.xlsx')
    ws = wb.active
    new_row = [date, profit, maxBet, tradesTaken, target]
    ws.append(new_row)
    wb.save('AutoTrader.xlsx')

#Google Sheets Logger using Cloud Console
def logger2(date, profit, maxBet, tradesTaken, target):
    scope = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]
    SpreadSheetId = '1wGZV2Vk5GJS59EDJvNY0BJA0F7WFqkJHwLyPA2MN_4Y'
    SheetName = 'Sheet1'
    CredentialsFile = '/Users/farhan_46/Desktop/Farhan_Python/autotraderlogger-b0f2aa716505.json'

    creds = ServiceAccountCredentials.from_json_keyfile_name(CredentialsFile, scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(SpreadSheetId).worksheet(SheetName)

    new_row = [date, profit, maxBet, tradesTaken, target]
    sheet.append_row(new_row)

maxBet = []
noOfTrade = 0
target = 10

print("\n\n\t\t****** Launching Olymptrade ******\n\n")

speak("Auto Trader", 'Samantha', 170, var="")

#chrome driver path
driver = webdriver.Chrome()

# username & password
username = credentials.get('username')
password = credentials.get('password')


#launching website
driver.get('https://olymptrade.com/')
speak("Launching Olymp Trade", 'Samantha', 170, var="")
driver.maximize_window()
time.sleep(3)

#login process
registrationBtn = driver.find_element(By.XPATH, '//*[@id="gatsby-focus-wrapper"]/div/div[1]/header/div/div[2]/div[1]/div/button/div/div/div/div/span').click()
loginBtn = driver.find_element(By.XPATH, '//*[@id="gatsby-focus-wrapper"]/div/div[4]/div/div[2]/div[2]/div[1]/div/header/button[1]').click()
usernameField = driver.find_element(By.XPATH, "//input[@name='email']").send_keys(username)
passwordField = driver.find_element(By.XPATH, "//input[@name='password']").send_keys(password)
# time.sleep(25)    #google captcha manually bypass
finalLoginClick = driver.find_element(By.XPATH, "//*[@id='gatsby-focus-wrapper']/div/div[4]/div/div[2]/div[2]/div[2]/div/form/div[5]/button/div/div").click()
time.sleep(30)

#Reducing bet time  
timeReduceBtn = driver.find_element(By.XPATH, "(//button[@class='_633ZZh0WP6 input-controls__button'])[3]")
for i in range(4):
    timeReduceBtn.click()

initialBalance = currentBalance()  

#Win Function
def win():
    global noOfTrade
    if currentBalance() - initialBalance >= target:
        profit = currentBalance()-initialBalance

        print(f'\n\n\t\tCongratulations!!!\n\tSuccessfully Booked Profit of ${profit} !!!\n')

        #Logging the trade details in AutoTrader.xlsx file
        logger(time.ctime(), f'${profit}', max(maxBet), noOfTrade, target)
        logger2(time.ctime(), f'${profit}', max(maxBet), noOfTrade, target)
        speak("Congratulations, Successfully Booked Profit of $", 'Samantha', 170, var=int(profit))
        popup("Auto Trader", "Congratulations, Successfully Booked Profit of $", profit)
        quit()

    noOfTrade += 1
    tempBal = currentBalance()
    betUpBtn = driver.find_element(By.XPATH, "//button[@class='_633ZZh0WP6 deal-button deal-button_up']").click()
    time.sleep(8)
    if currentBalance() > tempBal:
        win()
    else:
        lose()

#Loss Function
x = 3
def lose():
    global noOfTrade
    global x

    if x == 6561:
        loss = initialBalance-currentBalance()
        logger(time.ctime(), f'$-{loss}', max(maxBet), noOfTrade, target)
        logger2(time.ctime(), f'$-{loss}', max(maxBet), noOfTrade, target)
        speak("Bad luck this time, loss of $", 'Samantha', 170, var=int(loss))
        popup("Auto Trader", "Bad luck this time, loss of $", f'{loss}')
        quit()

    noOfTrade += 1
    tempBal = currentBalance()
    betAmount = driver.find_element(By.XPATH, "//input[@class='_62AGWSkQlh _1PzrAtXMqD -V0a1Yk7Pu jWr94-Ldfm odeF0h-OkA input-with-step__input-base']")
    betAmount.click()
    for i in range(3):
        betAmount.send_keys(Keys.BACK_SPACE)
    betAmount.send_keys(x)
    maxBet.append(x)
    betUpBtn = driver.find_element(By.XPATH, "//button[@class='_633ZZh0WP6 deal-button deal-button_up']").click()
    time.sleep(8)


    if currentBalance() <= tempBal:
        x *= 3
        lose()
    else:
        betAmount = driver.find_element(By.XPATH, "//input[@class='_62AGWSkQlh _1PzrAtXMqD -V0a1Yk7Pu jWr94-Ldfm odeF0h-OkA input-with-step__input-base']")
        betAmount.click()
        for i in range(4):
            betAmount.send_keys(Keys.BACK_SPACE)
        betAmount.send_keys('1')
        x = 3
        win()

win()