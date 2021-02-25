from transitions.extensions import GraphMachine

from utils import send_text_message
from utils import send_button_message
from utils import send_choose_message


class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)


    def is_going_to_hungry(self, event):
        text = event.message.text
        return text.lower() == "從頭開始"

    def on_enter_hungry(self, event):
        print("I'm entering hungry")

        reply_token = event.reply_token
        send_choose_message(reply_token,'https://i.imgur.com/wRJQghC.png',"緊急特豹","你是一隻小海豹，月底，飢腸轆轆的你不得不去覓食，但此時你只有65元...","育樂街將就一下吧","高級自助餐!!!")


    def is_going_to_yule(self, event):
        text = event.message.text
        return text.lower() == "育樂街將就一下吧"

    def on_enter_yule(self, event):
        print("I'm entering yule")

        reply_token = event.reply_token
        
        send_choose_message(reply_token,'https://i.imgur.com/G4vilT2.png',"性命攸關","此刻一個關係到你未來的抉擇擺在你面前----吃啥...","我大煦悅","活力小廚")
        
    def is_going_to_xuyue(self, event):
        text = event.message.text
        return text.lower() == "我大煦悅"

    def on_enter_xuyue(self, event):
        print("I'm entering xuyue")

        reply_token = event.reply_token

        send_button_message(reply_token,'https://i.imgur.com/Qc44A5b.png',"尊榮獨享","經過重重難關，你終於成功了--煦悅的美味焢肉飯，還有喝不完的綠豆湯...","暴飲暴食")

    
    def is_going_to_win(self, event):
        text = event.message.text
        return text.lower() == "暴飲暴食"

    def on_enter_win(self, event):
        print("I'm entering win")

        reply_token = event.reply_token
        
        send_button_message(reply_token,'https://i.imgur.com/xdnAtg7.png',"功成身退","酒足飯飽過後，你充實而欣慰，有錢人的快樂，就是這麼樸實無華，且枯燥...","從頭開始")
        self.go_back()

    def is_going_to_huoli(self, event):
        text = event.message.text
        return text.lower() == "活力小廚"

    def on_enter_huoli(self, event):
        print("I'm entering huoli")

        reply_token = event.reply_token
        
        send_choose_message(reply_token,'https://i.imgur.com/YLD7gJj.png',"生死交關","此時，一件意想不到的事發生了，大概有八百人在排隊!!!此時你應該...","我大煦悅","堅持到底")
    
    def is_going_to_queue(self, event):
        text = event.message.text
        return text.lower() == "堅持到底"

    def on_enter_queue(self, event):
        print("I'm entering queue")

        reply_token = event.reply_token
        
        send_button_message(reply_token,'https://i.imgur.com/RjNGPAw.png',"白駒過隙","\"我可以慢慢等...\"但是人實在太多了，直到關門你都沒能買到便當...","一敗塗地")
        

    def is_going_to_buffet(self, event):
        text = event.message.text
        return text.lower() == "高級自助餐!!!"

    def on_enter_buffet(self, event):
        print("I'm entering buffet")

        reply_token = event.reply_token
        
        send_choose_message(reply_token,'https://i.imgur.com/M7aoGbU.png',"世紀難題","以本公子的身分，當然是吃高級Buffet了，不過今天要吃哪一間呢...","饗食天堂","漢來海港")

        
    def is_going_to_xiangshi(self, event):
        text = event.message.text
        return text.lower() == "饗食天堂"

    def on_enter_xiangshi(self, event):
        print("I'm entering xiangshi")

        reply_token = event.reply_token
        
        send_button_message(reply_token,'https://i.imgur.com/LtKBxlV.png',"身無長物","就說你只有65塊了...","一敗塗地")

    def is_going_to_hanlai(self, event):
        text = event.message.text
        return text.lower() == "漢來海港"

    def on_enter_hanlai(self, event):
        print("I'm entering hanlai")

        reply_token = event.reply_token
        
        send_button_message(reply_token,'https://i.imgur.com/LtKBxlV.png',"身無長物","就說你只有65塊了...","一敗塗地")
   

    def is_going_to_defeat(self, event):
        text = event.message.text
        return text.lower() == "一敗塗地"

    def on_enter_defeat(self, event):
        print("I'm entering defeat")

        reply_token = event.reply_token
        
        send_button_message(reply_token,'https://i.imgur.com/2YLUX87.png',"時光倒流","你拿起街邊的破碗，本來準備要就地行乞，突然眼前出現了月光寶盒...","從頭開始")
        self.go_back()

    
    def is_going_to_interrupt(self, event):
        text = event.message.text
        return text.lower() == "誰"

    def on_enter_interrupt(self, event):
        print("I'm entering interrupt")

        reply_token = event.reply_token
        
        send_button_message(reply_token,'https://i.imgur.com/M0R5FCw.png',"風雲變色","一道閃電砸下，讓眼前的一切都灰飛煙滅，一切回到從前...","從頭開始")
        self.go_back()
   
        