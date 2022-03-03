import articles
import search
# import cProfile
# import pstats
import requests
import wx


'''
What can I say about GUIs except I'm no good at them. I'm not even convinced I will stick with wxPython. As of 3/3/22
this GUI is just a place holder and only handles accepting input. There are several new screens that need to be made, 
it's Frankenstein-ed together from RealPython's tutorial https://realpython.com/python-gui-with-wxpython/ and 
I generally am not sure if I'm doing it right though the answer is probably no.
'''


class MyFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='Wikipedia Pathfinder')

        panel = wx.Panel(self)
        my_sizer = wx.BoxSizer(wx.VERTICAL)

        # The text label for the start url input
        self.start_article_text = wx.StaticText(panel, label='Starting Article')
        my_sizer.Add(self.start_article_text, 0, wx.ALL | wx.LEFT, 5)

        # The input box for start url
        self.start_article_input = wx.TextCtrl(panel, value='https://en.wikipedia.org/wiki/Atomic_Age')
        my_sizer.Add(self.start_article_input, 0, wx.ALL | wx.EXPAND, 5)

        # The text label for the target url input
        self.target_article_text = wx.StaticText(panel, label='Target Article')
        my_sizer.Add(self.target_article_text, 0, wx.ALL | wx.LEFT, 5)

        # The input box for target url
        self.target_article_input = wx.TextCtrl(panel, value='https://en.wikipedia.org/wiki/Black_hole')
        my_sizer.Add(self.target_article_input, 0, wx.ALL | wx.EXPAND, 5)

        # The go button
        my_btn = wx.Button(panel, label='Search')
        my_btn.Bind(wx.EVT_BUTTON, self.on_press)
        my_sizer.Add(my_btn, 0, wx.ALL | wx.CENTER, 5)

        # Instructions for the imaginary person that might be using this
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

        # What this should do is find a random wiki article in the case that nothing was entered into the input boxes
        # However it doesn't seem to be working like that.
        # TODO: Article object creation filters are messing with the random article request, add condition for random
        if start == '':
            start = articles.ArticleAsync(requests.get('https://en.wikipedia.org/wiki/Special:Random'))
        else:
            start = articles.ArticleAsync(requests.get(start))

        if target == '':
            target = articles.ArticleAsync(requests.get('https://en.wikipedia.org/wiki/Special:Random'))
        else:
            target = articles.ArticleAsync(requests.get(target))

        # TODO: Move these out of GUI, maybe into search algo
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
