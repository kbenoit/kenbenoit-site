---
author: Ken
categories:
- Macintosh
- Statistics
date: "2009-01-14T17:51:40Z"
id: 261
tags:
- firewall
- http_proxy
- proxy
- R
title: How to set proxy settings for R (Mac OSX)
url: /how-to-set-proxy-settings-for-r-mac-osx/
---
I run R behind a firewall, and found it tricky to set the proxy settings for R so that I could directly install packages, access outside data using `load(url())`, etc. The solution lies in the http_proxy environment variable. Here is how to set it up:

Create a text file called .Rprofile in your home directory (on Mac OSX, this is `~` or `/Users/myuser/`). This text file should have the following line in it:

    Sys.setenv(http_proxy="http://username:password@tcdproxy.tcd.ie:8080-8243")

substituting your own username, password, and proxy server and port settings of course.

It seems that running this from R before you need it does not work, since I have heard reports that it only works if you run it as the first command in R when you start a new R session. By setting this up in your `~/.Rprofile` you avoid having to retype it each time you start R, as well as making sure that this command is run at startup.

