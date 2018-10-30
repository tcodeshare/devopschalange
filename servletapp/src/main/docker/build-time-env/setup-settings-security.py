#!/usr/bin/env python

from subprocess import Popen, PIPE, STDOUT
import os
import time
import sys
import re
import stat
import shutil
import getpass

deploy_servers = ["remote-nexus-repo", "nexus.ubs.net:18081"]
backup_suffix = "." + str(time.time())


def match_mode(mode, file):
    filemode = stat.S_IMODE(os.stat(file).st_mode)
    return filemode == mode


def cre_set_file(settings_file, server_pass):

    set_tmpl = """
<settings>
  <servers>
    $SERVERS
  </servers>
  <profiles>
    <profile>
      <id>remote-nexus-repo</id>
      <properties>
        <!-- Format: id::layout::url -->
        <altDeploymentRepository>remote-nexus-repo::default::http://nexus.ubs.net:8081/nexus/content/repositories/releases</altDeploymentRepository>
        <altReleaseDeploymentRepository>remote-nexus-repo::default::http://nexus.ubs.net:8081/nexus/content/repositories/releases</altReleaseDeploymentRepository>
        <altSnapshotDeploymentRepository>remote-nexus-repo::default::http://nexus.ubs.net:8081/nexus/content/repositories/snapshots</altSnapshotDeploymentRepository>
      </properties>
    </profile>
  </profiles>
  <activeProfiles>
    <activeProfile>remote-nexus-repo</activeProfile>
  </activeProfiles>
</settings>

"""

    if os.path.exists(settings_file):
        shutil.move(settings_file, settings_file + backup_suffix)

    p = Popen(['mvn', '--encrypt-password', server_pass],
              stdout=PIPE, stdin=PIPE, stderr=STDOUT)
    # TODO: pass it over input instead of CLI switch
    # out=p.communicate(input=m_pass)[0]
    out = p.communicate()[0]

    p = re.compile('{.*}')
    m = p.search(out)

    server_pass = m.group()

    logname = "ubs-uploader"

    server_section = ""

    for deploy_server in deploy_servers:
        server_entry = """
        <server>
            <id>""" + deploy_server + """</id>
            <username>""" + logname + """</username>
            <password>""" + server_pass + """</password>
        </server>"""

        server_section = server_section + server_entry

    # Updated template about encrypted password
    p = re.compile('\$SERVERS')
    set_tmpl = p.sub(server_section, set_tmpl)

    sec_file = open(settings_file, 'w')
    sec_file.write(set_tmpl)
    sec_file.close()


def cre_sec_file(sec_set_file, m_pass):
    sec_tmpl = """
<settingsSecurity>
  <master>$PASS</master>
</settingsSecurity>

"""
    if os.path.exists(sec_set_file):
        shutil.move(sec_set_file, sec_set_file + backup_suffix)

    # Encrypt the password
    p = Popen(['mvn', '--encrypt-master-password', m_pass],
              stdout=PIPE, stdin=PIPE, stderr=STDOUT)
    # TODO: pass it over input instead of CLI switch
    # out=p.communicate(input=m_pass)[0]
    out = p.communicate()[0]

    p = re.compile('{.*}')
    m = p.search(out)
    encMPass = m.group()

    # Updated template about encrypted password
    p = re.compile('\$PASS')
    sec_tmpl = p.sub(encMPass, sec_tmpl)

    sec_file = open(sec_set_file, 'w')
    sec_file.write(sec_tmpl)
    sec_file.close()


def cre_dir_struct(home):

    mvn_cfg_dir = home + os.sep + '.m2'

    if not os.path.exists(mvn_cfg_dir):
        os.makedirs(mvn_cfg_dir)
    else:
        if not match_mode(0o700, mvn_cfg_dir):
            os.chmod(mvn_cfg_dir, 0o700)


def main():
    # set the restrictive umask
    os.umask(0o077)

    master_pass = getpass.getpass(
        "Enter maven security settings master password:")
    server_pass = getpass.getpass("Enter (maven/docker) repository password:")

    home = os.path.expanduser("~")
    settings_file = home + os.sep + '.m2' + os.sep + 'settings.xml'
    sec_file = home + os.sep + '.m2' + os.sep + 'settings-security.xml'

    cre_dir_struct(home)

    cre_sec_file(sec_file, master_pass)
    cre_set_file(settings_file, server_pass)


if __name__ == '__main__':
    main()
