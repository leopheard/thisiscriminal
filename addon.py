from xbmcswift2 import Plugin, xbmcgui
from resources.lib import thisiscriminal

plugin = Plugin()

# base url for fetching podcasts 
URL = "http://feeds.thisiscriminal.com/CriminalShow"

@plugin.route('/')
def main_menu():
    """
    main menu 
    """
    items = [
#        {
#            'label': plugin.get_string(30000), 
#            'path': "http://www.abc.net.au/radio/stations/RN/live?play=true",
#            'thumbnail': "http://www.abc.net.au/local/global_img/programs/howtolisten.jpg", 
#            'is_playable': True},
        {
            'label': plugin.get_string(30001), 
            'path': plugin.url_for('just_in'),
            'thumbnail': "http://paperandfox.com/wp-content/uploads/2014/12/Criminal_Podcast_Logo_medium.jpg"},
#        {
#            'label': plugin.get_string(30002), 
#            'path': plugin.url_for('subject_list'),
#            'thumbnail': "https://pbs.twimg.com/profile_images/470802028856213504/A4Dg37Ey_400x400.jpeg"},
#        {
#            'label': plugin.get_string(30003),
#            'path': plugin.url_for('program_list'),
#            'thumbnail': "https://pbs.twimg.com/profile_images/470802028856213504/A4Dg37Ey_400x400.jpeg"},
    ]

    return items


@plugin.route('/just_in/')
def just_in():
    """
    contains playable podcasts listed as just-in
    """
    soup = thisiscriminal.get_soup(URL)
    
    playable_podcast = thisiscriminal.get_playable_podcast(soup)
    
    items = thisiscriminal.compile_playable_podcast(playable_podcast)

    return items


@plugin.route('/subject_list/')
def subject_list():
    """
    contains a list of navigable podcast by subjects
    """
    items = []

    soup = thisiscriminal.get_soup(URL)
    
    subject_heading = thisiscriminal.get_podcast_heading(soup)
    
    for subject in subject_heading:
        items.append({
            'label': subject['title'],
            'path': plugin.url_for('subject_item', url=subject['url']),
        })

    return items


@plugin.route('/subject_item/<url>/')
def subject_item(url):
    """
    contains the playable podcasts for subjects
    """
    soup = thisiscriminal.get_soup(url)
    
    playable_podcast = thisiscriminal.get_playable_podcast(soup)

    items = thisiscriminal.compile_playable_podcast(playable_podcast)

    return items


@plugin.route('/program_list/')
def program_list():
    """
    contains a list of navigable menu items by program name 
    """
    items = []

    soup = thisiscriminal.get_soup(URL + "/podcasts/program")
    
    program_heading = thisiscriminal.get_podcast_heading(soup)

    for program in program_heading:
        items.append({
            'label': program['title'],
            'path': plugin.url_for('program_item', url=program['url']),
        })

    return items


@plugin.route('/program_list/<url>/')
def program_item(url):
    """
    contains the playable podcasts for program names
    """
    items = []
    
    soup = thisiscriminal.get_soup(url)

    playable_podcast = thisiscriminal.get_playable_podcast(soup)

    items = thisiscriminal.compile_playable_podcast(playable_podcast)

    return items


if __name__ == '__main__':
    plugin.run()
