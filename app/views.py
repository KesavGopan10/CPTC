from django.shortcuts import render
from .models import AudioFiles , TextFiles
import io
import os       
from django.shortcuts import render
from dotenv import load_dotenv
from openai import OpenAI
from django.core.files.base import ContentFile
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
