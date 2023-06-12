import supervisor
import socketpool
import time
import os
import storage
from duckyinpython import getProgrammingStatus
import wsgiserver as server
from adafruit_wsgi.wsgi_app import WSGIApp
from adafruit_wsgi import request
import wifi
from duckyinpython import *
import re
import json

config = json.load(open('./config.json'))

template_html = """<html lang="en">
<head>
<title>Select Payload</title>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" href="/style1.css">
</head>
<body>

<nav class="w3-sidebar w3-red w3-collapse w3-top w3-large w3-padding" style="z-index:3;width:300px;font-weight:bold;" id="mySidebar"><br>
  <a href="javascript:void(0)" onclick="w3_close()" class="w3-button w3-hide-large w3-display-topleft" style="width:100%;font-size:22px">Close Menu</a>
  <div class="w3-container">
    <h3 class="w3-padding-64"><b>Pico<br>Ducky</b></h3>
  </div>
  <div class="w3-bar-block">
    <a href="/ducky" onclick="w3_close()" disabled class="w3-bar-item w3-button w3-hover-white">Payloads</a> 
    <a href="/new" onclick="w3_close()" class="w3-bar-item w3-button w3-hover-white">New Payload</a> 
    <a href="preferences" onclick="w3_close()" class="w3-bar-item w3-button w3-hover-white">Preferences</a> 
  </div>
</nav>

<header class="w3-container w3-top w3-hide-large w3-red w3-xlarge w3-padding">
  <a href="javascript:void(0)" class="w3-button w3-red w3-margin-right" onclick="w3_open()">☰</a>
  <span>Pico Ducky</span>
</header>

<div class="w3-overlay w3-hide-large" onclick="w3_close()" style="cursor:pointer" title="close side menu" id="myOverlay"></div>

<div class="w3-main" style="margin-left:340px;margin-right:40px">

{}

</div>
    <script src="/script.js" onload="changeFunc(); checkForm(); unlockForm();"></script>
</body>
</html>"""

payload_html = """<div class="w3-container" id="services" style="margin-top:75px">
    <h1 class="w3-xxxlarge w3-text-red"><b>Payloads</b></h1>
    <hr style="width:50px;border:5px solid red" class="w3-round">
    <select onchange="changeFunc();" id="payloadSelect" class="w3-block w3-padding-large w3-light-blue w3-margin-bottom">0
        {}
    </select>
    <br/>
    <div id="buttonBox">
        <a href="/run/"><button type="submit" disabled class="w3-button w3-block w3-padding-large w3-blue w3-margin-bottom">Run Payload</button></a>
        <a href="/edit/"><button type="submit" disabled class="w3-button w3-block w3-padding-large w3-green w3-margin-bottom">Edit Payload</button></a>
        <a href="/delete/"><button type="submit" disabled class="w3-button w3-block w3-padding-large w3-red w3-margin-bottom">Delete Payload</button></a>
    </div>
  </div>
  </div>
    <script src="/script.js" onload="changeFunc()"></script>
"""

edit_html = """
<div class="w3-main" style="margin-left:340px;margin-right:40px">

  <div class="w3-container" id="services" style="margin-top:75px">
    <h1 class="w3-xxxlarge w3-text-red"><b>Editing {}</b></h1>
    <hr style="width:50px;border:5px solid red" class="w3-round">

    <br/>
    <div id="buttonBox">
      <form action="/write/{}" method="POST" enctype="text/plain">
        <textarea name="scriptData" rows="10" class="w3-block w3-padding-large w3-margin-bottom editBox" >{}</textarea>
        <button type="submit" class="w3-button w3-block w3-padding-large w3-blue w3-margin-bottom">Save</button>
      </form>
      </div>
  </div>
  </div>
    <script src="/script.js" onload=""></script>
"""


new_html = """    <div class="w3-container" id="services" style="margin-top:75px">
      <h1 class="w3-xxxlarge w3-text-red"><b>New Script</b></h1>
      <hr style="width:50px;border:5px solid red" class="w3-round">
  
      <br/>
      <div id="buttonBox">
        <form action="/new" method="POST" enctype="text/plain">
          <input id="scriptNameInput" oninput="unlockForm();" type="text" placeholder="Name your script..." name="scriptName" class="w3-block w3-padding-large w3-margin-bottom">
          <textarea placeholder="Code away..." class="w3-block w3-padding-large w3-margin-bottom newInput" name="scriptData"></textarea>
          <button id="submitButton" disabled class="w3-button w3-block w3-padding-large w3-blue w3-margin-bottom" type="submit"><p>Create</p></button>
        </form>
        </div>
    </div>
    </div>
    <script src="/script.js" onload="unlockForm();"></script>
"""

