#!/usr/bin/env python
# encoding: utf-8

"""
@version: 0.1
@author: liuzhangpei
@contact: liuzhangpei@126.com
@site: http://www.livenowhy.com
@time: 16/9/26 18:05
"""

import requests

base_url = 'https://hub.docker.com/explore/?page='


from bs4 import BeautifulSoup
import subprocess



def get_image_name(page):
    url = base_url + str(page)
    response = requests.get(url, timeout=10)

    html = response.content
    soup = BeautifulSoup(html, 'lxml')
    fp = open('repo.conf', 'a+')

    for articlelist in soup.find_all('ul', attrs={"class": "large-12 columns no-bullet"}):
        for node in articlelist.find_all('div', attrs={"class": "RepositoryListItem__head___3ubbP RepositoryListItem__section___1CXRq"}):
            for repoName in node.find_all('div', attrs={"class": "RepositoryListItem__repoName___28cOR"}):
                repo_name = repoName.get_text()
                fp.writelines(repo_name + '\n')
                fp.flush()
                print repo_name
    fp.close()

def pull_image(repo_name):
    try:
        cmdstr = 'docker pull ' + str(repo_name)
        ps = subprocess.Popen(cmdstr, shell=True)
        retcode = ps.wait()

        if str(retcode) == '0':
            print cmdstr + ' is ok'
    except Exception as msg:
        print msg.message



def run():
    # for page in range(1, 20):
    #     get_image_name(page)

    with open('repo.conf', 'r') as fp:
        for line in fp:
            line = line.strip()
            pull_image(line)

if __name__ == '__main__':

    for i in range(0, 3):
        run()
