'''
Revisionist: a module to get the latest source code revision for a Django project, 
for use as a static content versioning device. Currently supports Mercurial and Git.
'''
import logging
import os
import sys
import time
import subprocess


DEFAULT_REVISION = time.strftime("%j", time.localtime())

logger = logging.getLogger('revisionist')
if not logger.handlers:
    logger.addHandler(logging.StreamHandler(sys.stderr))

def _get_django_module_dir():
    django_module_dir = '.'
    if os.environ.has_key('DJANGO_SETTINGS_MODULE'):
        django_settings_module = __import__(os.environ['DJANGO_SETTINGS_MODULE'])
        return os.path.dirname(django_settings_module.__file__)
    else:
        logger.warn('DJANGO_SETTINGS_MODULE not set; using current directory.')
    return django_module_dir

def _findrepo(type = None, path = None):
    if not path:
        path = os.getcwd()
    while not os.path.isdir(os.path.join(path, '.' + type)):
        oldpath, path = path, os.path.dirname(path)
        if path == oldpath:
            return ''
    return path




def rev(path=None):
    '''
    Get the latest revision of the Django project from its version control repository.
    It will try to detect the version control system
    '''
    revision = DEFAULT_REVISION
    try:
        
        if not path:
            path = _get_django_module_dir()

        if os.path.isdir(os.path.join (path, '.hg')):
            revision = subprocess.Popen(['hg', 'id', '-i'], stdout=subprocess.PIPE).communicate()[0].strip('+')[:7]

        if os.path.isdir(os.path.join (path, '.git')):
            #git_path = _findrepo('git', path)
            revision = subprocess.Popen(['git', 'rev-parse', '--short', 'HEAD'], stdout=subprocess.PIPE, cwd=path).communicate()[0].strip()

    except Exception, e:
        logger.warn('Could not determine revision for %s: %s' % (path, e))
        logger.warn('Using default revision: %s' % DEFAULT_REVISION)
    return revision

#
#def bzrrev(path=None):
#    '''
#    Get the latest revision of the Django project from its Bazaar repository.
#    '''
#    revision = DEFAULT_REVISION
#    try:
#        from bzrlib import workingtree
#        
#        if not path:
#            path = _get_django_module_dir()
#        wt = workingtree.WorkingTree.open(path)
#        revision = str(wt.branch.revno())
#    except Exception, e:
#        logger.warn('Could not determine Bazaar revision for %s: %s' % (path, e))
#        logger.warn('Using default revision: %s' % DEFAULT_REVISION)
#    return revision
#
#def hgrev(path=None):
#    '''
#    Get the latest revision of the Django project from its Mercurial repository.
#    '''
#    revision = DEFAULT_REVISION
#    try:
#        from mercurial.hg import repository
#        from mercurial.ui import ui
#        
#        if not path:
#            path = _get_django_module_dir()
#        repo = _findhgrepo(path)
#        revision = str(len(repository(ui(), repo).changelog))
#    except Exception, e:
#        logger.warn('Could not determine Mercurial revision for %s: %s' % (path, e))
#        logger.warn('Using default revision: %s' % DEFAULT_REVISION)
#    return revision
#
#def svnrev(path=None):
#    '''
#    Get the latest revision of the Django project from its Subversion repository.
#    Requires pysvn, available from http://pysvn.tigris.org/.
#    '''
#    revision = DEFAULT_REVISION
#    try:
#        import pysvn
#        client = pysvn.Client()
#        if not path:
#            path = _get_django_module_dir()
#        info = client.info(path)
#        revision = str(info.revision.number)
#    except Exception, e:
#        logger.warn('Could not determine Subversion revision for %s: %s' % (path, e))
#        logger.warn('Using default revision: %s' % DEFAULT_REVISION)
#    return revision
#
