def fm_korea(soup) :
      post_html = soup.find("div", {"id": "bd_capture"})
      print('--------------------------------------')
      print(post_html.prettify());
      title = post_html.find("h1")
      print(title);
      print('--------------------------------------')