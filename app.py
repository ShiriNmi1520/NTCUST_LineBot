import os
import requests as httpRequest

from flask import Flask, request as flaskReqest, abort, send_file, jsonify, render_template
from flask.logging import create_logger

from linebot import (
    LineBotApi, WebhookHandler
)

from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

from datetime import datetime, timedelta

from lib.firebase import *

from lib.flexMessageHandle import *

from lib.taichungBus import *

from apscheduler.schedulers.background import BackgroundScheduler

# pylint: disable=C0103
app = Flask(__name__)
log = create_logger(app)

# Channel Access Token
line_bot_api = LineBotApi(
    'lDq9TtQgojc3zHAG2UhC2USrfnHRGql8DtA8wKftENtr2iQuWJrjUCJkr4Yq1PA1DCH7it7cGyEFtst1wSZWzcUWPJ8r33xiFtyJDcpbmZevsSrHmHAXravu48Y0Q4LPuAMhMiQH8DjM4PF1bVzchAdB04t89/1O/w1cDnyilFU=')

# Channel Secret
handler = WebhookHandler('01b2e630b6634fe1b960e759eb12f41a')


def checkAndSendSchedule():
  data = taskSchedule()
  if(data):
    for key in list(data.keys()):
      # print(data[key]) #data
      # print(key) #id
      for task in data[key]:
        url = 'https://www.google.com/calendar/render?action=TEMPLATE&text={0}&details={1}'.format(
            'Line助理通知'+'%20' + task['content'], task['content'])
        line_bot_api.push_message(key, FlexSendMessage(
            'task notify', scheduleNotify({'content': 'Line助理通知'+' ' + task['content'], 'url': url})))
    print("task sent complete")
  else:
    print("no upcoming task found")


@app.route("/")
def hello():
  return "NTCUST Line Bot v1.0"


@app.route("/privacy")
def privacy():
  return send_file("static/privacy.html")


@app.route("/callback", methods=['POST'])
def callback():
  # get X-Line-Signature header value
  signature = flaskReqest.headers['X-Line-Signature']
  # get request body as text
  body = flaskReqest.get_data(as_text=True)
  log.info("Request body: " + body)
  # handle webhook body
  try:
    handler.handle(body, signature)
  except InvalidSignatureError:
    abort(400)
  return 'OK'

