import random
from datetime import datetime
from time import gmtime, strftime


def generateScheduleFlex(data):
  message = {
      "type": "carousel",
      "contents": [
      ]
  }
  for i in data:
    template = {
        "type": "bubble",
        "size": "kilo",
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
            "backgroundColor": "change",
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
    }

    def r(): return random.randint(0, 255)
    template['header']['contents'][0]['text'] = data[i]['to'] + \
        ' ' + data[i]['date'] + ' ' + data[i]['time']
    template['header']['backgroundColor'] = '#%02X%02X%02X' % (r(), r(), r())
    template['body']['contents'][0]['contents'][0]['text'] = data[i]['content']
    message['contents'].append(template)

  return message


def scheduleNotify(data):  # data(content, google calandar url)
  message = {
      "type": "carousel",
      "contents": [
          {
              "type": "bubble",
              "body": {
                  "type": "box",
                  "layout": "horizontal",
                  "contents": [
                      {
                          "type": "text",
                          "text": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
                          "wrap": True
                      }
                  ]
              },
              "footer": {
                  "type": "box",
                  "layout": "horizontal",
                  "contents": [
                      {
                          "type": "button",
                          "style": "primary",
                          "action": {
                              "type": "uri",
                              "label": "新增至Google日曆",
                              "uri": "https://example.com"
                          }
                      }
                  ]
              }
          }
      ]
  }
  message['contents'][0]['body']['contents'][0]['text'] = data['content']
  message['contents'][0]['footer']['contents'][0]['action']['uri'] = data['url']

  return message


def nearbyBusGenerate(data):
  dt = datetime.now()
  date_str = dt.strftime('%Y-%m-%d %H:%M:%S')

  message = {
      "type": "bubble",
      "body": {
          "type": "box",
          "layout": "vertical",
          "contents": [
              {
                  "type": "text",
                  "text": "附近公車站 (500公尺)",
                  "weight": "bold",
                  "color": "#1DB446",
                  "size": "xl"
              },
              {
                  "type": "separator",
                  "margin": "xxl"
              },
              {
                  "type": "box",
                  "layout": "vertical",
                  "margin": "xxl",
                  "spacing": "md",
                  "contents": [
                  ]
              }
          ]
      },
      "styles": {
          "footer": {
              "separator": True
          }
      }
  }

  separator = {
      "type": "separator",
      "margin": "xxl"
  }

  footer = {
      "type": "box",
      "layout": "horizontal",
      "margin": "md",
      "contents": [
          {
              "type": "text",
              "text": "最後更新時間",
              "size": "xs",
              "color": "#aaaaaa",
              "flex": 0
          },
          {
              "type": "text",
              "text": "",
              "color": "#aaaaaa",
              "size": "xs",
              "align": "end"
          }
      ]
  }

  footer["contents"][1]["text"] = date_str
  for index in data:
    template = {
        "type": "box",
        "layout": "horizontal",
        "contents": [
            {
                "type": "text",
                "text": "",
                "size": "md",
                "color": "#555555",
                "flex": 0
            }
        ]
    }
    template["contents"][0]["text"] = index
    message["body"]["contents"][2]["contents"].append(template.copy())
    for item in data[index]:
      template1 = {
          "type": "box",
          "layout": "horizontal",
          "contents": [
              {
                  "type": "text",
                  "text": "",
                  "size": "sm",
                  "color": "#555555",
                  "flex": 0
              }
          ]
      }
      template1["contents"][0]["text"] = item
      message["body"]["contents"][2]["contents"].append(template1.copy())
    message["body"]["contents"][2]["contents"].append(separator.copy())

  message["body"]["contents"][2]["contents"].append(footer)
  return message


