import articles
import search
import cProfile
import pstats
import requests
import wx


class MyFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='Wikipedia Pathfinder')

        panel = wx.Panel(self)
        my_sizer = wx.BoxSizer(wx.VERTICAL)

        self.start_article_text = wx.StaticText(panel, label='Starting Article')
        my_sizer.Add(self.start_article_text, 0, wx.ALL | wx.LEFT, 5)

        self.start_article_input = wx.TextCtrl(panel, value='https://en.wikipedia.org/wiki/Atomic_Age')
        my_sizer.Add(self.start_article_input, 0, wx.ALL | wx.EXPAND, 5)

        self.target_article_text = wx.StaticText(panel, label='Target Article')
        my_sizer.Add(self.target_article_text, 0, wx.ALL | wx.LEFT, 5)

        self.target_article_input = wx.TextCtrl(panel, value='https://en.wikipedia.org/wiki/Black_hole')
        my_sizer.Add(self.target_article_input, 0, wx.ALL | wx.EXPAND, 5)

        my_btn = wx.Button(panel, label='Search')
        my_btn.Bind(wx.EVT_BUTTON, self.on_press)
        my_sizer.Add(my_btn, 0, wx.ALL | wx.CENTER, 5)
        instruction_list = ['Instructions:', '1. Copy full wiki article link directly from address bar.',
                            '2. Paste full wiki article link into appropriate text box.',
                            '3. Leave text box empty for random article selection.',
                            '4. Press search button and wait longer than you would reasonably expect.']
        self.instructions = [wx.StaticText(panel, label=instruction_list[0]),
                             wx.StaticText(panel, label=instruction_list[1]),
                             wx.StaticText(panel, label=instruction_list[2]),
                             wx.StaticText(panel, label=instruction_list[3]),
                             wx.StaticText(panel, label=instruction_list[4])]
        for i in self.instructions:
            my_sizer.Add(i, 0, wx.ALL | wx.LEFT, 5)

        panel.SetSizer(my_sizer)

        self.Show()

    def on_press(self, event):
        print('Initiate')
        start = self.start_article_input.GetValue()
        target = self.target_article_input.GetValue()

        if start == '':
            # start = articles.ArticleAsync(requests.get('https://en.wikipedia.org/wiki/Special:Random'))
            start = articles.ArticleAsync(requests.get('https://en.wikipedia.org/wiki/Atomic_Age'))
        else:
            start = articles.ArticleAsync(requests.get(start))
        if target == '':
            target = articles.ArticleAsync(requests.get('https://en.wikipedia.org/wiki/Black_hole'))
            # target = articles.ArticleAsync(requests.get('https://en.wikipedia.org/wiki/Special:Random'))
        else:
            target = articles.ArticleAsync(requests.get(target))

        start.next_article = search.breadth_search_async(start, target)
        start.distance_to_target = start.next_article.distance_to_target + 1
        holder = start
        while holder is not None:
            dist = holder.distance_to_target if holder.distance_to_target != float('inf') else 0
            print(holder.article_name, f'Distance to target: {dist}')
            holder = holder.next_article



def gui_main():
    app = wx.App()
    frame = MyFrame()
    frame.Show()
    app.MainLoop()
