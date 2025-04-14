"""
GitHubPackages (GHP for Short). A Manager for Packages on GitHub.
It should be in "C:/Users/[You]/AppData/Local/Programs/Python/Python[Version]/Lib/site-packages/".

| Term    | Meaning                | Example       |
|---------|------------------------|---------------|
| Name    | Package Name           | ``MyPackage`` |
| Owner   | Initials               | ``Me``        |
| Account | Account Name on GitHub | ``MyAccount`` |

A Package is a Repository in a Specific Format.
Name - ``Python-[Owner]_[Name]``, by - ``[Account]``.
Contains a Folder Named ``[Owner]_[Name]``.
The Folder is a Normal Python Project,
The Same Thing You'd Install Via PIP -
It is What GHP will Actually Use -
Everything OutSide is Ignored.
"""

__PACKAGES__: str = ...
"""Path to The Packages."""

def Assert( Name: str, Owner: str = 'KM_CM', Account: str = '0KMCM0' ) -> None:
    """
Tries to Get The Package ``Name`` from ``Owner`` at ``Account``.
If Successful, You can Import The Result at ``KM_CM_GitHubPackages.<Owner>.<Name>``.
Can Determine Whether The Package Needs an Update or is Missing.

WARNING: Slow. Will Do Nothing without Internet Access. Use at Your Program's Beginning.
    """