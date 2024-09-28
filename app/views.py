# views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import win32print
import win32ui
from PIL import Image, ImageWin
import os

# 프린터에 이미지를 출력하는 함수
def print_image(file_path):
    try:
        PHYSICALWIDTH = 110
        PHYSICALHEIGHT = 111

        # 기본 프린터 가져오기
        printer_name = win32print.GetDefaultPrinter()

        # 프린터 장치 컨텍스트 생성
        hDC = win32ui.CreateDC()
        hDC.CreatePrinterDC(printer_name)

        # 프린터 해상도 가져오기
        printer_size = hDC.GetDeviceCaps(PHYSICALWIDTH), hDC.GetDeviceCaps(PHYSICALHEIGHT)

        # 이미지 불러오기
        bmp = Image.open(file_path)

        # 세로로 긴 이미지 회전
        if bmp.size[0] < bmp.size[1]:
            bmp = bmp.rotate(90, expand=True)  # expand=True로 회전 후 전체 크기 유지

        # 이미지와 프린터 크기 비율 계산
        img_ratio = bmp.size[0] / bmp.size[1]  # 이미지 가로/세로 비율
        printer_ratio = printer_size[0] / printer_size[1]  # 프린터 가로/세로 비율

        # 비율에 맞춰 출력 크기 계산
        if img_ratio > printer_ratio:
            # 이미지가 더 가로로 길 경우, 프린터의 가로 크기에 맞춤
            new_width = printer_size[0]
            new_height = int(printer_size[0] / img_ratio)
        else:
            # 이미지가 더 세로로 길 경우, 프린터의 세로 크기에 맞춤
            new_height = printer_size[1]
            new_width = int(printer_size[1] * img_ratio)

        # 프린트 작업 시작
        hDC.StartDoc(file_path)
        hDC.StartPage()

        # 이미지를 프린터에 맞게 출력
        dib = ImageWin.Dib(bmp)
        dib.draw(hDC.GetHandleOutput(), (0, 0, new_width, new_height))  # 비율 유지하며 이미지 출력

        # 프린트 작업 종료
        hDC.EndPage()
        hDC.EndDoc()
        hDC.DeleteDC()

    except Exception as e:
        raise Exception(f"프린트 작업 중 오류 발생: {str(e)}")

@csrf_exempt
def print_file(request):
    if request.method == 'POST':
        try:
            # 요청에서 파일 가져오기
            uploaded_file = request.FILES['file']
            
            # 파일을 임시로 저장 (인쇄를 위해)
            temp_file_path = f"C:\\temp\\{uploaded_file.name}"
            with open(temp_file_path, 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)

            # 이미지를 프린터로 전송
            print_image(temp_file_path)

            # 인쇄 후 파일 삭제
            os.remove(temp_file_path)

            return JsonResponse({"status": "success", "message": "프린트 작업이 완료되었습니다!"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})
    return JsonResponse({"status": "failed", "message": "잘못된 요청입니다."})
