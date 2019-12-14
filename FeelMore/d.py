from gtts import gTTS

input_word = input("input: ")
ek = gTTS(text=input_word, lang='en-GB')
ek.save('영국 발음.mp3')
en = gTTS(text=input_word, lang='en-US')
en.save('미국 발음.mp3')
print('Text converted successfully')