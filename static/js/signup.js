function change()
{
    const el = document.getElementById('change__text');
    if ( el.innerHTML  == 'Producer' )
        el.innerHTML = 'Consumer';
    else
        el.innerHTML = 'Producer';
}