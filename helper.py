
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from os.path import basename
import re
import smtplib
import dns.resolver


# Address used for SMTP MAIL FROM command
fromAddress = 'r.ahmadifar.1377@gmail.com'

# Simple Regex for syntax checking
regex = '^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,})$'


def check(emailAddress):

    try:
        # Syntax check
        match = re.match(regex, emailAddress)
        if match == None:
            return False

        # Get domain for DNS lookup
        splitAddress = emailAddress.split('@')
        domain = str(splitAddress[1])

        # MX record lookup
        records = dns.resolver.resolve(domain, 'MX')
        mxRecord = records[0].exchange
        mxRecord = str(mxRecord)

        # SMTP lib setup (use debug level for full output)
        server = smtplib.SMTP(timeout=2)
        server.set_debuglevel(0)

        # SMTP Conversation
        server.connect(mxRecord)

        # server.local_hostname(Get local server hostname)
        server.helo(server.local_hostname)
        server.mail(fromAddress)
        code, message = server.rcpt(emailAddress)
        server.quit()

        # Assume SMTP response 250 is success
        if code == 250:
            return True
        else:
            return False
    except KeyError:
        return False
    except Exception as e:
        return False


def saveResult(correct):
    frw = open("result.txt", "r+")
    nums = frw.read().split("/")
    tot = int(nums[1])
    cur = int(nums[0])
    tot += 1
    if correct:
        cur += 1
    dw = str(cur) + "/" + str(tot)
    frw.seek(0)
    frw.write(dw)
    frw.close()

    return dw, cur


def saveOutputs(fc, email):
    frw = open("./outputs/valid " + fc + ".csv", "a")
    frw.write(email + "\n")
    frw.close()


def addEmail2List(email):
    frw = open("all.txt", "a")
    frw.write(email + "\n")
    frw.close()


def isDuplicate(email):
    frw = open("all.txt", "r")
    mm = email in frw.read()
    frw.close()
    return mm


mxf = 100000


def validation(file, email, arg):
    isCorrect = False
    result = ''
    if isDuplicate(email):
        isCorrect = False
        result, count = saveResult(isCorrect)
    else:
        addEmail2List(email)
        isCorrect = check(email)
        result, count = saveResult(isCorrect)

        if isCorrect:
            if count % 100000 == 0:
                # new file
                name = str((int(count / mxf) - 1) * mxf)
                name += "-"
                name += str((int(count / mxf)) * mxf)
            else:
                # append
                name = str((int(count / mxf)) * mxf)
                name += "-"
                name += str((int(count / mxf) + 1) * mxf)

            saveOutputs("[" + name + "]", email)

    #
    cond = str(isCorrect)
    if isCorrect:
        cond = cond + " "
    print("#", cond, '(' + result + ')', email, file)
