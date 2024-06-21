import azure.cognitiveservices.speech as speechsdk
import base64
import os
speech_key = os.environ.get("AZURE_SPEECH_KEY")
service_region = os.environ.get("AZURE_SPEECH_REGION")

speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)

options = {
    "male": "en-US-AndrewNeural",
    "female": "en-US-JennyNeural",
}


def synthesize_text(text, voice):
    speech_config.speech_synthesis_voice_name = options[voice]
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)
    result = speech_synthesizer.speak_text_async(text).get()
    # Check result
    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("Speech synthesized for text [{}]".format(text))
        audio_data = result.audio_data
        audio_base64 = base64.b64encode(audio_data).decode('utf-8')
        return {
            "audio": audio_base64,
            "text": text,
        }
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print("Speech synthesis canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))
    
