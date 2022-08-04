import smtplib
import ssl
import sys, argparse
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def _parseArgs():
    parser = argparse.ArgumentParser(description='mail app.')
    parser.add_argument("--cc")
    parser.add_argument("--to",required=True)
    parser.add_argument("--attach")
    parser.add_argument("--password",required=True)
    parser.add_argument("--sender",required=True)
    parser.add_argument("--subject")
    parser.add_argument("--body")
    
    return parser.parse_args()
    
        
def _strToList(commaSeperated):
    
    _list = []
    
    #sanity
    if (isinstance(commaSeperated,str)):
        #to list
        mArr = commaSeperated.split(",")
            
        #strip all mails and append
        _list.extend(map(str.strip,mArr))  
        
    else:
        msg = "not supported list. comma seperated expected: " 
        raise Exception(msg + str(commaSeperated))
    
    return _list
        

def _getFilePayload(fname):
    
    with open(fname, "rb") as file:
        payload = MIMEApplication(
            file.read(),
            Name=basename(fname)
        )
        
    payload['Content-Disposition'] = 'attachment; filename="%s"' % basename(fname)
        
    return payload;
        

def getMailText(): 
    msg = """Thank you for joining Momentix.
    attached please find
    
    1. your signed NDA
    2. mailApp.py
    3. just an image
    
    Thank you
    
    Momentix mail app
    """
    return msg


def _attachFiles(files, msg, filesPath):
        
    if filesPath is None:
        #treat like not supplied
        filesPath = ""
        
    for f in files:
        #get palylaod and attach
        msg.attach(_getFilePayload(filesPath + f))
        
        
def _getList(listOrStr):
    
    _list = []
    
    if (isinstance(listOrStr, str)):
        _list.append(listOrStr)
    elif (isinstance(listOrStr, list)):
        #clone
        _list = listOrStr[:]

    
    return _list
    
    
def sendMail(sender, password, to, cc, subject, message, files, filesPath = ""):
    
    try:
                
        onlyTo = _getList(to) 
        onlyCc = _getList(cc)
        # add cc to full mails list
        toListFull = onlyTo[:]
        toListFull.extend(_getList(cc))
        
        #msg object
        msg = MIMEMultipart()

        msg['From']= sender        
        msg['To'] = ",".join(onlyTo)
        msg['Subject']= subject
        
        # cc recipients if exist 
        if (isinstance(onlyCc, list)):
            #add cc if supplied - convert to str
            msg['Cc'] = ",".join(onlyCc)
        
        #mail msg
        msg.attach(MIMEText(message, 'plain'))
        
        #attachments
        _attachFiles(files, msg, filesPath)
        
        #open connection
        conn = smtplib.SMTP('smtp.gmail.com', 587)
        
        #say hello
        conn.ehlo()
        
        #secure
        context = ssl.create_default_context()
        conn.starttls(context=context) 
        
        conn.login(sender, password)
        
        conn.sendmail(sender, toListFull, msg.as_string())
        
        conn.quit()
        return  True
    except Exception as e:
        print('send mail ex: '+ str(e))
        return False


def _testsendMail():
    sender = "orenjamil@gmail.com"
    psswrd = "qsqjkepmxcgipmux"
    
    to = "gamilmatana@gmail.com"
    cc = "orenjamil.p@gmail.com"
    sub = "mail sub"
    body = "Dear body"
    files = ["Thinking.jpg"]
    filesPath = "D:\\Projects\\Momentix\\mailApp\\attachments\\"
    
    print ("testsendMail")
    res = sendMail(sender,psswrd,to,cc,sub,body,files,filesPath)
    print ("testsendMail done", res)

def main(args):
    _testsendMail()
    return

    mailArgs = _parseArgs()
    print("mail app called",mailArgs)

    #1. 
    sender = mailArgs.sender
    
    #2. 
    subject = mailArgs.subject
    
    #3. msg = getMailText()
    msg = mailArgs.body
    
    #4. account app key
    password = mailArgs.password 
    
    #5. 
    to = _strToList(mailArgs.to)
    
    #6. cc list - if supplied
    cc = ""
    if mailArgs.cc is not None:
        cc = _strToList(mailArgs.cc)
    
    #7. attachments names
    files = _strToList(mailArgs.attach)
    
    #send
    sendMail(sender, password, to, cc, subject, msg, files)
    
    print("mail app done")
    

if __name__ == '__main__':
   
    main(sys.argv)
  
