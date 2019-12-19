import os

from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from sdk.api.message import Message

base_url = "https://www.rightteeth.com/"
time_list = {"육평": "6", "구평": "9", "수능": "final"}
subject_list = {"국어": "kor", "수리 가": "math-1", "수리": "math-1", "수리 나": "math-2"}


class PengsuTeacher(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data["action"]["parameters"]

        # "2019년 / 6평 / 수리 가 / 16번 문제"
        print(data)
        year = data["BID_DT_CYEAR"]["value"]
        test = data["test"]["value"]  # NUGU에게 그대로 던져줌
        _test = time_list[test]  # sns에 url로 사용됨
        subject = data["subject"]["value"]  # NUGU에게 그대로 던져줌
        _subject = subject_list[subject]  # sns에 url로 사용됨
        question = data["question"]["value"]

        # Send solution url by sms
        question_url = f"{year}-{_test}-{_subject}#{question}"
        url = f"{base_url}q/{question_url}"

        params = dict()
        params["type"] = "sms"
        params["to"] = "01041928818,01027868089"
        params["from"] = "01041928818"
        params["text"] = f"당신의 공부 도우미 펭수입니다. {url}"

        cool = Message(os.environ.get("sms_api_key"), os.environ.get("sms_api_secret"))
        response = cool.send(params)
        print(response)

        response_builder = {
            "version": "2.0",
            "resultCode": "OK",
            "output": {
                "year": year,
                "time": test,
                "subject": subject,
                "question": question,
            },
        }
        return Response(response_builder)


class PengsuListening(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        # data = getattr(request.data["action"]["parameters"])
        #
        # # "2019년 / 수능 / 영어듣기 / 1번 문제" 재생해줘
        # # "2019년 / 수능 / 영어듣기" 재생해줘
        # year = getattr(data["BID_DT_CYEAR"]["value"])
        # test = getattr(data["test"]["value"])
        # test = getattr(time_list[test])
        # question = getattr(data["question"]["value"])

        response_builder = {
            "version": "2.0",
            "resultCode": "OK",
            "output": {},
            "directives": [
                {
                    "type": "AudioPlayer.Play",
                    "audioItem": {
                        "stream": {
                            "url": "https://res.cloudinary.com/googit/video/upload/v1576762107/SAT/eng_listening/muxed_ikfu02.mp3",
                            "offsetInMilliseconds": 0,
                            "progressReport": {
                                "progressReportDelayInMilliseconds": 0,
                                "progressReportIntervalInMilliseconds": 0,
                            },
                            "token": "Way_back_home",
                        }
                    },
                }
            ],
        }
        return Response(response_builder)
