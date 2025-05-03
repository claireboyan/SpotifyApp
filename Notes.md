# NOTES

### Misspelling Sensitivity

Spotify search API differs from app/web client search. It appears you need to have the beginning character match to get the result you're looking for, even if it shows up correctly in the app or web client.

Examples:
- Searching *weaponx* in the app/web client correctly provides the top artist result **XweaponX**, but search API returns artists named
    
        [WEAPON_X., WeaponX Int'l, WeaponX, ...]
    However, searching *xweapon* in the search API returns the correct top result.
- Searching *etown concrete* in the app/web client correctly provides the top artist result **E-Town Concrete**, but search API returns no matches.
However, searching *e.town concrete*, *e town concrete*, or *e-town concrete* in the search API returns the correct top result.

Keep this in mind.

### Intermittent Invalid Client Error

If your credentials match the ones in the app, you might just need to delete the cache file.