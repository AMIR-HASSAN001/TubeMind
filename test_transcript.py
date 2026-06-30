from transcript import fetch_transcript

url = input("Enter YouTube URL: ")

text = fetch_transcript(url)

print("\nTranscript Preview:\n")
print(text[:1000])