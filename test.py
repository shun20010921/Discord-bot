# インストールした discord.py を読み込む
import discord

# 自分のBotのアクセストークンに置き換えてください
TOKEN = ''

# 接続に必要なオブジェクトを生成
client = discord.Client()

helpmess="""

九工大Discord鯖の教科別テキストチャンネルの管理botです。

チャンネルの命名規則は "[教科名]-[先生名]"で統一してください。
また、Ⅰはⅰ、Ⅱはⅱなど、大文字ギリシャ文字やCはc、など大文字アルファベットをチャンネル名に使用することはできないので、小文字で登録をお願いします。
じゃないと**バグります。**

各コマンドに2つ以上の因数がある場合は１つの半角スペースで区切るようにしてください。
教科を作成したいときは[/create]コマンドを使用してください。
何かエラーが起きた時は、もう一度しっかりと入力しているrole名やchannel名が正しいかどうかを確認し、それでも解決しない場合は　`Shun#2950`　まで連絡ください。

>>> コマンド一覧(すべてのコマンドは"/"で始められる必要があります。)
"/help","/h" : このヘルプメッセージを表示します。
"/delrole [role名]" : [role名]の役職を削除します。
"/addrole [role名]" : [role名]の役職を作成します。
"/setrole [channel名]" : [channel名]の既存のテキストチャンネルに権限設定、権限が存在しなければ作成します。
"/get [channel名]" : [channel名]の閲覧権限を付与します。
"/create [channel名]" : [channel名]のチャンネル、roleを作成し、発言者に閲覧権限を付与します。
"/list" : 教科のチャンネル一覧を表示します。

"""

# 起動時に動作する処理
@client.event
async def on_ready():
    # 起動したらターミナルにログイン通知が表示される
    print('ログインしました')

# メッセージ受信時に動作する処理
@client.event
async def on_message(message):
    try:
        # メッセージ送信者がBotだった場合は無視する
        if message.author.bot:
            return
        if message.content=='/list':
            text = ""
            for ch in message.guild.text_channels:
                if ch.category_id == 711163039919112243:
                    text += str(ch.name)+"\n"
            print(text)
            await message.channel.send(text)
        if message.content=='/help':
            await message.channel.send(helpmess)
            return
        if message.content=='/h':
            await message.channel.send(helpmess)
            return
        if message.content.startswith('/delrole '):
            guild = message.guild
            rolename = message.content.replace("/delrole ","")
            role = discord.utils.get(guild.roles, name=rolename)
            if role == None:
                await message.channel.send(rolename+'の役職はもともと存在しません。')
            else:
                await role.delete()
                await message.channel.send(rolename+'の役職を削除しました。')
            return

        if message.content.startswith('/addrole '):
            rolename = message.content.replace("/addrole ","")
            guild = message.guild
            await guild.create_role(name=rolename)
            await message.channel.send(rolename+'の役職を作成しました。')
            return

        if message.content.startswith('/setrole '):
            rolename = message.content.replace("/setrole ","")
            guild = message.guild

            exsr = discord.utils.get(guild.roles, name=rolename)
            if exsr == None:
                role = await guild.create_role(name=rolename)
                await message.channel.send(rolename+'roleを作成しました。')

            channel = discord.utils.get(guild.text_channels, name=rolename)
            if channel == None:
                await message.channel.send(rolename+'チャンネルが存在しません。')
                return
            else:
                await channel.set_permissions(role,read_messages=True,send_messages=True)
                rolee = discord.utils.get(guild.roles, name="@everyone")
                await channel.set_permissions(rolee,read_messages=False,send_messages=False)
                await message.channel.send(rolename+'チャンネルの権限設定完了しました。')
                return

        if message.content.startswith('/get '):
            guild = message.guild
            cmd_search = str(message.content)
            role_name = cmd_search.replace("/get ","")
            exsr = discord.utils.get(guild.roles, name=role_name)

            if exsr == None:
                await message.channel.send(role_name+'のroleは存在していません。')
                await message.channel.send('チャンネルが作成されているかどうか確認してください。')
                return
            else:
                member = guild.get_member(message.author.id)
                await member.add_roles(exsr)#発言者に権限付与
                await message.channel.send(role_name+'の閲覧権限を付与しました。')
                return
        if message.content.startswith('/create '):
            category_id = 711163039919112243 #教科カテゴリ
            category = message.guild.get_channel(category_id)
            guild = message.guild

            cmd_search = str(message.content)
            ch_name = cmd_search.replace("/create ","")

            exs = discord.utils.get(message.guild.text_channels, name=ch_name)

            if exs == None:
                new_channel = await category.create_text_channel(name= ch_name)
                reply = f'{new_channel.mention} を作成しました。'
                await message.channel.send(reply)
            else:
                await message.channel.send('既に'+ch_name+'チャンネルは存在しています。')
                await message.channel.send('正常に終了しませんでした。手動で操作してください。')
                return

            exsr = discord.utils.get(guild.roles, name=ch_name)

            if exsr == None:
                role = await guild.create_role(name=ch_name)
                member = guild.get_member(message.author.id)
                await member.add_roles(role)#発言者に権限付与
                reply2 = f'{role.mention} を作成しました'
                await message.channel.send(reply2)
                await message.channel.send(+ch_name+'の閲覧権限を付与しました。')
            else:
                await message.channel.send('既に'+ch_name+'のroleは存在しています。')
                await message.channel.send('正常に終了しませんでした。手動で操作してください。')
                return

            await new_channel.set_permissions(role,read_messages=True,send_messages=True)
            rolee = discord.utils.get(guild.roles, name="@everyone")
            await new_channel.set_permissions(rolee,read_messages=False,send_messages=False)
            await message.channel.send(ch_name+'チャンネルの権限設定完了しました。')

            report_channel = client.get_channel(711182674894651430)
            await report_channel.send(reply)

            return
    except Exception as e:
        await message.channel.send("予期せぬエラーが発生しました。")
        await message.channel.send(str(e))
        return


# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)