from fabric.api import *
import yaml

env.use_ssh_config = True

env.hosts = ['sA']
#DEBUG = True
DEBUG = False
jokesLocal = 'jokes-server'
excludesFile = 'excludes'

with open("config.yaml", 'r') as stream:
    data = yaml.load(stream)


@task
def deploy(project):

    local(rsync(data[project]))

    actions = cd_action('/web/jokes-server') + [
        'php artisan optimize',
        'php artisan cache:clear',
        'php artisan route:clear',
        'php artisan route:cache',
    ]

    runit(glue_actions(actions))


@task
def test(project):
    cmnd = rsync(data[project])
    print cmnd
    #local(cmnd)

def rsync(locations):
    return "rsync "+locations['local']+" sA:"+locations['remote']+" -alz --delete --exclude-from='"+excludesFile+"'"

def cd_action(path):
    return ['cd ' + path]

def glue_actions(actions):
    return ' && '.join(actions)

def runit(actions):
    if DEBUG:
        print '**************'
        print(actions)
        return actions
    else:
        return run(actions)