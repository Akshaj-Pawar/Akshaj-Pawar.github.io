# 6.0001/6.00 Problem Set 5 - RSS Feed Filter
# Name:
# Collaborators:
# Time:

import feedparser
import string
import time
import threading
from project_util import translate_html
from mtTkinter import *
from datetime import datetime
import pytz


#-----------------------------------------------------------------------

#======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
#======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        description = translate_html(entry.description)
        pubdate = translate_html(entry.published)

        try:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %Z")
            pubdate.replace(tzinfo=pytz.timezone("GMT"))
          #  pubdate = pubdate.astimezone(pytz.timezone('EST'))
          #  pubdate.replace(tzinfo=None)
        except ValueError:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %z")

        newsStory = NewsStory(guid, title, description, link, pubdate)
        ret.append(newsStory)
    return ret

#======================
# Data structure design
#======================

# Problem 1

class NewsStory(object):

    def __init__(self, guid, title, description, link, pubdate):
        self._guid = guid
        self._title = title
        self._description = description
        self._link = link
        self._pubdate = pubdate

    def get_guid(self):
        return self._guid

    def get_title(self):
        return self._title

    def get_description(self):
        return self._description

    def get_link(self):
        return self._link

    def get_pubdate(self):
        return self._pubdate

#======================
# Triggers
#======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        # DO NOT CHANGE THIS!
        raise NotImplementedError

# PHRASE TRIGGERS

# Problem 2
class PhraseTrigger(Trigger):

    def is_phrase_in(self, text, trigger_phrase):
        lower_text = text.lower() + ' '
        lower_trigger_phrase = trigger_phrase.lower() + ' '
        space = False

        stripped_text = ''
        for char in lower_text:
            if char in string.punctuation:
                if space == False:
                    stripped_text += ' '
                    space = True
            elif char == ' ':
                if space == False:
                    stripped_text += char
                    space = True
            else:
                stripped_text += char
                space = False

        i = 0

        for char in stripped_text:
            if char == lower_trigger_phrase[i]:
                i += 1
            else:
                i = 0
            if i == len(lower_trigger_phrase):
                return True

        return False


# Problem 3
class TitleTrigger(PhraseTrigger):

    def __init__(self, trigger_phrase):
        self._trigger_phrase = trigger_phrase

    def get_trigger_phrase(self):
        return self._trigger_phrase

    def evaluate(self, story):
        trigger_phrase = self.get_trigger_phrase()
        text = story.get_title()
        in_phrase = self.is_phrase_in(text, trigger_phrase)
        if in_phrase:
            return True
        else:
            return False


# Problem 4
class DescriptionTrigger(PhraseTrigger):

    def __init__(self, trigger_phrase):
        self._trigger_phrase = trigger_phrase

    def get_trigger_phrase(self):
        return self._trigger_phrase

    def evaluate(self, story):
        trigger_phrase = self.get_trigger_phrase()
        text = story.get_description()
        in_phrase = self.is_phrase_in(text, trigger_phrase)
        if in_phrase:
            return True
        else:
            return False

# TIME TRIGGERS

# Problem 5
class TimeTrigger(Trigger):

    def __init__(self, time_string):
        self._trigpubdate = datetime.strptime(str(time_string), "%d %b %Y %H:%M:%S")

    def get_trigpubdate(self):
        x = (self._trigpubdate).replace(tzinfo=pytz.timezone("EST"))
        return x

# Problem 6
class BeforeTrigger(TimeTrigger):

    def evaluate(self, story):
        trigpubdate = self.get_trigpubdate()
        pubdate = story.get_pubdate()
        zoned_pubdate = pubdate.replace(tzinfo=pytz.timezone("EST"))
        if zoned_pubdate < trigpubdate:
            return True
        else:
            return False

class AfterTrigger(TimeTrigger):

    def evaluate(self, story):
        trigpubdate = self.get_trigpubdate()
        pubdate = story.get_pubdate()
        zoned_pubdate = pubdate.replace(tzinfo=pytz.timezone("EST"))
        if zoned_pubdate > trigpubdate:
            return True
        else:
            return False

# COMPOSITE TRIGGERS

# Problem 7
class NotTrigger(Trigger):

    def __init__(self, truth_trigger):
        self._truth_trigger = truth_trigger

    def get_truth_trigger(self):
        return self._truth_trigger

    def evaluate(self, story):
        return not (self._truth_trigger).evaluate(story)

# Problem 8
class AndTrigger(Trigger):

    def __init__(self, truth_trigger_A, truth_trigger_B):
        self._truth_trigger_A = truth_trigger_A
        self._truth_trigger_B = truth_trigger_B

    def get_truth_trigger_A(self):
        return self._truth_trigger_A

    def get_truth_trigger_B(self):
        return self._truth_trigger_B

    def evaluate(self, story):
        x = (self.get_truth_trigger_A()).evaluate(story)
        y = (self.get_truth_trigger_B()).evaluate(story)
        if x and y:
            return True
        else:
            return False

# Problem 9
class OrTrigger(Trigger):

    def __init__(self, truth_trigger_A, truth_trigger_B):
        self._truth_trigger_A = truth_trigger_A
        self._truth_trigger_B = truth_trigger_B

    def get_truth_trigger_A(self):
        return self._truth_trigger_A

    def get_truth_trigger_B(self):
        return self._truth_trigger_B

    def evaluate(self, story):
        x = (self.get_truth_trigger_A()).evaluate(story)
        y = (self.get_truth_trigger_B()).evaluate(story)
        if x or y:
            return True
        else:
            return False


