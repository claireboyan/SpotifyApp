Spotify search API differs from app/web client search. It appears you need to have the beginning character match to get the result you're looking for, even if it shows up correctly in the app or web client.
Example:
Searching "weaponx" in the app/web client correctly provides the top artist result XweaponX, but search API returns artists named
    [WEAPON_X., WeaponX Int'l, WeaponX, ...]
However, searching "xweapon" in the search API returns the correct top result.

Keep this in mind.