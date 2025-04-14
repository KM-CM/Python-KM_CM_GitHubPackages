from os.path import isdir as _isdir, dirname as _dirname, abspath as _abspath, join as _path_join
from os import walk as _path_walk, makedirs as _makedirs
from requests import get as _get
from hashlib import sha1 as _sha1
from shutil import rmtree as _rmtree
from sys import executable as _executable
from argparse import ArgumentParser as _ArgumentParser

__PACKAGES__ = _path_join( _dirname( _abspath( __file__ ) ), 'Packages' )

def Assert( Name, Owner = 'KM_CM', Account = '0KMCM0' ):
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

try:
    assert _get( 'https://api.github.com' ).status_code == 200
except:
    M = '[KM_CM_GitHubPackages] UnAble to Access `api.github.com`.'
    X = input( f'{ M } Are You Sure You Wish to Proceed? (Y\'es / D\'ebug)\n' ).lower()
    if X.startswith( 'y' ):
        def Assert( Name, Owner = ..., Account = ... ): pass
    elif X.startswith( 'd' ):
        def Assert( Name, Owner = 'KM_CM', Account = '0KMCM0' ): print( f'[KM_CM_GitHubPackages: { Account }, { Owner }, { Name }]' )
    else: raise BaseException( M )
else:
    try:
        R = _get( f'https://api.github.com/repos/0KMCM0/Python-KM_CM_GitHubPackages/git/refs/heads/main' )
        R = _get( f'https://api.github.com/repos/0KMCM0/Python-KM_CM_GitHubPackages/git/trees/{ R.json()[ 'object' ][ 'sha' ] }?recursive=1' )
        R.raise_for_status()
        R = R.json()
        CheckSum = None
        for X in R[ 'tree' ]:
            if X[ 'path' ] == 'KM_CM_GitHubPackages':
                CheckSum = X[ 'sha' ]
                break
        H = _sha1()
        M = _dirname( _abspath( __file__ ) )
        for P in [ '__init__.py', '__init__.pyi' ]:
            T = _sha1()
            with open( _path_join( P, M ), 'rb' ) as F:
                while C := F.read( 8192 ):
                    T.update( C )
            H.update( T.hexdigest().encode( 'utf-8' ) )
        H = H.hexdigest()
        if H != CheckSum and input( '[KM_CM_GitHubPackages] InCorrect CheckSum. Update?' ).lower().startswith( 'y' ):
            R = _get( f'https://api.github.com/repos/0KMCM0/Python-KM_CM_GitHubPackages/contents/KM_CM_GitHubPackages' )
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
                        with open( _path_join( M, O[ 'name' ] ), 'wb') as W:
                            W.write( R.content )
            Download( R.json() )
    except Exception as E:
        print( f'[KM_CM_GitHubPackages] An Error in Auto Updater.\nAdmin Command to Engage Auto Updater\n"{ _executable }" "{ _abspath( __file__ ) }" -Upgrade' )

if __name__ == '__main__':
    Parser = _ArgumentParser( prog = 'KM_CM_GitHubPackages',
                              description = 'https://github.com/0KMCM0/Python-KM_CM_GitHubPackages' )
    Parser.add_argument( '-Upgrade', action = 'store_true', help = 'Check for Upgrades and Update. Requires Admin Rights.' )
    Args = Parser.parse_args()
    if Args.Upgrade:
        R = _get( f'https://api.github.com/repos/0KMCM0/Python-KM_CM_GitHubPackages/git/refs/heads/main' )
        R = _get( f'https://api.github.com/repos/0KMCM0/Python-KM_CM_GitHubPackages/git/trees/{ R.json()[ 'object' ][ 'sha' ] }?recursive=1' )
        R.raise_for_status()
        R = R.json()
        CheckSum = None
        for X in R[ 'tree' ]:
            if X[ 'path' ] == 'KM_CM_GitHubPackages':
                CheckSum = X[ 'sha' ]
                break
        H = _sha1()
        M = _dirname( _abspath( __file__ ) )
        for P in [ '__init__.py', '__init__.pyi' ]:
            T = _sha1()
            with open( _path_join( P, M ), 'rb' ) as F:
                while C := F.read( 8192 ):
                    T.update( C )
            H.update( T.hexdigest().encode( 'utf-8' ) )
        H = H.hexdigest()
        if H != CheckSum:
            R = _get( f'https://api.github.com/repos/0KMCM0/Python-KM_CM_GitHubPackages/contents/KM_CM_GitHubPackages' )
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
                        with open( _path_join( M, O[ 'name' ] ), 'wb') as W:
                            W.write( R.content )
            Download( R.json() )