# 處理訊息


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
  # message = TextSendMessage(text=event.message.text)
  if(event.message.text.startswith("record")):
    profile = line_bot_api.get_profile(event.source.user_id)
    writeToFireBase(
        "user", {"id": event.source.user_id, "name": profile.display_name})
    message = TextSendMessage(text="done")
    line_bot_api.reply_message(event.reply_token, message)

  # bus schedule example
  elif(event.message.text.startswith("exampleBus")):
    message = {
        "type": "bubble",
        "size": "mega",
        "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "FROM",
                            "color": "#ffffff66",
                            "size": "sm"
                        },
                        {
                            "type": "text",
                            "text": "Akihabara",
                            "color": "#ffffff",
                            "size": "xl",
                            "flex": 4,
                            "weight": "bold"
                        }
                    ]
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "TO",
                            "color": "#ffffff66",
                            "size": "sm"
                        },
                        {
                            "type": "text",
                            "text": "Shinjuku",
                            "color": "#ffffff",
                            "size": "xl",
                            "flex": 4,
                            "weight": "bold"
                        }
                    ]
                }
            ],
            "paddingAll": "20px",
            "backgroundColor": "#0367D3",
            "spacing": "md",
            "height": "154px",
            "paddingTop": "22px"
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "Total: 1 hour",
                    "color": "#b7b7b7",
                    "size": "xs"
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {
                            "type": "text",
                            "text": "20:30",
                            "size": "sm",
                            "gravity": "center"
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "filler"
                                },
                                {
                                    "type": "box",
                                    "layout": "vertical",
                                    "contents": [],
                                    "cornerRadius": "30px",
                                    "height": "12px",
                                    "width": "12px",
                                    "borderColor": "#EF454D",
                                    "borderWidth": "2px"
                                },
                                {
                                    "type": "filler"
                                }
                            ],
                            "flex": 0
                        },
                        {
                            "type": "text",
                            "text": "Akihabara",
                            "gravity": "center",
                            "flex": 4,
                            "size": "sm"
                        }
                    ],
                    "spacing": "lg",
                    "cornerRadius": "30px",
                    "margin": "xl"
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {
                            "type": "box",
                            "layout": "baseline",
                            "contents": [
                                {
                                    "type": "filler"
                                }
                            ],
                            "flex": 1
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "box",
                                    "layout": "horizontal",
                                    "contents": [
                                        {
                                            "type": "filler"
                                        },
                                        {
                                            "type": "box",
                                            "layout": "vertical",
                                            "contents": [],
                                            "width": "2px",
                                            "backgroundColor": "#B7B7B7"
                                        },
                                        {
                                            "type": "filler"
                                        }
                                    ],
                                    "flex": 1
                                }
                            ],
                            "width": "12px"
                        },
                        {
                            "type": "text",
                            "text": "Walk 4min",
                            "gravity": "center",
                            "flex": 4,
                            "size": "xs",
                            "color": "#8c8c8c"
                        }
                    ],
                    "spacing": "lg",
                    "height": "64px"
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "20:34",
                                    "gravity": "center",
                                    "size": "sm"
                                }
                            ],
                            "flex": 1
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "filler"
                                },
                                {
                                    "type": "box",
                                    "layout": "vertical",
                                    "contents": [],
                                    "cornerRadius": "30px",
                                    "width": "12px",
                                    "height": "12px",
                                    "borderWidth": "2px",
                                    "borderColor": "#6486E3"
                                },
                                {
                                    "type": "filler"
                                }
                            ],
                            "flex": 0
                        },
                        {
                            "type": "text",
                            "text": "Ochanomizu",
                            "gravity": "center",
                            "flex": 4,
                            "size": "sm"
                        }
                    ],
                    "spacing": "lg",
                    "cornerRadius": "30px"
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {
                            "type": "box",
                            "layout": "baseline",
                            "contents": [
                                {
                                    "type": "filler"
                                }
                            ],
                            "flex": 1
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "box",
                                    "layout": "horizontal",
                                    "contents": [
                                        {
                                            "type": "filler"
                                        },
                                        {
                                            "type": "box",
                                            "layout": "vertical",
                                            "contents": [],
                                            "width": "2px",
                                            "backgroundColor": "#6486E3"
                                        },
                                        {
                                            "type": "filler"
                                        }
                                    ],
                                    "flex": 1
                                }
                            ],
                            "width": "12px"
                        },
                        {
                            "type": "text",
                            "text": "Metro 1hr",
                            "gravity": "center",
                            "flex": 4,
                            "size": "xs",
                            "color": "#8c8c8c"
                        }
                    ],
                    "spacing": "lg",
                    "height": "64px"
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {
                            "type": "text",
                            "text": "20:40",
                            "gravity": "center",
                            "size": "sm"
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "filler"
                                },
                                {
                                    "type": "box",
                                    "layout": "vertical",
                                    "contents": [],
                                    "cornerRadius": "30px",
                                    "width": "12px",
                                    "height": "12px",
                                    "borderColor": "#6486E3",
                                    "borderWidth": "2px"
                                },
                                {
                                    "type": "filler"
                                }
                            ],
                            "flex": 0
                        },
                        {
                            "type": "text",
                            "text": "Shinjuku",
                            "gravity": "center",
                            "flex": 4,
                            "size": "sm"
                        }
                    ],
                    "spacing": "lg",
                    "cornerRadius": "30px"
                }
            ]
        }
    }
    line_bot_api.reply_message(
        event.reply_token, FlexSendMessage("bus schedule", message))

  # task schedule example
  elif(event.message.text.startswith("exampleSchedule")):
    message = {
        "type": "carousel",
        "contents": [
            {
                "type": "bubble",
                "size": "micro",
                "header": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "備註(收件者 日期)",
                            "color": "#ffffff",
                            "align": "start",
                            "size": "md",
                            "gravity": "center"
                        },
                        {
                            "type": "text",
                            "text": "70%",
                            "color": "#ffffff",
                            "align": "start",
                            "size": "xs",
                            "gravity": "center",
                            "margin": "lg"
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "box",
                                    "layout": "vertical",
                                    "contents": [
                                        {
                                            "type": "filler"
                                        }
                                    ],
                                    "width": "70%",
                                    "backgroundColor": "#0D8186",
                                    "height": "6px"
                                }
                            ],
                            "backgroundColor": "#9FD8E36E",
                            "height": "6px",
                            "margin": "sm"
                        }
                    ],
                    "backgroundColor": "#27ACB2",
                    "paddingTop": "19px",
                    "paddingAll": "12px",
                    "paddingBottom": "16px"
                },
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "備註內容",
                                    "color": "#8C8C8C",
                                    "size": "sm",
                                    "wrap": True
                                }
                            ],
                            "flex": 1
                        }
                    ],
                    "spacing": "md",
                    "paddingAll": "12px"
                },
                "styles": {
                    "footer": {
                        "separator": False
                    }
                }
            },
            {
                "type": "bubble",
                "size": "micro",
                "header": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "Pending",
                            "color": "#ffffff",
                            "align": "start",
                            "size": "md",
                            "gravity": "center"
                        },
                        {
                            "type": "text",
                            "text": "30%",
                            "color": "#ffffff",
                            "align": "start",
                            "size": "xs",
                            "gravity": "center",
                            "margin": "lg"
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "box",
                                    "layout": "vertical",
                                    "contents": [
                                        {
                                            "type": "filler"
                                        }
                                    ],
                                    "width": "30%",
                                    "backgroundColor": "#DE5658",
                                    "height": "6px"
                                }
                            ],
                            "backgroundColor": "#FAD2A76E",
                            "height": "6px",
                            "margin": "sm"
                        }
                    ],
                    "backgroundColor": "#FF6B6E",
                    "paddingTop": "19px",
                    "paddingAll": "12px",
                    "paddingBottom": "16px"
                },
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "Wash my car",
                                    "color": "#8C8C8C",
                                    "size": "sm",
                                    "wrap": True
                                }
                            ],
                            "flex": 1
                        }
                    ],
                    "spacing": "md",
                    "paddingAll": "12px"
                },
                "styles": {
                    "footer": {
                        "separator": False
                    }
                }
            },
            {
                "type": "bubble",
                "size": "micro",
                "header": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "In Progress",
                            "color": "#ffffff",
                            "align": "start",
                            "size": "md",
                            "gravity": "center"
                        },
                        {
                            "type": "text",
                            "text": "100%",
                            "color": "#ffffff",
                            "align": "start",
                            "size": "xs",
                            "gravity": "center",
                            "margin": "lg"
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "box",
                                    "layout": "vertical",
                                    "contents": [
                                        {
                                            "type": "filler"
                                        }
                                    ],
                                    "width": "100%",
                                    "backgroundColor": "#7D51E4",
                                    "height": "6px"
                                }
                            ],
                            "backgroundColor": "#9FD8E36E",
                            "height": "6px",
                            "margin": "sm"
                        }
                    ],
                    "backgroundColor": "#A17DF5",
                    "paddingTop": "19px",
                    "paddingAll": "12px",
                    "paddingBottom": "16px"
                },
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "Buy milk and lettuce before class",
                                    "color": "#8C8C8C",
                                    "size": "sm",
                                    "wrap": True
                                }
                            ],
                            "flex": 1
                        }
                    ],
                    "spacing": "md",
                    "paddingAll": "12px"
                },
                "styles": {
                    "footer": {
                        "separator": False
                    }
                }
            }
        ]
    }
    line_bot_api.reply_message(
        event.reply_token, FlexSendMessage("task schedule", message))

  # add task
  elif(event.message.text.startswith("addTask")):
    try:
      # 格式內容: [addTask 收件者 日期(YYYY/MM/DD) 時間(HH:MM) 內容]
      textData = event.message.text.split()
      addSchedule(event.source.user_id, {
                  "to": textData[1], "date": textData[2], "time": textData[3], "content": textData[4], "status": False})
      line_bot_api.reply_message(
          event.reply_token, TextSendMessage(text="新增完成!"))
    except:
      line_bot_api.reply_message(
          event.reply_token, TextSendMessage(text="新增時發生錯誤，請確認訊息格式\n指令：addTask 收件者 時間(YYYY/MM/DD HH:MM) 內容"))

  elif(event.message.text == "getSchedule"):
    scheduleData = getSchedule(event.source.user_id)
    if(scheduleData):
      line_bot_api.reply_message(
          event.reply_token, FlexSendMessage("task schedule", generateScheduleFlex(scheduleData)))
    else:
      line_bot_api.reply_message(
          event.reply_token, TextSendMessage(text="查無紀錄行程"))

  elif(event.message.text.startswith("記帳")):
    try:
      textData = event.message.text.split()
      date = datetime.strptime(
          textData[1] + ' ' + textData[2], "%Y/%m/%d %H:%M")
      addAccounting(event.source.user_id, textData[3], str(date.year) + "/" + str(date.month), {"date": textData[1] + ' ' + textData[2], "item": textData[4], "amount": textData[5], "type": textData[6]}
                    )
      line_bot_api.reply_message(
          event.reply_token, TextSendMessage(text="新增完成!")
      )
    except:
      line_bot_api.reply_message(
          event.reply_token, TextSendMessage(
              text="新增時發生錯誤，請確認訊息格式\n指令：記帳 時間(YYYY/MM/DD HH:MM) 分類 內容 金額 類別(收入/支出)")
      )

  elif(event.message.text == ("附近公車站名")):
    try:
      location = getLocation(event.source.user_id)
      if(location):
        busStation = getNearbyStation(location)
        line_bot_api.reply_message(event.reply_token, FlexSendMessage(
            "nearby bus", nearbyBusGenerate(busStation)))
      else:
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text="無定位紀錄"))
    except:
      line_bot_api.reply_message(
          event.reply_token, TextSendMessage(
              text="發生錯誤")
      )
  elif(event.message.text.startswith("公車到站查詢")):
      location = getLocation(event.source.user_id)
      textData = event.message.text.split()
      print(textData)
      if(location):
        busStation = getDetailedBus(textData[1],location)
        print(busStation)
        line_bot_api.reply_message(event.reply_token, FlexSendMessage(
            "bus info", generateBusInfo(textData[1],busStation)))
      else:
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text="無定位紀錄"))
  elif(event.message.text.startswith("前往")):
    location = getLocation(event.source.user_id)
    destination = str(event.message.text).split("前往")
    if(location):
      data = directionRoute(location, destination[1])
      if(data):
        line_bot_api.reply_message(event.reply_token, FlexSendMessage(
            "bus route", generateBusRoute(data)))
      else:
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text="無最佳路線"))
    else:
      line_bot_api.reply_message(
          event.reply_token, TextSendMessage(text="無定位紀錄"))
  # if nothing match
  else:
    message = TextSendMessage(text="無對應指令")
    line_bot_api.reply_message(event.reply_token, message)


@handler.add(MessageEvent, message=LocationMessage)
def hande_location(event):
  updateLocation(event.source.user_id, {
                 "latitude": event.message.latitude, "longitude": event.message.longitude})
  line_bot_api.reply_message(
      event.reply_token, TextSendMessage(text="定位更新完成"))


if __name__ == '__main__':
  sched = BackgroundScheduler(daemon=True)
  sched.add_job(checkAndSendSchedule, 'interval', minutes=1)
  sched.start()
  app.run(debug=False, port=int(os.environ.get('PORT', 8080)), host='0.0.0.0')
