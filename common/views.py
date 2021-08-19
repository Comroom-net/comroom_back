from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from utils import telegrambot


@api_view(['POST'])
def send_telegram(request):
    msg = request.data.get('msg')
    sender = request.data.get('sender')
    contact = request.data.get('contact')

    if sender:
        msg += f"\n보내는 사람: {sender}"
    if contact:
        msg += f"\n연락처: {contact}"

    telegrambot.send_msg(msg)

    return Response(status=status.HTTP_200_OK)