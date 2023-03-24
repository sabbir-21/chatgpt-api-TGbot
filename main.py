import os, json
try:
    from pyrogram import Client, filters
    from pyrogram.types import Message
    import openai
    from dotenv import load_dotenv
    
except ImportError:
    os.system("pip install pyrogram")
    os.system("pip install openai")
    os.system("pip install python-dotenv")
    from pyrogram import Client, filters
    from pyrogram.types import Message
    import openai
    from dotenv import load_dotenv

load_dotenv()
bot_token = os.environ.get('BOT_TOKEN')
api = os.environ.get('API_KEY')
hash = os.environ.get('API_HASH')

webdl = Client("sabbir21", bot_token=bot_token, api_id=api, api_hash=hash)

print('Running')

def api():
    completion = openai.ChatCompletion.create(model="gpt-3.5-turbo",messages=[{"role": "user", "content": question}])
    if completion.choices[0].message!=None:
        return completion.choices[0].message
    else :
        return 'Failed to Generate response!'

@webdl.on_message(filters.command(["start"]))
async def start(_, message: Message):
    text = "Welcome to ChatGPT bot! \nBefore using, send command ```\n /set OPENAI_API_KEY \n```"
    await message.reply_text(text=text)

@webdl.on_message(filters.command(["set"]))
async def set(_, message: Message):
    gptapi = message.text
    userid = message.from_user.id
    gptapi= gptapi.split('/set ')[1]
    try:
        with open("read_api.txt", "r") as f:
            lines = f.readlines()
    except FileNotFoundError:
        lines = []
    was_updated = False
    for i, line in enumerate(lines):
        if str(userid) in line:
            lines[i] = f"{userid}:{gptapi}\n"
            was_updated = True
            break
    if not was_updated:
        lines.append(f"{userid}:{gptapi}\n")
    with open("read_api.txt", "w") as f:
        f.writelines(lines)
    if was_updated:
        text = "API updated successfully"
    else:
        text = "API set successfully"

    await message.reply_text(text=text+'\n'+'User id: '+str(userid)+"\nLet's chat and explore together. Type question for assistance.")

@webdl.on_message(filters.text)
async def chat(_, message: Message):
    global question
    question = str(message.text)
    userid = message.from_user.id
    with open("read_api.txt", "r") as f:
        lines = f.readlines()
    for line in lines:
        if str(userid) in line:
            openai.api_key = line.split(":")[1].strip()
            try:
                res = api()
                sim = str(res)
                data = json.loads(sim)
                cont = data['content']
                await message.reply_text(text=cont, disable_web_page_preview=True, quote=True)
            except Exception as e:
                await message.reply_text(text=e, disable_web_page_preview=True, quote=True)
            break
    else:
        await message.reply_text(text="You haven't set your API key yet. Use the command ```\n /set OPENAI_API_KEY \n``` to set your OpenAI API key.")

webdl.run()
