import threading
import time
import Queue


import os
import fnmatch


def create_test_account_file(accountId):
    """Checks if the notification on screen are ordered by time

    @param  acountId notification on screen
    """
    #fullpath_filename = "//pps//services//notify//settings//act."+acountId;
    fullpath_filename = "d:/pythontest/act."+accountId;
    accountfile = open(fullpath_filename, 'w');
    accountFileContent = "@act." + accountId +  "\nbadge::off\ncategory::messages\ndisplay::off\ndisplay_name::Gmail\nemail_address::bbiatester@gmail.com\nled::on\npreview::on\nseeded::false\nsound::off\ntone::/usr/share/sounds/notification-tones/messages/warm.m4a\ntype::account\nuib::off\nuser::bbiatester@gmail.com\nvibrate::off\nvisible::true";
    accountfile.write(accountFileContent);
    accountfile.close();
    return





def main():

   
   create_test_account_file("123456");
   
    
  
   
main()
   
   