preferences_html = """<div class="w3-container" id="services" style="margin-top:75px">
      <h1 class="w3-xxxlarge w3-text-red"><b>Preferences</b></h1>
      <hr style="width:50px;border:5px solid red" class="w3-round">
  
      <br/>
      <div class="form" class="w3-block">
        <form action="/preferences" method="POST" enctype="Text/plain">
            <strong><p> SSID: </p></strong><input oninput="checkForm();" class="w3-block w3-border-light-blue w3-padding-large w3-light-blue w3-margin-bottom" type="text" placeholder="SSID Name..." name="ssid" id="ssidInputBox" value="{}">
            <strong><p> Password: </p></strong><input oninput="checkForm();" id="passwordInputBox" type="password" placeholder="Password (8 char min)..." name="password" class ="w3-block w3-border-light-blue w3-padding-large w3-light-blue w3-margin-bottom" value="{}">
              <strong><p style="display: inline; vertical-align: middle;"> Autorun: </p></strong><input style="vertical-align: middle;display: inline; width: 24px;height: 24px;" value="on" {} class=".w3-check .w3-show-inline-block" type="checkbox" name="autorun" >
           <strong> <p> Default: </p></strong><select class="w3-block w3-padding-large w3-light-blue w3-margin-bottom" name="defaultScript" id="scripts">{}</select>
            <button disabled type="submit" id ="submit" class="w3-button w3-block w3-padding-large w3-blue w3-margin-bottom"><p>Save Options</p></button>
        </form>
    </div>
    </div>
    <script src="/script.js" onload="checkForm();"></script>
"""

response_html = """
    <div class="w3-container" id="services" style="margin-top:75px">
      <h1 class="w3-xxxlarge w3-text-red"><b>{}</b></h1>

      
      <hr style="width:50px;border:5px solid red" class="w3-round">
      
      <h1 class="w3-xlarge w3-text-red"><b>{}</b></h1>
      <br/>
      <p>You Will be Redirected in 5 seconds...</p>
    </div>
    <script src="/script.js" onload="goHome();"></script>"""
newrow_html = "<option {}>{}</option>"
newrowPreference_html = "<option value='{}' {} >{}</option>"

def setPayload(payload_number):
    if(payload_number == 1):
        payload = "payload.dd"
    else:
        payload = "payload"+str(payload_number)+".dd"
    return(payload)

def ducky_main(request):
    payloads = []
    rows = ""
    files = os.listdir('./scripts')
    selectedFile = '';
    for f in files:
        if ('.dd' in f) == True:
            selected = ''
            if config['config']['defaultFile'] == f:
                selected = 'selected'
                selectedFile = f;
            payloads.append(f)
            newrow = newrow_html.format(selected, f)
            rows = rows + newrow

    response = payload_html.format(rows, selectedFile,selectedFile,selectedFile)
    response = template_html.format(response)

    return(response)

def cleanup_text(buffer):
    return_buffer = buffer.replace('+', ' ').replace('%0D%0A', '\n') + '\n'
    return(return_buffer)

web_app = WSGIApp()

@web_app.route("/")
def index(request):
    response = ducky_main(request)
    return("200 OK", [('Content-Type', 'text/html')], response)

@web_app.route("/ducky")
def duck_main(request):
    response = ducky_main(request)
    return("200 OK", [('Content-Type', 'text/html')], response)

@web_app.route("/run/<filename>")
def run_script(request, filename):
    runScript(filename)
    response = response_html.format("Success","Running Script: " + filename)
    response = template_html.format(response)
    return("200 OK",[('Content-Type', 'text/html')], response)

@web_app.route("/edit/<filename>")
def edit(request, filename):
    if '.css' in filename:
        return
    f = open(f"./scripts/{filename}","r",encoding='utf-8')
    textbuffer = ''
    for line in f:
        textbuffer = textbuffer + line
    f.close()
    response = edit_html.format(filename,filename,textbuffer)
    response = template_html.format(response)
    return("200 OK",[('Content-Type', 'text/html')], response)

