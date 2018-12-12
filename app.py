import os
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    TemplateSendMessage, MessageAction, URIAction,
    CarouselTemplate, CarouselColumn, LocationMessage, LocationSendMessage
)

from pyzomato import Pyzomato

# configure

app = Flask(__name__)

line_bot_api = LineBotApi('LINE_CHANNEL_ACCESS_TOKEN')
handler = WebhookHandler('LINE_CHANNEL_SECRET')
p = Pyzomato("ZOMATO_API_KEY")

@app.route("/callback", methods=['POST'])
def callback():
    # Get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # Get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # Handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

# handle message berbentuk Location

@handler.add(MessageEvent, message = LocationMessage)
def handle_location_message(event):
    latitude = event.message.latitude 
    longitude = event.message.longitude
    
    carousel_template = CarouselTemplate(columns = [
        CarouselColumn(text = p.getByGeocode(lan = latitude, lon = longitude)['nearby_restaurants'][0]['restaurant']['cuisines'], title = p.getByGeocode(lan = latitude, lon = longitude)['nearby_restaurants'][0]['restaurant']['name'], actions = [
            URIAction(label = 'Lihat Menu', uri = p.getByGeocode(lan = latitude, lon = longitude)['nearby_restaurants'][0]["restaurant"]["menu_url"]),
            URIAction(label = 'Lihat Review', uri = p.getByGeocode(lan = latitude, lon = longitude)['nearby_restaurants'][0]["restaurant"]["url"])
        ]),
        CarouselColumn(text = p.getByGeocode(lan = latitude, lon = longitude)['nearby_restaurants'][1]['restaurant']['cuisines'], title = p.getByGeocode(lan = latitude, lon = longitude)['nearby_restaurants'][1]['restaurant']['name'], actions = [
            URIAction(label = 'Lihat Menu', uri = p.getByGeocode(lan = latitude, lon = longitude)['nearby_restaurants'][1]["restaurant"]["menu_url"]),
            URIAction(label = 'Lihat Review', uri = p.getByGeocode(lan = latitude, lon = longitude)['nearby_restaurants'][1]["restaurant"]["url"])
        ]),
        CarouselColumn(text = p.getByGeocode(lan = latitude, lon = longitude)['nearby_restaurants'][2]['restaurant']['cuisines'], title = p.getByGeocode(lan = latitude, lon = longitude)['nearby_restaurants'][2]['restaurant']['name'], actions = [
            URIAction(label = 'Lihat Menu', uri = p.getByGeocode(lan = latitude, lon = longitude)['nearby_restaurants'][2]["restaurant"]["menu_url"]),
            URIAction(label = 'Lihat Review', uri = p.getByGeocode(lan = latitude, lon = longitude)['nearby_restaurants'][2]["restaurant"]["url"])
        ]),
        CarouselColumn(text = p.getByGeocode(lan = latitude, lon = longitude)['nearby_restaurants'][3]['restaurant']['cuisines'], title = p.getByGeocode(lan = latitude, lon = longitude)['nearby_restaurants'][3]['restaurant']['name'], actions = [
            URIAction(label = 'Lihat Menu', uri = p.getByGeocode(lan = latitude, lon = longitude)['nearby_restaurants'][3]["restaurant"]["menu_url"]),
            URIAction(label = 'Lihat Review', uri = p.getByGeocode(lan = latitude, lon = longitude)['nearby_restaurants'][3]["restaurant"]["url"])
        ]),
        CarouselColumn(text = p.getByGeocode(lan = latitude, lon = longitude)['nearby_restaurants'][4]['restaurant']['cuisines'], title = p.getByGeocode(lan = latitude, lon = longitude)['nearby_restaurants'][4]['restaurant']['name'], actions = [
            URIAction(label = 'Lihat Menu', uri = p.getByGeocode(lan = latitude, lon = longitude)['nearby_restaurants'][4]["restaurant"]["menu_url"]),
            URIAction(label = 'Lihat Review', uri = p.getByGeocode(lan = latitude, lon = longitude)['nearby_restaurants'][4]["restaurant"]["url"])
        ]),
    ])
    template_message = TemplateSendMessage(
        alt_text='Carousel Zomato', template = carousel_template)
    line_bot_api.reply_message(event.reply_token, [TextSendMessage(text = "Oke, ini ya rekomendasi tempat makan enak! Rekomendasi diambil dari Zomato." ), template_message])

# handle message berbentuk text

@handler.add(MessageEvent, message = TextMessage)
def handle_text_message(event):

    text = event.message.text
    profile = line_bot_api.get_profile(event.source.user_id) 
    
    if text == 'lapar':
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text = "Hai {}! Bisa infokan kamu sedang di mana dengan menggunakan fitur Share Location?".format(profile.display_name)))
    else:
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text = "Maaf, saya belum belajar bahasa manusia :("))

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)