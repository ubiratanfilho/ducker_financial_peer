### YouTube Summarizer

# This script retrieves all videos from a YouTube playlist, and generates a dataset with the transcriptions of them. In this project, it is used to synthetsize data for a Financial LLM Application.

### References
# - https://github.com/DevRico003/youtube_summarizer

# Dependencies
from youtube_transcript_api import YouTubeTranscriptApi

# getting the transcript of a video
def get_transcript(youtube_url):
    video_id = youtube_url.split("v=")[-1]
    transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

    # Try fetching the manual transcript
    try:
        transcript = transcript_list.find_manually_created_transcript()
        language_code = transcript.language_code  # Save the detected language
    except:
        # If no manual transcript is found, try fetching an auto-generated transcript in a supported language
        try:
            generated_transcripts = [trans for trans in transcript_list if trans.is_generated]
            transcript = generated_transcripts[0]
            language_code = transcript.language_code  # Save the detected language
        except:
            # If no auto-generated transcript is found, raise an exception
            raise Exception("No suitable transcript found.")

    full_transcript = " ".join([part['text'] for part in transcript.fetch()])
    return full_transcript, language_code  # Return both the transcript and detected language

trans = get_transcript('https://www.youtube.com/watch?v=mINrILM4LeM&list=PLDlxlCF-E-Dd1vyFCYR5IUdEeLbtuQBLp&index=1')
print(trans[0])