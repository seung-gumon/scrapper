def fm_korea(soup):
    try:
      return_dict = {}
      post_html = soup.find("div", {"id": "bd_capture"})
      title = post_html.find("h1").text
      if not title:
            raise Exception('empty title')
      return {
            'post_title' : title
      }
    except Exception as e:
        if str(e) == 'empty title':
            return 'empty title'
        return {}
