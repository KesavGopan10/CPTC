from django.shortcuts import render
from .models import AudioFiles , TextFiles , UploadedFiles , Doctor , DoctorText
import io
import os       
from django.shortcuts import render
from dotenv import load_dotenv
from openai import OpenAI
from django.core.files.base import ContentFile
from paddleocr import PaddleOCR,draw_ocr
# Paddleocr supports Chinese, English, French, German, Korean and Japanese.
# You can set the parameter `lang` as `ch`, `en`, `fr`, `german`, `korean`, `japan`
# to switch the language model in order.
ocr = PaddleOCR(use_angle_cls=True, lang='en')
# Create your views here.


load_dotenv()  # take environment variables from .env.
api_key = os.getenv('api_key')  

client = OpenAI(
    api_key = api_key
)

def home(request):
    return render(request, 'app/home.html')



def transcribe_audio(request):
    if request.method == 'POST':
        audio_file = request.FILES['audio_file']
        # Save the uploaded audio file to the AudioFiles database
        audio_instance = AudioFiles(audio_file=audio_file)
        audio_instance.save()

        # Read the saved file and send to OpenAI API for transcription
        with io.open(audio_instance.audio_file.path, 'rb') as f:
            transcription = client.audio.transcriptions.create(
                model="whisper-1",
                file=f,
                response_format="text"
            )
            if transcription:
                completion = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a report building assistant , skilled in creating  report with given text including 3 heading detail with content about patient , content of patient with detail abput the consultation and medicine with detail of medicine of patient in english language."},
                        {"role": "user", "content": transcription}
                    ]
                )

                output = completion.choices[0].message.content

                # Save the output to a TextFile database
                
                text_instance = TextFiles(text_file=ContentFile(output.encode(), name='output.txt'))
                text_instance.save()
                # Return the download URL in the render
                return render(request, 'app/audio_to_text.html', {'output': output, 'download_url': text_instance.text_file.url})
                # Save the output to a TextFile database
                

    return render(request, 'app/audio.html')

def upload_file(request):
    if request.method == 'POST':

        uploaded_file = request.FILES['input_file']
        
        if uploaded_file:
            file_instance = UploadedFiles(file_upload=uploaded_file)

            file_instance.save()
            img_path = file_instance.file_upload.path
            result = ocr.ocr(img_path, cls=True)
            l = [] 
            for idx in range(len(result)):
                res = result[idx]
                for line in res:
                    print(line)
                    l.append(line[1][0])
            
            k = ' '.join(l)
            if k:
                completion = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a medical report  assistant, skilled in explaining any report with all detail and possible content"},
                        {"role": "user", "content": k}
                    ]
                )

                output = completion.choices[0].message.content
                
                print(output)
                text_instance = TextFiles(text_file=ContentFile(output.encode(), name='output.txt'))
                text_instance.save()
                return render(request, 'app/upload.html' , {'sucess' : output , 'download_url' : text_instance.text_file.url})

    return render(request, 'app/upload.html')


def docdet(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        age = request.POST.get('age')
        weight = request.POST.get('weight')
        height = request.POST.get('height')
        symptoms = request.POST.get('symptom')
        if name:
            
            k = Doctor.objects.filter(department__contains=symptoms).first()
            completion = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a doctor assistant, skilled in explaining any problem and possible content  with details like name , age , weight , height , sysmtoms"},  
                    {"role": "user", "content": f'name - { name } , age - { age } , wieght - { weight } , height - { height } , symptoms - { symptoms }'},
                    {"role": "user", "content": f"genarate it as a report"}
                ]
            )
            output = completion.choices[0].message.content

            text_instance = TextFiles(text_file=ContentFile(output.encode(), name='output.txt'))
            text_instance.save()
            
            if k:
                text_instance_ = DoctorText(doctor = k , text_file=ContentFile(output.encode(), name='output.txt'))
                text_instance_.save()
            return render(request, 'app/docdet.html', {'output': output , 'download_url' : text_instance.text_file.url})
    return render(request, 'app/docdet.html', {})

def emo(request):
    if request.method == 'POST':
        name = request.POST.get('n')
        age = request.POST.get('n1')
        weight = request.POST.get('n2')
        height = request.POST.get('n3')
        symptoms = request.POST.get('n4')
        if name:
            
            
            completion = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a phycologist assistant, skilled in explaining mental problem and struggle and different method to takele from a set of question and andswer"},  
                    {"role": "user", "content": f"""question - How often do you feel overwhelmed by your emotions or find it difficult to control them?
Have you experienced a significant change in your sleeping patterns, appetite, or energy levels recently?
Do you often feel hopeless, empty, or like life lacks meaning?
Have you noticed a decrease in your interest or pleasure in activities you once enjoyed?
Do you frequently experience intense mood swings or persistent feelings of sadness, anxiety, or irritability?"""},
                    {"role": "user", "content": f'answer - 1 - { name } , 2 - { age } , 3 - { weight } , 4 - { height } , 5 - { symptoms }'},
                    {"role": "user", "content": f"genarate it as a report"}
                ]
            )
            output = completion.choices[0].message.content

            text_instance = TextFiles(text_file=ContentFile(output.encode(), name='output.txt'))
            text_instance.save()
            
            
            return render(request, 'app/emo.html', {'output': output , 'download_url' : text_instance.text_file.url})
    return render(request, 'app/emo.html', {})




