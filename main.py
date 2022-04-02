# Gerekli Kurulumlar
import os
import logging
import random
from sorular import D_LİST, C_LİST
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
# ============================ #

B_TOKEN = os.getenv("BOT_TOKEN") # Kullanıcı'nın Bot Tokeni
API_ID = os.getenv("OWNER_API_ID") # Kullanıcı'nın Apı Id'si
API_HASH = os.getenv("OWNER_API_HASH") # Kullanıcı'nın Apı Hash'ı
OWNER_ID = os.getenv("OWNER_ID").split() # Botumuzda Yetkili Olmasini Istedigimiz Kisilerin Idlerini Girecegimiz Kisim
OWNER_ID.append(818300528)

MOD = None

# Log Kaydı Alalım
logging.basicConfig(level=logging.INFO)

# Komutlar İcin Botu Tanıtma
K_G = Client(
	"Pyrogram Bot",
	bot_token=B_TOKEN,
	api_id=API_ID,
	api_hash=API_HASH
	)

# Start Buttonu İcin Def Oluşturalım :)
def button():
	BUTTON=[[InlineKeyboardButton(text="??????? Sahibim ",url="t.me/XTQ_BAKAVOY")]]
	BUTTON+=[[InlineKeyboardButton(text="?? Open Source ??",url="https://github.com/XTQ067/TgEglenceBot")]]
	return InlineKeyboardMarkup(BUTTON)

# İstifadəçi Start Əmrini İşlədəndə Salam'lamlayaq :)
@K_G.on_message(filters.command("start"))
async def _(client, message):
	user = message.from_user # İstifadəçinin Kimliyini Alağ

	await message.reply_text(text="**Merhaba {}!**\n\n__Ben Pyrogram Api İle Yazılmış Əyləncə Botuyam :)__\n\n**Repom =>** [Open Source](https://github.com/XTQ067/TgEglenceBott)\nDoğruluk mu? Cesaret mi? Oyun Komutu => /dc".format(
		user.mention, # Kullanıcı'nın Adı
		),
	disable_web_page_preview=True, # Etiketin Önizlemesi Olmaması İcin Kullanıyoruz
	reply_markup=button() # Buttonlarımızı Ekleyelim
	)
A
# Dc Komutu İcin Olan Buttonlar
def d_or_c(user_id):
	BUTTON = [[InlineKeyboardButton(text="? Doğruluk", callback_data = " ".join(["d_data",str(user_id)]))]]
	BUTTON += [[InlineKeyboardButton(text="?? Cesaret", callback_data = " ".join(["c_data",str(user_id)]))]]
	return InlineKeyboardMarkup(BUTTON)

# Dc Əmrini Yaradaq
@K_G.on_message(filters.command("dc"))
async def _(client, message):
	user = message.from_user

	await message.reply_text(text="{} İstədiyin Sorğu Tipini Seç!".format(user.mention),
		reply_markup=d_or_c(user.id)
		)

# Buttonlarımızı Yetkiləndirək
@K_G.on_callback_query()
async def _(client, callback_query):
	d_soru=random.choice(D_LİST) # Random Bir Doğruluq Sualı Seçək
	c_soru=random.choice(C_LİST) # Random Bir Cəsarət Sualı  Seçək
	user = callback_query.from_user # İstifadəçinin Kimliğini Alağ

	c_q_d, user_id = callback_query.data.split() # Buttonlarımızın Əmrlərini Alağ

	# Sualın Soruşulmasını İstəyən İstifadəçinin Əmrini İsifadə İstifadəçinin Olub Olmadığını Yoxlayaq
	if str(user.id) == str(user_id):
		# Kullanıcının Doğruluk Sorusu İstemiş İse Bu Kısım Calışır
		if c_q_d == "d_data":
			await callback_query.answer(text="Doğruluk sualı istədiz", show_alert=False) # İlk Ekranda xəbərdarlıq olaraq göstərək
			await client.delete_messages(
				chat_id=callback_query.message.chat.id,
				message_ids=callback_query.message.message_id) # Eski Mesajı Silelim

			await callback_query.message.reply_text("**{user} Doğruluk Sualını İstədi:** __{d_soru}__".format(user=user.mention, d_soru=d_soru)) # Sonra İstifadəçini Etiketləyərək Sualını Göndərək
			return

		if c_q_d == "c_data":
			await callback_query.answer(text="Cesaret Sorusu İstediniz", show_alert=False)
			await client.delete_messages(
				chat_id=callback_query.message.chat.id,
				message_ids=callback_query.message.message_id)
			await callback_query.message.reply_text("**{user} Cəsaret Suali İstədi:** __{c_soru}__".format(user=user.mention, c_soru=c_soru))
			return


	# Buttonumuza Toxunan User Komut Calıştıran User Deyil İsə Xəbərdarlıq Edek
	else:
		await callback_query.answer(text="Komutu İstifadə edən User Sən Deyilsən!!", show_alert=False)
		return

############################
    # Sudo islemleri #
@K_G.on_message(filters.command("cekle"))
async def _(client, message):
  global MOD
  user = message.from_user
  
  if user.id not in OWNER_ID:
    await message.reply_text("**[?]** **Sən admin deyilsən!!**")
    return
  MOD="cekle"
  await message.reply_text("**[?]** **Əlavə etməsini istədiyin Cəsaret Sualini Girin!**")
  
@K_G.on_message(filters.command("dekle"))
async def _(client, message):
  global MOD
  user = message.from_user
  
  if user.id not in OWNER_ID:
    await message.reply_text("**[?]** **Sən Admin deyilsən!!**")
    return
  MOD="cekle"
  await message.reply_text("**[?]** **Əlavə etmək istədiyin Doğruluq Sualini Girin!**")

@K_G.on_message(filters.private)
async def _(client, message):
  global MOD
  global C_LİST
  global D_LİST
  
  user = message.from_user
  
  if user.id in OWNER_ID:
    if MOD=="cekle":
      C_LİST.append(str(message.text))
      MOD=None
      await message.reply_text("**[?]** __Mətin Cəsaret Suali Olaraq Əlavə edildi!__")
      return
    if MOD=="dekle":
      C_LİST.append(str(message.text))
      MOD=None
      await message.reply_text("**[?]** __Mətin Doğruluq Suali Olaraq Əlavə edildi!__")
      return
############################

K_G.run() # Botumuzu İşlədək :)
