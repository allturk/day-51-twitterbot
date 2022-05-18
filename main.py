from intspeedtwitbot import InternetSpeedTwitterBot
import time

bot = InternetSpeedTwitterBot()
bot.get_internet_speed()
bot.tweet_at_provider()

time.sleep(3)
bot.close_browser()