#======================
# Filtering
#======================

# Problem 10
def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory instances.

    Returns: a list of only the stories for which a trigger in triggerlist fires.
    """

    filtered_stories = []
    for story in stories:
        for trigger in triggerlist:
            valid = trigger.evaluate(story)
            if valid:
                filtered_stories += story
                break

    return filtered_stories

#======================
# User-Specified Triggers
#======================
# Problem 11

def create_trigger(t, potential_triggers):
    for i in potential_triggers:
        if i[0] == t:
            if i[1] == 'TITLE':
                return TitleTrigger(i[2])

            if i[1] == 'DESCRIPTION':
                return DescriptionTrigger(i[2])

            if i[1] == 'AND':
                x = create_trigger(i[2], potential_triggers)
                y = create_trigger(i[3], potential_triggers)
                # recurse until you have a trigger
                return AndTrigger(x, y)

            if i[1] == 'OR':
                x = create_trigger(i[2], potential_triggers)
                y = create_trigger(i[3], potential_triggers)
                # recurse until you have a trigger
                return OrTrigger(x, y)

            if i[1] == 'NOT':
                x = create_trigger(i[2], potential_triggers)
                # recurse until you have a trigger
                return AndTrigger(x)

            if i[1] == 'AFTER':
                return AfterTrigger(i[2])

            if i[1] == 'BEFORE':
                return BeforeTrigger(i[2])

    return False


def read_trigger_config(filename):
    """
    filename: the name of a trigger configuration file

    Returns: a list of trigger objects specified by the trigger configuration
        file.
    """
    # We give you the code to read in the file and eliminate blank lines and
    # comments. You don't need to know how it works for now!
    trigger_file = open(filename, 'r')
    lines = []
    potential_triggers = []
    trigger_list = []
    stage = 0
    for line in trigger_file:
        line = line.rstrip()
        if not (len(line) == 0 or line.startswith('//')):
            lines.append(line)
    for line in lines:
        Adding = False
        potential_trigger = []
        trigger_name = ''
        trigger_type = ''
        trigger_string = ''
        for char in line:
            if char == ',':
                stage += 1
                t = ''
            elif stage == 0:
                trigger_name += char
                if trigger_name == 'ADD':

                    Adding = True
                    t += char
                    trigger = create_trigger(t, potential_triggers)
                    if trigger == False:
                        pass
                    else:
                        trigger_list += trigger

            elif (stage == 1) and (Adding == False):
                trigger_type += char
            elif (stage > 1) and (Adding == False):
                if trigger_type == 'AND':
                    pass
                if trigger_type == 'OR':
                    pass
                if trigger_type == 'NOT':
                    pass
                else:
                    trigger_string += char
        potential_trigger = [trigger_name, trigger_type, trigger_string]
        potential_triggers += potential_trigger

    return trigger_list






    # TODO: Problem 11
    # line is the list of lines that you need to parse and for which you need
    # to build triggers

    print(lines) # for now, print it so you see what it contains!



SLEEPTIME = 120 #seconds -- how often we poll

def main_thread(master):
    # A sample trigger list - you might need to change the phrases to correspond
    # to what is currently in the news
    try:
        t1 = TitleTrigger("war")
        t2 = DescriptionTrigger("Israel")
        t3 = DescriptionTrigger("Ukraine")
        t4 = AndTrigger(t2, t3)
        triggerlist = [t1, t4]

        # Problem 11
        # TODO: After implementing read_trigger_config, uncomment this line 
        # triggerlist = read_trigger_config('triggers.txt')
        
        # HELPER CODE - you don't need to understand this!
        # Draws the popup window that displays the filtered stories
        # Retrieves and filters the stories from the RSS feeds
        frame = Frame(master)
        frame.pack(side=BOTTOM)
        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT,fill=Y)

        t = "Google & Yahoo Top News"
        title = StringVar()
        title.set(t)
        ttl = Label(master, textvariable=title, font=("Helvetica", 18))
        ttl.pack(side=TOP)
        cont = Text(master, font=("Helvetica",14), yscrollcommand=scrollbar.set)
        cont.pack(side=BOTTOM)
        cont.tag_config("title", justify='center')
        button = Button(frame, text="Exit", command=root.destroy)
        button.pack(side=BOTTOM)
        guidShown = []
        def get_cont(newstory):
            if newstory.get_guid() not in guidShown:
                cont.insert(END, newstory.get_title()+"\n", "title")
                cont.insert(END, "\n---------------------------------------------------------------\n", "title")
                cont.insert(END, newstory.get_description())
                cont.insert(END, "\n*********************************************************************\n", "title")
                guidShown.append(newstory.get_guid())

        while True:

            print("Polling . . .", end=' ')
            # Get stories from Google's Top Stories RSS news feed
            stories = process("http://news.google.com/news?output=rss")

            # Get stories from Yahoo's Top Stories RSS news feed
            stories.extend(process("http://news.yahoo.com/rss/topstories"))

            stories = filter_stories(stories, triggerlist)

            list(map(get_cont, stories))
            scrollbar.config(command=cont.yview)


            print("Sleeping...")
            time.sleep(SLEEPTIME)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    root = Tk()
    root.title("Some RSS parser")
    t = threading.Thread(target=main_thread, args=(root,))
    t.start()
    root.mainloop()

