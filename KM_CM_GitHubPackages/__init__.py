from os.path import isdir as _isdir, dirname as _dirname, abspath as _abspath, join as _path_join
from os import walk as _path_walk, makedirs as _makedirs
from requests import get as _get
from hashlib import sha1 as _sha1
from shutil import rmtree as _rmtree

__PACKAGES__ = _path_join( _dirname( _abspath( __file__ ) ), 'Packages' )

def Assert( Name, Owner, Account ):
    Type = True
    Path = _path_join( __PACKAGES__, Owner, Name )
    if _isdir( Path ):
        R = _get( f'https://api.github.com/repos/{ Account }/Python-{ Owner }_{ Name }/git/refs/heads/main' )
        if R.status_code == 404: raise BaseException( f'[KM_CM_GitHubPackages, { Account }, { Owner }, { Name }] Asserting Non-Existent Package.' )
        R = _get( f'https://api.github.com/repos/{ Account }/Python-{ Owner }_{ Name }/git/trees/{ R.json()[ 'object' ][ 'sha' ] }?recursive=1' )
        R.raise_for_status()
        R = R.json()
        CheckSum = None
        N = f'{ Owner }_{ Name }'
        for X in R[ 'tree' ]:
            if X[ 'path' ] == N:
                CheckSum = X[ 'sha' ]
                break
        H = _sha1()
        for D, _, I in _path_walk( Path ):
            for N in I:
                T = _sha1()
                with open( _path_join( D, N ), 'rb' ) as F:
                    while C := F.read( 8192 ):
                        T.update( C )
                H.update( T.hexdigest().encode( 'utf-8' ) )
        H = H.hexdigest()
        if H == CheckSum: Type = None
        else: Type = False
    M = None
    if Type is True:
        M = f'[KM_CM_GitHubPackages: { Account }, { Owner }, { Name }] Missing.'
        R = input( f'{ M } Download?\n' )
        if not R.lower().startswith( 'y' ): raise BaseException( M )
    elif Type is False:
        M = f'[KM_CM_GitHubPackages: { Account }, { Owner }, { Name }] InCorrect CheckSum.'
        R = input( f'{ M } Update?\n' )
        if not R.lower().startswith( 'y' ): raise BaseException( M )
    if M is None: return
    R = input( f'Are You Sure?\n' )
    if not R.lower().startswith( 'y' ): raise BaseException( M )
    if Type is False: _rmtree( Path )
    _makedirs( Path )
    R = _get( f'https://api.github.com/repos/{ Account }/Python-{ Owner }_{ Name }/contents/{ Owner }_{ Name }' )
    R.raise_for_status()
    def Download( R ):
        for O in R:
            T = O[ 'type' ]
            if T == 'dir':
                R = _get( O[ 'url' ] )
                R.raise_for_status()
                Download( R.json() )
            elif T == 'file':
                R = _get( O[ 'download_url' ] )
                with open( _path_join( __PACKAGES__, Owner, Name, O[ 'name' ] ), 'wb') as W:
                    W.write( R.content )
    Download( R.json() )