@web_app.route("/write/<filename>",methods=["POST"])
def write_script(request, filename):
    data = request.body.getvalue()
    fields = data.split('\r\n')
    form_data = {}
    for field in fields:
        if "=" in field:
            key,value = field.split('=')
            form_data[key] = value
    f = open(f"/scripts/{filename}","w",encoding='utf-8')
    textbuffer = form_data['scriptData']
    textbuffer = cleanup_text(textbuffer)
    for line in textbuffer:
        f.write(line)
    f.close()
    response = response_html.format("Success", "Wrote Script: " + filename)
    response = template_html.format(response)
    return("200 OK",[('Content-Type', 'text/html')], response)

@web_app.route("/new",methods=['GET','POST'])
def write_new_script(request):
    response = ''
    if(request.method == 'GET'):
        response = template_html.format(new_html)
    else:
        data = request.body.getvalue()
        fields = data.split('\r\n')
        form_data = {}
        for field in fields:
            if "=" in field:
                key,value = field.split('=')
                form_data[key] = value

        filename = form_data['scriptName']
        textbuffer = form_data['scriptData']
        textbuffer = cleanup_text(textbuffer)
        storage.remount("/",readonly=False)
        f = open(f"/scripts/{filename}.dd","w",encoding='utf-8')
        for line in textbuffer:
            f.write(line)
        f.close()
        response = response_html.format("Success", "Created Script: " + filename)
        response = template_html.format(response)
    return("200 OK",[('Content-Type', 'text/html')], response)

@web_app.route("/delete/<filename>")
def delete_script(request, filename):
    if '.dd' in filename:
        os.remove(f"./scripts/{filename}")
    response = response_html.format("Success", "Deleted script " + filename)
    response = template_html.format(response)
    return("200 OK",[('Content-Type', 'text/html')], response)

@web_app.route('/style1.css')
def css(request):
    return("200 OK", [('Content-Type', 'text/css')], open('./style1.css'))

@web_app.route('/script.js')
def css(request):
    return("200 OK", [('Content-Type', 'application/javascript')], open('script.js'))


@web_app.route("/preferences",methods=['GET','POST'])
def preferences(request):
    response = ''
    if(request.method == 'GET'):
        payloads = []
        rows = ""
        files = os.listdir('./scripts')
        for f in files:
            if ('.dd' in f) == True:
                payloads.append(f)
                selected = '';
                if f == config['config']['defaultFile']:
                    selected = 'selected'
                newrow = newrowPreference_html.format(f,selected,f)
                rows = rows + newrow
                autorun = '';
                if config['config']['autorun'] == True:
                    autorun = 'checked'
            if len(rows) < 0.5:
                autorun = 'disabled'
        response = preferences_html.format(config['config']['ssid'], config['config']['password'],autorun, rows)
        response = template_html.format(response)

        return("200 OK",[('Content-Type', 'text/html')], response)
    else:
        data = request.body.getvalue()
        fields = data.split('\r\n')
        form_data = {}
        for field in fields:
            if "=" in field:
                key,value = field.split('=')
                form_data[key] = value

        if not 'autorun' in form_data:
            form_data['autorun'] = 'off'

        if len(config['config']['ssid']) > 0:
            config['config']['ssid'] = form_data['ssid']
        else:
            response = response_html.format("400 BAD Request", "SSID Too Short")
            response = template_html.format(response)

            return("400 SSID Too Short",[('Content-Type', 'text/html')], response)

        if len(form_data['password']) > 7:
            config['config']['password'] = form_data['password']
        else:
            response = response_html.format("400 BAD Request", "Password Too Short")
            response = template_html.format(response)
            return("400 Password Too Short",[('Content-Type', 'text/html')], response)

        if form_data['autorun'] == 'on':
            config['config']['autorun'] = True
        else: 
            config['config']['autorun'] = False

        config['config']['defaultFile'] = form_data['defaultScript']


        with open('config.json', 'w') as f:
            json.dump(config, f)
        response = response_html.format("Success", "Restart the device to activate changes.")
        response = template_html.format(response)
    return("200 OK",[('Content-Type', 'text/html')], response)

async def startWebService():
    HOST = repr(wifi.radio.ipv4_address_ap)
    PORT = 80
    wsgiServer = server.WSGIServer(80, application=web_app)
    print(f"open this IP in your browser: http://{HOST}:{PORT}/")
    wsgiServer.start()
    while True:
        try:
            wsgiServer.update_poll()
            await asyncio.sleep(0.1)
        except (ValueError, RuntimeError, BrokenPipeError) as e:
            print(f"Error Code:{e} | Restarting...")
            supervisor.reload()
            continue

