#coding=utf-8

# github client 
# supply base api to get files from our git account
# author niyoufa
# date : 2016-06-23

import pdb
import ods.libs.github3 as github3
from github3 import login

class Github3Client(object):
    __username = "niyoufa@tmlsystem.com"
    __password = "19922011nyf"

    def __init__(self,*args,**options):
        self.username = options.get("username",Github3Client.__username)
        self.password = options.get("password",Github3Client.__password)
        print "wait login git ..."
        self.gh = login(self.username,self.password)
        print "login success!"
        self.user = self.gh.me()
        self.repo_dict = {}
        self.contents = {}

    def get_login(self):
        return self.user.login

    def get_name(self):
        return self.user.name

    def get_followers_count(self):
        return self.user.followers_count

    def get_follower_names(self):
        follower_names = []
        gt_followers = self.gh.followers()

        for f in gt_followers:
            follower_names.append(str(f))

        return follower_names

    def get_followers(self):
        followers = []
        gt_follower_names = self.get_follower_names()
        for name in gt_follower_names :
            followers.append(self.gh.user(name))
        return followers

    def statistic_my_followers_f_count(self):
        """statistic my followers´s followers_count"""

        f_count_list = []
        followers = self.get_followers()
        for f in followers :
            f_count_list.append(dict(
                name = f.name,
                f_count = f.followers_count,
            ))
        return f_count_list

    def get_repository(self,repo_name="ods"):
        if self.repo_dict.has_key(repo_name):
            repo = self.repo_dict[repo_name]
        else :
            repo = self.gh.repository(self.get_login(),repo_name)
            self.repo_dict[repo_name] = repo
        return repo

    def get_repo_dc(self,repo,dir_name="."):
        contents = repo.directory_contents(dir_name)
        return contents

    def get_repo_fc(self,repo,dir_name="."):
        contents = repo.file_contents(dir_name)
        return contents

    def get_repo_info_tree(self,repo_name="ods",root_dir_name="."):
        repo = self.get_repository(repo_name)
        contents = {}
        content_obj_list = self.get_repo_dc(repo,root_dir_name)

        if root_dir_name == "." :
            print "requesting data ..."
            root_dir_name = repo_name
        contents[root_dir_name] = []
        # print "==========================================="\
        # "================================================="
        for obj in content_obj_list :
            content = obj[1]
            if content.type == "dir":
                dir_name = content.name
                if root_dir_name == repo_name:
                    sub_root_dir_name = dir_name
                else :
                    sub_root_dir_name = root_dir_name + "/" + dir_name
                if not contents.has_key(dir_name):
                    contents[root_dir_name].append(dict(
                        name = content.name,
                        path = content.path,
                        sha = content.sha,
                        size = content.size,
                        url = content.url,
                        html_url = content.html_url,
                        git_url = content.git_url,
                        download_url = content.download_url,
                        type = content.type,
                        _links = content._links,
                        sub_contents = self.get_repo_info_tree(repo_name,
                            sub_root_dir_name)
                    ))
                else:
                    pass

            elif content.type == "file":
                contents[root_dir_name].append(dict(
                    name = content.name,
                    path = content.path,
                    sha = content.sha,
                    size = content.size,
                    url = content.url,
                    html_url = content.html_url,
                    git_url = content.git_url,
                    download_url = content.download_url,
                    type = content.type,
                    _links = content._links,
                ))
            else :
                raise Exception("github3 exception : content type error")
            # print content.name
            # print content.download_url
            # print "-----------------------------"
        return contents

    def get_repo_files(self,repo_name="ods",root_dir_name="."):
        repo = self.get_repository(repo_name)
        content_obj_list = self.get_repo_dc(repo,root_dir_name)

        if root_dir_name == "." :
            print "requesting data ..."
            root_dir_name = repo_name
        self.contents[root_dir_name] = []
        print "==========================================="\
        "================================================="
        for obj in content_obj_list :
            content = obj[1]
            if content.type == "dir":
                dir_name = content.name
                if root_dir_name == repo_name:
                    sub_root_dir_name = dir_name
                else :
                    sub_root_dir_name = root_dir_name + "/" + dir_name
                if not self.contents.has_key(dir_name):
                    self.get_repo_files(repo_name,sub_root_dir_name)
                else:
                    pass
            elif content.type == "file":
                self.contents[root_dir_name].append(dict(
                    name = content.name,
                    path = content.path,
                    sha = content.sha,
                    size = content.size,
                    url = content.url,
                    html_url = content.html_url,
                    git_url = content.git_url,
                    download_url = content.download_url,
                    type = content.type,
                ))
                print content.name
                print content.download_url
                print "-----------------------------"
            else :
                raise Exception("github3 exception : content type error")
        return self.contents


if __name__ == "__main__":
    pass
    niyoufa = Github3Client()
    ods_info = niyoufa.get_repo_info()

"""
from ods.clients.github3_bypy import *
niyoufa = Github3Client()
ods_info = niyoufa.get_repo_info()
"""