def generateBusRoute(data):
  message = {
      "type": "bubble",
      "size": "giga",
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
                          "text": "406台灣台中市太平區立德街84號",
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
                          "color": "#ffffff",
                          "size": "xl",
                          "flex": 4,
                          "weight": "bold",
                          "text": "aa"
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
              }
          ]
      }
  }

  stopTemplate = {
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
  }

  busLineTemplate = {
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
  }

  startTemplate = {
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
  }

  walkLineTemplate = {
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
  }

  message["header"]["contents"][0]["contents"][1]["text"] = data["departureAddress"]
  message["header"]["contents"][1]["contents"][1]["text"] = data["arrivalAddress"]
  message["body"]["contents"][0]["text"] = "Total: " + data["duration"]
  startTemplate["contents"][0]["text"] = data["estimatedTimeDeparture"]
  startTemplate["contents"][2]["text"] = data["departureAddress"]
  walkLineTemplate["contents"][2]["text"] = "走路 " + data["walkTime"]
  message["body"]["contents"].append(startTemplate.copy())
  message["body"]["contents"].append(walkLineTemplate.copy())

  for item in data["bus"]:
    stopTemplate_loop = {
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
    }
    stopTemplate["contents"][0]["contents"][0]["text"] = item["departureTime"]
    stopTemplate["contents"][2]["text"] = item["departureStop"] + \
        " 公車： " + item["busNo"]
    busLineTemplate["contents"][2]["text"] = "站數： " + \
        str(item["stops"]) + " 時間： " + item["duration"]
    message["body"]["contents"].append(stopTemplate.copy())
    message["body"]["contents"].append(busLineTemplate.copy())
    stopTemplate_loop["contents"][0]["contents"][0]["text"] = item["arrivalTime"]
    stopTemplate_loop["contents"][2]["text"] = item["arrivalStop"]
    message["body"]["contents"].append(stopTemplate_loop.copy())

  return message


def generateBusInfo(busNo, data):
  message = {
      "type": "bubble",
      "size": "giga",
      "body": {
          "type": "box",
          "layout": "vertical",
          "contents": [
            {
                "type": "text",
                "text": "附近公車資訊",
                "weight": "bold",
                "color": "#1DB446",
                "size": "xl"
            },
              {
                "type": "separator",
                "margin": "xxl"
            },
              {
                "type": "box",
                "layout": "vertical",
                "margin": "xxl",
                "spacing": "md",
                "contents": [
                ]
            }
          ]
      },
      "styles": {
          "footer": {
              "separator": True
          }
      }
  }

  separator = {
      "type": "separator",
      "margin": "xxl"
  }

  message["body"]["contents"][0]["text"] = "附近公車資訊({0})".format(busNo)
  for item in data:
    if(data[item]):
      for nestedData in data[item]:
        print(nestedData)
        for index in nestedData.keys():
          print(index)
          template = {
              "type": "box",
              "layout": "horizontal",
              "contents": [
                  {
                      "type": "text",
                      "text": "",
                      "size": "md",
                      "color": "#555555",
                      "flex": 0
                  }
              ]
          }
          text = {
              "type": "text",
              "text": "$2.99",
              "size": "sm",
              "color": "#111111",
              "align": "end"
          }
          print(item, index, nestedData[index])
          template["contents"][0]["text"] = item + \
              str(" 去程 " if index == "0" else " 回程 ")
          text["text"] = "車牌" + nestedData[index]["PlateNumb"] + \
              " " + strftime("%M", gmtime(nestedData[index]["EstimateTime"])) + "分"
          template["contents"].append(text.copy())
          message["body"]["contents"][2]["contents"].append(template.copy())

  return message


if __name__ == "__main__":
  print(generateBusInfo(41, {'宜欣郵局': [{'0': {'PlateNumb': '061-U8', 'EstimateTime': 960}, '1': {'PlateNumb': '062-U8', 'EstimateTime': 300}}], '新高兒童公園': [], '樹德廣三街口': [], '樹德育才路口': [], '新城里福德祠': [], '樹德育賢路口': [], '新平國小': []}))
